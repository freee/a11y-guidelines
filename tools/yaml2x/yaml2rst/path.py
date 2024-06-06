import os
from config import AVAILABLE_LANGUAGES

# Directories
DATA_DIR = 'data'
YAML_DIR = 'yaml'
JSON_DIR = 'json'
DEST_DIR_BASE = 'source'

# axe-core directories
AXE_SRC_BASE = 'vendor/axe-core'
AXE_RULES_DIR = 'lib/rules'
AXE_LOCALE_DIR = 'locales'
AXE_LOCALE_JA_FILE = 'ja.json'
AXE_PKG_FILE = 'package.json'

# File paths
FAQ_INDEX_FILENAME = 'index.rst'
MAKEFILE_FILENAME = 'incfiles.mk'
ALL_CHECKS_FILENAME = "allchecks.rst"
WCAG_MAPPING_FILENAME = "wcag21-mapping.rst"
PRIORITY_DIFF_FILENAME = "priority-diff.rst"
MISCDEFS_FILENAME = "defs.txt"
AXE_RULES_FILENAME = 'axe-rules.rst'

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
    'miscdefs': 'misc-defs.txt',
    'axe_rules': 'axe-rules.rst',
    'makefile': 'incfiles.mk',
}
def get_dest_dirnames(basedir, lang):
    """
    Returns a dictionary of destination directory names for the given language.

    Args:
        lang (str): Language code

    Returns:
        dict: Dictionary of destination directory names
    """
    langdir = os.path.join(basedir, lang)
    if len(AVAILABLE_LANGUAGES) == 1:
        langdir = basedir
    inc_dest_dir = os.path.join(langdir, DEST_DIR_BASE, 'inc')
    faq_dest_dir = os.path.join(langdir, DEST_DIR_BASE, 'faq')
    return {
        'base': langdir,
        'guidelines': os.path.join(inc_dest_dir, 'gl'),
        'checks': os.path.join(inc_dest_dir, 'checks'),
        'misc': os.path.join(inc_dest_dir, 'misc'),
        'info2gl': os.path.join(inc_dest_dir, 'info2gl'),
        'info2faq': os.path.join(inc_dest_dir, 'info2faq'),
        'faq_base': faq_dest_dir,
        'faq_articles': os.path.join(faq_dest_dir, 'articles'),
        'faq_tags': os.path.join(faq_dest_dir, 'tags')
    }

def get_static_dest_files(basedir, lang):
    """
    Returns a dictionary of static destination file paths for the given language.

    Args:
        lang (str): Language code

    Returns:
        dict: Dictionary of static destination file paths
    """
    dest_dirnames = get_dest_dirnames(basedir, lang)
    return {
        'all_checks': os.path.join(dest_dirnames['checks'], ALL_CHECKS_FILENAME),
        'wcag21mapping': os.path.join(dest_dirnames['misc'], WCAG_MAPPING_FILENAME),
        'priority_diff': os.path.join(dest_dirnames['misc'], PRIORITY_DIFF_FILENAME),
        'miscdefs': os.path.join(dest_dirnames['misc'], MISCDEFS_FILENAME),
        'faq_index': os.path.join(dest_dirnames['faq_base'], FAQ_INDEX_FILENAME),
        'faq_article_index': os.path.join(dest_dirnames['faq_articles'], FAQ_INDEX_FILENAME),
        'faq_tag_index': os.path.join(dest_dirnames['faq_tags'], FAQ_INDEX_FILENAME),
        'makefile': os.path.join(dest_dirnames['base'], MAKEFILE_FILENAME),
        'axe_rules': os.path.join(dest_dirnames['misc'], AXE_RULES_FILENAME)
    }

