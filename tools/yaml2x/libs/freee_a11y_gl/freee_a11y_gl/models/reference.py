"""Reference models for accessibility standards and citations."""
from typing import Dict, List, Optional, Any, ClassVar
from urllib.parse import quote as url_encode
from dataclasses import dataclass
from .base import BaseModel
from ..relationship_manager import RelationshipManager
import re
from ..config import Config, LanguageCode
from ..utils import tag2sc

@dataclass
class LocalizedReference:
    """Container for localized reference data."""
    title: Dict[str, str]
    url: Dict[str, str]

class WcagSc(BaseModel):
    """Web Content Accessibility Guidelines (WCAG) Success Criteria."""

    object_type = "wcag_sc"
    _instances: Dict[str, 'WcagSc'] = {}

    def __init__(self, sc_id: str, sc: Dict[str, Any]):
        """Initialize WCAG success criterion.
        
        Args:
            sc_id: Success criterion ID
            sc: Dictionary containing SC data
        """
        super().__init__(sc_id)
        self.scnum = sc['id']
        self.sort_key = sc['sortKey']
        self.level = sc['level']
        self.local_priority = sc['localPriority']
        self.data = LocalizedReference(
            title={
                'ja': sc['ja']['title'],
                'en': sc['en']['title']
            },
            url={
                'ja': sc['ja']['url'],
                'en': sc['en']['url']
            }
        )
        WcagSc._instances[sc_id] = self

    def template_data(self) -> Dict[str, Any]:
        """Get template data for success criterion."""
        return {
            'sc': self.scnum,
            'level': self.level,
            'LocalLevel': self.local_priority,
            'sc_en_title': self.data.title['en'],
            'sc_ja_title': self.data.title['ja'],
            'sc_en_url': self.data.url['en'],
            'sc_ja_url': self.data.url['ja']
        }

    @classmethod
    def get_all(cls) -> Dict[str, 'WcagSc']:
        """Get all success criteria, sorted by sort key."""
        sorted_keys = sorted(cls._instances.keys(), key=lambda sc: cls._instances[sc].sort_key)
        return {key: cls.get_by_id(key) for key in sorted_keys}

class InfoRef(BaseModel):
    """Information reference model for both internal and external references."""

    object_type = "info_ref"
    _instances: Dict[str, 'InfoRef'] = {}

    def __new__(cls, ref: str, data: Optional[Dict[str, Any]] = None) -> 'InfoRef':
        """Create or return existing InfoRef instance.
        
        Args:
            ref: Reference string
            data: Optional reference data for external refs
        """
        ref_id = url_encode(ref)
        if ref_id in cls._instances:
            return cls._instances[ref_id]
        instance = super(InfoRef, cls).__new__(cls)
        cls._instances[ref_id] = instance
        return instance

    def __init__(self, ref: str, data: Optional[Dict[str, Any]] = None):
        """Initialize info reference.
        
        Args:
            ref: Reference string
            data: Optional reference data from pickle
        """
        if hasattr(self, 'initialized'):
            return

        super().__init__(url_encode(ref))
        self.ref = ref
        self.internal = not bool(re.match(r'(https?://|\|.+\|)', ref))

        # データは内部/外部に関係なく保存
        self.ref_data = data if data else None
        self.initialized = True

    def refstring(self) -> str:
        """Get reference string format."""
        if self.internal:
            return f':ref:`{self.ref}`'
        # Check if it's a |name| style reference
        if re.match(r'\|.+\|', self.ref):
            return self.ref
        # For HTTP URLs, return as is
        return self.ref

    def link_data(self) -> Optional[Dict[str, Dict[str, str]]]:
        """Get link data for references.
        
        Returns:
            Dictionary with localized text and URLs for all reference types
        """
        # pickleから取得したデータが存在する場合はそれを使用
        if self.ref_data:
            return {
                'text': self.ref_data['text'],
                'url': self.ref_data['url']
            }

        # デフォルトケース: pickleデータがない場合は参照タイプに応じて生成
        result = {
            'text': {},
            'url': {}
        }

        # textにはrefstringを使用
        refstr = self.refstring()
        result['text'] = {lang: refstr for lang in ['ja', 'en']}

        # URLは空文字をデフォルトとし、HTTP(S)の場合のみURLを設定
        if re.match(r'https?://', self.ref):
            result['url'] = {lang: self.ref for lang in ['ja', 'en']}
        else:
            result['url'] = {lang: '' for lang in ['ja', 'en']}

        return result

    def set_link(self, data: Dict[str, Dict[str, str]]) -> None:
        """Set link data for references.
        
        Args:
            data: Dictionary containing localized url and text
        """
        self.ref_data = data

    @classmethod
    def list_all_internal(cls) -> List['InfoRef']:
        """Get all internal references."""
        return [ref for ref in cls._instances.values() if ref.internal]

    @classmethod
    def list_all_external(cls) -> List['InfoRef']:
        """Get all external references."""
        return [ref for ref in cls._instances.values() if not ref.internal]

    @classmethod
    def list_has_guidelines(cls) -> List['InfoRef']:
        """Get references that have associated guidelines."""
        rel = RelationshipManager()
        return [ref for ref in cls._instances.values() if rel.get_related_objects(ref, 'guideline')]

    @classmethod
    def list_has_faqs(cls) -> List['InfoRef']:
        """Get references that have associated FAQs."""
        rel = RelationshipManager()
        return [ref for ref in cls._instances.values() if rel.get_related_objects(ref, 'faq')]
