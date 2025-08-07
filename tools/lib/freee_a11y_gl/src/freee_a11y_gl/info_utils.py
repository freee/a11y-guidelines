"""
Utility functions for info and link processing.
"""

import pickle
from pathlib import Path
from typing import Dict, Any, List, Optional

# Constants
LANGUAGES: List[str] = ['ja', 'en']
PICKLE_PATH: str = 'build/doctrees/environment.pickle'


class InfoUtilsError(Exception):
    """Custom exception for info utilities related errors."""
    pass


def get_info_links(basedir: Optional[str] = None, baseurl: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract labels and links from the environment pickle file.

    Args:
        basedir: Project root directory containing language-specific data.
                If None, value from settings will be used. If not in settings, defaults to '.'
        baseurl: Base URL for related information links.
                If None, value from settings will be used. If not in settings, defaults to ''

    Returns:
        Dictionary containing extracted labels and their associated information

    Raises:
        InfoUtilsError: If pickle file cannot be loaded or processed
    """
    from .config import Config

    # Get values from settings if not provided
    effective_basedir = basedir if basedir is not None else Config.get_basedir()
    effective_baseurl = baseurl if baseurl is not None else Config.get_base_url(None)

    info: Dict[str, Dict[str, Dict[str, str]]] = {}
    path_prefix = {
        'ja': '',
        'en': 'en/'
    }

    for lang in LANGUAGES:
        pickle_path = Path(effective_basedir) / lang / PICKLE_PATH
        try:
            with open(pickle_path, 'rb') as f:
                doctree = pickle.load(f)
        except Exception as e:
            raise InfoUtilsError(f'Failed to load pickle file {pickle_path}: {str(e)}')

        labels = doctree.domaindata['std']['labels']
        for label in labels:
            if not all(labels[label][i] for i in range(3)):
                continue

            if label not in info:
                info[label] = {
                    'text': {},
                    'url': {}
                }
            info[label]['text'][lang] = labels[label][2]
            info[label]['url'][lang] = f'{effective_baseurl}/{path_prefix[lang]}{labels[label][0]}.html#{labels[label][1]}'

    return info
