import os
import sys
import json
import yaml
from jsonschema import validate, ValidationError, RefResolver
from a11y_guidelines import Category, WcagSc, InfoRef, Guideline, Check, Faq, FaqTag, CheckTool, RelationshipManager
from constants import CHECK_TOOLS
from path import SRCDIR, SCHEMA_FILENAMES, COMMON_SCHEMA_PATH, MISC_INFO_SRCFILES

def setup_instances(no_check=False):
    # Mapping of entity type, srcdir, schema filename, and constructor.
    # The order is important for the initialization of the instances.
    entity_config = [
        ('check', SRCDIR['checks'], SCHEMA_FILENAMES['checks'], Check),
        ('guideline', SRCDIR['guidelines'], SCHEMA_FILENAMES['guidelines'], Guideline),
        ('faq', SRCDIR['faq'], SCHEMA_FILENAMES['faq'], Faq)
    ]
    static_entity_config = [
        ('category', MISC_INFO_SRCFILES['gl_categories'], Category),
        ('wcag_sc', MISC_INFO_SRCFILES['wcag_sc'], WcagSc),
        ('faq_tag', MISC_INFO_SRCFILES['faq_tags'], FaqTag),
        ('external_info', MISC_INFO_SRCFILES['info'], InfoRef)
    ]

    # Setup CheckTool instances
    for tool_id, tool_names in CHECK_TOOLS.items():
        CheckTool(tool_id, tool_names)

    for entity_type, srcfile, constructor in static_entity_config:
        process_static_entity_file(entity_type, srcfile, constructor)

    for entity_type, srcdir, schema_filename, constructor in entity_config:
        process_entity_files(entity_type, srcdir, schema_filename, constructor, no_check)

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

def setup_resolver():
    try:
        file_content = read_file_content(COMMON_SCHEMA_PATH)
        common_schema = json.loads(file_content)
    except Exception as e:
        handle_file_error(e, COMMON_SCHEMA_PATH)
    schema_path = f'file://{SRCDIR["schema"]}/'
    resolver = RefResolver(schema_path, common_schema)
    return resolver

def process_entity_files(entity_type, srcdir, schema_filename, constructor, no_check):
    if not no_check:
        resolver = setup_resolver()
    files = ls_dir(srcdir)
    for file in files:
        try:
            file_content = read_file_content(file)
        except Exception as e:
            handle_file_error(e, file)
        parsed_data = yaml.safe_load(file_content)
        if not no_check:
            try:
                validate_data(parsed_data, os.path.join(SRCDIR['schema'], schema_filename), resolver)
            except Exception as e:
                handle_file_error(e, file)
        parsed_data['src_path'] = os.path.relpath(file, start=os.getcwd())
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
