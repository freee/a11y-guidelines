"""Models package for a11y-guidelines.

This package contains models for:
- Base functionality (BaseModel, RelationshipManager)
- Content (Category, Guideline)
- Checks (Check, CheckTool, etc.)
- FAQs (Faq, FaqTag)
- References (WcagSc, InfoRef)
- axe-core integration (AxeRule)
"""
from .base import BaseModel, RelationshipManager
from .content import Category, Guideline
from .check import Check, CheckTool, Condition, Procedure, Implementation, Method
from .faq import Faq, FaqTag
from .reference import WcagSc, InfoRef
from .axe import AxeRule

__all__ = [
    # Base
    'BaseModel',
    'RelationshipManager',
    
    # Content
    'Category',
    'Guideline',
    
    # Checks
    'Check',
    'CheckTool',
    'Condition',
    'Procedure',
    'Implementation',
    'Method',
    
    # FAQs
    'Faq',
    'FaqTag',
    
    # References
    'WcagSc',
    'InfoRef',
    
    # axe-core
    'AxeRule',
]
