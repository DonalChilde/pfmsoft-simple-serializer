####################################################
#                                                  #
#        src/snippets/hash/file_hash.py
#                                                  #
####################################################
# Created by: Chad Lowe                            #
# Created on: 2023-02-28T08:31:08-07:00            #
# Last Modified: 2023-03-01T15:20:06.269228+00:00  #
# Source: https://github.com/DonalChilde/snippets  #
####################################################

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO, Callable, Protocol

if TYPE_CHECKING:
    from hashlib import _Hash


def hash_binary_file(
    file_handle: BinaryIO, hasher: "_Hash", block_size: int = 2**10 * 64
) -> str:
    """
    Calculate the hash digest for a file as a hexidecimal string.

    https://stackoverflow.com/a/3431835/105844
    https://www.pythonmorsels.com/reading-binary-files-in-python/

    Args:
        file_handle: The file handle for a file opened in binary mode.
        hasher: The hasher used to generate the hexdigest.
        block_size: The block size used to read the file. Defaults to 2**10*64 (64K).

    Returns:
        A hexidecimal string representing the file hash.
    """
    with file_handle:
        block = file_handle.read(block_size)
        while block:
            hasher.update(block)
            block = file_handle.read(block_size)
    return hasher.hexdigest()


def hash_file(file_path: Path, hasher: "_Hash", block_size: int = 2**10 * 64) -> str:
    """
    Calculate the hash digest for a file as a hexidecimal string.

    https://stackoverflow.com/a/3431835/105844
    https://www.pythonmorsels.com/reading-binary-files-in-python/

    Args:
        file_path: The path for a file to be opened in binary mode.
        hasher: The hasher used to generate the hexdigest.
        block_size: The block size used to read the file. Defaults to 2**10*64 (64K).

    Returns:
        A hexidecimal string representing the file hash.
    """
    with open(file_path, mode="rb") as file_handle:
        hex_digest = hash_binary_file(
            file_handle=file_handle, hasher=hasher, block_size=block_size
        )
    return hex_digest


class HashedFileProtocol(Protocol):
    file_path: Path
    file_hash: str
    hash_method: str


@dataclass
class HashedFile:
    file_path: Path
    file_hash: str
    hash_method: str


def hashed_file_result_factory(
    file_path: Path, file_hash: str, hash_method: str
) -> HashedFileProtocol:
    return HashedFile(file_path=file_path, file_hash=file_hash, hash_method=hash_method)


def make_hashed_file(
    file_path: Path,
    hasher: "_Hash",
    block_size: int = 2**10 * 64,
    result_factory: Callable[
        [Path, str, str], HashedFileProtocol
    ] = hashed_file_result_factory,
):
    hash_str = hash_file(file_path=file_path, hasher=hasher, block_size=block_size)
    return result_factory(file_path, hash_str, hasher.name)
