# API Reference

This document provides comprehensive API documentation for the freee_a11y_gl library, covering all public classes, methods, and functions available for external use.

## Table of Contents

- [Core Models](#core-models)
  - [Category](#category)
  - [Guideline](#guideline)
  - [Check](#check)
  - [FAQ](#faq)
  - [Reference Models](#reference-models)
- [Configuration](#configuration)
  - [Settings](#settings)
  - [Configuration Classes](#configuration-classes)
- [Utilities](#utilities)
  - [Initialization](#initialization)
  - [YAML Processing](#yaml-processing)
  - [Version Information](#version-information)
  - [Source Path Utilities](#source-path-utilities)
- [Relationship Management](#relationship-management)
- [Validation](#validation)
- [Error Handling](#error-handling)

## Core Models

### Category

Represents groupings of accessibility guidelines.

#### Class: `Category`

```python
class Category(BaseModel):
    """Category model representing groupings of guidelines."""
```

#### Constructor

```python
def __init__(self, category_id: str, names: Dict[str, str])
```

**Parameters:**
- `category_id` (str): Unique category identifier
- `names` (Dict[str, str]): Dictionary of localized names (lang code -> name)

#### Methods

##### `get_name(lang: str) -> str`

Get localized name for category.

**Parameters:**
- `lang` (str): Language code

**Returns:**
- `str`: Localized name, falls back to Japanese if language not found

**Example:**
```python
category = Category.get_by_id('form')
name_ja = category.get_name('ja')  # Returns Japanese name
name_en = category.get_name('en')  # Returns English name or falls back to Japanese
```

##### `get_dependency() -> List[str]`

Get list of file dependencies for this category.

**Returns:**
- `List[str]`: List of file paths that this category depends on

**Example:**
```python
category = Category.get_by_id('form')
dependencies = category.get_dependency()
# Returns list of YAML file paths for guidelines, checks, and FAQs
```

#### Class Methods

##### `list_all() -> List[Category]`

Get all category instances.

**Returns:**
- `List[Category]`: List of all category instances

**Example:**
```python
categories = Category.list_all()
for category in categories:
    print(f"Category: {category.get_name('ja')}")
```

### Guideline

Represents individual accessibility guidelines.

#### Class: `Guideline`

```python
class Guideline(BaseModel, TemplateDataMixin):
    """Guideline model representing accessibility guidelines."""
```

#### Constructor

```python
def __init__(self, gl: Dict[str, Any])
```

**Parameters:**
- `gl` (Dict[str, Any]): Dictionary containing guideline data

#### Properties

- `id` (str): Unique guideline identifier
- `sort_key` (str): Sort key for ordering
- `data` (GuidelineData): Container for guideline localized data
- `src_path` (str): Source file path

#### Methods

##### `get_category_and_id(lang: str) -> Dict[str, str]`

Get category name and guideline ID.

**Parameters:**
- `lang` (str): Language code

**Returns:**
- `Dict[str, str]`: Dictionary with category name and guideline ID

**Example:**
```python
guideline = Guideline.get_by_id('form-labeling')
info = guideline.get_category_and_id('ja')
# Returns: {'category': 'フォーム', 'guideline': 'form-labeling'}
```

##### `link_data(baseurl: str = '') -> Dict[str, Dict[str, str]]`

Get link data for guideline.

**Parameters:**
- `baseurl` (str, optional): Base URL for links

**Returns:**
- `Dict[str, Dict[str, str]]`: Dictionary with localized text and URLs

**Example:**
```python
guideline = Guideline.get_by_id('form-labeling')
links = guideline.link_data('https://example.com')
# Returns: {'text': {'ja': '...', 'en': '...'}, 'url': {'ja': '...', 'en': '...'}}
```

##### `template_data(lang: str) -> Dict[str, Any]`

Get template data for guideline.

**Parameters:**
- `lang` (str): Language code

**Returns:**
- `Dict[str, Any]`: Dictionary with guideline data formatted for templates

**Example:**
```python
guideline = Guideline.get_by_id('form-labeling')
data = guideline.template_data('ja')
# Returns comprehensive template data including checks, success criteria, etc.
```

#### Class Methods

##### `list_all_src_paths() -> List[str]`

Get all guideline source paths.

**Returns:**
- `List[str]`: List of source file paths

### Check

Represents accessibility checks and validation rules.

#### Class: `Check`

```python
class Check(BaseModel, TemplateDataMixin):
    """Check model representing accessibility checks."""
```

#### Constructor

```python
def __init__(self, check_data: Dict[str, Any])
```

**Parameters:**
- `check_data` (Dict[str, Any]): Dictionary containing check data

#### Properties

- `id` (str): Unique check identifier
- `sort_key` (str): Sort key for ordering
- `data` (CheckData): Container for check localized data
- `src_path` (str): Source file path
- `conditions` (List[Condition]): List of check conditions
- `implementations` (List[Implementation]): List of implementations

#### Methods

##### `template_data(lang: str, platform: List[str] = None) -> Dict[str, Any]`

Get template data for check.

**Parameters:**
- `lang` (str): Language code
- `platform` (List[str], optional): Platform filter

**Returns:**
- `Dict[str, Any]`: Dictionary with check data formatted for templates

**Example:**
```python
check = Check.get_by_id('form-label-check')
data = check.template_data('ja', platform=['web'])
# Returns template data filtered for web platform
```

#### Class Methods

##### `list_all_src_paths() -> List[str]`

Get all check source paths.

**Returns:**
- `List[str]`: List of source file paths

### FAQ

Represents frequently asked questions and articles.

#### Class: `Faq`

```python
class Faq(BaseModel, TemplateDataMixin):
    """FAQ model representing FAQ articles."""
```

#### Constructor

```python
def __init__(self, faq_data: Dict[str, Any])
```

**Parameters:**
- `faq_data` (Dict[str, Any]): Dictionary containing FAQ data

#### Properties

- `id` (str): Unique FAQ identifier
- `sort_key` (str): Sort key for ordering
- `data` (FaqData): Container for FAQ localized data
- `src_path` (str): Source file path

#### Methods

##### `link_data(baseurl: str = '') -> Dict[str, Dict[str, str]]`

Get link data for FAQ.

**Parameters:**
- `baseurl` (str, optional): Base URL for links

**Returns:**
- `Dict[str, Dict[str, str]]`: Dictionary with localized text and URLs

##### `template_data(lang: str) -> Dict[str, Any]`

Get template data for FAQ.

**Parameters:**
- `lang` (str): Language code

**Returns:**
- `Dict[str, Any]`: Dictionary with FAQ data formatted for templates

**Example:**
```python
faq = Faq.get_by_id('p0001')
data = faq.template_data('ja')
# Returns comprehensive FAQ template data
```

### Reference Models

#### WcagSc

Represents WCAG Success Criteria.

```python
class WcagSc(BaseModel):
    """WCAG Success Criteria model."""
```

#### InfoRef

Represents information references.

```python
class InfoRef(BaseModel):
    """Information reference model."""
```

#### AxeRule

Represents axe-core accessibility rules.

```python
class AxeRule(BaseModel):
    """Axe-core rule model."""
```

## Configuration

### Settings

The main settings object providing access to configuration.

#### Global Instance

```python
from freee_a11y_gl import settings
```

#### Methods

##### `get(key: str, default: Any = None) -> Any`

Get configuration value.

**Parameters:**
- `key` (str): Dot-separated key (e.g., "urls.base.ja")
- `default` (Any, optional): Default value if key not found

**Returns:**
- `Any`: Configuration value

**Example:**
```python
base_url = settings.get('base_url')
validation_mode = settings.get('validation.yaml_validation', 'strict')
```

##### `set(key: str, value: Any) -> None`

Set configuration value.

**Parameters:**
- `key` (str): Dot-separated key
- `value` (Any): Configuration value

**Example:**
```python
settings.set('validation.yaml_validation', 'warning')
```

##### `initialize(profile: Optional[str] = None, config_override: Optional[Dict[str, Any]] = None) -> None`

Initialize settings with profile and overrides.

**Parameters:**
- `profile` (str, optional): Profile name to use
- `config_override` (Dict[str, Any], optional): Configuration overrides

**Example:**
```python
settings.initialize(profile='development', config_override={
    'validation': {'yaml_validation': 'warning'}
})
```

#### Properties

##### `config -> GlobalConfig`

Get typed configuration object.

**Returns:**
- `GlobalConfig`: Validated configuration object

**Example:**
```python
config = settings.config
print(f"Base URL: {config.base_url}")
print(f"Available languages: {config.languages.available}")
```

##### `message_catalog -> MessageCatalog`

Get message catalog for internationalization.

**Returns:**
- `MessageCatalog`: Message catalog instance

### Configuration Classes

#### GlobalConfig

```python
class GlobalConfig(BaseModel):
    """Global configuration model."""
    languages: LanguageConfig
    base_url: str
    paths: PathConfig
    validation: ValidationConfig
    axe_core: AxeCoreConfig
```

#### LanguageConfig

```python
class LanguageConfig(BaseModel):
    """Language configuration."""
    available: List[str]
    default: str
```

#### PathConfig

```python
class PathConfig(BaseModel):
    """Path configuration."""
    guidelines: str
    faq: str
```

#### ValidationConfig

```python
class ValidationConfig(BaseModel):
    """Validation configuration."""
    yaml_validation: Literal["strict", "warning", "disabled"]
```

## Utilities

### Initialization

#### `setup_instances(basedir: Optional[str] = None) -> RelationshipManager`

Set up instances for all components.

**Parameters:**
- `basedir` (str, optional): Base directory containing data files

**Returns:**
- `RelationshipManager`: Relationship manager with resolved relationships

**Example:**
```python
from freee_a11y_gl import setup_instances

rel_manager = setup_instances('/path/to/data')
```

### YAML Processing

#### `process_yaml_data(file_path: str) -> Dict[str, Any]`

Process YAML data with validation.

**Parameters:**
- `file_path` (str): Path to YAML file

**Returns:**
- `Dict[str, Any]`: Processed YAML data

**Example:**
```python
from freee_a11y_gl import process_yaml_data

data = process_yaml_data('/path/to/file.yaml')
```

### Version Information

#### `get_version_info() -> Dict[str, str]`

Get version information.

**Returns:**
- `Dict[str, str]`: Version information dictionary

**Example:**
```python
from freee_a11y_gl import get_version_info

version_info = get_version_info()
print(f"Version: {version_info['version']}")
```

### Source Path Utilities

#### `get_src_path(basedir: str) -> Dict[str, str]`

Get source paths for different data types.

**Parameters:**
- `basedir` (str): Base directory path

**Returns:**
- `Dict[str, str]`: Dictionary mapping data types to paths

**Example:**
```python
from freee_a11y_gl import get_src_path

paths = get_src_path('/path/to/data')
print(f"Guidelines path: {paths['guidelines']}")
```

#### `get_info_links() -> List[InfoRef]`

Get information links.

**Returns:**
- `List[InfoRef]`: List of information reference objects

**Example:**
```python
from freee_a11y_gl import get_info_links

links = get_info_links()
for link in links:
    print(f"Link: {link.url}")
```

## Relationship Management

### RelationshipManager

Manages relationships between different model instances.

#### Class: `RelationshipManager`

```python
class RelationshipManager:
    """Manages relationships between model instances."""
```

#### Methods

##### `associate_objects(obj1: BaseModel, obj2: BaseModel) -> None`

Associate two objects.

**Parameters:**
- `obj1` (BaseModel): First object
- `obj2` (BaseModel): Second object

##### `get_related_objects(obj: BaseModel, object_type: str) -> List[BaseModel]`

Get related objects of specified type.

**Parameters:**
- `obj` (BaseModel): Source object
- `object_type` (str): Type of related objects to retrieve

**Returns:**
- `List[BaseModel]`: List of related objects

##### `get_sorted_related_objects(obj: BaseModel, object_type: str, key: str = 'sort_key') -> List[BaseModel]`

Get sorted related objects.

**Parameters:**
- `obj` (BaseModel): Source object
- `object_type` (str): Type of related objects to retrieve
- `key` (str, optional): Sort key attribute name

**Returns:**
- `List[BaseModel]`: List of sorted related objects

## Validation

### YamlValidator

Provides YAML validation functionality.

#### Class: `YamlValidator`

```python
class YamlValidator:
    """YAML validation with configurable modes."""
```

#### Constructor

```python
def __init__(self, schema_dir: str, validation_mode: str = 'strict')
```

**Parameters:**
- `schema_dir` (str): Directory containing JSON schema files
- `validation_mode` (str, optional): Validation mode ('strict', 'warning', 'disabled')

#### Methods

##### `validate_with_mode(data: Dict[str, Any], schema_name: str, file_path: str) -> None`

Validate data with configured mode.

**Parameters:**
- `data` (Dict[str, Any]): Data to validate
- `schema_name` (str): Schema name to validate against
- `file_path` (str): File path for error reporting

**Raises:**
- `ValidationError`: If validation fails in strict mode

**Example:**
```python
from freee_a11y_gl.yaml_validator import YamlValidator

validator = YamlValidator('/path/to/schemas', 'strict')
validator.validate_with_mode(data, 'guideline', '/path/to/file.yaml')
```

## Error Handling

### Custom Exceptions

#### ValidationError

```python
class ValidationError(Exception):
    """Raised when YAML validation fails."""
```

### ErrorRecovery

Provides error handling and recovery mechanisms.

#### Class: `ErrorRecovery`

```python
class ErrorRecovery:
    """Error handling and recovery mechanisms."""
```

#### Methods

##### `handle_error(error: Exception, context: Dict[str, Any] = None) -> None`

Handle and log errors with context.

**Parameters:**
- `error` (Exception): Exception to handle
- `context` (Dict[str, Any], optional): Additional context information

**Example:**
```python
from freee_a11y_gl.error_recovery import ErrorRecovery

recovery = ErrorRecovery()
try:
    # Your code here
    pass
except Exception as e:
    recovery.handle_error(e, context={'file': 'example.yaml'})
```

## Base Model

All model classes inherit from `BaseModel`, which provides common functionality.

### BaseModel

#### Class: `BaseModel`

```python
class BaseModel:
    """Base class for all model objects."""
```

#### Constructor

```python
def __init__(self, object_id: str)
```

**Parameters:**
- `object_id` (str): Unique identifier for the object

#### Properties

- `id` (str): Object identifier
- `object_type` (str): Type of object (defined in subclasses)

#### Class Methods

##### `get_by_id(object_id: str) -> Optional[BaseModel]`

Get object instance by ID.

**Parameters:**
- `object_id` (str): Object identifier

**Returns:**
- `Optional[BaseModel]`: Object instance or None if not found

**Example:**
```python
category = Category.get_by_id('form')
guideline = Guideline.get_by_id('form-labeling')
```

## Template Data Mixin

Provides template data generation functionality.

### TemplateDataMixin

#### Class: `TemplateDataMixin`

```python
class TemplateDataMixin:
    """Mixin for template data generation."""
```

#### Methods

##### `get_base_template_data(lang: str) -> Dict[str, Any]`

Get base template data.

**Parameters:**
- `lang` (str): Language code

**Returns:**
- `Dict[str, Any]`: Base template data

##### `join_platform_items(platforms: List[str], lang: str) -> str`

Join platform items with localized separators.

**Parameters:**
- `platforms` (List[str]): List of platform names
- `lang` (str): Language code

**Returns:**
- `str`: Joined platform string

This API reference covers all the main public interfaces of the freee_a11y_gl library. For more detailed examples and usage patterns, refer to the main README.md and configuration documentation.
