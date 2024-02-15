import os
import sys
import json
import yaml
from jsonschema import validate, ValidationError, RefResolver
import app_initializer
from path import SRCDIR, SCHEMA_FILENAMES, COMMON_SCHEMA_PATH, MISC_INFO_SRCFILES
from constants import CHECK_TOOLS
from a11y_guidelines import Category, WcagSc, InfoRef, Guideline, Check, Faq, FaqTag, CheckTool, RelationshipManager

def main():
    settings = app_initializer.setup_parameters()
    build_all, targets, lang, no_check = (
        settings.get('build_all'),
        settings.get('targets'),
        settings.get('lang'),
        settings.get('no_check')
    )
    DEST_DIRS, STATIC_FILES, MAKEFILE_VARS = app_initializer.setup_constants(lang)
    templates = app_initializer.setup_templates()

    if not no_check:
        try:
            file_content = read_file_content(COMMON_SCHEMA_PATH)
            common_schema = json.loads(file_content)
        except Exception as e:
            handle_file_error(e, COMMON_SCHEMA_PATH)
        schema_path = f'file://{SRCDIR["schema"]}/'
        resolver = RefResolver(schema_path, common_schema)

    data, makefile_vars, makefile_vars_list = app_initializer.setup_variables()

    # Setup CheckTool instances
    for tool_id, tool_names in CHECK_TOOLS.items():
        CheckTool(tool_id, tool_names)

    # Set up check instances
    files = ls_dir(SRCDIR['checks'])
    makefile_vars['check_yaml'] = ' '.join(files)
    data['checks'] = [process_yaml_file(f, SRCDIR['schema'], SCHEMA_FILENAMES['checks'], no_check, resolver) for f in files]
    if not no_check:
        check_duplicate_values(data['checks'], 'id', 'Check ID')
    for check in data['checks']:
        Check(check)

    # Set up guideline category instances
    try:
        file_content = read_file_content(MISC_INFO_SRCFILES['gl_categories'])
        data['categories'] = json.loads(file_content)
    except Exception as e:
        handle_file_error(e, MISC_INFO_SRCFILES['gl_categories'])
    for category_id, names in data['categories'].items():
        Category(category_id, names)

    # Set up WCAG SC instances
    try:
        file_content = read_file_content(MISC_INFO_SRCFILES['wcag_sc'])
        data['wcag_sc'] = json.loads(file_content)
    except Exception as e:
        handle_file_error(e, MISC_INFO_SRCFILES['wcag_sc'])
    for sc in data['wcag_sc'].values():
        WcagSc(sc)

    # Set up guideline instances
    files = ls_dir(SRCDIR['guidelines'])
    makefile_vars['gl_yaml'] = ' '.join(files)
    data['guidelines'] = [process_yaml_file(f, SRCDIR['schema'], SCHEMA_FILENAMES['guidelines'], no_check, resolver) for f in files]
    if not no_check:
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
    for tag_id, names in data['faq_tags'].items():
        FaqTag(tag_id, names)

    # Set up FAQ instances
    files = ls_dir(SRCDIR['faq'])
    makefile_vars['faq_yaml'] = ' '.join(files)
    data['faqs'] = [process_yaml_file(f, SRCDIR['schema'], SCHEMA_FILENAMES['faq'], no_check, resolver) for f in files]
    if not no_check:
        check_duplicate_values(data['faqs'], 'id', 'FAQ ID')
        check_duplicate_values(data['faqs'], 'sortKey', 'FAQ sortKey')
    for faq in data['faqs']:
        Faq(faq)

    rel = RelationshipManager()
    os.makedirs(DEST_DIRS['guidelines'], exist_ok=True)
    for category, guidelines in rel.get_guidelines_to_category().items():
        filename = f'{category}.rst'
        destfile = os.path.join(DEST_DIRS['guidelines'], filename)
        if build_all or destfile in targets:
            gl_object = [gl.template_object(lang) for gl in guidelines]
            templates['category_page'].write_rst({'lang': lang, 'guidelines': gl_object}, destfile)

    os.makedirs(DEST_DIRS['checks'], exist_ok=True)
    if build_all or STATIC_FILES['all_checks'] in targets:
        allchecks = Check.template_object_all(lang)
        templates['allchecks_text'].write_rst({'allchecks': allchecks}, STATIC_FILES['all_checks'])

    for tool in CheckTool.list_all():
        filename = f'examples-{tool.id}.rst'
        destfile = os.path.join(DEST_DIRS['checks'], filename)
        if build_all or destfile:
            templates['tool_example'].write_rst(tool.example_template_object(lang), destfile)

    os.makedirs(DEST_DIRS['faq_articles'], exist_ok=True)
    for faq in Faq.list_all():
        filename = f'{faq.id}.rst'
        destfile = os.path.join(DEST_DIRS['faq_articles'], filename)
        if build_all or destfile in targets:
            templates['faq_article'].write_rst(faq.template_object(lang), destfile)

    os.makedirs(DEST_DIRS['faq_tags'], exist_ok=True)
    for tag in FaqTag.list_all():
        filename = f'{tag.id}.rst'
        destfile = os.path.join(DEST_DIRS['faq_tags'], filename)
        if tag.article_count() > 0 and build_all or destfile in targets:
            templates['faq_tagpage'].write_rst(tag.template_object(lang), destfile)

    sorted_tags = sorted(FaqTag.list_all(), key=lambda x: x.names[lang])
    tags = [tag.template_object(lang) for tag in sorted_tags if tag.article_count() > 0]
    tagpages = [tagpage.template_object(lang) for tagpage in sorted_tags if tagpage.article_count() > 0]
    if build_all or STATIC_FILES['faq_index'] in targets:
        articles = [article.template_object(lang) for article in Faq.list_all(sort_by='date')]
        templates['faq_index'].write_rst({'articles': articles, 'tags': tags}, STATIC_FILES['faq_index'])

    if build_all or STATIC_FILES['faq_tag_index'] in targets:
        templates['faq_tag_index'].write_rst({'tags': tagpages}, STATIC_FILES['faq_tag_index'])

    if build_all or STATIC_FILES['FAQ_ARTICLE_INDEX_PATH'] in targets:
        articles = [article.template_object(lang) for article in Faq.list_all(sort_by='sortKey')]
        templates['faq_article_index'].write_rst({'articles': articles}, STATIC_FILES['faq_article_index'])

    os.makedirs(DEST_DIRS['info2gl'], exist_ok=True)
    for info in InfoRef.get_all_internals():
        if len(rel.get_info_to_guidelines(info)) > 0:
            filename = f'{info.ref}.rst'
            destfile = os.path.join(DEST_DIRS['info2gl'], filename)
            if build_all or destfile in targets:
                sorted_guidelines = sorted(rel.get_info_to_guidelines(info), key=lambda item: item.sort_key)
                guidelines = [guideline.get_category_and_id(lang) for guideline in sorted_guidelines]
                templates['info_to_gl'].write_rst({'guidelines': guidelines}, destfile)

    os.makedirs(DEST_DIRS['info2faq'], exist_ok=True)
    for info in InfoRef.get_all_internals():
        if len(rel.get_info_to_faqs(info)) > 0:
            filename = f'{info.ref}.rst'
            destfile = os.path.join(DEST_DIRS['info2faq'], filename)
            makefile_vars_list['info_to_faq_target'].append(destfile)
            if build_all or destfile in targets:
                templates['info_to_faq'].write_rst({'faqs': [faq.id for faq in rel.get_info_to_faqs(info)]}, destfile)

    os.makedirs(DEST_DIRS['misc'], exist_ok=True)
    if build_all or STATIC_FILES['wcag21mapping'] in targets:
        sc_mapping = [sc.template_object(lang) for sc in WcagSc.get_all().values() if len(rel.get_sc_to_guidelines(sc)) > 0]
        templates['wcag21mapping'].write_rst({'mapping': sc_mapping}, STATIC_FILES['wcag21mapping'])

    if build_all or STATIC_FILES['priority_diff'] in targets:
        diffs = [sc.template_object(lang) for sc in WcagSc.get_all().values() if sc.level != sc.local_priority]
        templates['priority_diff'].write_rst({'diffs': diffs}, STATIC_FILES['priority_diff'])

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
                'text': info_links[link]['text'][lang],
                'url': info_links[link]['url'][lang]
            })
        templates['miscdefs'].write_rst({'links': external_info_links}, STATIC_FILES['miscdefs'])

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

        for faq in Faq.list_all():
            filename = f'{faq.id}.rst'
            destfile = os.path.join(DEST_DIRS['faq_articles'], filename)
            makefile_vars_list['faq_article_target'].append(destfile)
            build_depends.append({'target': destfile, 'depends': ' '.join(faq.get_dependency())})

        for tag in FaqTag.list_all():
            if tag.article_count() == 0:
                continue
            filename = f'{tag.id}.rst'
            destfile = os.path.join(DEST_DIRS['faq_tags'], filename)
            makefile_vars_list['faq_tagpage_target'].append(destfile)
            build_depends.append({'target': destfile, 'depends': [' '.join(faq.get_dependency()) for faq in rel.get_tag_to_faqs(tag)]})

        for info in InfoRef.get_all_internals():
            if len(rel.get_info_to_guidelines(info)) > 0:
                filename = f'{info.ref}.rst'
                destfile = os.path.join(DEST_DIRS['info2gl'], filename)
                makefile_vars_list['info_to_gl_target'].append(destfile)
                build_depends.append({'target': destfile, 'depends': ' '.join([guideline.src_path for guideline in rel.get_info_to_guidelines(info)])})

            if info.internal and len(rel.get_info_to_faqs(info)) > 0:
                filename = f'{info.ref}.rst'
                destfile = os.path.join(DEST_DIRS['info2faq'], filename)
                makefile_vars_list['info_to_faq_target'].append(destfile)
                build_depends.append({'target': destfile, 'depends': ' '.join([faq.src_path for faq in rel.get_info_to_faqs(info)])})

        for key, value in makefile_vars_list.items():
            makefile_vars[key] = ' '.join(value)
            makefile_vars['depends'] = build_depends
        destfile = STATIC_FILES['makefile']
        templates['makefile'].write_rst({**makefile_vars, **MAKEFILE_VARS}, destfile)

def ls_dir(dirname):
    files = []
    for currentDir, dirs, fs in os.walk(dirname):
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



if __name__ == "__main__":
    main()
