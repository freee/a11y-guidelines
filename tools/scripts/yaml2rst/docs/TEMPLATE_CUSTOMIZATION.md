# Template Customization Guide

This guide explains how to customize templates in yaml2rst to modify the appearance and structure of generated RST documentation files.

## Overview

The yaml2rst template customization system allows you to override built-in templates on a per-file basis with a priority-based fallback system:

1. **Custom templates** (highest priority) - Specified via `--template-dir` command-line option
2. **User templates** (medium priority) - Located in `~/.config/freee_a11y_gl/templates/`
3. **Built-in templates** (lowest priority) - Default templates included with yaml2rst

## Quick Start

### 1. Export Default Templates

```bash
# Export all built-in templates to default user directory
yaml2rst --export-templates
```

This will export 15 template files to `~/.config/freee_a11y_gl/templates/`:
- Core templates (gl-category.rst, wcag21-mapping.rst, etc.)
- Check templates (checks/allchecks.rst, checks/examples-tool.rst)
- FAQ templates (faq/article.rst, faq/index.rst, etc.)

### 2. Customize Templates

```bash
# Edit the exported templates
nano ~/.config/freee_a11y_gl/templates/gl-category.rst
```

### 3. Generate Documentation

```bash
# The customized templates will be used automatically
yaml2rst --lang ja --basedir /path/to/data
```

## Configuration Methods

### Method 1: Configuration File

Create `~/.config/freee_a11y_gl/yaml2rst.conf`:

```ini
[templates]
user_template_dir = ~/.config/freee_a11y_gl/templates
fallback_to_builtin = true
```

**Configuration Options:**

- `user_template_dir`: Path to your custom templates directory
- `fallback_to_builtin`: Whether to fall back to built-in templates when custom templates are not found (default: true)

### Method 2: Environment Variables

```bash
export YAML2RST_USER_TEMPLATE_DIR="~/.config/freee_a11y_gl/templates"
export YAML2RST_FALLBACK_TO_BUILTIN="true"
```

**Available Environment Variables:**

- `YAML2RST_USER_TEMPLATE_DIR`: Override user template directory
- `YAML2RST_FALLBACK_TO_BUILTIN`: Override fallback behavior (true/false)

### Method 3: Command-Line Options

```bash
python -m yaml2rst --template-dir /path/to/custom/templates
```

**Command-Line Options:**

- `--template-dir`: Specify a custom template directory (highest priority)

## Priority System

Templates are resolved in the following priority order:

1. **Custom directory** (specified via `--template-dir`)
2. **User directory** (from config file or environment variable)
3. **Built-in directory** (default templates)

If a template is not found in a higher-priority location, the system automatically falls back to the next priority level.

## Available Templates

### Core Templates

| Template File | Purpose | Generator |
|---------------|---------|-----------|
| `gl-category.rst` | Category pages for guidelines | CategoryGenerator |
| `wcag21-mapping.rst` | WCAG 2.1 mapping reference | WcagMappingGenerator |
| `axe-rules.rst` | Axe accessibility rules reference | AxeRulesGenerator |
| `priority-diff.rst` | Priority difference documentation | PriorityDiffGenerator |
| `info_to_gl.rst` | Info to guidelines mapping | InfoToGuidelinesGenerator |
| `info_to_faq.rst` | Info to FAQ mapping | InfoToFaqsGenerator |
| `misc-defs.txt` | Miscellaneous definitions | MiscDefinitionsGenerator |
| `incfiles.mk` | Makefile includes | MakefileGenerator |

### Template Subdirectories

- `checks/` - Templates for check-related content
- `faq/` - Templates for FAQ content

## Template Customization Examples

### Example 1: Customizing Category Pages

Create `~/.config/freee_a11y_gl/templates/gl-category.rst`:

```jinja2
{# Custom category template with enhanced styling #}
{% for gl in guidelines -%}
.. _{{ gl.id }}:

{{ gl.title|make_heading(2, 'custom-guideline') }}

**📋 Guideline:** {{ gl.guideline }}

**🎯 Target Platforms:** {{ gl.platform }}

**💡 Intent:**
{{ gl.intent | indent(3) }}

{# Add custom styling for WCAG mapping #}
**🔗 WCAG 2.1 Success Criteria:**
{% for sc in gl.scs %}
- **{{ sc.sc }}** (Level {{ sc.level }}): `{{ sc.sc_en_title }} <{{ sc.sc_en_url }}>`__
{% endfor %}

{# Custom check section with enhanced formatting #}
{{ "📝 Checklist Items"|make_heading(3, 'checklist-section') }}

{% for check in gl.checks -%}
{{ (":ref:`check-" + check.id + "`")|make_heading(4, 'check-item') }}

**Description:** {{ check.check }}

| **Target** | **Platform** | **Severity** |
|------------|--------------|--------------|
| {{ check.target }} | {{ check.platform }} | {{ check.severity }} |

{% endfor %}
{% endfor %}
```

