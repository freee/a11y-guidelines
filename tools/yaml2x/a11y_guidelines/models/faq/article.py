"""FAQ article model."""
import datetime
from typing import Dict, List, Any, Optional, ClassVar
from ..base import BaseModel, RelationshipManager

class Faq(BaseModel):
    """FAQ article model."""

    object_type = "faq"
    _instances: Dict[str, 'Faq'] = {}

    def __init__(self, faq: Dict[str, Any]):
        """Initialize FAQ article.
        
        Args:
            faq: Dictionary containing FAQ data
        """
        super().__init__(faq['id'])
        if self.id in self._instances:
            raise ValueError(f'Duplicate FAQ ID: {self.id}')
        
        self.sort_key = faq['sortKey']
        if self.sort_key in [f.sort_key for f in self._instances.values()]:
            raise ValueError(f'Duplicate FAQ sortKey: {self.sort_key}')

        self.src_path = faq['src_path']
        self.updated = datetime.datetime.fromisoformat(faq['updated'])
        
        # Store localized content
        self.title = faq['title']
        self.problem = faq['problem']
        self.solution = faq['solution']
        self.explanation = faq['explanation']

        self._create_relationships(faq)
        Faq._instances[self.id] = self

    def _create_relationships(self, faq: Dict[str, Any]) -> None:
        """Create relationships with other objects."""
        rel = RelationshipManager()

        # Associate tags
        from .tag import FaqTag
        for tag_id in faq['tags']:
            rel.associate_objects(self, FaqTag.get_by_id(tag_id))

        # Associate guidelines if present
        if 'guidelines' in faq:
            from ..content import Guideline
            for gl_id in faq['guidelines']:
                rel.associate_objects(self, Guideline.get_by_id(gl_id))

        # Associate checks if present
        if 'checks' in faq:
            from ..check import Check
            for check_id in faq['checks']:
                rel.associate_objects(self, Check.get_by_id(check_id))

        # Associate info references if present
        if 'info' in faq:
            from ..reference import InfoRef
            for info in faq['info']:
                rel.associate_objects(self, InfoRef(info))

        # Add unresolved FAQ relationships
        if 'faqs' in faq:
            for related_faq in faq['faqs']:
                rel.add_unresolved_faqs(self.id, related_faq)

    def get_dependency(self) -> List[str]:
        """Get file dependencies for this FAQ."""
        rel = RelationshipManager()
        dependency = [self.src_path]
        
        guidelines = rel.get_related_objects(self, 'guideline')
        if guidelines:
            dependency.extend(gl.src_path for gl in guidelines)

        checks = rel.get_related_objects(self, 'check')
        if checks:
            dependency.extend(check.src_path for check in checks)

        return list(dict.fromkeys(dependency))

    def link_data(self, baseurl: str = '') -> Dict[str, Dict[str, str]]:
        """Get link data for FAQ.
        
        Args:
            baseurl: Optional base URL prefix
            
        Returns:
            Dictionary with localized text and URLs
        """
        basedir = {
            'ja': '/faq/articles/',
            'en': '/en/faq/articles/'
        }
        data = {
            'text': {},
            'url': {}
        }
        for lang in self.title.keys():
            data['text'][lang] = self.title[lang]
            data['url'][lang] = f'{baseurl}{basedir[lang]}{self.id}.html'
        return data

    def template_data(self, lang: str) -> Dict[str, Any]:
        """Get template data for FAQ.
        
        Args:
            lang: Language code
            
        Returns:
            Dictionary containing FAQ data formatted for templates
        """
        rel = RelationshipManager()
        tags = rel.get_related_objects(self, 'faq_tag')
        
        # Format date based on language
        date_format = "%Y年%-m月%-d日" if lang == 'ja' else "%B %-d, %Y"
        formatted_date = self.updated.strftime(date_format)

        data = {
            'id': self.id,
            'title': self.title[lang],
            'problem': self.problem[lang],
            'solution': self.solution[lang],
            'explanation': self.explanation[lang],
            'updated': formatted_date,
            'tags': [tag.get_name(lang) for tag in tags]
        }

        # Add guidelines if present
        guidelines = rel.get_sorted_related_objects(self, 'guideline')
        if guidelines:
            data['guidelines'] = [
                gl.get_category_and_id(lang)
                for gl in guidelines
            ]

        # Add checks if present
        checks = rel.get_sorted_related_objects(self, 'check')
        if checks:
            data['checks'] = [check.template_data(lang) for check in checks]

        # Add info references if present
        info = rel.get_related_objects(self, 'info_ref')
        if info:
            data['info_refs'] = [inforef.refstring() for inforef in info]

        # Add related FAQs if present
        related_faqs = rel.get_sorted_related_objects(self, 'faq')
        if related_faqs:
            data['faqs'] = [faq.id for faq in related_faqs]

        return data

    @classmethod
    def list_all(cls) -> List['Faq']:
        """Get all FAQ instances sorted by sort key."""
        return sorted(cls._instances.values(), key=lambda x: x.sort_key)
