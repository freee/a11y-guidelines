# Configuration Guide

This document provides comprehensive information about configuring the freee_a11y_gl library, including the settings system, configuration files, profiles, and all available configuration options.

## Table of Contents

- [Overview](#overview)
- [Configuration Hierarchy](#configuration-hierarchy)
- [Settings System](#settings-system)
- [Configuration Files](#configuration-files)
- [Configuration Options](#configuration-options)
- [Profiles](#profiles)
- [Message Catalogs](#message-catalogs)
- [Validation Configuration](#validation-configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)

## Overview

The freee_a11y_gl library uses a hierarchical configuration system that allows for flexible customization while providing sensible defaults. The configuration system supports:

- **Profile-based configuration**: Different settings for different environments
- **Hierarchical overrides**: Settings can be overridden at multiple levels
- **Type validation**: Configuration is validated using Pydantic models
- **Message catalogs**: Internationalization support with customizable messages
- **YAML validation modes**: Configurable validation behavior

## Configuration Hierarchy

Configuration values are resolved in the following order of precedence (highest to lowest):

1. **Program-specified configuration** - Set via `settings.initialize()`
2. **Profile settings** - `~/.config/freee_a11y_gl/profiles/{profile}.yaml`
3. **Default profile** - `~/.config/freee_a11y_gl/profiles/default.yaml`
4. **Library defaults** - `~/.config/freee_a11y_gl/lib/config.yaml`
5. **Built-in defaults** - Package internal defaults
6. **Emergency fallback** - Minimal hardcoded values

## Settings System

### Global Settings Instance

The library provides a global settings instance that can be imported and used throughout your application:

```python
from freee_a11y_gl import settings

# Access configuration
config = settings.config
base_url = settings.get('base_url')

# Update settings
settings.set('validation.yaml_validation', 'warning')
```

### Settings Class

#### Constructor

```python
Settings(profile: Optional[str] = None)
```

**Parameters:**
- `profile` (str, optional): Profile name to use (defaults to "default")

#### Methods

##### `get(key: str, default: Any = None) -> Any`

Get a configuration value using dot notation.

**Parameters:**
- `key` (str): Dot-separated configuration key (e.g., "validation.yaml_validation")
- `default` (Any, optional): Default value if key is not found

**Returns:**
- `Any`: Configuration value

**Example:**
```python
# Get simple values
base_url = settings.get('base_url')
default_lang = settings.get('languages.default')

# Get with default
timeout = settings.get('network.timeout', 30)
```

##### `set(key: str, value: Any) -> None`

Set a configuration value using dot notation.

**Parameters:**
- `key` (str): Dot-separated configuration key
- `value` (Any): Value to set

**Example:**
```python
settings.set('base_url', 'https://localhost:3000')
settings.set('validation.yaml_validation', 'warning')
```

##### `initialize(profile: Optional[str] = None, config_override: Optional[Dict[str, Any]] = None) -> None`

Initialize settings with a specific profile and configuration overrides.

**Parameters:**
- `profile` (str, optional): Profile name to use
- `config_override` (Dict[str, Any], optional): Configuration overrides

**Example:**
```python
# Initialize with development profile
settings.initialize(profile='development')

# Initialize with overrides
settings.initialize(
    profile='testing',
    config_override={
        'validation': {'yaml_validation': 'disabled'},
        'base_url': 'https://test.example.com'
    }
)
```

##### `update(settings: Optional[Dict[str, Any]] = None) -> None`

Update multiple configuration values at once.

**Parameters:**
- `settings` (Dict[str, Any], optional): Dictionary of settings to update

**Example:**
```python
settings.update({
    'languages': {
        'available': ['ja', 'en', 'fr'],
        'default': 'en'
    },
    'validation': {
        'yaml_validation': 'warning'
    }
})
```

#### Properties

##### `config -> GlobalConfig`

Get the typed configuration object with validation.

**Returns:**
- `GlobalConfig`: Validated configuration object

**Example:**
```python
config = settings.config
print(f"Available languages: {config.languages.available}")
print(f"Base URL: {config.base_url}")
print(f"Validation mode: {config.validation.yaml_validation}")
```

##### `message_catalog -> MessageCatalog`

Get the message catalog for internationalization.

**Returns:**
- `MessageCatalog`: Message catalog instance

**Example:**
```python
catalog = settings.message_catalog
check_tools = catalog.check_tools
```

## Configuration Files

### File Locations

Configuration files are stored in the user's configuration directory:

```
~/.config/freee_a11y_gl/
├── profiles/
│   ├── default.yaml          # Default profile
│   ├── development.yaml      # Development profile
│   └── production.yaml       # Production profile
├── lib/
│   └── config.yaml          # Library-level defaults
└── messages/
    ├── default.yaml         # Default message catalog
    └── development.yaml     # Profile-specific messages
```

### Configuration File Format

Configuration files use YAML format:

```yaml
# Example configuration file
languages:
  available: ["ja", "en"]
  default: "ja"

base_url: "https://a11y-guidelines.freee.co.jp"

paths:
  guidelines: "/categories/"
  faq: "/faq/articles/"

validation:
  yaml_validation: "strict"

axe_core:
  submodule_name: "vendor/axe-core"
  base_dir: "vendor/axe-core"
  deque_url: "https://dequeuniversity.com/rules/axe/"
  pkg_file: "package.json"
  rules_dir: "lib/rules"
  locale_dir: "locales"
  locale_ja_file: "ja.json"
```

## Configuration Options

### GlobalConfig

The main configuration object with the following structure:

```python
class GlobalConfig(BaseModel):
    languages: LanguageConfig
    base_url: str
    paths: PathConfig
    validation: ValidationConfig = Field(default_factory=ValidationConfig)
    axe_core: AxeCoreConfig
```

### LanguageConfig

Language-related configuration:

```python
class LanguageConfig(BaseModel):
    available: List[str]  # Available language codes
    default: str          # Default language code
```

**Example:**
```yaml
languages:
  available: ["ja", "en", "fr"]
  default: "ja"
```

### PathConfig

URL path configuration for different content types:

```python
class PathConfig(BaseModel):
    guidelines: str  # Guidelines path (must start and end with /)
    faq: str        # FAQ path (must start and end with /)
```

**Validation Rules:**
- Paths must start with "/"
- Paths must end with "/"
- Paths cannot be empty

**Example:**
```yaml
paths:
  guidelines: "/categories/"
  faq: "/faq/articles/"
```

### ValidationConfig

YAML validation configuration:

```python
class ValidationConfig(BaseModel):
    yaml_validation: Literal["strict", "warning", "disabled"] = "strict"
```

**Options:**
- `strict`: Validation errors cause program termination
- `warning`: Validation errors are logged as warnings but don't stop execution
- `disabled`: No validation is performed

**Example:**
```yaml
validation:
  yaml_validation: "warning"
```

### AxeCoreConfig

Configuration for axe-core integration:

```python
class AxeCoreConfig(BaseModel):
    submodule_name: str    # Git submodule name
    base_dir: str          # Base directory for axe-core
    deque_url: str         # Deque University URL for rules
    pkg_file: str          # Package.json file name
    rules_dir: str         # Rules directory
    locale_dir: str        # Locale directory
    locale_ja_file: str    # Japanese locale file
```

**Example:**
```yaml
axe_core:
  submodule_name: "vendor/axe-core"
  base_dir: "vendor/axe-core"
  deque_url: "https://dequeuniversity.com/rules/axe/"
  pkg_file: "package.json"
  rules_dir: "lib/rules"
  locale_dir: "locales"
  locale_ja_file: "ja.json"
```

## Profiles

Profiles allow you to maintain different configuration sets for different environments or use cases.

### Creating Profiles

Create profile-specific configuration files in `~/.config/freee_a11y_gl/profiles/`:

#### Development Profile (`development.yaml`)

```yaml
base_url: "https://localhost:3000"
validation:
  yaml_validation: "warning"
languages:
  default: "en"
```

#### Production Profile (`production.yaml`)

```yaml
base_url: "https://a11y-guidelines.freee.co.jp"
validation:
  yaml_validation: "strict"
languages:
  default: "ja"
```

#### Testing Profile (`testing.yaml`)

```yaml
base_url: "https://test.example.com"
validation:
  yaml_validation: "disabled"
```

### Using Profiles

#### Programmatic Profile Selection

```python
from freee_a11y_gl import settings

# Initialize with specific profile
settings.initialize(profile='development')

# Or create settings instance with profile
from freee_a11y_gl.settings import Settings
dev_settings = Settings(profile='development')
```

#### Environment-based Profile Selection

```python
import os
from freee_a11y_gl import settings

# Use environment variable to select profile
profile = os.getenv('A11Y_PROFILE', 'default')
settings.initialize(profile=profile)
```

## Message Catalogs

Message catalogs provide internationalization support and customizable messages.

### Message Catalog Structure

```yaml
# Example message catalog
check_tools:
  axe:
    ja: "axe"
    en: "axe"
  nvda:
    ja: "NVDA"
    en: "NVDA"
  voiceover:
    ja: "VoiceOver"
    en: "VoiceOver"

text_separators:
  ja: "："
  en: ": "

platform_separators:
  ja: "、"
  en: ", "
```

### Custom Message Catalogs

Create custom message catalogs in `~/.config/freee_a11y_gl/messages/`:

#### Profile-specific Messages (`development.yaml`)

```yaml
check_tools:
  custom_tool:
    ja: "カスタムツール"
    en: "Custom Tool"

text_separators:
  ja: " - "
  en: " - "
```

### Using Message Catalogs

```python
from freee_a11y_gl import settings

catalog = settings.message_catalog
check_tools = catalog.check_tools

# Access tool names
axe_name_ja = check_tools['axe']['ja']  # "axe"
nvda_name_en = check_tools['nvda']['en']  # "NVDA"
```

## Validation Configuration

The library provides flexible YAML validation configuration to suit different development workflows.

### Validation Modes

#### Strict Mode (Default)

```yaml
validation:
  yaml_validation: "strict"
```

- Validation errors cause immediate program termination
- Best for production environments
- Ensures data integrity

#### Warning Mode

```yaml
validation:
  yaml_validation: "warning"
```

- Validation errors are logged as warnings
- Program continues execution
- Useful for development and debugging

#### Disabled Mode

```yaml
validation:
  yaml_validation: "disabled"
```

- No validation is performed
- Maximum performance
- Use only when data integrity is guaranteed

### Programmatic Validation Configuration

```python
from freee_a11y_gl import settings

# Set validation mode
settings.set('validation.yaml_validation', 'warning')

# Or during initialization
settings.initialize(
    config_override={
        'validation': {'yaml_validation': 'disabled'}
    }
)
```

## Examples

### Basic Configuration Setup

```python
from freee_a11y_gl import settings, setup_instances

# Initialize with development profile
settings.initialize(profile='development')

# Set up library instances
rel_manager = setup_instances('/path/to/data')

# Access configuration
config = settings.config
print(f"Using base URL: {config.base_url}")
```

### Custom Configuration Override

```python
from freee_a11y_gl import settings

# Initialize with custom configuration
settings.initialize(
    profile='production',
    config_override={
        'base_url': 'https://custom.example.com',
        'validation': {
            'yaml_validation': 'warning'
        },
        'languages': {
            'available': ['ja', 'en', 'fr'],
            'default': 'en'
        }
    }
)
```

### Environment-specific Configuration

```python
import os
from freee_a11y_gl import settings

# Determine configuration based on environment
env = os.getenv('ENVIRONMENT', 'development')

if env == 'production':
    settings.initialize(
        profile='production',
        config_override={
            'validation': {'yaml_validation': 'strict'}
        }
    )
elif env == 'testing':
    settings.initialize(
        profile='testing',
        config_override={
            'validation': {'yaml_validation': 'disabled'}
        }
    )
else:
    settings.initialize(profile='development')
```

### Dynamic Configuration Updates

```python
from freee_a11y_gl import settings

# Update configuration at runtime
settings.update({
    'base_url': 'https://new-domain.com',
    'paths': {
        'guidelines': '/new-guidelines/',
        'faq': '/new-faq/'
    }
})

# Individual updates
settings.set('validation.yaml_validation', 'warning')
settings.set('languages.default', 'en')
```

## Best Practices

### 1. Use Profiles for Different Environments

Create separate profiles for development, testing, and production:

```yaml
# ~/.config/freee_a11y_gl/profiles/development.yaml
validation:
  yaml_validation: "warning"
base_url: "https://localhost:3000"

# ~/.config/freee_a11y_gl/profiles/production.yaml
validation:
  yaml_validation: "strict"
base_url: "https://a11y-guidelines.freee.co.jp"
```

### 2. Validate Configuration Early

Initialize and validate configuration at application startup:

```python
from freee_a11y_gl import settings

try:
    settings.initialize(profile='production')
    config = settings.config  # This validates the configuration
    print("Configuration loaded successfully")
except Exception as e:
    print(f"Configuration error: {e}")
    exit(1)
```

### 3. Use Environment Variables for Profile Selection

```python
import os
from freee_a11y_gl import settings

profile = os.getenv('A11Y_PROFILE', 'default')
settings.initialize(profile=profile)
```

### 4. Keep Sensitive Information Out of Configuration Files

Use environment variables or secure configuration management for sensitive data:

```python
import os
from freee_a11y_gl import settings

settings.initialize(
    config_override={
        'base_url': os.getenv('A11Y_BASE_URL', 'https://localhost:3000')
    }
)
```

### 5. Document Custom Configurations

When creating custom profiles or message catalogs, document the purpose and usage:

```yaml
# ~/.config/freee_a11y_gl/profiles/ci.yaml
# Configuration for Continuous Integration environment
# - Validation disabled for performance
# - Custom base URL for testing
validation:
  yaml_validation: "disabled"
base_url: "https://ci.example.com"
```

### 6. Test Configuration Changes

Always test configuration changes in a development environment before applying to production:

```python
from freee_a11y_gl import settings

# Test configuration
settings.initialize(profile='development')
try:
    config = settings.config
    print("Configuration is valid")
except Exception as e:
    print(f"Configuration error: {e}")
```

### 7. Use Hierarchical Configuration

Take advantage of the configuration hierarchy to minimize duplication:

```yaml
# ~/.config/freee_a11y_gl/lib/config.yaml (base configuration)
languages:
  available: ["ja", "en"]
  default: "ja"

# ~/.config/freee_a11y_gl/profiles/development.yaml (override only what's needed)
base_url: "https://localhost:3000"
validation:
  yaml_validation: "warning"
```

This configuration system provides flexibility while maintaining type safety and validation. Use profiles and the configuration hierarchy to create maintainable, environment-specific configurations for your accessibility guidelines processing needs.