### Example 2: Custom WCAG Mapping

Create `~/.config/freee_a11y_gl/templates/wcag21-mapping.rst`:

```jinja2
{# Enhanced WCAG mapping with better organization #}
{{ "WCAG 2.1 Success Criteria Mapping"|make_heading(1) }}

This document provides a comprehensive mapping between our accessibility guidelines and WCAG 2.1 Success Criteria.

{{ "Success Criteria Overview"|make_heading(2) }}

{% for sc in wcag_mapping -%}
{{ ("SC " + sc.sc + ": " + sc.title)|make_heading(3) }}

**Level:** {{ sc.level }}
**URL:** `{{ sc.title }} <{{ sc.url }}>`__

**Related Guidelines:**
{% for guideline in sc.guidelines %}
- :ref:`{{ guideline.id }}` - {{ guideline.title }}
{% endfor %}

---

{% endfor %}
```

### Example 3: Project-Specific Template Directory

For project-specific customizations, use the command-line option:

```bash
# Use project-specific templates
python -m yaml2rst --template-dir ./project-templates/

# Directory structure:
# project-templates/
# ├── gl-category.rst      # Custom category template
# ├── wcag21-mapping.rst   # Custom WCAG mapping
# └── checks/
#     └── implementation.rst # Custom check implementation template
```

## Template Development

### Template Variables

Templates have access to various data structures depending on their purpose:

#### Category Templates (`gl-category.rst`)
- `guidelines`: List of guideline objects
- `lang`: Current language ('ja' or 'en')
- Each guideline contains: `id`, `title`, `guideline`, `platform`, `intent`, `scs`, `checks`, etc.

#### WCAG Mapping Templates (`wcag21-mapping.rst`)
- `wcag_mapping`: List of WCAG success criteria
- Each SC contains: `sc`, `title`, `level`, `url`, `guidelines`

#### Check Templates
- `check`: Check object with `id`, `check`, `target`, `platform`, `severity`
- `implementations`: Implementation details (if available)
- `conditions`: Test conditions (if available)

### Custom Filters

Templates can use the built-in `make_heading` filter:

```jinja2
{{ "My Heading"|make_heading(level, css_class) }}
```

**Parameters:**
- `level`: Heading level (1-6)
- `css_class`: Optional CSS class name

**Example:**
```jinja2
{{ "Important Section"|make_heading(2, 'important') }}
```

Generates:
```rst
.. rst-class:: important

Important Section
=================
```

### Multibyte Character Support

The `make_heading` filter automatically handles multibyte characters (Japanese, Chinese, Korean) correctly:

```jinja2
{{ "アクセシビリティ"|make_heading(1) }}
```

Generates proper RST with correct underline length:
```rst
##################
アクセシビリティ
##################
```

## Testing Template Changes

### 1. Validate Template Syntax

```bash
# Test template loading
python -c "
from yaml2rst.template_manager import TemplateManager
from yaml2rst.template_config import TemplateConfig

config = TemplateConfig()
manager = TemplateManager.from_config(config)
template = manager.load('gl-category.rst')
print('Template loaded successfully')
"
```

### 2. Generate Test Output

```bash
# Generate with custom templates
python -m yaml2rst --template-dir ./test-templates/ --lang ja

# Check the generated files
ls -la ja/source/categories/
```

### 3. Compare Output

```bash
# Generate with built-in templates
python -m yaml2rst --lang ja
mv ja/source/categories/form.rst form_builtin.rst

# Generate with custom templates
python -m yaml2rst --template-dir ./custom-templates/ --lang ja
mv ja/source/categories/form.rst form_custom.rst

# Compare the differences
diff form_builtin.rst form_custom.rst
```

## Troubleshooting

### Template Not Found

**Error:** `TemplateNotFound: template_name.rst`

**Solutions:**
1. Check that the template file exists in your custom directory
2. Verify the file name matches exactly (case-sensitive)
3. Ensure `fallback_to_builtin = true` in your configuration

### Template Syntax Errors

**Error:** `TemplateSyntaxError: ...`

**Solutions:**
1. Validate Jinja2 syntax in your template
2. Check for unmatched `{% %}` blocks
3. Ensure proper variable names and filters

### Configuration Not Loading

**Error:** Templates not being customized despite configuration

**Solutions:**
1. Check configuration file location: `~/.config/freee_a11y_gl/yaml2rst.conf`
2. Verify INI file syntax
3. Check environment variable names (must start with `YAML2RST_`)
4. Use absolute paths in configuration

### Permission Issues

**Error:** `PermissionError: [Errno 13] Permission denied`

**Solutions:**
1. Check directory permissions: `chmod 755 ~/.config/freee_a11y_gl/templates/`
2. Check file permissions: `chmod 644 ~/.config/freee_a11y_gl/templates/*.rst`
3. Ensure the user has read access to template files

