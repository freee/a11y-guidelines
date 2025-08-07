"""Utility functions for the accessibility guidelines."""

import re
from typing import List, TypeVar, Sequence

from .config import Config

T = TypeVar('T')


def join_items(items: List[str], lang: str) -> str:
    """Join platform items with localized separator.

    Args:
        items: List of platform identifiers
        lang: Language code ('ja' or 'en')

    Returns:
        Joined string with localized separators
    """
    return Config.get_list_separator(lang).join(
        [Config.get_platform_name(item, lang) for item in items]
    )


def uniq(seq: Sequence[T]) -> List[T]:
    """Remove duplicates from a sequence while preserving order.

    Args:
        seq: Input sequence

    Returns:
        List with duplicates removed, preserving original order
    """
    return list(dict.fromkeys(seq))


def tag2sc(tag: str) -> str:
    """Convert axe-core tag to WCAG SC identifier.

    Args:
        tag: axe-core tag (e.g., 'wcag111')

    Returns:
        WCAG SC identifier (e.g., '1.1.1')
    """
    return re.sub(r'wcag(\d)(\d)(\d+)', r'\1.\2.\3', tag)
