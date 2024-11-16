from pathlib import Path

import pytest

# Add an option to mark slow tests, so that they don't run every time.


def pytest_addoption(parser):
    # https://docs.pytest.org/en/stable/example/simple.html#control-skipping-of-tests-according-to-command-line-option
    # conftest.py must be in the root test package.
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture(scope="session", name="test_output_dir")
def test_output_dir_(tmp_path_factory) -> Path:
    """make a temp directory for output data."""
    test_app_data_dir = tmp_path_factory.mktemp("pdf2txt")
    return test_app_data_dir
