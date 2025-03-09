"""Generators for WCAG content."""
from typing import Dict, Any, List

from freee_a11y_gl import WcagSc, InfoRef, AxeRule
from freee_a11y_gl.relationship_manager import RelationshipManager
from ..base_generator import BaseGenerator
from ..common_generators import SingleFileGenerator

class WcagGeneratorBase(BaseGenerator):
    """Base class for WCAG-related generators."""
    
    def __init__(self, lang: str):
        super().__init__(lang)
        self.relationship_manager = RelationshipManager()

    def get_dependencies(self) -> list[str]:
        """Get WCAG SC file dependencies."""
        return [sc.src_path for sc in WcagSc.get_all().values()]

    def get_guidelines_for_sc(self, sc: WcagSc) -> List[Any]:
        """Get guidelines for a success criterion."""
        return [
            guideline.get_category_and_id(self.lang)
            for guideline in self.relationship_manager.get_sc_to_guidelines(sc)
        ]

class WcagMappingGenerator(SingleFileGenerator, WcagGeneratorBase):
    """Generates WCAG mapping pages."""

    def get_template_data(self) -> Dict[str, Any]:
        """Generate WCAG mapping data."""
        mappings = []
        for sc in WcagSc.get_all().values():
            sc_object = sc.template_data()
            guidelines = self.get_guidelines_for_sc(sc)
            if guidelines:
                sc_object['guidelines'] = guidelines
            mappings.append(sc_object)
        return {'mapping': mappings}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate mapping data."""
        return 'mapping' in data and isinstance(data['mapping'], list)

class PriorityDiffGenerator(SingleFileGenerator, WcagGeneratorBase):
    """Generates priority difference pages."""

    def get_template_data(self) -> Dict[str, Any]:
        """Generate priority difference data."""
        diffs = [
            sc.template_data() 
            for sc in WcagSc.get_all().values() 
            if sc.level != sc.local_priority
        ]
        return {'diffs': diffs}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate priority difference data."""
        return 'diffs' in data and isinstance(data['diffs'], list)
