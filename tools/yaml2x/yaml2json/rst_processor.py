"""
RST text processing module.

This module handles the processing of RST markup in text content,
including references, keyboard shortcuts, and text width formatting.
"""

import re
from typing import Dict, Any

# Regular expression patterns
RST_REF_PATTERN = re.compile(r':ref:`([-a-z0-9]+)`')
RST_KBD_PATTERN = re.compile(r':kbd:`(.+)`')
FULLWIDTH_CHARS = r'[----]'
HALFWIDTH_CHARS = r'[---]'

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
    # Replace references
    text = RST_REF_PATTERN.sub(lambda m: info[m.group(1)]['text'][lang], text)
    
    # Replace keyboard shortcuts
    text = RST_KBD_PATTERN.sub(lambda m: m.group(1), text)
    
    # Clean up whitespace
    text = text.strip()
    
    # Remove unnecessary spaces between width chars
    text = re.sub(rf'({FULLWIDTH_CHARS})\s+({FULLWIDTH_CHARS})', r'\1\2', text)
    text = re.sub(rf'({FULLWIDTH_CHARS})\s+({HALFWIDTH_CHARS})', r'\1\2', text)
    text = re.sub(rf'({HALFWIDTH_CHARS})\s+({FULLWIDTH_CHARS})', r'\1\2', text)
    
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
