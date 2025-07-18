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
from .constants import CHECK_TOOLS, AXE_CORE
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
    for tool_id, tool_names in CHECK_TOOLS.items():
        CheckTool(tool_id, tool_names)

    for entity_type, srcfile, constructor in static_entity_config:
        process_static_entity_file(srcfile, constructor)

    for entity_type, srcdir, constructor, schema_name in entity_config:
        process_entity_files(srcdir, constructor, schema_name, validator)

    process_axe_rules(basedir, AXE_CORE)
    rel = RelationshipManager()
    rel.resolve_faqs()
    return rel

def process_axe_rules(basedir: Optional[str], AXE_CORE):
    """
    Process axe-core rules from the Git submodule.
    
    Args:
        basedir: Base directory containing the Git repository.
                If None, value from settings will be used. If not in settings, defaults to '.'
        AXE_CORE: Dictionary containing axe-core configuration
    
    Raises:
        ValueError: If the axe-core submodule is not found
    """
    from .config import Config

    effective_basedir = basedir if basedir is not None else Config.get_basedir()
    root_repo = git.Repo(effective_basedir)
    submodule = None
    for sm in root_repo.submodules:
        if sm.name == AXE_CORE['submodule_name']:
            submodule = sm
            break

    if submodule is None:
        raise ValueError(f'Submodule with name {AXE_CORE["submodule_name"]} not found.')

    axe_base = os.path.join(effective_basedir, AXE_CORE['base_dir'])
    axe_commit_id = submodule.hexsha
    axe_repo = git.Repo(axe_base)
    axe_commit = axe_repo.commit(axe_commit_id)

    # Get message file
    msg_ja_path = os.path.join(AXE_CORE['locale_dir'], AXE_CORE['locale_ja_file'])
    blob = axe_commit.tree / msg_ja_path
    file_content = blob.data_stream.read().decode('utf-8')
    messages_ja = json.loads(file_content)

    # Get rule files
    tree = axe_commit.tree / AXE_CORE['rules_dir']
    rule_blobs = [item for item in tree.traverse() if item.type == 'blob' and item.path.endswith('.json')]
    for blob in rule_blobs:
        file_content = blob.data_stream.read().decode('utf-8')
        parsed_data = json.loads(file_content)
        AxeRule(parsed_data, messages_ja)

    # Get the package file
    blob = axe_commit.tree / AXE_CORE['pkg_file']
    file_content = blob.data_stream.read().decode('utf-8')
    parsed_data = json.loads(file_content)
    AxeRule.version = parsed_data['version']
    AxeRule.major_version = re.sub(r'(\d+)\.(\d+)\.\d+', r'\1.\2', parsed_data['version'])
    AxeRule.deque_url = AXE_CORE['deque_url']
    AxeRule.timestamp = time.strftime("%F %T%z", time.localtime(axe_commit.authored_date))

def ls_dir(dirname, extension=None):
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
    try:
        file_content = read_file_content(file)
    except Exception as e:
        handle_file_error(e, file)
    data = yaml.safe_load(file_content)

    return data

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
        except Exception as e:
            handle_file_error(e, file)
        
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

def process_static_entity_file(srcfile, constructor):
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
