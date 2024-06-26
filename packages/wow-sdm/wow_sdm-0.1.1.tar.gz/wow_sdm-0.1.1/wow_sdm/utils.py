# -*- coding: utf-8 -*-

import typing as T
import itertools

from pathlib_mate import Path
from ordered_set import OrderedSet

from .logger import logger


def get_values(enum_class) -> OrderedSet:
    """
    Get all values from an enum class.

    Example::

        >>> class Color:
        ...     RED = 1
        ...     GREEN = 2
        ...     BLUE = 3
        >>> get_values(Color)
        OrderedSet([1, 2, 3])
    """
    return OrderedSet(
        [v for k, v in enum_class.__dict__.items() if not k.startswith("_")]
    )


KT = T.TypeVar("KT")
VT = T.TypeVar("VT")


def group_by(
    iterable: T.Iterable[VT],
    get_key: T.Callable[[VT], KT],
) -> T.Dict[KT, T.List[VT]]:  # pragma: no cover
    """
    Group items by it's key, with type hint.

    Example::

        >>> class Record:
        ...     def __init__(self, product: str, date: str, sale: int):
        ...         self.product = product
        ...         self.date = date
        ...         self.sale = sale

        >>> records = [
        ...     Record("apple", "2020-01-01", 10),
        ...     Record("apple", "2020-01-02", 20),
        ...     Record("apple", "2020-01-03", 30),
        ...     Record("banana", "2020-01-01", 10),
        ...     Record("banana", "2020-01-02", 20),
        ...     Record("banana", "2020-01-03", 30),
        ... ]

        >>> group_by(records, lambda x: x.product)
        {
            "apple": [
                Record("apple", "2020-01-01", 10),
                Record("apple", "2020-01-02", 20),
                Record("apple", "2020-01-03", 30),
            ],
            "banana": [
                Record("banana", "2020-01-01", 10),
                Record("banana", "2020-01-02", 20),
                Record("banana", "2020-01-03", 30),
            ],
        }
    """
    grouped = dict()
    for item in iterable:
        key = get_key(item)
        try:
            grouped[key].append(item)
        except KeyError:
            grouped[key] = [item]
    return grouped


def concat_lists(*lists) -> list:
    """
    Concatenate multiple lists into one list.

    Example::

        >>> concat_lists([1, 2], [3, 4], [5, 6])
        [1, 2, 3, 4, 5, 6]
    """
    return list(itertools.chain(*lists))


def apply(
    path: Path,
    content: str,
    real_run: bool = False,
    verbose: bool = True,
):
    r"""
    Apply a content to a file (Write to the file in ``World of Warcraft\WTF\...``).

    :param path: The file path to write to.
    :param content: The content to write.
    :param real_run: If True, do not write to the file.
    :param verbose: If True, print log.
    """
    if verbose:
        # 使用 file:// URI 使得可以点击打印在 Console 中的输出直接跳转到文件
        logger.info(f"Write to: file://{path}")
    if real_run:
        try:
            path.write_text(content, encoding="utf-8")
        except FileNotFoundError:
            path.parent.mkdir(parents=True)
            path.write_text(content, encoding="utf-8")
