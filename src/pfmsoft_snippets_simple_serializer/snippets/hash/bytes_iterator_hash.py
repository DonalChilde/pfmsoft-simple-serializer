####################################################
#                                                  #
#     src/snippets/hash/bytes_iterator_hash.py
#                                                  #
####################################################
# Created by: Chad Lowe                            #
# Created on: 2023-02-28T08:31:31-07:00            #
# Last Modified: 2023-02-28T15:36:17.990172+00:00  #
# Source: https://github.com/DonalChilde/snippets  #
####################################################

from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from hashlib import _Hash


def bytes_iterator_hash(
    bytes_iterator: Iterator[bytes],
    hasher: "_Hash",
) -> str:
    """
    Get the hash digest of a bytes iterator as a hexidecimal string.

    https://stackoverflow.com/a/3431835/105844


    Args:
        bytes_iterator: The byte iterator
        hasher: The hash function from :py:mod:`hashlib`

    Returns:
         The hexidecimal str from `hexdigest()`
    """

    for block in bytes_iterator:
        hasher.update(block)
    return hasher.hexdigest()
