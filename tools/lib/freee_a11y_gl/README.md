# freee_a11y_gl

A comprehensive Python library for managing accessibility guidelines, checks, and related content. This library provides a framework for processing YAML-based accessibility guidelines, performing validation, and managing relationships between different accessibility entities.

## Features

- **Model-based Architecture**: Structured models for categories, guidelines, checks, FAQ articles, and WCAG success criteria
- **YAML Processing**: Robust YAML file processing with validation and error handling
- **Relationship Management**: Automatic relationship resolution between different entities
- **Configuration System**: Flexible configuration management with profile support
- **Internationalization**: Multi-language support with message catalogs
- **Validation**: Comprehensive YAML validation with configurable modes
- **axe-core Integration**: Built-in support for axe-core accessibility rules

## Installation

```bash
pip install freee_a11y_gl
```

### Requirements

- Python 3.9 or higher
- PyYAML >= 6.0
- GitPython >= 3.1.43
- Pydantic >= 2.7.0

## Quick Start

### Basic Usage

```python
import freee_a11y_gl as a11y

# Initialize the library with your data directory
rel_manager = a11y.setup_instances(basedir='/path/to/your/data')

# Access categories
categories = a11y.Category.list_all()
for category in categories:
    print(f"Category: {category.get_name('ja')}")

# Access guidelines
guidelines = a11y.Guideline.list_all()
for guideline in guidelines:
    template_data = guideline.template_data('ja')
    print(f"Guideline: {template_data['title']}")

# Access checks
checks = a11y.Check.list_all()
for check in checks:
    print(f"Check: {check.id}")
```

### Working with Settings

```python
from freee_a11y_gl import settings

# Access configuration
config = settings.config
print(f"Base URL: {config.base_url}")
print(f"Available languages: {config.languages.available}")

# Update settings
settings.set('validation.yaml_validation', 'warning')

# Initialize with custom profile
settings.initialize(profile='development')
```

### YAML Processing

```python
from freee_a11y_gl import process_yaml_data

# Process YAML data with validation
data = process_yaml_data('/path/to/yaml/file.yaml')
```

## Data Structure

The library expects a specific directory structure for your accessibility data:

```
data/
├── json/
│   ├── guideline-categories.json
│   ├── wcag-sc.json
│   ├── faq-tags.json
│   ├── info.json
│   └── schemas/
│       ├── guideline.json
│       ├── check.json
│       └── faq.json
└── yaml/
    ├── gl/           # Guidelines
    ├── checks/       # Accessibility checks
    └── faq/          # FAQ articles
```

## Core Models

### Category
Represents groupings of accessibility guidelines.

```python
category = a11y.Category.get_by_id('form')
name_ja = category.get_name('ja')
dependencies = category.get_dependency()
```

### Guideline
Represents individual accessibility guidelines.

```python
guideline = a11y.Guideline.get_by_id('form-labeling')
template_data = guideline.template_data('ja')
link_data = guideline.link_data('https://example.com')
```

### Check
Represents accessibility checks and validation rules.

```python
check = a11y.Check.get_by_id('form-label-check')
template_data = check.template_data('ja', platform=['web'])
```

### FAQ
Represents frequently asked questions and articles.

```python
faq = a11y.Faq.get_by_id('p0001')
template_data = faq.template_data('ja')
```

## Configuration

The library supports hierarchical configuration with the following precedence:

1. Program-specified configuration (`settings.initialize()`)
2. Profile settings (`~/.config/freee_a11y_gl/profiles/{profile}.yaml`)
3. Default profile (`~/.config/freee_a11y_gl/profiles/default.yaml`)
4. Library defaults (`~/.config/freee_a11y_gl/lib/config.yaml`)
5. Built-in defaults
6. Emergency fallback values

### Configuration Example

```yaml
# ~/.config/freee_a11y_gl/profiles/development.yaml
languages:
  available: ["ja", "en"]
  default: "ja"
base_url: "https://localhost:3000"
paths:
  guidelines: "/categories/"
  faq: "/faq/articles/"
validation:
  yaml_validation: "warning"
```

## Validation

The library provides comprehensive YAML validation with three modes:

- **strict**: Validation errors cause program termination
- **warning**: Validation errors are logged as warnings
- **disabled**: No validation is performed

```python
from freee_a11y_gl.yaml_validator import YamlValidator

validator = YamlValidator('/path/to/schemas', 'strict')
validator.validate_with_mode(data, 'guideline', '/path/to/file.yaml')
```

## Error Handling

The library includes robust error handling and recovery mechanisms:

```python
from freee_a11y_gl.error_recovery import ErrorRecovery

recovery = ErrorRecovery()
try:
    # Your code here
    pass
except Exception as e:
    recovery.handle_error(e, context={'file': 'example.yaml'})
```

## Utilities

### Version Information

```python
from freee_a11y_gl import get_version_info

version_info = get_version_info()
print(f"Version: {version_info['version']}")
```

### Source Path Utilities

```python
from freee_a11y_gl import get_src_path

src_paths = get_src_path('/path/to/data')
print(f"Guidelines path: {src_paths['guidelines']}")
```

### Info Links

```python
from freee_a11y_gl import get_info_links

links = get_info_links()
for link in links:
    print(f"Link: {link.url}")
```

## Documentation

For detailed API documentation and configuration guides, see the [docs](./docs/) directory:

- [API Reference](./docs/API_REFERENCE.md) - Comprehensive API documentation
- [Configuration Guide](./docs/CONFIGURATION.md) - Detailed configuration documentation

## Development

### Running Tests

```bash
cd tools/lib/freee_a11y_gl
python -m pytest tests/
```

### Code Quality

The library maintains high code quality standards:
- 100% test coverage (594 tests)
- Zero flake8 warnings
- Comprehensive docstrings following PEP 257

## License

This library is part of the freee accessibility guidelines project.

## Contributing

Please refer to the main project's contributing guidelines for information on how to contribute to this library.
