# yaml2rst

A Python tool for converting YAML files into reStructuredText (RST) files for the freee a11y-guidelines project.

## Overview

yaml2rst is a specialized content generation tool that processes YAML data files and converts them into properly formatted RST files for inclusion in the a11y-guidelines documentation. It supports multiple content types including guidelines, FAQs, checks, and reference materials, with full internationalization support.

### Key Features

- **Multi-language support**: Generate content for Japanese and English
- **Template-based generation**: Flexible Jinja2 template system
- **Modular architecture**: Clean mixin-based design for extensibility
- **Comprehensive testing**: 99.56% test coverage with 404+ tests
- **Performance optimized**: Efficient processing of large datasets
- **Type safety**: Full type hints and validation

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Dependencies

The tool requires the following Python packages:

```bash
pip install jinja2 freee_a11y_gl>=0.1.0
```

### Development Dependencies

For development and testing:

```bash
pip install pytest pytest-cov pytest-mock psutil flake8
```

### Installation from Source

1. Clone the repository:
```bash
git clone <repository-url>
cd a11y-guidelines/tools/scripts/yaml2rst
```

2. Install in development mode:
```bash
pip install -e .
```

## Basic Usage

### Command Line Interface

The primary way to use yaml2rst is through the command line:

```bash
# Generate all content for Japanese
yaml2rst --lang ja --basedir /path/to/a11y-guidelines

# Generate all content for English
yaml2rst --lang en --basedir /path/to/a11y-guidelines

# Generate specific files only
yaml2rst --lang ja --basedir /path/to/a11y-guidelines category.rst faq_index.rst

# Use custom template directory
yaml2rst --lang ja --basedir /path/to/a11y-guidelines --template-dir /custom/templates

# Export default templates for customization
yaml2rst --export-templates

# Export templates to custom directory
yaml2rst --export-templates --template-dir /custom/templates
```

### Available Options

- `--lang, -l`: Target language (ja/en)
- `--basedir, -b`: Base directory of the a11y-guidelines project
- `--template-dir, -t`: Custom template directory path
- `--export-templates`: Export built-in templates and exit
- `files`: Optional list of specific files to generate (positional arguments)
- `--help`: Show detailed help information

### Template Customization

yaml2rst supports template customization through a priority-based system:

```bash
# Export default templates for customization
yaml2rst --export-templates

# Export to custom directory
yaml2rst --export-templates --template-dir /path/to/custom/templates

# Use custom templates during generation
yaml2rst --lang ja --template-dir /path/to/custom/templates
```

**Template Resolution Priority:**
1. Custom templates (specified via `--template-dir`)
2. User templates (`~/.config/freee_a11y_gl/templates/`)
3. Built-in templates (default)

For detailed template customization guide, see [TEMPLATE_CUSTOMIZATION.md](docs/TEMPLATE_CUSTOMIZATION.md).

### Supported Content Types

yaml2rst can generate the following types of content:

- **Guidelines**: Category pages with accessibility guidelines
- **Checks**: Checklist items and examples
- **FAQ**: Frequently asked questions and tag pages
- **References**: WCAG mappings, priority information, and tool references
- **Build files**: Makefiles for documentation building

## Architecture Overview

yaml2rst follows a modular, mixin-based architecture designed for maintainability and extensibility.

### Core Components

- **ContentGeneratorBase**: Foundation class combining all mixins
- **Mixins**: Reusable functionality (RelationshipMixin, ValidationMixin, UtilityMixin)
- **Content Generators**: Specialized classes for different content types
- **FileGenerator**: Orchestrates the generation process
- **TemplateManager**: Handles Jinja2 template loading and rendering

### Design Patterns

- **Mixin Pattern**: Shared functionality across generators
- **Template Method**: Consistent generation workflow
- **Singleton**: Shared resource management
- **Factory**: Dynamic generator instantiation

