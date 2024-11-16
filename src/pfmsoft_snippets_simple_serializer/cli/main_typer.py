"""Command-line interface."""

from hashlib import md5
from pathlib import Path
from time import perf_counter_ns
from typing import Annotated

import typer
from pfmsoft_snippets_simple_serializer.snippets.hash.file_hash import hash_file


def default_options(
    ctx: typer.Context,
    debug: Annotated[bool, typer.Option(help="Enable debug output.")] = False,
    verbosity: Annotated[int, typer.Option("-v", help="Verbosity.", count=True)] = 1,
):
    """Hash a file."""

    ctx.ensure_object(dict)
    ctx.obj["START_TIME"] = perf_counter_ns()
    ctx.obj["DEBUG"] = debug
    typer.echo(f"Verbosity: {verbosity}")
    ctx.obj["VERBOSITY"] = verbosity


app = typer.Typer(callback=default_options)


@app.command()
def hash_md5(
    ctx: typer.Context, path_in: Annotated[Path, typer.Argument(help="file to hash.")]
):
    hashcode = hash_file(path_in, md5())
    typer.echo(f"{hashcode}  {path_in.name}")


if __name__ == "__main__":
    app()
