import logging
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import NoReturn, TypeVar

from exponent.core.remote_execution import files, git, system_context
from exponent.core.remote_execution.code_execution import execute_code
from exponent.core.remote_execution.file_write import execute_file_write
from exponent.core.remote_execution.session import (
    RemoteExecutionClientSession,
    get_session,
)
from exponent.core.remote_execution.types import (
    CLIConnectedState,
    CodeExecutionRequest,
    CreateChatResponse,
    ExecutionEndResponse,
    FileWriteRequest,
    GetAllTrackedFilesRequest,
    GetFileAttachmentRequest,
    GetMatchingFilesRequest,
    HeartbeatInfo,
    ListFilesRequest,
    RemoteExecutionRequestType,
    RemoteExecutionResponse,
    RemoteExecutionResponseType,
    SignalResponse,
    SignalStatus,
    StartChatRequest,
    StartChatResponse,
    SystemContextRequest,
    UseToolsConfig,
)
from exponent.core.remote_execution.utils import (
    deserialize_request_data,
    format_error_log,
    safe_deserialize_list_response_data,
    safe_deserialize_response_data,
    serialize_message,
)
from httpx import (
    AsyncClient,
    Response,
    codes as http_status,
)
from pydantic import BaseModel

logger = logging.getLogger(__name__)


TModel = TypeVar("TModel", bound=BaseModel)


class ExponentError(Exception):
    pass


class RemoteExecutionClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        session: RemoteExecutionClientSession,
    ):
        self.headers = {"API-KEY": api_key}
        self.base_url = base_url
        self.current_session = session

        self.file_cache: files.FileCache = files.FileCache(session.working_directory)

    @property
    def working_directory(self) -> str:
        return self.current_session.working_directory

    async def get_execution_requests(
        self, chat_uuid: str
    ) -> list[RemoteExecutionRequestType]:
        async with AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/remote_execution/{chat_uuid}/requests",
                headers=self.headers,
            )

        return await self._safe_deserialize_execution_request_list(response)

    async def post_execution_result(
        self, chat_uuid: str, response: RemoteExecutionResponse
    ) -> None:
        async with AsyncClient() as client:
            await client.post(
                f"{self.base_url}/api/remote_execution/{chat_uuid}/result",
                headers=self.headers,
                content=serialize_message(response),
            )

    async def check_remote_end_event(self, chat_uuid: str) -> bool:
        async with AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/remote_execution/{chat_uuid}/execution_end",
                headers=self.headers,
            )
        execution_end_response = await self._safe_deserialize(
            response, ExecutionEndResponse
        )
        return execution_end_response.execution_ended

    async def create_chat(self) -> CreateChatResponse:
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/remote_execution/create_chat",
                headers=self.headers,
            )
        return await self._safe_deserialize(response, CreateChatResponse)

    async def start_chat(
        self, chat_uuid: str, prompt: str, use_tools_config: UseToolsConfig
    ) -> StartChatResponse:
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/remote_execution/start_chat",
                headers=self.headers,
                json=StartChatRequest(
                    chat_uuid=chat_uuid,
                    prompt=prompt,
                    use_tools_config=use_tools_config,
                ).model_dump(),
                timeout=60,
            )
        return await self._safe_deserialize(response, StartChatResponse)

    def get_heartbeat_info(self) -> HeartbeatInfo:
        return HeartbeatInfo(
            system_info=system_context.get_system_info(self.working_directory),
        )

    async def send_heartbeat(self, chat_uuid: str) -> CLIConnectedState:
        logger.info(f"Sending heartbeat for chat_uuid {chat_uuid}")
        heartbeat_info = self.get_heartbeat_info()
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/remote_execution/{chat_uuid}/heartbeat",
                headers=self.headers,
                content=heartbeat_info.model_dump_json(),
                timeout=60,
            )
        if response.status_code != http_status.OK:
            raise Exception(
                f"Heartbeat failed with status code {response.status_code} and response {response.text}"
            )
        connected_state = await self._safe_deserialize(response, CLIConnectedState)
        logger.info(f"Heartbeat response: {connected_state}")
        return connected_state

    async def handle_request(
        self, request: RemoteExecutionRequestType
    ) -> RemoteExecutionResponseType:
        response: RemoteExecutionResponseType
        if isinstance(request, CodeExecutionRequest):
            response = await execute_code(
                request, self.current_session, working_directory=self.working_directory
            )
        if isinstance(request, FileWriteRequest):
            response = execute_file_write(
                request, working_directory=self.working_directory
            )
        elif isinstance(request, ListFilesRequest):
            response = files.list_files(request)
        elif isinstance(request, GetFileAttachmentRequest):
            response = files.get_file_attachment(request)
        elif isinstance(request, GetMatchingFilesRequest):
            response = files.get_matching_files(request, self.file_cache)
        elif isinstance(request, SystemContextRequest):
            response = system_context.get_system_context(
                request, self.working_directory
            )
        elif isinstance(request, GetAllTrackedFilesRequest):
            response = git.get_all_tracked_files(request, self.working_directory)
        return response

    async def disconnect_signal_received(self, chat_uuid: str) -> bool:
        async with AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/remote_execution/{chat_uuid}/signal/disconnect/check",
                headers=self.headers,
                timeout=60,
            )
        if response.status_code != http_status.OK:
            raise Exception(
                f"Failed to fetch disconnect status {response.status_code} and response {response.text}"
            )
        signal = await self._safe_deserialize(response, SignalResponse)
        return signal.status == SignalStatus.sent

    async def acknowledge_disconnect_signal(self, chat_uuid: str) -> None:
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/remote_execution/{chat_uuid}/signal/disconnect/acknowledge",
                headers=self.headers,
                timeout=60,
            )
        if response.status_code != http_status.OK:
            raise Exception(
                f"Failed to fetch disconnect status {response.status_code} and response {response.text}"
            )

    async def _safe_deserialize_execution_request_list(
        self,
        response_data: Response,
    ) -> list[RemoteExecutionRequestType]:
        return await safe_deserialize_list_response_data(
            response_data, deserialize_request_data, self._get_log_and_reraise()
        )

    async def _safe_deserialize(
        self,
        response_data: Response,
        data_model: type[TModel],
    ) -> TModel:
        return await safe_deserialize_response_data(
            response_data, data_model.model_validate, self._get_log_and_reraise()
        )

    def _get_log_and_reraise(
        self,
    ) -> Callable[[Exception, str | None], Awaitable[NoReturn]]:
        async def _impl(exc: Exception, attachment_data: str | None = None) -> NoReturn:
            await self._log_exception_f(exc, attachment_data)
            raise exc

        return _impl

    async def _log_exception_f(
        self, exc: Exception, attachment_data: str | None = None
    ) -> None:
        error_log = format_error_log(exc)
        if not error_log:
            return
        async with AsyncClient() as client:
            await client.post(
                f"{self.base_url}/api/remote_execution/log_error",
                headers=self.headers,
                content=error_log.model_dump_json(),
                timeout=60,
            )

    @staticmethod
    @asynccontextmanager
    async def session(
        api_key: str, base_url: str, working_directory: str
    ) -> AsyncGenerator["RemoteExecutionClient", None]:
        async with get_session(working_directory) as session:
            yield RemoteExecutionClient(api_key, base_url, session)
