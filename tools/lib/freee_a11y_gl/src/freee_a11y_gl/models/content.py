"""Content models for a11y-guidelines."""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from .base import BaseModel
from ..relationship_manager import RelationshipManager
from ..config import Config
from ..utils import uniq

@dataclass
class GuidelineData:
    """Container for guideline localized data."""
    title: Dict[str, str]
    platform: List[str]
    guideline: Dict[str, str]
    intent: Dict[str, str]

class Category(BaseModel):
    """Category model representing groupings of guidelines."""

    object_type = "category"
    _instances: Dict[str, 'Category'] = {}

    def __init__(self, category_id: str, names: Dict[str, str]):
        """Initialize category.
        
        Args:
            category_id: Unique category identifier
            names: Dictionary of localized names (lang code -> name)
        """
        super().__init__(category_id)
        self.names = names
        Category._instances[category_id] = self

    def get_name(self, lang: str) -> str:
        """Get localized name for category.
        
        Args:
            lang: Language code
            
        Returns:
            Localized name, falls back to Japanese if language not found
        """
        return self.names.get(lang, self.names['ja'])

    def get_dependency(self) -> List[str]:
        """Get list of file dependencies for this category.
        
        Returns:
            List of file paths that this category depends on
        """
        rel = RelationshipManager()
        dependency = []
        for guideline in rel.get_sorted_related_objects(self, 'guideline'):
            dependency.append(guideline.src_path)
            # Add check dependencies
            dependency.extend([check.src_path for check in rel.get_related_objects(guideline, 'check')])
            # Add FAQ dependencies
            dependency.extend([faq.src_path for faq in rel.get_related_objects(guideline, 'faq')])
        return uniq(dependency)  # Remove duplicates while preserving order

    @classmethod
    def list_all(cls) -> List['Category']:
        """Get all category instances.
        
        Returns:
            List of all category instances
        """
        return list(cls._instances.values())

class Guideline(BaseModel):
    """Guideline model representing accessibility guidelines."""

    object_type = "guideline"
    _instances: Dict[str, 'Guideline'] = {}

    def __init__(self, gl: Dict[str, Any]):
        """Initialize guideline.
        
        Args:
            gl: Dictionary containing guideline data
        """
        super().__init__(gl['id'])

        if self.id in self._instances:
            raise ValueError(f'Duplicate guideline ID: {self.id}')
        
        self.sort_key = gl['sortKey']
        if self.sort_key in [g.sort_key for g in self._instances.values()]:
            raise ValueError(f'Duplicate guideline sortKey: {self.sort_key}')

        # Store guideline data
        self.data = GuidelineData(
            title=gl['title'],
            platform=gl['platform'],
            guideline=gl['guideline'],
            intent=gl['intent']
        )
        self.src_path = gl['src_path']

        # Set up relationships
        rel = RelationshipManager()
        if not Category.get_by_id(gl['category']):
            raise ValueError(f'Category ID {gl["category"]} referenced in guideline {self.id} does not exist.')
        rel.associate_objects(self, Category.get_by_id(gl['category']))
        
        # Associate checks
        for check_id in gl.get('checks', []):
            from .check import Check  # Import here to avoid circular imports
            if not Check.get_by_id(check_id):
                raise ValueError(f'Check ID {check_id} referenced in guideline {self.id} does not exist.')
            rel.associate_objects(self, Check.get_by_id(check_id))

        # Associate WCAG success criteria
        for sc in gl.get('sc', []):
            from .reference import WcagSc  # Import here to avoid circular imports
            if not WcagSc.get_by_id(sc):
                raise ValueError(f'Success criterion ID {sc} referenced in guideline {self.id} does not exist.')
            rel.associate_objects(self, WcagSc.get_by_id(sc))

        # Associate info references
        if 'info' in gl:
            for info in gl['info']:
                from .reference import InfoRef  # Import here to avoid circular imports
                info_ref = InfoRef(info)
                rel.associate_objects(self, info_ref)
                for check in rel.get_related_objects(self, 'check'):
                    rel.associate_objects(check, info_ref)

        Guideline._instances[self.id] = self

    def get_category_and_id(self, lang: str) -> Dict[str, str]:
        """Get category name and guideline ID.
        
        Args:
            lang: Language code
            
        Returns:
            Dictionary with category name and guideline ID
        """
        rel = RelationshipManager()
        category = rel.get_related_objects(self, 'category')[0]
        return {
            'category': category.get_name(lang),
            'guideline': self.id
        }

    def link_data(self, baseurl: str = '') -> Dict[str, Dict[str, str]]:
        """Get link data for guideline.
        
        Args:
            baseurl: Base URL for links
            
        Returns:
            Dictionary with localized text and URLs
        """
        data = {
            'text': {},
            'url': {}
        }
        rel = RelationshipManager()
        category = rel.get_related_objects(self, 'category')[0]

        for lang in self.data.title.keys():
            separator_char = Config.get_text_separator(lang)
            basedir = Config.get_guidelines_path()
            base_url = Config.get_base_url(lang)
            data['text'][lang] = f'{category.get_name(lang)}{separator_char}{self.data.title[lang]}'
            data['url'][lang] = f'{baseurl or base_url}{basedir}{category.id}.html#{self.id}'
        return data

    def template_data(self, lang: str) -> Dict[str, Any]:
        """Get template data for guideline.
        
        Args:
            lang: Language code
            
        Returns:
            Dictionary with guideline data formatted for templates
        """
        rel = RelationshipManager()
        data = {
            'id': self.id,
            'title': self.data.title[lang],
            'platform': self.join_items(self.data.platform, lang),
            'guideline': self.data.guideline[lang],
            'intent': self.data.intent[lang],
            'category': rel.get_related_objects(self, 'category')[0].names[lang],
        }

        # Add checks data
        data['checks'] = [
            check.template_data(lang, platform=self.data.platform)
            for check in rel.get_sorted_related_objects(self, 'check', key='id')
        ]

        # Add success criteria data
        data['scs'] = [
            sc.template_data()
            for sc in rel.get_sorted_related_objects(self, 'wcag_sc')
        ]

        # Add FAQ data if present
        faqs = rel.get_sorted_related_objects(self, 'faq')
        if faqs:
            data['faqs'] = [faq.id for faq in faqs]

        # Add info references if present
        info = rel.get_related_objects(self, 'info_ref')
        if info:
            data['info'] = [inforef.refstring() for inforef in info]

        return data

    @staticmethod
    def join_items(items: List[str], lang: str) -> str:
        """Join platform items with localized separator.
        
        Args:
            items: List of platform items
            lang: Language code
            
        Returns:
            Joined string with localized separator
        """
        separator = Config.get_list_separator(lang)
        platform_names = [
            Config.get_platform_name(item, lang)
            for item in items
        ]
        return separator.join(platform_names)

    @classmethod
    def list_all_src_paths(cls) -> List[str]:
        """Get all guideline source paths.
        
        Returns:
            List of source file paths
        """
        return [guideline.src_path for guideline in cls._instances.values()]
