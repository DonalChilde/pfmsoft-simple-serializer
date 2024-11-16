"""Test cases for the console module."""

from importlib import resources

import pytest
from tests.resources import RESOURCES_ANCHOR
from typer.testing import CliRunner
from pfmsoft_snippets_simple_serializer.cli.main_typer import app

DATA_FILE_NAME = "ipsum_1.txt"
DATA_FILE_PATH = "files_1"
DATA_FILE_ANCHOR = f"{DATA_FILE_PATH}/{DATA_FILE_NAME}"


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_app(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0


def test_hash_md5(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["hash-md5", "--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0


def test_default_options(runner: CliRunner) -> None:
    file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_ANCHOR)
    with resources.as_file(file_resource) as input_path:
        result = runner.invoke(app, ["-vvv", "hash-md5", str(input_path)])
        assert "Verbosity: 3" in result.stdout
        print(result.stdout)
        if result.stderr_bytes is not None:
            print(result.stderr)
        assert result.exit_code == 0
