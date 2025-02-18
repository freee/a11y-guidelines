"""Generators for reference content like WCAG mappings and misc definitions."""
from typing import Dict, Any, Iterator

from a11y_guidelines import WcagSc, InfoRef, RelationshipManager, AxeRule
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

class InfoToGuidelinesGenerator(BaseGenerator):
    """Generates guideline reference pages from info."""

    def generate(self) -> Iterator[Dict[str, Any]]:
        rel = RelationshipManager()
        for info in InfoRef.list_has_guidelines():
            if not info.internal:
                continue
            sorted_guidelines = sorted(
                rel.get_info_to_guidelines(info),
                key=lambda item: item.sort_key
            )
            guidelines = [guideline.get_category_and_id(self.lang) 
                         for guideline in sorted_guidelines]
            yield {
                'filename': info.ref,
                'guidelines': guidelines
            }

    def get_dependencies(self) -> list[str]:
        return [info.src_path for info in InfoRef.list_has_guidelines()]

class InfoToFaqsGenerator(BaseGenerator):
    """Generates FAQ reference pages from info."""

    def generate(self) -> Iterator[Dict[str, Any]]:
        rel = RelationshipManager()
        for info in InfoRef.list_has_faqs():
            if not info.internal:
                continue
            faqs = [faq.id for faq in rel.get_info_to_faqs(info)]
            yield {
                'filename': info.ref,
                'faqs': faqs
            }

    def get_dependencies(self) -> list[str]:
        return [info.src_path for info in InfoRef.list_has_faqs()]

class AxeRulesGenerator(BaseGenerator):
    """Generates axe rules documentation."""

    def generate(self) -> Iterator[Dict[str, Any]]:
        yield {
            'version': AxeRule.version,
            'major_version': AxeRule.major_version,
            'deque_url': AxeRule.deque_url,
            'timestamp': AxeRule.timestamp,
            'rules': [rule.template_data(self.lang) for rule in AxeRule.list_all()]
        }

    def get_dependencies(self) -> list[str]:
        return [rule.src_path for rule in AxeRule.list_all()]
