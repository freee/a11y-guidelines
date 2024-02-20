import os
import argparse
import config
from path import get_dest_dirnames, get_static_dest_files, get_src_path, TEMPLATE_DIR, TEMPLATE_FILENAMES
from template_manager import TemplateManager

def setup_parameters():
    args = parse_args()
    return process_arguments(args)

def setup_constants(settings):
    lang = settings['lang']
    basedir = settings['basedir']
    DEST_DIRS = get_dest_dirnames(basedir, lang)
    STATIC_FILES = get_static_dest_files(basedir, lang)
    src_path = get_src_path(basedir)

    MAKEFILE_VARS = {
            'all_checks_target': STATIC_FILES['all_checks'],
            'faq_index_target': " ".join([STATIC_FILES[key] for key in ['faq_index', 'faq_tag_index', 'faq_article_index']]),
            'wcag_mapping_target': STATIC_FILES['wcag21mapping'],
            'priority_diff_target': STATIC_FILES['priority_diff'],
            'miscdefs_target': STATIC_FILES['miscdefs'],
            'wcag_sc': src_path['wcag_sc'],
            'info_src': src_path['info']
    }

    return DEST_DIRS, STATIC_FILES, MAKEFILE_VARS

def setup_variables():
    makefile_vars = {
        'gl_yaml': '',
        'check_yaml': '',
        'faq_yaml': ''
    }
    makefile_vars_list = {
        'guideline_category_target': [],
        'check_example_target': [],
        'faq_article_target': [],
        'faq_tagpage_target': [],
        'info_to_gl_target': [],
        'info_to_faq_target': [],
    }
    return makefile_vars, makefile_vars_list

def setup_templates(lang):
    templates = {}
    template_dir = os.path.join(TEMPLATE_DIR, lang)
    for name, filename in TEMPLATE_FILENAMES.items():
        template = TemplateManager(template_dir)
        templates[name] = template.load(filename)
    return templates

def parse_args():
    languages = config.AVAILABLE_LANGUAGES
    parser = argparse.ArgumentParser(description="Process YAML files into rst files for the a11y-guidelines.")
    parser.add_argument('--no-check', action='store_true', help='Do not run various checks of YAML files')
    parser.add_argument('--lang', '-l', type=str, choices=languages, default='ja', help=f'the language of the output file ({" ".join(languages)})')
    parser.add_argument('--basedir', '-b', type=str, default='..', help='Base directory where the data directory is located.')
    parser.add_argument('files', nargs='*', help='Filenames')
    return parser.parse_args()

def process_arguments(args):
    """
    Process the command-line arguments to determine the build mode, target files, and other options.

    Args:
        args: The parsed command-line arguments.

    Returns:
        A dictionary containing settings derived from the command-line arguments.
    """
    settings = {
        'build_all': not args.files,
        'targets': args.files if args.files else [],
        'no_check': args.no_check,
        'lang': args.lang,
        'basedir': args.basedir
    }
    return settings