## Best Practices

### 1. Version Control

Keep your custom templates in version control:

```bash
cd ~/.config/freee_a11y_gl/
git init
git add templates/ yaml2rst.conf
git commit -m "Initial template customization"
```

### 2. Template Organization

Organize templates by purpose:

```
~/.config/freee_a11y_gl/templates/
├── categories/
│   └── gl-category.rst
├── references/
│   ├── wcag21-mapping.rst
│   └── axe-rules.rst
├── checks/
│   ├── implementation.rst
│   └── procedure.rst
└── faq/
    └── article.rst
```

### 3. Incremental Customization

Start with small changes:

1. Copy the original template
2. Make minimal modifications
3. Test thoroughly
4. Gradually add more customizations

### 4. Documentation

Document your customizations:

```jinja2
{# 
Custom category template for Project XYZ
Modified: 2024-01-15
Changes:
- Added emoji icons for better visual hierarchy
- Enhanced WCAG mapping section
- Custom CSS classes for styling
#}
```

### 5. Backup Strategy

Keep backups of working templates:

```bash
# Create backup before major changes
cp -r ~/.config/freee_a11y_gl/templates/ ~/.config/freee_a11y_gl/templates.backup.$(date +%Y%m%d)
```

## Advanced Usage

### Custom Template Loaders

For advanced use cases, you can create custom template loaders:

```python
from yaml2rst.template_config import TemplateConfig
from yaml2rst.template_manager import TemplateManager

# Custom configuration
config = TemplateConfig()
config.custom_template_dir = "/path/to/project/templates"
config.user_template_dir = "/path/to/user/templates"
config.fallback_to_builtin = True

# Create manager with custom config
manager = TemplateManager.from_config(config)
```

### Template Inheritance

Use Jinja2 template inheritance for complex customizations:

**Base template** (`base.rst`):
```jinja2
{# Base template with common structure #}
{{ title|make_heading(1) }}

{% block content %}
{# Content will be provided by child templates #}
{% endblock %}

{% block footer %}
.. note:: Generated by yaml2rst
{% endblock %}
```

**Child template** (`gl-category.rst`):
```jinja2
{% extends "base.rst" %}

{% block content %}
{% for gl in guidelines %}
{{ gl.title|make_heading(2) }}
{{ gl.guideline }}
{% endfor %}
{% endblock %}
```

## Migration Guide

### From Built-in to Custom Templates

1. **Export all built-in templates:**
   ```bash
   # Export to default user directory
   yaml2rst --export-templates
   ```

2. **Verify exported templates:**
   ```bash
   ls -la ~/.config/freee_a11y_gl/templates/
   ```

3. **Test the migration:**
   ```bash
   yaml2rst --lang ja --basedir /path/to/data
   ```

### Alternative: Manual Template Setup

If you prefer manual setup:

1. **Create user template directory:**
   ```bash
   mkdir -p ~/.config/freee_a11y_gl/templates
   ```

2. **Create configuration file:**
   ```bash
   cat > ~/.config/freee_a11y_gl/yaml2rst.conf << EOF
   [templates]
   user_template_dir = ~/.config/freee_a11y_gl/templates
   fallback_to_builtin = true
   EOF
   ```

3. **Copy specific templates manually:**
   ```bash
   # Copy only the templates you want to customize
   cp /path/to/yaml2rst/src/yaml2rst/templates/gl-category.rst ~/.config/freee_a11y_gl/templates/
   ```

### Updating Custom Templates

When yaml2rst is updated, you may need to update your custom templates:

1. **Check for template changes:**
   ```bash
   diff ~/.config/freee_a11y_gl/templates/gl-category.rst /path/to/new/yaml2rst/templates/gl-category.rst
   ```

2. **Merge changes carefully:**
   - Keep your customizations
   - Add new variables or blocks from the updated template
   - Test thoroughly after merging

## Support and Resources

### Getting Help

1. **Check template resolution:**
   ```python
   from yaml2rst.template_config import TemplateConfig
   config = TemplateConfig()
   paths = config.get_template_search_paths()
   print("Template search paths:", paths)
   ```

2. **Validate configuration:**
   ```python
   from yaml2rst.template_config import TemplateConfig
   config = TemplateConfig()
   loaded = config.load_config()
   print("Loaded configuration:", loaded)
   ```

3. **List available templates:**
   ```python
   from yaml2rst.template_resolver import TemplateResolver
   from yaml2rst.template_config import TemplateConfig
   
   resolver = TemplateResolver(TemplateConfig())
   templates = resolver.list_available_templates()
   print("Available templates:", templates)
   ```

### Community Templates

Consider sharing useful template customizations with the community by contributing them to the project repository.

---

For more information about yaml2rst, see the main documentation and source code repository.
