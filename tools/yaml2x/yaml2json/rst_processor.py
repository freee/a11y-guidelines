"""
RST text processing module.

This module handles the processing of RST markup in text content,
including references, keyboard shortcuts, and text width formatting.
"""

import re
from typing import Dict, Any

# Regular expression patterns
RST_REF_PATTERN = re.compile(r':ref:`([-a-z0-9]+)`')  # Match reference IDs
RST_KBD_PATTERN = re.compile(r':kbd:`(.+)`')  # Match keyboard shortcuts

def normalize_text(text: str) -> str:
    """Normalize whitespace and spacing between characters."""
    # Remove leading and trailing whitespaces
    text = text.strip()

    # Define regexp for half and full width chars
    fullwidth_chars = r'[----]'
    halfwidth_chars = r'[---]'

    # Remove whitespaces between fullwidth chars
    text = re.sub(rf'({fullwidth_chars})\s+({fullwidth_chars})', r'\1\2', text)

    # Remove whitespaces between halfwidth chars and full width chars
    text = re.sub(rf'({fullwidth_chars})\s+({halfwidth_chars})', r'\1\2', text)
    text = re.sub(rf'({halfwidth_chars})\s+({fullwidth_chars})', r'\1\2', text)

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
