import os
import sys
import re
import yaml
import json
import unicodedata
from jsonschema import validate, ValidationError, RefResolver
import argparse
from jinja2 import Template, Environment, FileSystemLoader
import datetime
from config import AVAILABLE_LANGUAGES, CHECK_TOOLS, SRCDIR, SCHEMA_FILENAMES, COMMON_SCHEMA_PATH, TEMPLATE_DIR, TEMPLATE_FILENAMES, MISC_INFO_SRCFILES, get_dest_dirnames, get_static_dest_files
from a11y_guidelines import Category, WCAG_SC, InfoRef, Guideline, Check, FAQ, FAQ_Tag, CheckTool

def main():
    args = parse_args()
    settings = process_arguments(args)
    build_all = settings.get('build_all')
    targets = settings.get('targets')
    LANG = settings.get('lang')
    DEST_DIRS = get_dest_dirnames(LANG)
    STATIC_FILES = get_static_dest_files(LANG)

    template_env = setup_template_environment()
    templates = load_templates(template_env)

    if not args.no_check:
        try:
            file_content = read_file_content(COMMON_SCHEMA_PATH)
            common_schema = json.loads(file_content)
        except Exception as e:
            handle_file_error(e, COMMON_SCHEMA_PATH)
        schema_path = f'file://{SRCDIR["schema"]}/'
        resolver = RefResolver(schema_path, common_schema)

    data = {
        'guidelines': [],
        'checks': [],
        'faqs': [],
        'faq_tags': [],
        'categories': [],
        'wcag_sc': []
    }

    makefile_vars = {
        'all_checks_target': STATIC_FILES['all_checks'],
        'faq_index_target': " ".join([STATIC_FILES[key] for key in ['faq_index', 'faq_tag_index', 'faq_article_index']]),
        'wcag_mapping_target': STATIC_FILES['wcag21mapping'],
        'priority_diff_target': STATIC_FILES['priority_diff'],
        'miscdefs_target': STATIC_FILES['miscdefs'],
        'wcag_sc': MISC_INFO_SRCFILES['wcag_sc'],
        'info_src': MISC_INFO_SRCFILES['info'],
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

    # Setup CheckTool instances
    for tool_id, tool_names in CHECK_TOOLS.items():
        CheckTool(tool_id, tool_names)
    
    # Set up check instances
    files = ls_dir(SRCDIR['checks'])
    makefile_vars['check_yaml'] = ' '.join(files)
    data['checks'] = [process_yaml_file(f, SRCDIR['schema'], SCHEMA_FILENAMES['checks'], args.no_check, resolver) for f in files]
    if not args.no_check:
        check_duplicate_values(data['checks'], 'id', 'Check ID')
    for check in data['checks']:
        Check(check)
    
    # Set up guideline category instances
    try:
        file_content = read_file_content(MISC_INFO_SRCFILES['gl_categories'])
        data['categories'] = json.loads(file_content)
    except Exception as e:
        handle_file_error(e, MISC_INFO_SRCFILES['gl_categories'])
    for id, names in data['categories'].items():
        Category(id, names)

    # Set up WCAG SC instances
    try:
        file_content = read_file_content(MISC_INFO_SRCFILES['wcag_sc'])
        data['wcag_sc'] = json.loads(file_content)
    except Exception as e:
        handle_file_error(e, MISC_INFO_SRCFILES['wcag_sc'])
    for sc in data['wcag_sc'].values():
        WCAG_SC(sc)
    
    # Set up guideline instances
    files = ls_dir(SRCDIR['guidelines'])
    makefile_vars['gl_yaml'] = ' '.join(files)
    data['guidelines'] = [process_yaml_file(f, SRCDIR['schema'], SCHEMA_FILENAMES['guidelines'], args.no_check, resolver) for f in files]
    if not args.no_check:
        check_duplicate_values(data['guidelines'], 'id', 'Guideline ID')
        check_duplicate_values(data['guidelines'], 'sortKey', 'Guideline sortKey')
    for gl in data['guidelines']:
        Guideline(gl)

    # Set up FAQ tag instances
    try:
        file_content = read_file_content(MISC_INFO_SRCFILES['faq_tags'])
        data['faq_tags'] = json.loads(file_content)
    except Exception as e:
        handle_file_error(e, MISC_INFO_SRCFILES['faq_tags'])
    for id, names in data['faq_tags'].items():
        FAQ_Tag(id, names)

    # Set up FAQ instances
    files = ls_dir(SRCDIR['faq'])
    makefile_vars['faq_yaml'] = ' '.join(files)
    data['faqs'] = [process_yaml_file(f, SRCDIR['schema'], SCHEMA_FILENAMES['faq'], args.no_check, resolver) for f in files]
    if not args.no_check:
        check_duplicate_values(data['faqs'], 'id', 'FAQ ID')
        check_duplicate_values(data['faqs'], 'sortKey', 'FAQ sortKey')
    for faq in data['faqs']:
        FAQ(faq)

    os.makedirs(DEST_DIRS['guidelines'], exist_ok=True)
    for cat in Category.list_all():
        filename = f'{cat.id}.rst'
        destfile = os.path.join(DEST_DIRS['guidelines'], filename)
        if build_all or destfile in targets:
            gl_object = [gl.template_object(LANG) for gl in cat.get_guidelines()]
            write_rst(templates['category_page'], {'lang': LANG, 'guidelines': gl_object}, destfile)

    os.makedirs(DEST_DIRS['checks'], exist_ok=True)
    if build_all or STATIC_FILES['all_checks'] in targets:
        allchecks = Check.template_object_all(LANG)
        write_rst(templates['allchecks_text'], {'allchecks': allchecks}, STATIC_FILES['all_checks'])

    for tool in CheckTool.list_all():
        filename = f'examples-{tool.id}.rst'
        destfile = os.path.join(DEST_DIRS['checks'], filename)
        if build_all or destfile:
            write_rst(templates['tool_example'], tool.example_template_object(LANG), destfile)
        
    os.makedirs(DEST_DIRS['faq_articles'], exist_ok=True)
    for faq in FAQ.list_all():
        filename = f'{faq.id}.rst'
        destfile = os.path.join(DEST_DIRS['faq_articles'], filename)
        if build_all or destfile in targets:
            write_rst(templates['faq_article'], faq.template_object(LANG), destfile)

    os.makedirs(DEST_DIRS['faq_tags'], exist_ok=True)
    for tag in FAQ_Tag.list_all():
        filename = f'{tag.id}.rst'
        destfile = os.path.join(DEST_DIRS['faq_tags'], filename)
        if tag.article_count() > 0 and build_all or destfile in targets:
            write_rst(templates['faq_tagpage'], tag.template_object(LANG), destfile)

    sorted_tags = sorted(FAQ_Tag.list_all(), key=lambda x: x.names[LANG])
    tags = [tag.template_object(LANG) for tag in sorted_tags if tag.article_count() > 0]
    tagpages = [tagpage.template_object(LANG) for tagpage in sorted_tags if tagpage.article_count() > 0]
    sorted_articles_by_date = FAQ.list_all(sort_by='date')
    sorted_articles_by_sortkey = FAQ.list_all(sort_by='sortKey')
    if build_all or STATIC_FILES['faq_index'] in targets:
        articles = [article.template_object(LANG) for article in sorted_articles_by_date]
        write_rst(templates['faq_index'], {'articles': articles, 'tags': tags}, STATIC_FILES['faq_index'])
        
    if build_all or STATIC_FILES['faq_tag_index'] in targets:
        write_rst(templates['faq_tag_index'], {'tags': tagpages}, STATIC_FILES['faq_tag_index'])

    if build_all or STATIC_FILES['FAQ_ARTICLE_INDEX_PATH'] in targets:
        articles = [article.template_object(LANG) for article in sorted_articles_by_sortkey]
        write_rst(templates['faq_article_index'], {'articles': articles}, STATIC_FILES['faq_article_index'])

    os.makedirs(DEST_DIRS['info2gl'], exist_ok=True)
    for info in InfoRef.get_all_internals():
        if len(info.guidelines) > 0:
            filename = f'{info.ref}.rst'
            destfile = os.path.join(DEST_DIRS['info2gl'], filename)
            if build_all or destfile in targets:
                write_rst(templates['info_to_gl'], {'guidelines': info.get_guidelines(LANG)}, destfile)

    os.makedirs(DEST_DIRS['info2faq'], exist_ok=True)
    for info in InfoRef.get_all_internals():
        if len(info.faqs) > 0:
            filename = f'{info.ref}.rst'
            destfile = os.path.join(DEST_DIRS['info2faq'], filename)
            makefile_vars_list['info_to_faq_target'].append(destfile)
            if build_all or destfile in targets:
                write_rst(templates['info_to_faq'], {'faqs': info.get_faqs()}, destfile)

    os.makedirs(DEST_DIRS['misc'], exist_ok=True)
    if build_all or STATIC_FILES['wcag21mapping'] in targets:
        sc_mapping = [sc.template_object(LANG) for sc in WCAG_SC.get_all().values() if len(sc.guidelines) > 0]
        write_rst(templates['wcag21mapping'], {'mapping': sc_mapping}, STATIC_FILES['wcag21mapping'])

    if build_all or STATIC_FILES['priority_diff'] in targets:
        diffs = [sc.template_object(LANG) for sc in WCAG_SC.get_all().values() if sc.level != sc.localPriority]
        write_rst(templates['priority_diff'], {'diffs': diffs}, STATIC_FILES['priority_diff'])

    if build_all or STATIC_FILES['miscdefs'] in targets:
        try:
            file_content = read_file_content(MISC_INFO_SRCFILES['info'])
            info_links = json.loads(file_content)
        except Exception as e:
            handle_file_error(e, MISC_INFO_SRCFILES['info'])

        external_info_links = []
        for link in info_links:
            external_info_links.append({
                'label': link,
                'text': info_links[link]['text'][LANG],
                'url': info_links[link]['url'][LANG]
            })
        write_rst(templates['miscdefs'], {'links': external_info_links}, STATIC_FILES['miscdefs'])

    if build_all or STATIC_FILES['makefile'] in targets:
        build_depends = []
        for cat in Category.list_all():
            filename = f'{cat.id}.rst'
            destfile = os.path.join(DEST_DIRS['guidelines'], filename)
            makefile_vars_list['guideline_category_target'].append(destfile)
            build_depends.append({'target': destfile, 'depends': ' '.join(cat.get_dependency())})

        for tool in CheckTool.list_all():
            filename = f'examples-{tool.id}.rst'
            destfile = os.path.join(DEST_DIRS['checks'], filename)
            makefile_vars_list['check_example_target'].append(destfile)
            build_depends.append({'target': destfile, 'depends': ' '.join(tool.get_dependency())})

        for faq in FAQ.list_all():
            filename = f'{faq.id}.rst'
            destfile = os.path.join(DEST_DIRS['faq_articles'], filename)
            makefile_vars_list['faq_article_target'].append(destfile)
            build_depends.append({'target': destfile, 'depends': ' '.join(faq.get_dependency())})

        for tag in FAQ_Tag.list_all():
            if tag.article_count() == 0:
                continue
            filename = f'{tag.id}.rst'
            destfile = os.path.join(DEST_DIRS['faq_tags'], filename)
            makefile_vars_list['faq_tagpage_target'].append(destfile)
            build_depends.append({'target': destfile, 'depends': [' '.join(faq.get_dependency()) for faq in tag.faqs]})

        for info in InfoRef.get_all_internals():
            if len(info.guidelines) > 0:
                filename = f'{info.ref}.rst'
                destfile = os.path.join(DEST_DIRS['info2gl'], filename)
                makefile_vars_list['info_to_gl_target'].append(destfile)
                build_depends.append({'target': destfile, 'depends': ' '.join([guideline.src_path for guideline in info.guidelines])})

            if info.internal and len(info.faqs) > 0:
                filename = f'{info.ref}.rst'
                destfile = os.path.join(DEST_DIRS['info2faq'], filename)
                makefile_vars_list['info_to_faq_target'].append(destfile)
                build_depends.append({'target': destfile, 'depends': ' '.join([faq.src_path for faq in info.faqs])})

        for key, value in makefile_vars_list.items():
            makefile_vars[key] = ' '.join(value)
            makefile_vars['depends'] = build_depends
        destfile = STATIC_FILES['makefile']
        write_rst(templates['makefile'], makefile_vars, destfile)


def ls_dir(dir):
    files = []
    for currentDir, dirs, fs in os.walk(dir):
        for f in fs:
            files.append(os.path.join(currentDir, f))
    return files

def read_file_content(file_path):
    """
    Read and return the content of a file.

    Args:
        file_path: Path to the file.

    Returns:
        The content of the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise e

def handle_file_error(e, file_path):
    """
    Handle file-related errors.

    Args:
        e: The exception object.
        file_path: Path to the file that caused the error.
    """
    print(f"Error with file {file_path}: {e}", file=sys.stderr)
    sys.exit(1)

def read_yaml_file(file):
    try:
        with open(file, encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        print(f'Exception occurred while loading YAML {file}...', file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

    return data

def validate_data(data, schema_file, common_resolver=None):
    try:
        with open(schema_file) as f:
            schema = json.load(f)
    except Exception as e:
        print(f'Exception occurred while loading schema {schema_file}...', file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

    try:
        validate(data, schema, resolver=common_resolver)
    except ValidationError as e:
        raise ValueError("Validation failed.") from e

def process_yaml_file(file_path, schema_dir, schema_file, no_check, resolver):
    """
    Read, validate, and process a YAML file.

    Args:
        file_path: The path to the YAML file.
        schema_dir: The directory containing the schema file.
        schema_file: The schema file for validation.
        no_check: Boolean indicating whether to skip validation.
        resolver: The resolver for schema validation.

    Returns:
        The processed YAML data with an additional source path.
    """
    data = read_yaml_file(file_path)
    
    if not no_check:
        try:
            validate_data(data, os.path.join(schema_dir, schema_file), resolver)
        except ValueError as e:
            print(f'Exception occurred while validating {file_path}...', file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)

    data['src_path'] = os.path.relpath(file_path, start=os.getcwd())
    return data

def make_heading(title, level, className=""):
    
    def _isMultiByte(c):
        return unicodedata.east_asian_width(c) in ['F', 'W', 'A']
        
    def _width(c):
        return 2 if _isMultiByte(c) else 1

    def width(s):
        return sum([_width(c) for c in s])
        
    # Modify heading_styles accordingly
    heading_styles = [('#', True), ('*', True), ('=', False), ('-', False), ('^', False), ('"', False)]
    
    if not 1 <= level <= len(heading_styles):
        raise ValueError(f'Invalid level: {level}. Must be between 1 and {len(heading_styles)}')

    char, overline = heading_styles[level - 1]
    line = char * width(title)

    heading_lines = []

    if className:
        heading_lines.append(f'.. rst-class:: {className}\n')

    if overline:
        heading_lines.append(line)

    heading_lines.append(title)
    heading_lines.append(line)

    return '\n'.join(heading_lines)

def check_duplicate_values(lst, key, dataset):
    # Extract the values for the given key across the list of dictionaries
    values = [d[key] for d in lst]

    # Find the non-unique values
    non_unique_values = [value for value in values if values.count(value) > 1]

    # Convert to set to remove duplicates
    non_unique_values = set(non_unique_values)

    # Check if there are any non-unique values and raise error if so
    if non_unique_values:
        raise ValueError(f"Duplicate values in {dataset}: {non_unique_values}")

def parse_args():
    parser = argparse.ArgumentParser(description="Process YAML files into rst files for the a11y-guidelines.")
    parser.add_argument('--no-check', action='store_true', help='Do not run various checks of YAML files')
    parser.add_argument('--lang', '-l', type=str, choices=AVAILABLE_LANGUAGES, default='ja', help=f'the language of the output file ({" ".join(AVAILABLE_LANGUAGES)})')
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
        'lang': args.lang
    }

    # 例：新しいオプション 'verbose' の処理
    # if hasattr(args, 'verbose'):
    #     settings['verbose'] = args.verbose

    return settings

def setup_template_environment():
    """
    Set up the Jinja2 template environment.

    Returns:
        The configured Jinja2 environment object.
    """
    template_env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR)
    )
    template_env.filters['make_heading'] = make_heading
    return template_env

def load_templates(template_env):
    """
    Load the necessary templates using the provided Jinja2 environment.

    Args:
        template_env: The Jinja2 environment object.

    Returns:
        A dictionary of Jinja2 templates.
    """

    templates = {name: template_env.get_template(filename) for name, filename in TEMPLATE_FILENAMES.items()}
    return templates

def write_rst(template, data, output_path):
    """
    Render a Jinja2 template with provided data and write the output to an RST file.

    Args:
        template: Jinja2 template object.
        data: Data to be used in the template.
        output_path: Path to the output RST file.

    Returns:
        None
    """
    rendered_content = template.render(data)
    with open(output_path, mode='w', encoding='utf-8', newline='\n') as file:
        file.write(rendered_content)

if __name__ == "__main__":
    main()
