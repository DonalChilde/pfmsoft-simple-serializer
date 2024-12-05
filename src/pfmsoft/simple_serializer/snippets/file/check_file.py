"""Check file."""

from pathlib import Path


def check_file(
    path_out: Path, overwrite: bool = False, ensure_parents: bool = True
) -> bool:
    """Make sure the path_out is valid for a file."""
    if path_out.exists():
        if path_out.is_dir():
            raise ValueError(f"Output path exists and it is a directory. {path_out}")
        if path_out.is_file():
            if not overwrite:
                raise ValueError(
                    f"Output path exists and overwrite is false. {path_out}"
                )
    if ensure_parents:
        path_out.parent.mkdir(parents=True, exist_ok=True)
    return True
