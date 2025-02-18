"""Package for specific content generators."""
from .category_generator import CategoryGenerator
from .check_generator import AllChecksGenerator, CheckExampleGenerator
from .faq_generator import (
    FaqArticleGenerator,
    FaqTagPageGenerator,
    FaqIndexGenerator,
    FaqTagIndexGenerator,
    FaqArticleIndexGenerator
)
from .reference_generator import (
    WcagMappingGenerator,
    PriorityDiffGenerator,
    MiscDefinitionsGenerator,
    InfoToGuidelinesGenerator,
    InfoToFaqsGenerator,
    AxeRulesGenerator
)
from .makefile_generator import MakefileGenerator

__all__ = [
    'CategoryGenerator',
    'AllChecksGenerator',
    'CheckExampleGenerator',
    'FaqArticleGenerator',
    'FaqTagPageGenerator',
    'FaqIndexGenerator',
    'FaqTagIndexGenerator',
    'FaqArticleIndexGenerator',
    'WcagMappingGenerator',
    'PriorityDiffGenerator',
    'MiscDefinitionsGenerator',
    'InfoToGuidelinesGenerator',
    'InfoToFaqsGenerator',
    'AxeRulesGenerator',
    'MakefileGenerator'
]
