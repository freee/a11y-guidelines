# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **freee Accessibility Guidelines** repository - a comprehensive documentation project for web and mobile accessibility guidelines. The project generates multi-language (Japanese/English) HTML documentation using Sphinx, with content sourced from YAML files and converted to reStructuredText.

**Main branch:** `develop`

**Published documentation:** https://a11y-guidelines.freee.co.jp/

## Core Architecture

### Build System

The project uses a **two-stage build process**:

1. **YAML → RST conversion** (`yaml2rst` tool)
   - Converts YAML guideline/check/FAQ data to reStructuredText
   - Generates category pages, reference tables, and cross-references
   - Runs before Sphinx build

2. **RST → HTML generation** (Sphinx)
   - Builds Japanese docs in `ja/` directory
   - Builds English docs in `en/` directory
   - Supports both multi-page HTML and single-page HTML output

### Data Structure

```
data/
├── json/
│   ├── guideline-categories.json    # Category definitions
│   ├── wcag-sc.json                  # WCAG success criteria mapping
│   ├── faq-tags.json                 # FAQ tag definitions
│   ├── info.json                     # Reference link definitions
│   └── schemas/                      # JSON schemas for validation
│       ├── guideline.json
│       ├── check.json
│       └── faq.json
└── yaml/
    ├── gl/                           # Guidelines by category
    ├── checks/                       # Accessibility checks
    └── faq/                          # FAQ articles
```

### Custom Python Libraries

**`tools/lib/freee_a11y_gl`** - Core library for accessibility guideline management
- Models: Category, Guideline, Check, FAQ, WCAG mappings
- YAML processing and validation
- Relationship management between entities
- Multi-language support

**`tools/scripts/yaml2rst`** - RST content generator
- Template-based content generation using Jinja2
- Converts YAML data to Sphinx-compatible RST files
- Generates category pages, indexes, and cross-references

## Common Commands

### Building Documentation

```bash
# Build both Japanese and English HTML
make html

# Build specific language
cd ja && make html
cd en && make html

# Build single-page HTML (singlehtml)
make singlehtml

# Clean build artifacts
make clean

# Check that all include files are referenced
make check-includes
```

### Testing and Validation

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
npm install

# Run Python tests (yaml2rst)
cd tools/scripts/yaml2rst
python run_tests.py
python run_tests.py --coverage

# Run Python tests (freee_a11y_gl)
cd tools/lib/freee_a11y_gl
python -m pytest tests/

# Validate YAML against JSON schemas
ajv validate --spec=draft2020 -s data/json/schemas/guideline.json -r data/json/schemas/common.json -d data/yaml/gl/form/label.yaml

# Lint reStructuredText files
sphinx-lint --enable all --disable line-too-long ja/**/*.rst

# Lint Japanese text (textlint)
npx textlint ja/source/**/*.rst

# Code quality (Python)
black tools/
isort tools/
flake8 tools/
mypy tools/
```

### Development Workflow

The build process for each language (ja/en) follows:

1. `yaml2rst` generates RST files from YAML data into `source/inc/` and `source/faq/`
2. `incfiles.mk` tracks dependencies
3. Sphinx builds HTML from RST sources in `source/` directory
4. Output goes to `build/html/` (or `build/singlehtml/`)

### Working with Guidelines

Each guideline YAML file structure:
```yaml
id: gl-category-name          # Unique ID with gl- prefix
sortKey: 1901                  # Integer 1001-2199 for ordering
category: form                 # Category identifier
title:
  ja: "日本語タイトル"
  en: "English Title"
platform:
  - web                        # web and/or mobile
  - mobile
guideline:
  ja: "ガイドライン本文"
  en: "Guideline text"
sc:                            # WCAG success criteria
  - 1.1.1
  - 1.3.1
intent:
  ja: "意図の説明"
  en: "Intent explanation"
checks:                        # Related check IDs
  - '0931'
info:                          # Related info links
  - exp-form-labeling
```

### Pre-commit Hooks

The repository uses **Husky + lint-staged** for pre-commit validation:
- JSON schema validation for YAML files
- Sphinx linting for RST files
- Runs automatically on `git commit`

Configuration in `.lintstagedrc.mjs`

## Version Management

Version information is stored in `version.py`:
- `guidelines_version` - Main version (e.g., 'Ver. 202508.0')
- `checksheet_version` - Checksheet version
- `publishedDate` - Publication date

This file is imported by Sphinx configuration to set document version.

## Internationalization

The project supports **Japanese (ja)** and **English (en)**:

- Both languages share the same data structure
- YAML files contain i18n strings with `ja:` and `en:` keys
- Template directory symlink: `en/source/_templates → ja/source/_templates`
- Each language has its own Sphinx `conf.py` with locale settings

## Build Environment Notes

- **Locale required:** `ja_JP.UTF-8` must be installed for Japanese date formatting
- **Python version:** 3.9+ (see requirements)
- **Sphinx:** ~7.0 (specified in requirements.txt)
- **Theme:** sphinx_rtd_theme ~3.0

## GitHub Actions

The repository uses reusable workflows for building:
- `.github/workflows/reusable-build-doc.yml` - Main build workflow
- Builds for specific tags/versions with configurable Python/Sphinx/theme versions
- Supports artifact reuse to avoid rebuilding unchanged content
- Environment variables: `BASE_URL`, `GTM_ID`, build flags

## Common Tasks

**Adding a new guideline:**
1. Create YAML file in appropriate `data/yaml/gl/{category}/` directory
2. Follow the guideline schema (see `data/json/schemas/guideline.json`)
3. Run `make clean` and `make html` to rebuild
4. Validate with `ajv validate` command

**Modifying templates:**
1. Templates are in `yaml2rst` package (Jinja2 format)
2. Export with: `yaml2rst --export-templates`
3. Customize in `~/.config/freee_a11y_gl/templates/`
4. Template resolution: custom → user → built-in

**Testing a single component:**
```bash
# Test yaml2rst
cd tools/scripts/yaml2rst
pytest tests/unit/test_specific.py -v

# Test freee_a11y_gl
cd tools/lib/freee_a11y_gl
pytest tests/ -k "test_name"
```
