"""Initialization module for accessibility guidelines components.

This module handles the setup and initialization of all model instances,
including loading data from YAML and JSON files, processing axe-core rules
from Git submodules, and establishing relationships between entities.
"""

import os
import sys
import re
import json
import time
import yaml
import git
from typing import Optional
from .relationship_manager import RelationshipManager
from .models.content import Category, Guideline
from .models.reference import WcagSc, InfoRef
from .models.faq.article import Faq
from .models.faq.tag import FaqTag
from .models.axe import AxeRule
from .models.check import Check, CheckTool
from .source import get_src_path
from .yaml_validator import YamlValidator, ValidationError


def setup_instances(basedir: Optional[str] = None):
    """
    Set up instances for all components.

    Args:
        basedir: Base directory containing data files.
                If None, value from settings will be used. If not in settings, defaults to '.'

    Returns:
        RelationshipManager instance with resolved relationships
    """
    from .config import Config

    # Get value from settings if not provided
    effective_basedir = basedir if basedir is not None else Config.get_basedir()
    src_path = get_src_path(effective_basedir)

    # Initialize YAML validator with configuration
    schema_dir = os.path.join(effective_basedir, 'data', 'json', 'schemas')
    validation_mode = Config.get_yaml_validation_mode()
    validator = YamlValidator(schema_dir, validation_mode)

    # Mapping of entity type, srcdir, constructor, and schema name.
    # The order is important for the initialization of the instances.
    entity_config = [
        ('check', src_path['checks'], Check, 'check'),
        ('guideline', src_path['guidelines'], Guideline, 'guideline'),
        ('faq', src_path['faq'], Faq, 'faq')
    ]
    static_entity_config = [
        ('category', src_path['gl_categories'], Category),
        ('wcag_sc', src_path['wcag_sc'], WcagSc),
        ('faq_tag', src_path['faq_tags'], FaqTag),
        ('external_info', src_path['info'], InfoRef)
    ]

    # Setup CheckTool instances
    from .settings import settings
    check_tools = settings.message_catalog.check_tools
    for tool_id, tool_names in check_tools.items():
        CheckTool(tool_id, tool_names)

    for entity_type, srcfile, constructor in static_entity_config:
        process_static_entity_file(srcfile, constructor)

    for entity_type, srcdir, constructor, schema_name in entity_config:
        process_entity_files(srcdir, constructor, schema_name, validator)

    axe_core_config = Config.get_axe_core_config()
    process_axe_rules(basedir, axe_core_config)
    rel = RelationshipManager()
    rel.resolve_faqs()
    return rel


def process_axe_rules(basedir: Optional[str], axe_core_config):
    """
    Process axe-core rules from the Git submodule.

    Args:
        basedir: Base directory containing the Git repository.
                If None, value from settings will be used. If not in settings, defaults to '.'
        axe_core_config: Dictionary containing axe-core configuration

    Raises:
        ValueError: If the axe-core submodule is not found
    """
    from .config import Config

    effective_basedir = basedir if basedir is not None else Config.get_basedir()
    root_repo = git.Repo(effective_basedir)
    submodule = None
    for sm in root_repo.submodules:
        if sm.name == axe_core_config['submodule_name']:
            submodule = sm
            break

    if submodule is None:
        raise ValueError(f'Submodule with name {axe_core_config["submodule_name"]} not found.')

    axe_base = os.path.join(effective_basedir, axe_core_config['base_dir'])
    axe_commit_id = submodule.hexsha
    axe_repo = git.Repo(axe_base)
    axe_commit = axe_repo.commit(axe_commit_id)

    # Get message file
    msg_ja_path = os.path.join(axe_core_config['locale_dir'], axe_core_config['locale_ja_file'])
    blob = axe_commit.tree / msg_ja_path
    file_content = blob.data_stream.read().decode('utf-8')
    messages_ja = json.loads(file_content)

    # Get rule files
    tree = axe_commit.tree / axe_core_config['rules_dir']
    rule_blobs = [item for item in tree.traverse() if item.type == 'blob' and item.path.endswith('.json')]
    for blob in rule_blobs:
        file_content = blob.data_stream.read().decode('utf-8')
        parsed_data = json.loads(file_content)
        AxeRule(parsed_data, messages_ja)

    # Get the package file
    blob = axe_commit.tree / axe_core_config['pkg_file']
    file_content = blob.data_stream.read().decode('utf-8')
    parsed_data = json.loads(file_content)
    AxeRule.version = parsed_data['version']
    AxeRule.major_version = re.sub(r'(\d+)\.(\d+)\.\d+', r'\1.\2', parsed_data['version'])
    AxeRule.deque_url = axe_core_config['deque_url']
    AxeRule.timestamp = time.strftime("%F %T%z", time.localtime(axe_commit.authored_date))


def ls_dir(dirname, extension=None):
    """
    List all files in a directory recursively, optionally filtering by extension.

    Args:
        dirname: Directory path to search
        extension: File extension to filter by (optional)

    Returns:
        List of file paths
    """
    files = []
    for currentDir, dirs, fs in os.walk(dirname):
        for f in fs:
            if extension is None or f.endswith(extension):
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
    """
    Read and parse a YAML file.

    Args:
        file: Path to the YAML file

    Returns:
        Parsed YAML data

    Raises:
        Exception: If file reading or YAML parsing fails
    """
    try:
        file_content = read_file_content(file)
        data = yaml.safe_load(file_content)
        return data
    except Exception as e:
        handle_file_error(e, file)


def process_entity_files(srcdir, constructor, schema_name=None, validator=None):
    """
    Process entity files with optional validation.

    Args:
        srcdir: Source directory containing YAML files
        constructor: Constructor function for the entity
        schema_name: Name of the schema to validate against (optional)
        validator: YamlValidator instance (optional)
    """
    files = ls_dir(srcdir)
    for file in files:
        try:
            file_content = read_file_content(file)
            parsed_data = yaml.safe_load(file_content)

            # Perform validation if validator and schema_name are provided
            if validator and schema_name:
                try:
                    validator.validate_with_mode(parsed_data, schema_name, file)
                except ValidationError as e:
                    print(f"YAML Validation Error: {e}", file=sys.stderr)
                    sys.exit(1)

            parsed_data['src_path'] = os.path.abspath(file)
            try:
                constructor(parsed_data)
            except Exception as e:
                handle_file_error(e, file)
        except Exception as e:
            handle_file_error(e, file)


def process_static_entity_file(srcfile, constructor):
    """
    Process a static entity JSON file and create instances.

    Args:
        srcfile: Path to the JSON file containing entity data
        constructor: Constructor function for creating entity instances

    Raises:
        Exception: If file reading or JSON parsing fails
    """
    try:
        file_content = read_file_content(srcfile)
        parsed_data = json.loads(file_content)
        for key, data in parsed_data.items():
            try:
                constructor(key, data)
            except Exception as e:
                handle_file_error(e, srcfile)
    except Exception as e:
        handle_file_error(e, srcfile)
