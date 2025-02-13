"""Generators for reference content like WCAG mappings and misc definitions."""
from typing import Dict, Any, Iterator

from a11y_guidelines import WcagSc, InfoRef, RelationshipManager
from ..base_generator import BaseGenerator

class WcagMappingGenerator(BaseGenerator):
    """Generates WCAG 2.1 mapping pages."""

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate WCAG mapping data.
        
        Yields:
            Dictionary containing WCAG success criteria mappings
        """
        rel = RelationshipManager()
        mappings = []
        for sc in WcagSc.get_all().values():
            sc_object = sc.template_data()
            guidelines = rel.get_sc_to_guidelines(sc)
            if len(guidelines) > 0:
                sc_object['guidelines'] = [guideline.get_category_and_id(self.lang) for guideline in guidelines]
            mappings.append(sc_object)
        yield {'mapping': mappings}

    def get_dependencies(self) -> list[str]:
        return [sc.src_path for sc in WcagSc.get_all().values()]

class PriorityDiffGenerator(BaseGenerator):
    """Generates priority difference pages."""

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate priority difference data.
        
        Yields:
            Dictionary containing differences between WCAG levels and local priorities
        """
        diffs = [sc.template_data() for sc in WcagSc.get_all().values() if sc.level != sc.local_priority]
        yield {'diffs': diffs}

    def get_dependencies(self) -> list[str]:
        return [sc.src_path for sc in WcagSc.get_all().values()]

class MiscDefinitionsGenerator(BaseGenerator):
    """Generates miscellaneous definitions pages."""

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate miscellaneous definitions data.
        
        Yields:
            Dictionary containing external reference links and definitions
        """
        data = []
        for info in InfoRef.list_all_external():
            data.append({
                'label': info.refstring(),
                'text': info.text[self.lang],
                'url': info.url[self.lang]
            })
        yield {'links': data}

    def get_dependencies(self) -> list[str]:
        return [info.src_path for info in InfoRef.list_all_external()]
