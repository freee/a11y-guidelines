import datetime
import re
from urllib.parse import quote as url_encode
from .constants import PLATFORM_NAMES
from .config import Config
from .models.check import Check, CheckTool
from .models.content import Category, Guideline
from .models.reference import WcagSc, InfoRef
from .models.faq.article import Faq
from .models.faq.tag import FaqTag
from .models.axe import AxeRule

class RelationshipManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RelationshipManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._data = {}
        self._unresolved_faqs = {}
        self._initialized = True

    def associate_objects(self, obj1, obj2):
        obj1_type = obj1.object_type
        obj2_type = obj2.object_type
        obj1_id = obj1.id
        obj2_id = obj2.id
        if obj1_type not in self._data:
            self._data[obj1_type] = {}
        if obj1_id not in self._data[obj1_type]:
            self._data[obj1_type][obj1_id] = {}
        if obj2_type not in self._data[obj1_type][obj1_id]:
            self._data[obj1_type][obj1_id][obj2_type] = []
        if obj2 not in self._data[obj1_type][obj1_id][obj2_type]:
            self._data[obj1_type][obj1_id][obj2_type].append(obj2)

        if obj2_type not in self._data:
            self._data[obj2_type] = {}
        if obj2_id not in self._data[obj2_type]:
            self._data[obj2_type][obj2_id] = {}
        if obj1_type not in self._data[obj2_type][obj2_id]:
            self._data[obj2_type][obj2_id][obj1_type] = []
        if obj1 not in self._data[obj2_type][obj2_id][obj1_type]:
            self._data[obj2_type][obj2_id][obj1_type].append(obj1)

    def add_unresolved_faqs(self, faq1, faq2):
        if faq1 not in self._unresolved_faqs:
            self._unresolved_faqs[faq1] = []
        if faq2 not in self._unresolved_faqs[faq1]:
            self._unresolved_faqs[faq1].append(faq2)
        if faq2 not in self._unresolved_faqs:
            self._unresolved_faqs[faq2] = []
        if faq1 not in self._unresolved_faqs[faq2]:
            self._unresolved_faqs[faq2].append(faq1)

    def resolve_faqs(self):
        for faq_id in self._unresolved_faqs:
            for faq2_id in self._unresolved_faqs[faq_id]:
                faq1 = Faq.get_by_id(faq_id)
                faq2 = Faq.get_by_id(faq2_id)
                self.associate_objects(faq1, faq2)

    def get_guidelines_to_category(self):
        mapping = {}
        for category in self._data['category']:
            guidelines = self._data['category'][category]['guideline']
            sorted_guidelines = sorted(guidelines, key=lambda item: item.sort_key)
            mapping[category] = sorted_guidelines
        return mapping

    def get_category_to_guidelines(self, category):
        return sorted(self._data['category'][category.id]['guideline'], key=lambda item: item.sort_key)

    def get_check_to_guidelines(self, check):
        return sorted(self._data['check'][check.id]['guideline'], key=lambda item: item.sort_key)

    def get_guideline_to_checks(self, guideline):
        return sorted(self._data['guideline'][guideline.id]['check'], key=lambda item: item.id)

    def get_guideline_to_scs(self, guideline):
        return sorted(self._data['guideline'][guideline.id]['wcag_sc'], key=lambda item: item.sort_key)

    def get_sc_to_guidelines(self, sc):
        if sc.id not in self._data['wcag_sc'] or 'guideline' not in self._data['wcag_sc'][sc.id]:
            return []
        return sorted(self._data['wcag_sc'][sc.id]['guideline'], key=lambda item: item.sort_key)

    def get_guideline_to_info(self, guideline):
        if 'info_ref' in self._data['guideline'][guideline.id]:
            return self._data['guideline'][guideline.id]['info_ref']
        return []

    def get_info_to_guidelines(self, info):
        if 'guideline' in self._data['info_ref'][info.id]:
            return self._data['info_ref'][info.id]['guideline']
        return []

    def get_check_to_info(self, check):
        if 'info_ref' in self._data['check'][check.id]:
            return self._data['check'][check.id]['info_ref']
        return []

    def get_guideline_to_faqs(self, guideline):
        if 'faq' in self._data['guideline'][guideline.id]:
            return self._data['guideline'][guideline.id]['faq']
        return []

    def get_faq_to_guidelines(self, faq):
        if faq.id not in self._data['faq'] or 'guideline' not in self._data['faq'][faq.id]:
            return []
        return self._data['faq'][faq.id]['guideline']

    def get_faq_to_checks(self, faq):
        if faq.id not in self._data['faq'] or 'check' not in self._data['faq'][faq.id]:
            return []
        return self._data['faq'][faq.id]['check']

    def get_check_to_faqs(self, check):
        if 'faq' in self._data['check'][check.id]:
            faqs = self._data['check'][check.id]['faq']
            return sorted(faqs, key=lambda item: item.sort_key)
        return []

    def get_faq_to_tags(self, faq):
        return sorted(self._data['faq'][faq.id]['faq_tag'], key=lambda item: item.id)

    def get_tag_to_faqs(self, tag):
        if tag.id not in self._data['faq_tag'] or 'faq' not in self._data['faq_tag'][tag.id]:
            return []
        return self._data['faq_tag'][tag.id]['faq']

    def get_faq_to_info(self, faq):
        if 'info_ref' in self._data['faq'][faq.id]:
            return self._data['faq'][faq.id]['info_ref']
        return []

    def get_info_to_faqs(self, info):
        if 'faq' in self._data['info_ref'][info.id]:
            return self._data['info_ref'][info.id]['faq']
        return []

    def get_related_faqs(self, faq):
        if faq.id not in self._unresolved_faqs:
            return []
        return sorted(self._data['faq'][faq.id]['faq'], key=lambda item: item.sort_key)

    def get_axe_to_wcagsc(self, axe_rule):
        if 'wcag_sc' in self._data['axe_rule'][axe_rule.id]:
            return self._data['axe_rule'][axe_rule.id]['wcag_sc']
        return []

    def get_axe_to_guidelines(self, axe_rule):
        if 'guideline' in self._data['axe_rule'][axe_rule.id]:
            return self._data['axe_rule'][axe_rule.id]['guideline']
        return []

