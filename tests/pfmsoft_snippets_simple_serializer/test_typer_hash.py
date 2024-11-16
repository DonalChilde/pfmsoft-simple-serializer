"""Test cases for the console module."""

from importlib import resources

import pytest
from tests.resources import RESOURCES_ANCHOR
from typer.testing import CliRunner
from pfmsoft_snippets_simple_serializer.cli.main_typer import app

DATA_FILE_NAME = "ipsum_1.txt"
DATA_FILE_PATH = "files_1"
DATA_FILE_ANCHOR = f"{DATA_FILE_PATH}/{DATA_FILE_NAME}"
EXPECTED_HASH = "da7eacc24c8082e8963945b62b9c4365"


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_hash_md5(runner: CliRunner) -> None:
    file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_ANCHOR)
    with resources.as_file(file_resource) as input_path:
        result = runner.invoke(app, ["-vvv", "hash-md5", str(input_path)])
        assert "Verbosity: 3" in result.stdout
        assert EXPECTED_HASH in result.stdout
        assert input_path.name in result.stdout
        print(result.stdout)
        if result.stderr_bytes is not None:
            print(result.stderr)
        assert result.exit_code == 0
