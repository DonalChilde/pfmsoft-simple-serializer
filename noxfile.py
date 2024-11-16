import os
import shutil
from pathlib import Path

import nox

package = "pfmsoft_snippets_simple_serializer"
github_user = "DonalChilde"
# python_versions = ["3.10", "3.9", "3.8", "3.7"]

# Empty list means no default sessions
nox.options.sessions = []


@nox.session(tags=["fix"])
def black(session: nox.Session) -> None:
    """
    run black on code
    """
    session.install("black")
    session.run("black", "src", "tests")


@nox.session(tags=["fix"])
def isort(session: nox.Session) -> None:
    """
    run isort on code
    """
    session.install("isort")
    session.run("isort", "src", "tests")


@nox.session()
def tests(session: nox.Session):
    session.install(".[testing]")
    session.run("pytest")


# It's a good idea to keep your dev session out of the default list
# so it's not run twice accidentally
@nox.session(default=False)
def dev(session: nox.Session) -> None:
    """
    Set up a python development environment for the project at ".venv".
    """

    venv_dir = Path(".venv")
    if venv_dir.exists():
        shutil.rmtree(venv_dir)

    session.run("venv", ".venv", silent=True)
    session.run(".venv/bin/pip", "install", "-U", "pip", "wheel")

    # Use the venv's interpreter to install the project along with
    # all it's dev dependencies, this ensures it's installed in the right way
    session.run(".venv/bin/pip", "install", "-e", ".[dev,lint,doc,vscode,testing]")


@nox.session(name="docs-build")
def docs_build(session: nox.Session) -> None:
    """Build the documentation."""
    args = session.posargs or ["docs/source", "docs/build"]
    if not session.posargs and "FORCE_COLOR" in os.environ:
        args.insert(0, "--color")

    session.install(".[doc]")
    # session.install("sphinx", "sphinx-click", "furo", "myst-parser")

    build_dir = Path("docs", "build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", *args)


@nox.session(name="docs-serve")
def docs_serve(session: nox.Session) -> None:
    """Build and serve the documentation with live reloading on file changes."""
    args = session.posargs or ["--open-browser", "docs/source", "docs/build"]
    session.install(".[doc]")
    # session.install("sphinx", "sphinx-autobuild", "sphinx-click", "furo", "myst-parser")

    build_dir = Path("docs", "build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", *args)