For detailed architectural information, see [ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Development

### Running Tests

Use the provided test runner for comprehensive testing:

```bash
# Run all tests
python run_tests.py

# Run with coverage reporting
python run_tests.py --coverage

# Run specific test categories
python run_tests.py --type unit
python run_tests.py --type integration
python run_tests.py --type functional
python run_tests.py --type performance

# Run in fast mode (skip slow tests)
python run_tests.py --fast

# Run with verbose output
python run_tests.py --verbose
```

### Test Structure

The test suite is organized into three main categories:

- **Unit tests** (`tests/unit/`): Individual component testing
- **Integration tests** (`tests/integration/`): Component interaction testing
- **Functional tests** (`tests/functional/`): End-to-end workflow testing

Performance tests are integrated within these categories using pytest markers.

### Code Quality

The project maintains high code quality standards:

- **Test Coverage**: 99.56% (target: >90%)
- **Type Safety**: Full type hints throughout codebase
- **Documentation**: Comprehensive docstrings and comments
- **Code Style**: PEP 8 compliant with automated checking

### Contributing

1. **Fork the repository** and create a feature branch
2. **Write tests** for new functionality (TDD approach recommended)
3. **Ensure all tests pass** with `python run_tests.py`
4. **Maintain or improve** test coverage percentage
5. **Follow coding standards** and add appropriate documentation
6. **Submit a pull request** with clear description of changes

### Development Workflow

1. **Set up development environment**:
```bash
pip install -e .
pip install pytest pytest-cov pytest-mock psutil flake8
```

2. **Run tests during development**:
```bash
python run_tests.py --fast --verbose
```

3. **Check coverage before committing**:
```bash
python run_tests.py --coverage
```

4. **Validate code style**:
```bash
flake8 src/ tests/
```

## Project Structure

```
yaml2rst/
├── src/yaml2rst/           # Main source code
│   ├── generators/         # Content generators
│   │   ├── mixins.py      # Shared mixin classes
│   │   ├── content_generator_base.py
│   │   └── content_generators/  # Specific generators
│   ├── config.py          # Configuration management
│   ├── initializer.py     # Setup and initialization
│   ├── template_manager.py # Template handling
│   └── yaml2rst.py        # Main entry point
├── tests/                  # Comprehensive test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── functional/        # Functional tests
├── run_tests.py           # Test runner script
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## Troubleshooting

### Common Issues

**Import Errors**:
- Ensure all dependencies are installed: `pip install -e .`
- Verify Python path includes the src directory

**Template Not Found**:
- Check that template files exist in the expected location
- Verify basedir parameter points to correct a11y-guidelines directory

**Permission Errors**:
- Ensure write permissions for output directories
- Check file system permissions for template and data directories

**Memory Issues**:
- For large datasets, consider processing in smaller batches
- Monitor memory usage with performance tests

### Debug Mode

For detailed troubleshooting information:

```bash
# Run with maximum verbosity
python run_tests.py --verbose

# Check specific test failures
pytest tests/unit/test_specific_component.py -v

# Profile performance issues
python run_tests.py --type performance --verbose
```

### Getting Help

1. **Check the documentation**: Review [ARCHITECTURE.md](docs/ARCHITECTURE.md) and [API_REFERENCE.md](docs/API_REFERENCE.md)
2. **Run the test suite**: Often reveals configuration or environment issues
3. **Check logs**: Enable verbose logging for detailed execution information
4. **Review examples**: Look at existing generators for implementation patterns

## Performance

yaml2rst is optimized for processing large datasets efficiently:

- **Benchmarks**: <0.1s per item for typical content generation
- **Memory usage**: <100MB increase for 1000 items processing
- **Scalability**: Linear scaling with dataset size
- **Concurrency**: Thread-safe design for parallel processing

## License

This project is part of the freee a11y-guidelines project. See the main project repository for license information.

## Authors

- **Masafumi NAKANE** - *Initial work and maintenance* - max@freee.co.jp

## Acknowledgments

- Built on the freee_a11y_gl library
- Uses Jinja2 templating engine
- Inspired by modern Python development practices
- Part of the broader freee accessibility initiative

---

For detailed technical documentation, see:
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Detailed architecture and design patterns
- [API_REFERENCE.md](docs/API_REFERENCE.md) - Complete API documentation
- [tests/README.md](tests/README.md) - Testing guide and best practices
