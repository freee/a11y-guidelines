"""
freee_a11y_gl - Accessibility Guidelines Library

This package provides a comprehensive framework for managing accessibility guidelines,
checks, and related content. It includes models for categories, guidelines, checks,
FAQ articles, and WCAG success criteria, along with utilities for YAML processing,
validation, and relationship management.

Main components:
- Models: Category, Guideline, Check, Faq, WcagSc, etc.
- YAML processing and validation
- Relationship management between entities
- Configuration and settings management
- Message catalog for internationalization
"""

# Core models
from .models.content import Category, Guideline
from .models.check import Check, CheckTool
from .models.reference import WcagSc, InfoRef
from .models.faq.article import Faq
from .models.faq.tag import FaqTag
from .models.axe import AxeRule
from .relationship_manager import RelationshipManager

# Constants and utilities
from .source import get_src_path
from .initializer import setup_instances
from .info_utils import get_info_links
from .version_utils import get_version_info
from .settings import settings

# Data processing
from .yaml_processor import process_yaml_data

__all__ = [
    # Models
    'Category', 'Check', 'Guideline', 'Faq', 'FaqTag',
    'WcagSc', 'InfoRef', 'AxeRule', 'CheckTool',
    # Managers
    'RelationshipManager',
    # Utils
    'get_src_path', 'setup_instances', 'get_info_links',
    'get_version_info',
    # YAML processing functionality
    'process_yaml_data',
    # Settings
    'settings'
]
