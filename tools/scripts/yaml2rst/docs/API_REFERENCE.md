# yaml2rst API Reference

This document provides comprehensive API documentation for all public classes, methods, and functions in the yaml2rst package.

## Table of Contents

1. [Core Classes](#core-classes)
2. [Mixin Classes](#mixin-classes)
3. [Content Generators](#content-generators)
4. [Utility Classes](#utility-classes)
5. [Configuration](#configuration)
6. [Exceptions](#exceptions)
7. [Usage Examples](#usage-examples)

## Core Classes

### ContentGeneratorBase

Base class for all content generators, combining all mixin functionality.

```python
class ContentGeneratorBase(RelationshipMixin, ValidationMixin, UtilityMixin)
```

**Inheritance:**
- `RelationshipMixin`: Provides access to RelationshipManager
- `ValidationMixin`: Common validation methods
- `UtilityMixin`: Utility functions for data processing

**Abstract Methods:**

#### `generate_content() -> Any`
Generate content specific to the generator type.

**Returns:**
- `Any`: Generated content (varies by implementation)

**Raises:**
- `NotImplementedError`: Must be implemented by subclasses

**Example:**
```python
class MyGenerator(ContentGeneratorBase):
    def generate_content(self):
        data = self.load_data()
        return self.process_template_data(data, self.lang)
```

### FileGenerator

Orchestrates the file generation process for multiple content generators.

```python
class FileGenerator:
    def __init__(self, templates: TemplateManager, lang: str)
```

**Parameters:**
- `templates` (`TemplateManager`): Template manager instance
- `lang` (`str`): Target language code (e.g., 'ja', 'en')

#### Methods

##### `generate(config: GeneratorConfig, build_all: bool, targets: List[str]) -> None`
Generate files based on the provided configuration.

**Parameters:**
- `config` (`GeneratorConfig`): Generator configuration object
- `build_all` (`bool`): Whether to build all languages
- `targets` (`List[str]`): List of target generator names to run

**Example:**
```python
file_generator = FileGenerator(templates, 'ja')
config = GeneratorConfig(CategoryGenerator, 'category_page', '/output/path')
file_generator.generate(config, False, ['category_page'])
```

### GeneratorConfig

Configuration object for content generators.

```python
class GeneratorConfig:
    def __init__(
        self, 
        generator_class: Type[ContentGeneratorBase],
        template_name: str,
        output_path: str,
        is_single_file: bool = False,
        extra_args: Dict[str, Any] = None
    )
```

**Parameters:**
- `generator_class` (`Type[ContentGeneratorBase]`): Generator class to instantiate
- `template_name` (`str`): Name of the template to use
- `output_path` (`str`): Path where generated files will be written
- `is_single_file` (`bool`, optional): Whether generator produces single file. Defaults to `False`
- `extra_args` (`Dict[str, Any]`, optional): Additional arguments for generator. Defaults to `None`

## Mixin Classes

### RelationshipMixin

Provides unified access to the RelationshipManager singleton.

```python
class RelationshipMixin
```

#### Properties

##### `relationship_manager -> RelationshipManager`
Get the RelationshipManager instance (lazy-loaded).

**Returns:**
- `RelationshipManager`: Singleton instance of RelationshipManager

**Example:**
```python
class MyGenerator(RelationshipMixin):
    def get_categories(self):
        return self.relationship_manager.get_categories()
```

### ValidationMixin

Provides common validation functionality for data processing.

```python
class ValidationMixin
```

#### Methods

##### `validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> bool`
Validate that all required fields are present in data.

**Parameters:**
- `data` (`Dict[str, Any]`): Data dictionary to validate
- `required_fields` (`List[str]`): List of required field names

**Returns:**
- `bool`: `True` if all required fields are present, `False` otherwise

**Example:**
```python
data = {'title': 'Example', 'content': 'Text'}
required = ['title', 'content', 'author']
is_valid = self.validate_required_fields(data, required)  # False
```

##### `validate_list_field(data: Dict[str, Any], field_name: str) -> bool`
Validate that a field exists and is a list.

**Parameters:**
- `data` (`Dict[str, Any]`): Data dictionary to validate
- `field_name` (`str`): Name of the field to validate

**Returns:**
- `bool`: `True` if field exists and is a list, `False` otherwise

**Example:**
```python
data = {'items': [1, 2, 3], 'title': 'Example'}
is_valid = self.validate_list_field(data, 'items')  # True
is_invalid = self.validate_list_field(data, 'title')  # False
```

##### `validate_string_field(data: Dict[str, Any], field_name: str, allow_empty: bool = False) -> bool`
Validate that a field exists and is a non-empty string.

**Parameters:**
- `data` (`Dict[str, Any]`): Data dictionary to validate
- `field_name` (`str`): Name of the field to validate
- `allow_empty` (`bool`, optional): Whether to allow empty strings. Defaults to `False`

**Returns:**
- `bool`: `True` if field is valid string, `False` otherwise

**Example:**
```python
data = {'title': 'Example', 'description': ''}
is_valid = self.validate_string_field(data, 'title')  # True
is_invalid = self.validate_string_field(data, 'description')  # False
is_valid_empty = self.validate_string_field(data, 'description', allow_empty=True)  # True
```

### UtilityMixin

Provides common utility methods for data processing and template preparation.

```python
class UtilityMixin
```

#### Methods

##### `get_sorted_objects(objects: List[Any], sort_key: str = 'sort_key') -> List[Any]`
Sort objects by a specified attribute.

**Parameters:**
- `objects` (`List[Any]`): List of objects to sort
- `sort_key` (`str`, optional): Attribute name to sort by. Defaults to `'sort_key'`

**Returns:**
- `List[Any]`: List of sorted objects

**Example:**
```python
class Item:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

items = [Item('B', 2), Item('A', 1), Item('C', 3)]
sorted_items = self.get_sorted_objects(items, 'priority')
# Result: [Item('A', 1), Item('B', 2), Item('C', 3)]
```

##### `get_sorted_objects_by_lang_name(objects: List[Any], lang: str) -> List[Any]`
Sort objects by their localized name.

**Parameters:**
- `objects` (`List[Any]`): List of objects to sort (must have 'names' attribute)
- `lang` (`str`): Language code

**Returns:**
- `List[Any]`: List of objects sorted by localized name

**Example:**
```python
class Category:
    def __init__(self, names):
        self.names = names

categories = [
    Category({'ja': 'カテゴリB', 'en': 'Category B'}),
    Category({'ja': 'カテゴリA', 'en': 'Category A'})
]
sorted_cats = self.get_sorted_objects_by_lang_name(categories, 'ja')
# Sorted by Japanese names
```

##### `process_template_data(obj: Any, lang: str) -> Dict[str, Any]`
Process an object into template data.

**Parameters:**
- `obj` (`Any`): Object to process (must have `template_data` method)
- `lang` (`str`): Language code

**Returns:**
- `Dict[str, Any]`: Template data dictionary

**Example:**
```python
class Guideline:
    def template_data(self, lang):
        return {'title': self.titles[lang], 'content': self.content[lang]}

guideline = Guideline()
template_data = self.process_template_data(guideline, 'ja')
```

##### `process_template_data_list(objects: List[Any], lang: str) -> List[Dict[str, Any]]`
Process a list of objects into template data.

**Parameters:**
- `objects` (`List[Any]`): List of objects to process
- `lang` (`str`): Language code

**Returns:**
- `List[Dict[str, Any]]`: List of template data dictionaries

##### `filter_objects_with_articles(objects: List[Any]) -> List[Any]`
Filter objects that have associated articles.

**Parameters:**
- `objects` (`List[Any]`): List of objects to filter (must have `article_count` method)

**Returns:**
- `List[Any]`: List of objects with articles

**Example:**
```python
class Tag:
    def __init__(self, name, article_count):
        self.name = name
        self._article_count = article_count
    
    def article_count(self):
        return self._article_count

tags = [Tag('A', 5), Tag('B', 0), Tag('C', 3)]
active_tags = self.filter_objects_with_articles(tags)
# Result: [Tag('A', 5), Tag('C', 3)]
```

## Content Generators

### CategoryGenerator

Generates guideline category pages.

```python
class CategoryGenerator(ContentGeneratorBase):
    def __init__(self, lang: str)
```

**Parameters:**
- `lang` (`str`): Target language code

#### Methods

##### `generate_content() -> List[Dict[str, Any]]`
Generate category page content.

**Returns:**
- `List[Dict[str, Any]]`: List of category data for template rendering

### FaqArticleGenerator

Generates individual FAQ article pages.

```python
class FaqArticleGenerator(ContentGeneratorBase):
    def __init__(self, lang: str)
```

#### Methods

##### `generate_content() -> List[Dict[str, Any]]`
Generate FAQ article content.

**Returns:**
- `List[Dict[str, Any]]`: List of FAQ article data

### CheckGenerator

Generates check item and example content.

```python
class CheckGenerator(ContentGeneratorBase):
    def __init__(self, lang: str)
```

#### Methods

##### `generate_content() -> List[Dict[str, Any]]`
Generate check content.

**Returns:**
- `List[Dict[str, Any]]`: List of check item data

### WcagMappingGenerator

Generates WCAG mapping reference documentation.

```python
class WcagMappingGenerator(ContentGeneratorBase):
    def __init__(self, lang: str)
```

#### Methods

##### `generate_content() -> Dict[str, Any]`
Generate WCAG mapping content.

**Returns:**
- `Dict[str, Any]`: WCAG mapping data for template rendering

### MakefileGenerator

Generates Makefile for documentation building.

```python
class MakefileGenerator(ContentGeneratorBase):
    def __init__(self, lang: str, config: MakefileConfig)
```

**Parameters:**
- `lang` (`str`): Target language code
- `config` (`MakefileConfig`): Makefile configuration object

#### Methods

##### `generate_content() -> Dict[str, Any]`
Generate Makefile content.

**Returns:**
- `Dict[str, Any]`: Makefile data for template rendering

## Utility Classes

### TemplateManager

Enhanced template management with customization support.

```python
class TemplateManager:
    def __init__(self, template_dir: str)
```

**Parameters:**
- `template_dir` (`str`): Directory containing template files

#### Class Methods

##### `from_config(config: TemplateConfig) -> TemplateManager`
Create TemplateManager instance from configuration.

**Parameters:**
- `config` (`TemplateConfig`): Template configuration object

**Returns:**
- `TemplateManager`: Configured template manager instance

**Example:**
```python
from yaml2rst.template_config import TemplateConfig

config = TemplateConfig()
config.load_config()
template_manager = TemplateManager.from_config(config)
```

#### Methods

##### `load(filename: str) -> Template`
Load a Jinja2 template by filename with priority-based resolution.

**Parameters:**
- `filename` (`str`): Template filename (without .j2 extension)

**Returns:**
- `Template`: Loaded Jinja2 template object

**Raises:**
- `TemplateNotFound`: If template file doesn't exist

**Example:**
```python
template_manager = TemplateManager('/path/to/templates')
template = template_manager.load('category_page')
```

##### `write_rst(data: Dict[str, Any], output_path: str) -> None`
Render template with data and write to RST file.

**Parameters:**
- `data` (`Dict[str, Any]`): Template data dictionary
- `output_path` (`str`): Output file path

**Example:**
```python
data = {'title': 'Example', 'content': 'Content'}
template_manager.write_rst(data, '/output/example.rst')
```

##### `make_heading(title: str, level: int, class_name: str = "") -> str`
Create RST heading with proper formatting.

**Parameters:**
- `title` (`str`): Heading title
- `level` (`int`): Heading level (1-6)
- `class_name` (`str`, optional): CSS class name. Defaults to `""`

**Returns:**
- `str`: Formatted RST heading

**Example:**
```python
heading = TemplateManager.make_heading('Section Title', 2)
# Returns:
# Section Title
# =============
```

### TemplateConfig

Configuration management for template resolution system.

```python
class TemplateConfig:
    def __init__(self)
```

#### Properties

##### `custom_template_dir -> Optional[str]`
Get/set custom template directory path (highest priority).

##### `user_template_dir -> Optional[str]`
Get/set user template directory path (medium priority).

##### `built_in_template_dir -> Path`
Get/set built-in template directory path (lowest priority).

##### `fallback_to_builtin -> bool`
Get/set whether to fall back to built-in templates when custom templates are not found.

#### Methods

##### `load_config() -> Dict[str, Any]`
Load configuration from file and environment variables.

**Returns:**
- `Dict[str, Any]`: Loaded configuration dictionary

**Example:**
```python
config = TemplateConfig()
loaded_config = config.load_config()
print(loaded_config)
```

##### `get_template_search_paths() -> List[Path]`
Get ordered list of template search paths based on priority.

**Returns:**
- `List[Path]`: List of template directory paths in priority order

**Example:**
```python
config = TemplateConfig()
config.load_config()
paths = config.get_template_search_paths()
print("Template search paths:", paths)
```

##### `get_user_template_dir_expanded() -> Path`
Get expanded user template directory path.

**Returns:**
- `Path`: Expanded path to user template directory

### TemplateResolver

Resolves template files with priority-based fallback system.

```python
class TemplateResolver:
    def __init__(self, config: TemplateConfig)
```

**Parameters:**
- `config` (`TemplateConfig`): Template configuration object

#### Methods

##### `resolve_template(filename: str) -> Path`
Resolve template file path using priority-based search.

**Parameters:**
- `filename` (`str`): Template filename to resolve

**Returns:**
- `Path`: Resolved template file path

**Raises:**
- `TemplateNotFound`: If template file is not found in any search path

**Example:**
```python
from yaml2rst.template_config import TemplateConfig
from yaml2rst.template_resolver import TemplateResolver

config = TemplateConfig()
config.load_config()
resolver = TemplateResolver(config)
template_path = resolver.resolve_template('gl-category.rst')
```

##### `list_available_templates() -> List[str]`
List all available template files across all search paths.

**Returns:**
- `List[str]`: List of available template filenames

**Example:**
```python
resolver = TemplateResolver(config)
templates = resolver.list_available_templates()
print("Available templates:", templates)
```

### MakefileConfig

Configuration object for Makefile generation.

```python
class MakefileConfig:
    def __init__(
        self,
        dest_dirs: Dict[str, str],
        makefile_vars: Dict[str, str],
        base_vars: Dict[str, Any],
        vars_list: List[str]
    )
```

**Parameters:**
- `dest_dirs` (`Dict[str, str]`): Destination directory mappings
- `makefile_vars` (`Dict[str, str]`): Makefile variable definitions
- `base_vars` (`Dict[str, Any]`): Base variable values
- `vars_list` (`List[str]`): List of variable names

## Configuration

### Configuration Functions

#### `setup_parameters() -> Dict[str, Any]`
Set up configuration parameters from command line arguments.

**Returns:**
- `Dict[str, Any]`: Configuration dictionary

#### `setup_constants(settings: Dict[str, Any]) -> Tuple[Dict[str, str], Dict[str, str], Dict[str, str]]`
Set up directory and file constants based on settings.

**Parameters:**
- `settings` (`Dict[str, Any]`): Configuration settings

**Returns:**
- `Tuple[Dict[str, str], Dict[str, str], Dict[str, str]]`: Destination directories, static files, and Makefile variables

#### `setup_templates() -> TemplateManager`
Set up template manager with configured template directory.

**Returns:**
- `TemplateManager`: Configured template manager instance

#### `get_available_languages() -> List[str]`
Get list of available language codes.

**Returns:**
- `List[str]`: List of supported language codes

#### `export_templates(target_dir: Optional[str] = None) -> None`
Export built-in templates to specified directory.

**Parameters:**
- `target_dir` (`Optional[str]`, optional): Target directory path. If None, uses default user template directory. Defaults to `None`

**Raises:**
- `TemplateExportError`: If export operation fails

**Example:**
```python
from yaml2rst.initializer import export_templates

# Export to default user directory
export_templates()

# Export to custom directory
export_templates('/custom/templates')
```

**Output:**
```
Templates exported to: /home/user/.config/freee_a11y_gl/templates
Exported 15 template files:
  - axe-rules.rst
  - checks/allchecks.rst
  - checks/examples-tool.rst
  - faq/article-index.rst
  - faq/article.rst
  - faq/index.rst
  - faq/tag-index.rst
  - faq/tagpage.rst
  - gl-category.rst
  - incfiles.mk
  - info_to_faq.rst
  - info_to_gl.rst
  - misc-defs.txt
  - priority-diff.rst
  - wcag21-mapping.rst

To customize templates:
1. Edit files in: /home/user/.config/freee_a11y_gl/templates
2. Run yaml2rst normally - custom templates will be used automatically
```

## Exceptions

### GeneratorError

Base exception class for all generator-related errors.

```python
class GeneratorError(Exception):
    """Base exception for generator errors."""
    pass
```

### ConfigurationError

Exception raised for configuration-related errors.

```python
class ConfigurationError(GeneratorError):
    """Configuration-related errors."""
    pass
```

### DataValidationError

Exception raised for data validation errors.

```python
class DataValidationError(GeneratorError):
    """Data validation errors."""
    pass
```

### TemplateError

Exception raised for template processing errors.

```python
class TemplateError(GeneratorError):
    """Template processing errors."""
    pass
```

### TemplateExportError

Exception raised when template export operation fails.

```python
class TemplateExportError(Exception):
    """Exception raised when template export operation fails."""
    pass
```

**Common Causes:**
- Permission denied when writing to target directory
- File system errors during copy operations
- Missing source template files
- Invalid target directory path

**Example:**
```python
from yaml2rst.initializer import export_templates, TemplateExportError

try:
    export_templates('/read-only/directory')
except TemplateExportError as e:
    print(f"Template export failed: {e}")
```

## Usage Examples

### Basic Generator Usage

```python
from yaml2rst.generators.content_generators import CategoryGenerator
from yaml2rst.template_manager import TemplateManager

# Initialize template manager
templates = TemplateManager('/path/to/templates')

# Create generator
generator = CategoryGenerator('ja')

# Generate content
content = generator.generate_content()

# Process with template
for item in content:
    template_data = generator.process_template_data(item, 'ja')
    templates.write_rst(template_data, f'/output/{item.id}.rst')
```

### Custom Generator Implementation

```python
from yaml2rst.generators.content_generator_base import ContentGeneratorBase

class CustomGenerator(ContentGeneratorBase):
    def __init__(self, lang):
        self.lang = lang
    
    def generate_content(self):
        # Load data using relationship manager
        data = self.relationship_manager.get_custom_data()
        
        # Validate data
        required_fields = ['title', 'content']
        for item in data:
            if not self.validate_required_fields(item, required_fields):
                raise DataValidationError(f"Missing required fields in {item}")
        
        # Process and return
        return self.process_template_data_list(data, self.lang)
```

### File Generation Workflow

```python
from yaml2rst.generators.file_generator import FileGenerator, GeneratorConfig
from yaml2rst.generators.content_generators import CategoryGenerator

# Set up file generator
file_generator = FileGenerator(templates, 'ja')

# Configure generator
config = GeneratorConfig(
    generator_class=CategoryGenerator,
    template_name='category_page',
    output_path='/output/categories'
)

# Generate files
file_generator.generate(config, build_all=False, targets=['category_page'])
```

### Validation Examples

```python
class MyGenerator(ContentGeneratorBase):
    def validate_item(self, item):
        # Check required fields
        if not self.validate_required_fields(item, ['title', 'content']):
            return False
        
        # Check specific field types
        if not self.validate_string_field(item, 'title'):
            return False
        
        if 'tags' in item and not self.validate_list_field(item, 'tags'):
            return False
        
        return True
    
    def generate_content(self):
        data = self.relationship_manager.get_data()
        valid_data = [item for item in data if self.validate_item(item)]
        return self.process_template_data_list(valid_data, self.lang)
```

### Template Data Processing

```python
class AdvancedGenerator(ContentGeneratorBase):
    def generate_content(self):
        # Get raw data
        categories = self.relationship_manager.get_categories()
        
        # Sort by localized name
        sorted_categories = self.get_sorted_objects_by_lang_name(categories, self.lang)
        
        # Filter categories with content
        active_categories = self.filter_objects_with_articles(sorted_categories)
        
        # Process for templates
        template_data = []
        for category in active_categories:
            data = self.process_template_data(category, self.lang)
            data['subcategories'] = self.process_template_data_list(
                category.subcategories, self.lang
            )
            template_data.append(data)
        
        return template_data
```

---

This API reference provides comprehensive documentation for all public interfaces in the yaml2rst package. For architectural details and design patterns, see [ARCHITECTURE.md](ARCHITECTURE.md). For usage guides and examples, see [README.md](../README.md).
