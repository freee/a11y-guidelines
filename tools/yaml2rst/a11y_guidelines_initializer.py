import os
import sys
import json
import yaml
from jsonschema import validate, ValidationError, RefResolver
from a11y_guidelines import Category, WcagSc, InfoRef, Guideline, Check, Faq, FaqTag, CheckTool, RelationshipManager
from constants import CHECK_TOOLS
from path import get_src_path

def setup_instances(settings):
    no_check = settings['no_check']
    basedir = settings['basedir']
    src_path = get_src_path(basedir)
    # Mapping of entity type, srcdir, schema filename, and constructor.
    # The order is important for the initialization of the instances.
    entity_config = [
        ('check', src_path['checks'], src_path['schema_filenames']['checks'], Check),
        ('guideline', src_path['guidelines'], src_path['schema_filenames']['guidelines'], Guideline),
        ('faq', src_path['faq'], src_path['schema_filenames']['faq'], Faq)
    ]
    static_entity_config = [
        ('category', src_path['gl_categories'], Category),
        ('wcag_sc', src_path['wcag_sc'], WcagSc),
        ('faq_tag', src_path['faq_tags'], FaqTag),
        ('external_info', src_path['info'], InfoRef)
    ]

    if not no_check:
        resolver = setup_resolver(src_path)
    else:
        resolver = None

    # Setup CheckTool instances
    for tool_id, tool_names in CHECK_TOOLS.items():
        CheckTool(tool_id, tool_names)

    for entity_type, srcfile, constructor in static_entity_config:
        process_static_entity_file(entity_type, srcfile, constructor)

    for entity_type, srcdir, schema_filename, constructor in entity_config:
        process_entity_files(entity_type, srcdir, src_path['schema'], schema_filename, resolver, constructor)

    return RelationshipManager()

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
        file_content = read_file_content(file)
    except Exception as e:
        handle_file_error(e, file)
    data = yaml.safe_load(file_content)

    return data

def validate_data(data, schema_file, common_resolver=None):
    try:
        schema_content = read_file_content(schema_file)
        schema = json.loads(schema_content)
    except Exception as e:
        raise e
    try:
        validate(data, schema, resolver=common_resolver)
    except ValidationError as e:
        raise ValueError("Validation failed.") from e

def setup_resolver(src_path):
    try:
        file_content = read_file_content(src_path['common_schema_path'])
        common_schema = json.loads(file_content)
    except Exception as e:
        handle_file_error(e, src_path['common_schema_path'])
    schema_path = f'file://{src_path["schema"]}/'
    resolver = RefResolver(schema_path, common_schema)
    return resolver

def process_entity_files(entity_type, srcdir, schema_dir, schema_filename, resolver, constructor):
    files = ls_dir(srcdir)
    for file in files:
        try:
            file_content = read_file_content(file)
        except Exception as e:
            handle_file_error(e, file)
        parsed_data = yaml.safe_load(file_content)
        if resolver is not None:
            try:
                validate_data(parsed_data, os.path.join(schema_dir, schema_filename), resolver)
            except Exception as e:
                handle_file_error(e, file)
        parsed_data['src_path'] = os.path.abspath(file)
        try:
            constructor(parsed_data)
        except Exception as e:
            handle_file_error(e, file)

def process_static_entity_file(entity_type, srcfile, constructor):
    try:
        file_content = read_file_content(srcfile)
    except Exception as e:
        handle_file_error(e, srcfile)
    parsed_data = json.loads(file_content)
    for key, data in parsed_data.items():
        try:
            constructor(key, data)
        except Exception as e:
            handle_file_error(e, srcfile)
