"""
RST text processing module.

This module handles the processing of RST markup in text content,
including references, keyboard shortcuts, and text width formatting.
"""

import re
from typing import Dict, Any

# Regular expression patterns
RST_REF_PATTERN = re.compile(r':ref:`([-a-z0-9]+)`')  # Match reference IDs
RST_KBD_PATTERN = re.compile(r':kbd:`([^`]+)`')  # Match keyboard shortcuts


def normalize_text(text: str) -> str:
    """Normalize whitespace and spacing between characters."""
    # Define regexp for half and full width chars
    fullwidth_chars = r'[\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]'
    halfwidth_chars = r'[\u0000-\u007F\uFF61-\uFFDC\uFFE8-\uFFEE]'

    # Define whitespace pattern excluding newlines and fullwidth space (U+3000)
    whitespace_no_newline = r'[ \t\f\v\r\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f]+'

    # Check if text contains bullet points before processing
    has_bullets = bool(re.search(r'^[ \t]*[*\-+][ \t]+', text, re.MULTILINE))

    # First, preserve bullet point patterns and their continuation lines
    # This pattern matches bullet lines and any indented continuation lines
    bullet_and_continuation_pattern = re.compile(r'^([ \t]*[*\-+][ \t]+.*(?:\n[ \t]+.*)*)', re.MULTILINE)
    bullet_matches = []

    def bullet_replacer(match):
        bullet_matches.append(match.group(1))  # Store the complete bullet block with indentation
        return f'__BULLET_PRESERVE_{len(bullet_matches)-1}__'

    text = bullet_and_continuation_pattern.sub(bullet_replacer, text)

    # Remove whitespaces (excluding newlines) between fullwidth chars
    text = re.sub(rf'({fullwidth_chars}){whitespace_no_newline}({fullwidth_chars})', r'\1\2', text)

    # Remove whitespaces (excluding newlines) between fullwidth and halfwidth chars
    text = re.sub(rf'({fullwidth_chars}){whitespace_no_newline}({halfwidth_chars})', r'\1\2', text)

    # Remove whitespaces (excluding newlines) between halfwidth and fullwidth chars
    text = re.sub(rf'({halfwidth_chars}){whitespace_no_newline}({fullwidth_chars})', r'\1\2', text)

    # Restore bullet point patterns with original indentation
    for i, bullet_pattern_str in enumerate(bullet_matches):
        text = text.replace(f'__BULLET_PRESERVE_{i}__', bullet_pattern_str)

    # Remove leading and trailing whitespaces, but preserve bullet indentation
    if has_bullets:
        # For text with bullets, only strip trailing whitespace
        text = text.rstrip()
    else:
        # For regular text, strip both leading and trailing whitespace
        text = text.strip()

    return text


def process_rst_text(text: str, info: Dict[str, Any], lang: str) -> str:
    """
    Process RST markup text by replacing references and keyboard shortcuts.

    Args:
        text: The RST text to process
        info: Dictionary containing reference information
        lang: Language code (e.g. 'en', 'ja')

    Returns:
        Processed text with RST markup replaced
    """
    def ref_replace(match):
        """Replace reference with its text."""
        ref_id = match.group(1)
        if ref_id not in info:
            return match.group(0)  # Keep original if reference not found
        return info[ref_id]['text'][lang]

    # Replace references
    text = RST_REF_PATTERN.sub(ref_replace, text)

    # Replace keyboard shortcuts
    text = RST_KBD_PATTERN.sub(lambda m: m.group(1), text)

    # Only normalize spacing for Japanese text
    if lang == 'ja':
        text = normalize_text(text)
    return text


def process_rst_condition(condition: Dict[str, Any], info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process RST markup in condition data.

    Args:
        condition: Dictionary containing condition data
        info: Dictionary containing reference information

    Returns:
        Processed condition with RST markup replaced
    """
    if condition['type'] == 'simple':
        if 'procedure' in condition:
            for lang in condition['procedure']['procedure']:
                condition['procedure']['procedure'][lang] = process_rst_text(
                    condition['procedure']['procedure'][lang],
                    info,
                    lang
                )
        return condition

    # Process nested conditions recursively
    condition['conditions'] = [
        process_rst_condition(cond, info)
        for cond in condition['conditions']
    ]
    return condition
