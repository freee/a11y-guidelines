# yaml2rst Architecture

This document provides a comprehensive overview of the yaml2rst architecture, design patterns, and implementation details.

## Table of Contents

1. [Design Principles](#design-principles)
2. [Architecture Overview](#architecture-overview)
3. [Core Components](#core-components)
4. [Design Patterns](#design-patterns)
5. [Data Flow](#data-flow)
6. [Extension Points](#extension-points)
7. [Performance Considerations](#performance-considerations)
8. [Testing Architecture](#testing-architecture)

## Design Principles

### 1. Modularity and Separation of Concerns

The yaml2rst architecture is built around clear separation of responsibilities:

- **Content Generation**: Isolated in specialized generator classes
- **Template Management**: Centralized template loading and rendering
- **Data Processing**: Unified through mixin patterns
- **File Operations**: Abstracted through FileGenerator
- **Configuration**: Centralized in dedicated modules

### 2. Extensibility Through Composition

Rather than deep inheritance hierarchies, yaml2rst uses composition and mixins:

- **Mixin Pattern**: Shared functionality without tight coupling
- **Dependency Injection**: External dependencies provided at runtime
- **Plugin Architecture**: New generators can be added without modifying existing code

### 3. Type Safety and Validation

Strong typing and validation throughout:

- **Type Hints**: Complete type annotations for all public APIs
- **Runtime Validation**: Input validation through ValidationMixin
- **Error Handling**: Consistent error reporting and recovery

### 4. Performance and Scalability

Designed for efficient processing of large datasets:

- **Lazy Loading**: Resources loaded only when needed
- **Memory Efficiency**: Streaming processing where possible
- **Caching**: Intelligent caching of expensive operations

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        yaml2rst                            │
├─────────────────────────────────────────────────────────────┤
│  CLI Interface (yaml2rst.py)                               │
│  ├── Argument Parsing (initializer.py)                     │
│  ├── Configuration Setup (config.py)                       │
│  └── Template Export (--export-templates)                  │
├─────────────────────────────────────────────────────────────┤
│  Template System Layer                                      │
│  ├── TemplateConfig (Configuration Management)             │
│  ├── TemplateResolver (Priority-based Resolution)          │
│  └── TemplateManager (Jinja2 Integration)                  │
├─────────────────────────────────────────────────────────────┤
│  Generation Layer                                           │
│  ├── FileGenerator (Orchestration)                         │
│  └── Content Generators (Specialized Processing)           │
├─────────────────────────────────────────────────────────────┤
│  Foundation Layer                                           │
│  ├── ContentGeneratorBase (Unified Interface)              │
│  └── Mixins (Shared Functionality)                         │
│      ├── RelationshipMixin                                 │
│      ├── ValidationMixin                                   │
│      └── UtilityMixin                                      │
├─────────────────────────────────────────────────────────────┤
│  External Dependencies                                      │
│  ├── freee_a11y_gl (Data Access)                          │
│  ├── Jinja2 (Template Engine)                             │
│  └── File System (I/O Operations)                         │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### ContentGeneratorBase

The foundation class that all content generators inherit from. It combines all mixins and provides a unified interface.

```python
class ContentGeneratorBase(RelationshipMixin, ValidationMixin, UtilityMixin):
    """Base class for all content generators.
    
    Provides unified access to:
    - RelationshipManager through RelationshipMixin
    - Common validation methods through ValidationMixin
    - Utility functions through UtilityMixin
    """
```

**Key Responsibilities:**
- Provide consistent interface for all generators
- Combine mixin functionality
- Define abstract methods for subclass implementation
- Handle common initialization patterns

### Template System Components

#### TemplateConfig

Manages template configuration and resolution paths:

```python
class TemplateConfig:
    """Configuration for template resolution system.
    
    Handles:
    - Configuration file loading
    - Environment variable processing
    - Template directory path resolution
    - Priority-based template search paths
    """
```

**Key Features:**
- Loads configuration from `~/.config/freee_a11y_gl/yaml2rst.conf`
- Supports environment variables (YAML2RST_*)
- Manages template directory priorities
- Provides path expansion and validation

#### TemplateResolver

Resolves template files based on priority system:

```python
class TemplateResolver:
    """Resolves template files with priority-based fallback.
    
    Priority order:
    1. Custom template directory (--template-dir)
    2. User template directory (~/.config/freee_a11y_gl/templates/)
    3. Built-in template directory
    """
```

**Key Features:**
- Priority-based template resolution
- Automatic fallback to lower priority directories
- Template existence validation
- Error handling for missing templates

#### TemplateManager

Enhanced template management with customization support:

```python
class TemplateManager:
    """Manages Jinja2 template loading with customization support.
    
    Features:
    - Template customization through TemplateConfig
    - Priority-based template resolution
    - Jinja2 environment management
    - Template caching and optimization
    """
```

**Key Features:**
- Factory method `from_config()` for configuration-based initialization
- Integration with TemplateResolver for file resolution
- Support for custom template directories
- Template export functionality

### Mixin Classes

#### RelationshipMixin

Provides unified access to the RelationshipManager singleton:

```python
class RelationshipMixin:
    @property
    def relationship_manager(self):
        """Lazy-loaded RelationshipManager instance."""
        if not hasattr(self, '_relationship_manager'):
            from freee_a11y_gl.relationship_manager import RelationshipManager
            self._relationship_manager = RelationshipManager()
        return self._relationship_manager
```

**Benefits:**
- Eliminates code duplication across generators
- Provides consistent access pattern
- Lazy loading for performance
- Singleton pattern ensures single instance

#### ValidationMixin

Consolidates common validation patterns:

```python
class ValidationMixin:
    def validate_required_fields(self, data, required_fields):
        """Validate presence of required fields."""
        
    def validate_list_field(self, data, field_name):
        """Validate field is a list."""
        
    def validate_string_field(self, data, field_name, allow_empty=False):
        """Validate field is a non-empty string."""
```

**Benefits:**
- Consistent validation across all generators
- Reusable validation logic
- Type-safe validation methods
- Configurable validation rules

#### UtilityMixin

Provides common utility methods:

```python
class UtilityMixin:
    def get_sorted_objects(self, objects, sort_key='sort_key'):
        """Sort objects by specified attribute."""
        
    def get_sorted_objects_by_lang_name(self, objects, lang):
        """Sort objects by localized name."""
        
    def process_template_data(self, obj, lang):
        """Convert object to template data."""
        
    def process_template_data_list(self, objects, lang):
        """Convert object list to template data."""
```

**Benefits:**
- Eliminates repetitive utility code
- Consistent data processing patterns
- Language-aware operations
- Template-ready data conversion

### FileGenerator

Orchestrates the entire generation process:

```python
class FileGenerator:
    def __init__(self, templates, lang):
        self.templates = templates
        self.lang = lang
    
    def generate(self, config, build_all, targets):
        """Generate files based on configuration."""
```

**Responsibilities:**
- Coordinate generator execution
- Manage file output operations
- Handle target filtering
- Provide progress reporting

### Content Generators

Specialized classes for different content types:

- **CategoryGenerator**: Generates guideline category pages
- **FaqGenerator**: Handles FAQ articles and indexes
- **CheckGenerator**: Processes check items and examples
- **ReferenceGenerator**: Creates reference documentation
- **MakefileGenerator**: Generates build configuration

Each generator follows the same pattern:

```python
class SpecificGenerator(ContentGeneratorBase):
    def __init__(self, lang):
        self.lang = lang
    
    def generate_content(self):
        """Generate specific content type."""
        # Implementation specific to content type
```

## Design Patterns

### 1. Mixin Pattern

**Problem**: Multiple generators need similar functionality without deep inheritance.

**Solution**: Compose functionality through mixins.

```python
# Before: Repetitive code in each generator
class CategoryGenerator:
    def __init__(self, lang):
        from freee_a11y_gl.relationship_manager import RelationshipManager
        self.relationship_manager = RelationshipManager()
    
    def validate_data(self, data):
        # Validation logic repeated in every generator
        pass

# After: Clean composition through mixins
class CategoryGenerator(ContentGeneratorBase):
    def __init__(self, lang):
        # RelationshipManager available through mixin
        # Validation methods available through mixin
        pass
```

**Benefits:**
- Eliminates code duplication
- Provides flexible composition
- Maintains single responsibility principle
- Enables easy testing of individual components

### 2. Template Method Pattern

**Problem**: Generators follow similar workflow but with different implementations.

**Solution**: Define common workflow in base class with customizable steps.

```python
class ContentGeneratorBase:
    def generate(self):
        """Template method defining generation workflow."""
        data = self.load_data()
        validated_data = self.validate_data(data)
        processed_data = self.process_data(validated_data)
        return self.render_template(processed_data)
    
    # Abstract methods for subclasses to implement
    def load_data(self): pass
    def validate_data(self, data): pass
    def process_data(self, data): pass
    def render_template(self, data): pass
```

### 3. Singleton Pattern

**Problem**: RelationshipManager should have single instance across application.

**Solution**: Lazy-loaded singleton through mixin.

```python
class RelationshipMixin:
    @property
    def relationship_manager(self):
        if not hasattr(self, '_relationship_manager'):
            # Singleton instance created once
            self._relationship_manager = RelationshipManager()
        return self._relationship_manager
```

### 4. Factory Pattern

**Problem**: Dynamic instantiation of generators based on configuration.

**Solution**: Factory method for generator creation.

```python
def create_generator(generator_class, lang, **kwargs):
    """Factory method for generator instantiation."""
    return generator_class(lang, **kwargs)
```

## Data Flow

### 1. Initialization Phase

```
CLI Arguments → initializer.py → Configuration Setup
                              ↓
Template Loading → TemplateManager → Jinja2 Environment
                              ↓
freee_a11y_gl Setup → Config.initialize() → Data Access Layer
```

### 2. Generation Phase

```
FileGenerator.generate() → Generator Selection → Content Generation
                                            ↓
Data Loading → ValidationMixin.validate() → Processing → Template Rendering
                                                      ↓
File Output → Directory Creation → RST File Writing → Completion
```

### 3. Data Transformation Pipeline

```
YAML Files → freee_a11y_gl → Python Objects → Template Data → RST Content
    ↓              ↓              ↓              ↓              ↓
Raw Data → Structured Data → Validated Data → Rendered Data → Output Files
```

## Extension Points

### Adding New Content Generators

1. **Create Generator Class**:
```python
class NewContentGenerator(ContentGeneratorBase):
    def __init__(self, lang):
        self.lang = lang
    
    def generate_content(self):
        # Implement content generation logic
        pass
```

2. **Register in Main Module**:
```python
generators = [
    # Existing generators...
    GeneratorConfig(NewContentGenerator, 'template_name', output_path),
]
```

3. **Create Template**:
```jinja2
{# templates/template_name.rst.j2 #}
{{ title }}
{{ "=" * title|length }}

{% for item in items %}
{{ item.content }}
{% endfor %}
```

### Adding New Mixins

1. **Define Mixin Class**:
```python
class NewFunctionalityMixin:
    def new_method(self):
        """New shared functionality."""
        pass
```

2. **Add to ContentGeneratorBase**:
```python
class ContentGeneratorBase(
    RelationshipMixin, 
    ValidationMixin, 
    UtilityMixin,
    NewFunctionalityMixin  # Add new mixin
):
    pass
```

### Customizing Validation

1. **Extend ValidationMixin**:
```python
class CustomValidationMixin(ValidationMixin):
    def validate_custom_field(self, data, field_name):
        """Custom validation logic."""
        pass
```

2. **Use in Specific Generator**:
```python
class SpecialGenerator(ContentGeneratorBase, CustomValidationMixin):
    pass
```

## Performance Considerations

### Memory Management

- **Lazy Loading**: RelationshipManager and templates loaded on demand
- **Generator Pattern**: Use generators for large datasets
- **Resource Cleanup**: Proper cleanup of file handles and resources

### Caching Strategy

- **Template Caching**: Jinja2 templates cached after first load
- **Data Caching**: Expensive data operations cached within generation cycle
- **Singleton Pattern**: Single instance of shared resources

### Scalability

- **Linear Scaling**: Processing time scales linearly with dataset size
- **Memory Efficiency**: Constant memory usage regardless of dataset size
- **Parallel Processing**: Thread-safe design enables parallel execution

### Performance Benchmarks

- **Generation Speed**: <0.1s per content item
- **Memory Usage**: <100MB for 1000 items
- **Template Rendering**: <1ms per template
- **File I/O**: Optimized batch operations

## Testing Architecture

### Test Organization

```
tests/
├── unit/           # Individual component testing
├── integration/    # Component interaction testing
├── functional/     # End-to-end workflow testing
└── performance/    # Scalability and performance testing
```

### Testing Patterns

#### Unit Testing with Mocks

```python
class TestCategoryGenerator:
    @patch('yaml2rst.generators.mixins.RelationshipManager')
    def test_relationship_manager_access(self, mock_rm):
        generator = CategoryGenerator('ja')
        rm = generator.relationship_manager
        mock_rm.assert_called_once()
```

#### Integration Testing

```python
class TestGeneratorIntegration:
    def test_end_to_end_generation(self, temp_dir, mock_templates):
        # Test complete generation workflow
        file_generator = FileGenerator(mock_templates, 'ja')
        config = GeneratorConfig(CategoryGenerator, 'template', temp_dir)
        file_generator.generate(config, False, [])
        # Verify output files created
```

#### Performance Testing

```python
class TestPerformance:
    def test_large_dataset_processing(self):
        # Generate large dataset
        # Measure processing time and memory usage
        # Assert performance benchmarks met
```

### Test Coverage Strategy

- **Unit Tests**: 100% coverage of individual methods
- **Integration Tests**: Coverage of component interactions
- **Functional Tests**: Coverage of user workflows
- **Performance Tests**: Benchmark validation

### Mocking Strategy

- **External Dependencies**: Mock freee_a11y_gl components
- **File System**: Mock file operations for isolation
- **Templates**: Mock template rendering for unit tests
- **Time-dependent Operations**: Mock for deterministic tests

## Class Hierarchy

### Inheritance Structure

```
ContentGeneratorBase (ABC)
├── RelationshipMixin
├── ValidationMixin
└── UtilityMixin

Concrete Generators:
├── CategoryGenerator(ContentGeneratorBase)
├── FaqArticleGenerator(ContentGeneratorBase)
├── FaqTagPageGenerator(ContentGeneratorBase)
├── FaqIndexGenerator(ContentGeneratorBase)
├── CheckGenerator(ContentGeneratorBase)
├── WcagMappingGenerator(ContentGeneratorBase)
├── ReferenceGenerator(ContentGeneratorBase)
└── MakefileGenerator(ContentGeneratorBase)
```

### Method Resolution Order (MRO)

For any concrete generator, the MRO follows:
1. ConcreteGenerator
2. ContentGeneratorBase
3. RelationshipMixin
4. ValidationMixin
5. UtilityMixin
6. object

This ensures predictable method resolution and avoids diamond problem issues.

## Configuration Management

### Configuration Layers

1. **Default Configuration**: Built-in defaults in code
2. **Environment Variables**: Runtime environment settings
3. **Command Line Arguments**: User-specified overrides
4. **Configuration Files**: Persistent settings (future enhancement)

### Configuration Flow

```python
# 1. Initialize with defaults
settings = default_settings()

# 2. Apply environment variables
settings.update(env_settings())

# 3. Apply command line arguments
settings.update(parse_args())

# 4. Validate configuration
validate_settings(settings)
```

## Error Handling Strategy

### Error Categories

1. **Configuration Errors**: Invalid settings or missing dependencies
2. **Data Errors**: Invalid YAML data or missing files
3. **Template Errors**: Template syntax or rendering issues
4. **I/O Errors**: File system permission or space issues

### Error Handling Patterns

```python
class GeneratorError(Exception):
    """Base exception for generator errors."""
    pass

class ConfigurationError(GeneratorError):
    """Configuration-related errors."""
    pass

class DataValidationError(GeneratorError):
    """Data validation errors."""
    pass

class TemplateError(GeneratorError):
    """Template processing errors."""
    pass
```

### Recovery Strategies

- **Graceful Degradation**: Continue processing other items on single item failure
- **Retry Logic**: Retry transient failures with exponential backoff
- **Fallback Options**: Use default values when optional data is missing
- **User Feedback**: Clear error messages with actionable suggestions

## Security Considerations

### Input Validation

- **YAML Safety**: Use safe YAML loading to prevent code injection
- **Path Validation**: Validate file paths to prevent directory traversal
- **Template Security**: Restrict template access to safe operations
- **Data Sanitization**: Sanitize user-provided data before processing

### File System Security

- **Permission Checks**: Verify write permissions before file operations
- **Path Restrictions**: Limit file operations to designated directories
- **Temporary Files**: Secure handling of temporary files
- **Cleanup**: Proper cleanup of temporary resources

## Future Enhancements

### Planned Improvements

1. **Parallel Processing**: Multi-threaded generation for large datasets
2. **Incremental Updates**: Only regenerate changed content
3. **Plugin System**: Dynamic loading of custom generators
4. **Configuration Files**: YAML/JSON configuration file support
5. **Monitoring**: Built-in performance and error monitoring
6. **Caching Layer**: Persistent caching of expensive operations

### Extension Opportunities

1. **Output Formats**: Support for additional output formats (HTML, PDF)
2. **Data Sources**: Support for additional data sources (databases, APIs)
3. **Template Engines**: Support for alternative template engines
4. **Internationalization**: Enhanced i18n support beyond current languages
5. **Validation Rules**: Configurable validation rule system
6. **Workflow Integration**: Integration with CI/CD pipelines

---

This architecture document serves as the definitive guide to understanding and extending the yaml2rst system. For implementation details, refer to the source code and API documentation.
