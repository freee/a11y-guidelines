"""Generators for miscellaneous definitions and reference content."""
from typing import Dict, Any, List

from freee_a11y_gl import InfoRef, AxeRule
from freee_a11y_gl.relationship_manager import RelationshipManager
from ..common_generators import SingleFileGenerator, ListBasedGenerator

class InfoToGuidelinesGenerator(ListBasedGenerator[InfoRef]):
    """Generates guideline reference pages from info."""

    def __init__(self, lang: str):
        super().__init__(lang)
        self.relationship_manager = RelationshipManager()

    def get_items(self) -> List[InfoRef]:
        """Get all internal infos that have guidelines."""
        return [info for info in InfoRef.list_has_guidelines() if info.internal]

    def process_item(self, info: InfoRef) -> Dict[str, Any]:
        """Process a single info reference."""
        guidelines = [
            guideline.get_category_and_id(self.lang) 
            for guideline in self.relationship_manager.get_sorted_related_objects(info, 'guideline')
        ]
        return {
            'filename': info.ref,
            'guidelines': guidelines
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate guideline reference data."""
        required_fields = ['filename', 'guidelines']
        if not all(field in data for field in required_fields):
            return False
        return isinstance(data['guidelines'], list)

    def get_dependencies(self) -> list[str]:
        """Get file dependencies."""
        return [info.src_path for info in InfoRef.list_has_guidelines()]

class InfoToFaqsGenerator(ListBasedGenerator[InfoRef]):
    """Generates FAQ reference pages from info."""

    def __init__(self, lang: str):
        super().__init__(lang)
        self.relationship_manager = RelationshipManager()

    def get_items(self) -> List[InfoRef]:
        """Get all internal infos that have FAQs."""
        return [info for info in InfoRef.list_has_faqs() if info.internal]

    def process_item(self, info: InfoRef) -> Dict[str, Any]:
        """Process a single info reference."""
        faqs = [
            faq.id
            for faq in self.relationship_manager.get_sorted_related_objects(info, 'faq', key='sort_key')
        ]
        return {
            'filename': info.ref,
            'faqs': faqs
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate FAQ reference data."""
        required_fields = ['filename', 'faqs']
        if not all(field in data for field in required_fields):
            return False
        return isinstance(data['faqs'], list)

    def get_dependencies(self) -> list[str]:
        """Get file dependencies."""
        return [info.src_path for info in InfoRef.list_has_faqs()]

class AxeRulesGenerator(SingleFileGenerator):
    """Generates axe rules documentation."""

    def get_template_data(self) -> Dict[str, Any]:
        """Generate axe rules data."""
        return {
            'version': AxeRule.version,
            'major_version': AxeRule.major_version,
            'deque_url': AxeRule.deque_url,
            'timestamp': AxeRule.timestamp,
            'rules': [rule.template_data(self.lang) for rule in AxeRule.list_all()]
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate axe rules data."""
        required_fields = ['version', 'major_version', 'deque_url', 'timestamp', 'rules']
        if not all(field in data for field in required_fields):
            return False
        return isinstance(data['rules'], list)

    def get_dependencies(self) -> list[str]:
        """Get file dependencies."""
        return [rule.src_path for rule in AxeRule.list_all()]

class MiscDefinitionsGenerator(SingleFileGenerator):
    """Generates miscellaneous definitions pages."""

    def get_template_data(self) -> Dict[str, Any]:
        """Generate miscellaneous definitions data."""
        data = []
        for info in InfoRef.list_all_external():
            data.append({
                'label': info.refstring(),
                'text': info.link_data()['text'][self.lang],
                'url': info.link_data()['url'][self.lang]
            })
        return {'links': data}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate miscellaneous definitions data."""
        if not isinstance(data, dict) or 'links' not in data:
            return False
            
        links = data['links']
        if not isinstance(links, list):
            return False
            
        for link in links:
            required_fields = ['label', 'text', 'url']
            if not all(field in link for field in required_fields):
                return False
                
        return True

    def get_dependencies(self) -> list[str]:
        """Get file dependencies."""
        return [info.src_path for info in InfoRef.list_all_external()]
