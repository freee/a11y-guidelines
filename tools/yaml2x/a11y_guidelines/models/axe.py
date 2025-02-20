"""Models for axe-core accessibility testing tool."""
import re
from typing import Dict, List, Optional, Any, ClassVar
from dataclasses import dataclass
from .base import BaseModel, RelationshipManager

@dataclass
class AxeMessage:
    """Container for axe-core message translations."""
    help: Dict[str, str]
    description: Dict[str, str]

class AxeRule(BaseModel):
    """axe-core rule model."""

    object_type = "axe_rule"
    _instances: Dict[str, 'AxeRule'] = {}
    
    # Class-level metadata
    timestamp: Optional[str] = None
    version: Optional[str] = None
    major_version: Optional[str] = None
    deque_url: Optional[str] = None

    def __init__(self, rule: Dict[str, Any], messages_ja: Dict[str, Any]):
        """Initialize axe rule.
        
        Args:
            rule: Dictionary containing rule data
            messages_ja: Dictionary containing Japanese translations
        """
        super().__init__(rule['id'])

        if self.id in self._instances:
            raise ValueError(f'Duplicate rule ID: {self.id}')

        # Set message data
        if self.id not in messages_ja['rules']:
            msg_ja = {
                'help': rule['metadata']['help'],
                'description': rule['metadata']['description']
            }
            self.translated = False
        else:
            msg_ja = messages_ja['rules'][self.id]
            self.translated = True

        self.message = AxeMessage(
            help={
                'en': rule['metadata']['help'],
                'ja': msg_ja['help']
            },
            description={
                'en': rule['metadata']['description'],
                'ja': msg_ja['description']
            }
        )

        # Set relationships
        self.has_wcag_sc = False
        self.has_guideline = False
        rel = RelationshipManager()

        # Find and associate WCAG success criteria
        wcag_scs = [
            tag2sc(tag)
            for tag in rule['tags']
            if re.match(r'wcag\d{3,}', tag)
        ]

        for sc in wcag_scs:
            from .reference import WcagSc
            if sc not in WcagSc._instances:
                continue
            rel.associate_objects(self, WcagSc.get_by_id(sc))
            self.has_wcag_sc = True
            for guideline in rel.get_related_objects(WcagSc.get_by_id(sc), 'guideline'):
                rel.associate_objects(self, guideline)
                self.has_guideline = True

        AxeRule._instances[self.id] = self

    def template_data(self, lang: str) -> Dict[str, Any]:
        """Get template data for axe rule.
        
        Args:
            lang: Language code
            
        Returns:
            Dictionary with template data
        """
        rel = RelationshipManager()
        data = {
            'id': self.id,
            'help': self.message.help,
            'description': self.message.description
        }

        if self.translated:
            data['translated'] = True

        if self.has_wcag_sc:
            from .reference import WcagSc
            scs = sorted(
                rel.get_related_objects(self, 'wcag_sc'),
                key=lambda x: x.sort_key
            )
            data['scs'] = [sc.template_data() for sc in scs]

        if self.has_guideline:
            guidelines = sorted(
                rel.get_related_objects(self, 'guideline'),
                key=lambda x: x.sort_key
            )
            data['guidelines'] = [
                gl.get_category_and_id(lang)
                for gl in guidelines
            ]

        return data

    @classmethod
    def list_all(cls) -> List['AxeRule']:
        """Get all axe rules sorted by relevance and ID."""
        sorted_all_rules = sorted(cls._instances, key=lambda x: cls._instances[x].id)
        with_guidelines = []
        with_sc = []
        without_sc = []

        for rule_id in sorted_all_rules:
            rule = cls._instances[rule_id]
            if rule.has_guideline:
                with_guidelines.append(rule)
            elif rule.has_wcag_sc:
                with_sc.append(rule)
            else:
                without_sc.append(rule)

        return with_guidelines + with_sc + without_sc

def tag2sc(tag: str) -> str:
    """Convert axe-core tag to WCAG SC identifier.
    
    Args:
        tag: axe-core tag (e.g., 'wcag111')
        
    Returns:
        WCAG SC identifier (e.g., '1.1.1')
    """
    return re.sub(r'wcag(\d)(\d)(\d+)', r'\1.\2.\3', tag)
