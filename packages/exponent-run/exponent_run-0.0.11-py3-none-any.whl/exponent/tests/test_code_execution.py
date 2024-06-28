from exponent.core.remote_execution.languages.shell import execute_shell


async def test_execute_shell(default_temporary_directory: str) -> None:
    output = await execute_shell(
        code="ls -1v", working_directory=default_temporary_directory
    )
    output_lines = output.strip().split("\n")
    expected_lines = 3
    assert len(output_lines) == expected_lines
    assert output_lines == [
        "exponent.txt",
        "test1.py",
        "test2.py",
    ]
