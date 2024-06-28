import os

from exponent.core.remote_execution.types import (
    WRITE_STRATEGY_FULL_FILE_REWRITE,
    FileWriteRequest,
    FileWriteResponse,
)
from exponent.core.remote_execution.utils import assert_unreachable


def execute_file_write(
    request: FileWriteRequest, working_directory: str
) -> FileWriteResponse:
    write_strategy = request.write_strategy
    if write_strategy == WRITE_STRATEGY_FULL_FILE_REWRITE:
        result = execute_full_file_rewrite(
            request.file_path, request.content, working_directory
        )
    else:
        assert_unreachable(write_strategy)
    return FileWriteResponse(
        content=result,
        correlation_id=request.correlation_id,
    )


def execute_full_file_rewrite(
    file_path: str, content: str, working_directory: str
) -> str:
    try:
        # Construct the absolute path
        full_file_path = os.path.join(working_directory, file_path)

        # Check if the directory exists, if not, create it
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        # Determine if the file exists and write the new content
        if os.path.exists(full_file_path):
            with open(full_file_path, "w") as file:
                file.write(content)
            return f"Modified file {file_path}"
        else:
            with open(full_file_path, "w") as file:
                file.write(content)
            return f"Created file {file_path}"

    except Exception as e:  # noqa: BLE001
        return f"An error occurred: {e!s}"
