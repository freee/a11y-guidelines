import os

# Default file locations and other configuration options for yaml2rst
#
# List of languages that are available for file generation.
AVAILABLE_LANGUAGES = ['ja']

# List of check tools and their names
CHECK_TOOLS = {
    'nvda': {
        'ja': 'NVDA',
        'en': 'NVDA'
    },
    'macos-vo': {
        'ja': 'macOS VoiceOver',
        'en': 'macOS VoiceOver'
    },
    'axe': {
        'ja': 'axe DevTools',
        'en': 'axe DevTools'
    },
    'ios-vo': {
        'ja': 'iOS VoiceOver',
        'en': 'iOS VoiceOver'
    },
    'android-tb': {
        'ja': 'Android TalkBack',
        'en': 'Android TalkBack'
    },
    'keyboard': {
        'ja': 'キーボード操作',
        'en': 'Keyboard'
    },
    'misc': {
        'ja': 'その他のツール',
        'en': 'Miscellaneous Tools'
    }
}

# Check targets
CHECK_TARGETS = {
    'design': {
        'ja': 'デザイン',
        'en': 'Design'
    },
    'code': {
        'ja': 'コード',
        'en': 'Code'
    },
    'product': {
        'ja': 'プロダクト',
        'en': 'Product'
    }
}

# Names for checks/guidelines/procedures target platforms
PLATFORM_NAMES = {
    'web': {
        'ja': 'Web',
        'en': 'Web'
    },
    'mobile': {
        'ja': 'モバイル',
        'en': 'Mobile'
    },
    'general': {
        'ja': 'Web、モバイル',
        'en': 'Web, Mobile'
    }
}

# Severity tags and its display names
SEVERITY_TAGS = {
    'critical': {
        'ja': '[CRITICAL]',
        'en': '[CRITICAL]'
    },
    'major': {
        'ja': '[MAJOR]',
        'en': '[MAJOR]'
    },
    'normal': {
        'ja': '[NORMAL]',
        'en': '[NORMAL]'
    },
    'minor': {
        'ja': '[MINOR]',
        'en': '[MINOR]'
    }
}

# Possible targets for implementation examples
IMPLEMENTATION_TARGETS = {
    'web': {
        'ja': 'Web',
        'en': 'Web'
    },
    'android': {
        'ja': 'Android',
        'en': 'Android'
    },
    'ios': {
        'ja': 'iOS',
        'en': 'iOS'
    }
}

# Directories
DATA_DIR = 'data'
YAML_DIR = os.path.join(DATA_DIR, 'yaml')
JSON_DIR = os.path.join(DATA_DIR, 'json')
DEST_DIR_BASE = 'source'

SRCDIR = {
    'guidelines': os.path.join(YAML_DIR, "gl"),
    'checks': os.path.join(YAML_DIR, 'checks'),
    'faq': os.path.join(YAML_DIR, 'faq'),
    'schema': os.path.join(JSON_DIR, 'schemas')
}

SCHEMA_FILENAMES = {
    'guidelines': 'guideline.json',
    'checks': 'check.json',
    'faq': 'faq.json',
    'common': 'common.json'
}
COMMON_SCHEMA_PATH = os.path.join(SRCDIR['schema'], SCHEMA_FILENAMES['common'])

# File paths
FAQ_INDEX_FILENAME = 'index.rst'
MAKEFILE_FILENAME = 'incfiles.mk'
ALL_CHECKS_FILENAME = "allchecks.rst"
WCAG_MAPPING_FILENAME = "wcag21-mapping.rst"
PRIORITY_DIFF_FILENAME = "priority-diff.rst"
MISCDEFS_FILENAME = "defs.txt"

MISC_INFO_SRCFILES = {
    'wcag_sc': os.path.join(JSON_DIR, 'wcag-sc.json'),
    'gl_categories': os.path.join(JSON_DIR, 'guideline-categories.json'),
    'faq_tags': os.path.join(JSON_DIR, 'faq-tags.json'),
    'info': os.path.join(JSON_DIR, 'info.json')
}

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
TEMPLATE_FILENAMES = {
    'tool_example': 'checks/examples-tool.rst',
    'allchecks_text': 'checks/allchecks.rst',
    'category_page': 'gl-category.rst',
    'info_to_gl': 'info_to_gl.rst',
    'info_to_faq': 'info_to_faq.rst',
    'faq_article': 'faq/article.rst',
    'faq_tagpage': 'faq/tagpage.rst',
    'faq_index': 'faq/index.rst',
    'faq_tag_index': 'faq/tag-index.rst',
    'faq_article_index': 'faq/article-index.rst',
    'wcag21mapping': 'wcag21-mapping.rst',
    'priority_diff': 'priority-diff.rst',
    'makefile': 'incfiles.mk',
    'miscdefs': 'misc-defs.txt'
}

def get_dest_dirnames(lang):
    """
    Returns a dictionary of destination directory names for the given language.

    Args:
        lang (str): Language code

    Returns:
        dict: Dictionary of destination directory names
    """
    if len(AVAILABLE_LANGUAGES) == 1:
        lang = ''
    inc_dest_dir = os.path.join(lang, DEST_DIR_BASE, 'inc')
    faq_dest_dir = os.path.join(lang, DEST_DIR_BASE, 'faq')
    return {
        'base': lang,
        'guidelines': os.path.join(inc_dest_dir, 'gl'),
        'checks': os.path.join(inc_dest_dir, 'checks'),
        'misc': os.path.join(inc_dest_dir, 'misc'),
        'info2gl': os.path.join(inc_dest_dir, 'info2gl'),
        'info2faq': os.path.join(inc_dest_dir, 'info2faq'),
        'faq_base': faq_dest_dir,
        'faq_articles': os.path.join(faq_dest_dir, 'articles'),
        'faq_tags': os.path.join(faq_dest_dir, 'tags')
    }

def get_static_dest_files(lang):
    """
    Returns a dictionary of static destination file paths for the given language.

    Args:
        lang (str): Language code

    Returns:
        dict: Dictionary of static destination file paths
    """
    dest_dirnames = get_dest_dirnames(lang)
    return {
        'all_checks': os.path.join(dest_dirnames['checks'], ALL_CHECKS_FILENAME),
        'wcag21mapping': os.path.join(dest_dirnames['misc'], WCAG_MAPPING_FILENAME),
        'priority_diff': os.path.join(dest_dirnames['misc'], PRIORITY_DIFF_FILENAME),
        'miscdefs': os.path.join(dest_dirnames['misc'], MISCDEFS_FILENAME),
        'faq_index': os.path.join(dest_dirnames['faq_base'], FAQ_INDEX_FILENAME),
        'faq_article_index': os.path.join(dest_dirnames['faq_articles'], FAQ_INDEX_FILENAME),
        'faq_tag_index': os.path.join(dest_dirnames['faq_tags'], FAQ_INDEX_FILENAME),
        'makefile': os.path.join(dest_dirnames['base'], MAKEFILE_FILENAME)
    }
