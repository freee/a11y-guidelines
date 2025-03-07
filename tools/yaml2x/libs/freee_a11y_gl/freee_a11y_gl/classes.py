import datetime
import re
from urllib.parse import quote as url_encode
from .constants import PLATFORM_NAMES, SEVERITY_TAGS, CHECK_TARGETS, IMPLEMENTATION_TARGETS
from .config import Config

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

class Guideline:
    all_guidelines = {}

    def __init__(self, gl):
        self.id = gl['id']
        self.object_type = 'guideline'
        if self.id in Guideline.all_guidelines:
            raise ValueError(f'Duplicate guideline ID: {self.id}')
        self.sort_key = gl['sortKey']
        if self.sort_key in [guideline.sort_key for guideline in Guideline.all_guidelines.values()]:
            raise ValueError(f'Duplicate guideline sortKey: {self.sort_key}')
        self.title = gl['title']
        self.platform = gl['platform']
        self.guideline = gl['guideline']
        self.intent = gl['intent']
        self.src_path = gl['src_path']
        self.category = Category.get_by_id(gl['category'])
        rel = RelationshipManager()
        rel.associate_objects(self, Category.get_by_id(gl['category']))
        for check_id in gl['checks']:
            rel.associate_objects(self, Check.get_by_id(check_id))
        for sc in gl['sc']:
            rel.associate_objects(self, WcagSc.get_by_id(sc))

        if 'info' in gl:
            for info in gl['info']:
                info_ref = InfoRef(info)
                rel.associate_objects(self, info_ref)
                if info_ref.internal:
                    rel.associate_objects(self, info_ref)
                for check in rel.get_guideline_to_checks(self):
                    rel.associate_objects(check, info_ref)

        Guideline.all_guidelines[self.id] = self

    def get_category_and_id(self, lang):
        return {
            'category': self.category.get_name(lang),
            'guideline': self.id
        }

    def link_data(self):
        langs = self.title.keys()
        data = {
            'text': {},
            'url': {}
        }
        for lang in langs:
            separator_char = Config.get_separator(lang, "text")
            basedir = Config.get_guidelines_path()
            baseurl = Config.get_base_url(lang)
            category = self.category.get_name(lang)
            basename = self.category.id
            data['text'][lang] = f'{category}{separator_char}{self.title[lang]}'
            data['url'][lang] = f'{baseurl}{basedir}{basename}.html#{self.id}'
        return data

    def template_data(self, lang):
        rel = RelationshipManager()
        template_data = {
            'id': self.id,
            'title': self.title[lang],
            'platform': join_items(self.platform, lang),
            'guideline': self.guideline[lang],
            'intent': self.intent[lang],
            'category': self.category.names[lang],
            'checks': [check.template_data(lang, platform=self.platform) for check in rel.get_guideline_to_checks(self)],
            'scs': [sc.template_data() for sc in rel.get_guideline_to_scs(self)],
        }
        faqs = rel.get_guideline_to_faqs(self)
        if len(faqs):
            template_data['faqs'] = [faq.id for faq in sorted(faqs, key=lambda item: item.sort_key)]
        info = rel.get_guideline_to_info(self)
        if len(info):
            template_data['info'] = [inforef.refstring() for inforef in info]
        return template_data

    @classmethod
    def get_by_id(cls, guideline_id):
        return cls.all_guidelines.get(guideline_id)

    @classmethod
    def list_all_src_paths(cls):
        for guideline in cls.all_guidelines.values():
            yield guideline.src_path

class Check:
    all_checks = {}

    def __init__(self, check):
        self.id = check['id']
        self.object_type = 'check'
        if self.id in Check.all_checks:
            raise ValueError(f'Duplicate check ID: {self.id}')
        self.sort_key = check['sortKey']
        if self.sort_key in [check.sort_key for check in Check.all_checks.values()]:
            raise ValueError(f'Duplicate check sortKey: {self.sort_key}')
        self.check = check['check']
        self.severity = check['severity']
        self.target = check['target']
        self.platform = check['platform']
        self.src_path = check['src_path']
        self.conditions = []
        self.implementations = []
        if 'conditions' in check:
            for condition in check['conditions']:
                self.conditions.append(Condition(condition, self))
        if 'implementations' in check:
            self.implementations = [Implementation(**implementation) for implementation in check['implementations']]
        Check.all_checks[self.id] = self

    def condition_platforms(self):
        return sorted({condition.platform for condition in self.conditions})

    def template_data(self, lang, **kwargs):
        rel = RelationshipManager()
        gl_platform = kwargs.get('platform')
        template_data = {
            'id': self.id,
            'check': self.check[lang],
            'severity': SEVERITY_TAGS[self.severity][lang],
            'target': CHECK_TARGETS[self.target][lang],
            'platform': join_items(self.platform, lang),
            'guidelines': []
        }
        if len(self.conditions) > 0:
            if not gl_platform:
                template_data['conditions'] = [cond.template_data(lang) for cond in self.conditions]
            else:
                template_data['conditions'] = [cond.template_data(lang) for cond in self.conditions if cond.platform == 'general' or cond.platform in gl_platform]
        if len(self.implementations) > 0:
            template_data['implementations'] = [implementation.template_data(lang) for implementation in self.implementations]
        info = rel.get_check_to_info(self)
        if len(info) > 0:
            template_data['info_refs'] = [inforef.refstring() for inforef in info]
        faqs = rel.get_check_to_faqs(self)
        if len(faqs) > 0:
            template_data['faqs'] = [faq.id for faq in faqs]
        for gl in rel.get_check_to_guidelines(self):
            template_data['guidelines'].append(gl.get_category_and_id(lang))
        return template_data

    def object_data(self, baseurl = ''):
        rel = RelationshipManager()
        data = {
            'id': self.id,
            'sortKey': self.sort_key,
            'check': self.check,
            'severity': f'[{self.severity.upper()}]',
            'target': self.target,
            'platform': self.platform,
            'guidelines': []
        }
        data['guidelines'] = [gl.link_data() for gl in rel.get_check_to_guidelines(self)]
        faqs = rel.get_check_to_faqs(self)
        if len(faqs) > 0:
            data['faqs'] = [faq.link_data() for faq in faqs]
        info = rel.get_check_to_info(self)
        if len(info) > 0:
            data['info'] = [inforef.link_data() for inforef in info]
        if len(self.conditions) > 0:
            data['conditions'] = [cond.object_data() for cond in self.conditions]
            data['conditionStatements'] = []
            for condition in self.conditions:
                statement = {
                    'platform': condition.platform,
                    'summary': {}
                }
                for lang in self.check:
                    statement['summary'][lang] = condition.summary(lang)
                data['conditionStatements'].append(statement)

        if len(self.implementations) > 0:
            implementations = {}
            for implementation in self.implementations:
                title = implementation.title
                for method in implementation.methods:
                    platform = method.platform
                    if platform not in implementations:
                        implementations[platform] = []
                    implementations[platform].append({
                        'title': title,
                        'method': method.method
                    })
            for platform, methods in implementations.items():
                platform_key = f'implementation_{platform}'
                if platform_key not in data:
                    data[platform_key] = {}
                for method in methods:
                    for lang, lang_title in method['title'].items():
                        if lang not in data[platform_key]:
                            data[platform_key][lang] = ''
                        data[platform_key][lang] += f'{lang_title}:\n{method["method"][lang]}\n\n'
        return data

    @classmethod
    def get_by_id(cls, check_id):
        return cls.all_checks.get(check_id)

    @classmethod
    def template_data_all(cls, lang):
        sorted_checks = sorted(cls.all_checks, key=lambda x: cls.all_checks[x].id)
        for check_id in sorted_checks:
            yield cls.all_checks[check_id].template_data(lang)

    @classmethod
    def object_data_all(cls, baseurl = ''):
        sorted_checks = sorted(cls.all_checks, key=lambda x: cls.all_checks[x].id)
        checks = {}
        for check_id in sorted_checks:
            checks[check_id] = cls.all_checks[check_id].object_data(baseurl)
        return checks


    @classmethod
    def list_all_src_paths(cls):
        for check in cls.all_checks.values():
            yield check.src_path

class Faq:
    all_faqs = {}

    def __init__(self, faq):
        self.id = faq['id']
        self.object_type = 'faq'
        if self.id in Faq.all_faqs:
            raise ValueError(f'Duplicate FAQ ID: {self.id}')
        self.sort_key = faq['sortKey']
        if self.sort_key in [faq.sort_key for faq in Faq.all_faqs.values()]:
            raise ValueError(f'Duplicate FAQ sortKey: {self.sort_key}')
        self.updated = datetime.datetime.fromisoformat(faq['updated'])
        self.title = faq['title']
        self.problem = faq['problem']
        self.solution = faq['solution']
        self.explanation = faq['explanation']
        self.src_path = faq['src_path']

        rel = RelationshipManager()
        if 'guidelines' in faq:
            for guideline_id in faq['guidelines']:
                rel.associate_objects(self, Guideline.get_by_id(guideline_id))

        for tag in faq['tags']:
            rel.associate_objects(self, FaqTag.get_by_id(tag))

        if 'checks' in faq:
            for check_id in faq['checks']:
                rel.associate_objects(self, Check.get_by_id(check_id))

        if 'info' in faq:
            for info in faq['info']:
                rel.associate_objects(self, InfoRef(info))
        if 'faqs' in faq:
            for related_faq in faq['faqs']:
                rel.add_unresolved_faqs(self.id, related_faq)
        Faq.all_faqs[self.id] = self

    def get_dependency(self):
        rel = RelationshipManager()
        dependency = [self.src_path]
        guidelines = rel.get_faq_to_guidelines(self)
        if len(guidelines) > 0:
            dependency.extend([guideline.src_path for guideline in guidelines])
        checks = rel.get_faq_to_checks(self)
        if len(checks) > 0:
            dependency.extend([check.src_path for check in checks])
        return uniq(dependency)

    def link_data(self):
        langs = self.title.keys()
        basedir = Config.get_faq_path()
        data = {
            'text': {},
            'url': {}
        }
        for lang in langs:
            baseurl = Config.get_base_url(lang)
            basename = self.id
            data['text'][lang] = self.title[lang]
            data['url'][lang] = f'{baseurl}{basedir}{basename}.html'
        return data

    def template_data(self, lang):
        rel = RelationshipManager()
        tags = rel.get_faq_to_tags(self)
        if lang == 'ja':
            date_format = "%Y年%-m月%-d日"
        else:
            date_format = "%B %-d, %Y"
        template_data = {
            'id': self.id,
            'updated': self.updated,
            'updated_str': self.updated.strftime(date_format),
            'title': self.title[lang],
            'problem': self.problem[lang],
            'solution': self.solution[lang],
            'explanation': self.explanation[lang],
            'tags': [tag.id for tag in tags],
        }
        guidelines = rel.get_faq_to_guidelines(self)
        if len(guidelines) > 0:
            sorted_guidelines = sorted(guidelines, key=lambda item: item.sort_key)
            template_data['guidelines'] = [guideline.get_category_and_id(lang) for guideline in sorted_guidelines]
        checks = rel.get_faq_to_checks(self)
        if len(checks) > 0:
            sorted_checks = sorted(checks, key=lambda item: item.id)
            template_data['checks'] = [{'id': check.id, 'check': check.check[lang]} for check in sorted_checks]
        info = rel.get_faq_to_info(self)
        if len(info):
            template_data['info'] = [inforef.refstring() for inforef in info]
        related_faqs = rel.get_related_faqs(self)
        if len(related_faqs) > 0:
            template_data['related_faqs'] = [faq.id for faq in related_faqs]
        return template_data

    @classmethod
    def list_all(cls, **kwargs):
        if 'sort_by' in kwargs:
            if kwargs['sort_by'] == 'date':
                return sorted(cls.all_faqs.values(), key=lambda faq: faq.updated, reverse=True)
        return sorted(cls.all_faqs.values(), key=lambda faq: faq.sort_key)

    @classmethod
    def list_all_src_paths(cls):
        for faq in cls.all_faqs.values():
            yield faq.src_path

    @classmethod
    def get_by_id(cls, faq_id):
        return cls.all_faqs.get(faq_id)

class Category:
    all_categories = {}

    def __init__(self, category_id, names):
        self.id = category_id
        self.object_type = 'category'
        self.names = names
        self.guidelines = []
        Category.all_categories[category_id] = self

    def get_name(self, lang):
        if lang in self.names:
            return self.names[lang]
        return self.names['ja']

    def get_dependency(self):
        rel = RelationshipManager()
        dependency = []
        for guideline in rel.get_category_to_guidelines(self):
            dependency.append(guideline.src_path)
            dependency.extend([check.src_path for check in rel.get_guideline_to_checks(guideline)])
            dependency.extend([faq.src_path for faq in rel.get_guideline_to_faqs(guideline)])
        return uniq(dependency)

    @classmethod
    def get_by_id(cls, category_id):
        return cls.all_categories.get(category_id)

    @classmethod
    def list_all(cls):
        return cls.all_categories.values()

class FaqTag:
    all_tags = {}

    def __init__(self, tag_id, names):
        self.id = tag_id
        self.object_type = 'faq_tag'
        self.names = names
        FaqTag.all_tags[tag_id] = self

    def article_count(self):
        rel = RelationshipManager()
        return len(rel.get_tag_to_faqs(self))

    def get_name(self, lang):
        if lang in self.names:
            return self.names[lang]
        return self.names['en']

    def template_data(self, lang):
        rel = RelationshipManager()
        faqs = rel.get_tag_to_faqs(self)
        if len(faqs) == 0:
            return None
        sorted_faqs = sorted(faqs, key=lambda item: item.sort_key)
        return {
            'tag': self.id,
            'label': self.names[lang],
            'articles': [faq.id for faq in sorted_faqs],
            'count': len(faqs)
        }

    @classmethod
    def get_by_id(cls, tag_id):
        return cls.all_tags.get(tag_id)

    @classmethod
    def list_all(cls, **kwargs):
        if 'sort_by' in kwargs:
            if kwargs['sort_by'] == 'count':
                return sorted(cls.all_tags.values(), key=lambda tag: tag.article_count(), reverse=True)
            if kwargs['sort_by'] == 'label':
                return sorted(cls.all_tags.values(), key=lambda tag: tag.names['en'])
        return cls.all_tags.values()

class WcagSc:
    all_scs = {}

    def __init__(self, sc_id, sc):
        self.id = sc_id
        self.object_type = 'wcag_sc'
        self.scnum = sc['id']
        self.sort_key = sc['sortKey']
        self.level = sc['level']
        self.local_priority = sc['localPriority']
        self.title = {
            'ja': sc['ja']['title'],
            'en': sc['en']['title']
        }
        self.url = {
            'ja': sc['ja']['url'],
            'en': sc['en']['url']
        }
        WcagSc.all_scs[self.id] = self

    def template_data(self):
        return {
            'sc': self.scnum,
            'level': self.level,
            'LocalLevel': self.local_priority,
            'sc_en_title': self.title['en'],
            'sc_ja_title': self.title['ja'],
            'sc_en_url': self.url['en'],
            'sc_ja_url': self.url['ja']
        }

    @classmethod
    def get_by_id(cls, sc_id):
        return cls.all_scs.get(sc_id)

    @classmethod
    def get_all(cls):
        sorted_keys = sorted(cls.all_scs.keys(), key=lambda sc: cls.all_scs[sc].sort_key)
        return {key: cls.get_by_id(key) for key in sorted_keys}

class InfoRef:
    all_inforefs = {}

    def __new__(cls, ref, *args):
        ref_id = url_encode(ref)
        if ref_id in cls.all_inforefs:
            return cls.all_inforefs[ref_id]
        instance = super(InfoRef, cls).__new__(cls)
        cls.all_inforefs[ref_id] = instance
        return instance

    def __init__(self, inforef, data=None):
        if hasattr(self, 'initialized'):
            return
        self.ref = inforef
        self.id = url_encode(self.ref)
        self.object_type = 'info_ref'
        self.internal = not bool(re.match(r'(https?://|\|.+\|)', self.ref))
        if not self.internal:
            self.url = data['url']
            self.text = data['text']
        self.initialized = True

    def refstring(self):
        if self.internal:
            return f':ref:`{self.ref}`'
        return self.ref

    def set_link(self, data):
        if not self.internal:
            return
        self.url = data['url']
        self.text = data['text']

    def link_data(self):
        if self.text:
            return {
                'text': self.text,
                'url': self.url
            }
        return None

    @classmethod
    def get_by_id(cls, ref_id):
        return cls.all_inforefs.get(ref_id)

    @classmethod
    def list_all_external(cls):
        for inforef in cls.all_inforefs.values():
            if not inforef.internal:
                yield inforef

    @classmethod
    def list_all_internal(cls):
        for inforef in cls.all_inforefs.values():
            if inforef.internal:
                yield inforef

    @classmethod
    def list_has_guidelines(cls):
        rel = RelationshipManager()
        for inforef in cls.all_inforefs.values():
            if len(rel.get_info_to_guidelines(inforef)):
                yield inforef

    @classmethod
    def list_has_faqs(cls):
        rel = RelationshipManager()
        for inforef in cls.all_inforefs.values():
            if len(rel.get_info_to_faqs(inforef)):
                yield inforef

class Condition:
    def __init__(self, condition, check):
        self.type = condition['type']
        if 'platform' in condition:
            self.platform = condition['platform']
        if self.type == 'simple':
            self.procedure = Procedure(condition, check)
            self.procedure.tool.add_example(Example(self.procedure, check))
        else:
            self.conditions = []
            for cond in condition['conditions']:
                self.conditions.append(Condition(cond, check))

    def procedures(self):
        if self.type == 'simple':
            return [self.procedure]
        procedures = []
        for cond in self.conditions:
            procedures.extend(cond.procedures())
        return procedures

    def summary(self, lang):
        if self.type == 'simple':
            return f'{self.procedure.id}{Config.get_pass_singular_text(lang)}'

        simple_conditions = [cond.summary(lang) for cond in self.conditions if cond.type == 'simple']
        complex_conditions = [f'({cond.summary(lang)})' for cond in self.conditions if cond.type != 'simple']

        if self.type == 'and':
            summary_separator = Config.get_separator(lang, "and")
            summary_connector = Config.get_conjunction(lang, "and")
            simple_pass = Config.get_pass_plural_text(lang)
        else:
            summary_separator = Config.get_separator(lang, "or")
            summary_connector = Config.get_conjunction(lang, "or")
            simple_pass = Config.get_pass_singular_text(lang)

        if len(simple_conditions) > 1:
            simple_conditions = [cond.replace(Config.get_pass_singular_text(lang), '') for cond in simple_conditions]
            simple_summary = f'{summary_separator.join(simple_conditions)}{simple_pass}'
            return f'{simple_summary}{summary_connector}{summary_connector.join(complex_conditions)}' if complex_conditions else simple_summary
        else:
            return summary_connector.join(simple_conditions + complex_conditions)

    def summary_formula(self):
        def convert_to_formula_format(conditions, func):
            return f'{func}({",".join(conditions)})'

        if self.type == 'simple':
            return self.procedure.id

        simple_conditions = [cond.summary_formula() for cond in self.conditions if cond.type == 'simple']
        complex_conditions = [cond.summary_formula() for cond in self.conditions if cond.type != 'simple']

        if self.type == 'and':
            func = 'AND'
        else:
            func = 'OR'

        return convert_to_formula_format(simple_conditions + complex_conditions, func)

    def template_data(self, lang):
        template_data = {}
        if self.platform is not None:
            template_data['platform'] = PLATFORM_NAMES[self.platform][lang]
            template_data['condition'] = self.summary(lang)
            procedures = self.procedures() 
            if len(procedures) > 0:
                template_data['procedures'] = [proc.template_data(lang) for proc in procedures]
        return template_data

    def object_data(self, platform = None):
        data = {}
        if hasattr(self, 'platform'):
            data['platform'] = self.platform
            platform = self.platform
        data['type'] = self.type
        if self.type == 'simple':
            data['procedure'] = self.procedure.object_data(platform)
        else:
            data['conditions'] = [cond.object_data(platform) for cond in self.conditions]
        return data

class Procedure:
    def __init__(self, condition, check):
        self.id = condition['id']
        tool = condition['tool']
        if tool in CheckTool.list_all_ids():
            basename = tool
            tool_display_name = None
        else:
            basename = 'misc'
            tool_display_name = tool
        tool = CheckTool.get_by_id(basename)
        self.tool = tool
        if tool_display_name:
            self.tool_display_name = tool_display_name
        else:
            self.tool_display_name = None
        self.procedure = condition['procedure']
        if 'note' in condition:
            self.note = condition['note']
        else:
            self.note = None
        if 'YouTube' in condition:
            self.youtube = YouTube(condition['YouTube'])
        else:
            self.youtube = None

    def template_data(self, lang):
        if not self.tool_display_name:
            self.tool_display_name = self.tool.get_name(lang)
        template_data = {
            'id': self.id,
            'tool_display_name': self.tool_display_name,
            'procedure': self.procedure[lang]
        }
        if self.note:
            template_data['note'] = self.note[lang]
        if self.youtube:
            template_data['YouTube'] = self.youtube.template_data()
        return template_data

    def object_data(self, platform):
        baseurl = {
            'ja': 'https://a11y-guidelines.freee.co.jp/checks/examples/',
            'en': 'https://a11y-guidelines.freee.co.jp/en/checks/examples/'
        }
        tool_link = {
            'text': {},
            'url': {}
        }
        langs = self.procedure.keys()
        for lang in langs:
            if self.tool_display_name is not None:
                tool_link['text'][lang] = self.tool_display_name
            else:
                tool_link['text'][lang] = self.tool.get_name(lang)
            tool_link['url'][lang] = f'{baseurl[lang]}{self.tool.id}.html#{self.id}'
        data = {
            'id': self.id,
            'platform': platform,
            'tool': self.tool.id,
            'toolLink': tool_link,
            'procedure': self.procedure
        }
        return data

class YouTube:
    def __init__(self, youtube):
        self.id = youtube['id']
        self.title = youtube['title']

    def template_data(self):
        return {
            'id': self.id,
            'title': self.title
        }

class Implementation:
    def __init__(self, title, methods):
        self.title = title
        self.methods = [Method(**method) for method in methods]

    def template_data(self, lang):
        return {
            'title': self.title[lang],
            'methods': [method.template_data(lang) for method in self.methods]
        }

class Example:
    def __init__(self, procedure, check):
        self.check_id = check.id
        self.check_text = check.check
        self.check_src_path = check.src_path
        self.procedure = procedure

    def template_data(self, lang):
        template_data = self.procedure.template_data(lang)
        template_data['tool'] = self.procedure.tool.id
        template_data['check_id'] = self.check_id
        template_data['check_text'] = self.check_text[lang]
        return template_data

class Method:
    def __init__(self, platform, method):
        self.platform = platform
        self.method = method

    def template_data(self, lang):
        return {
            'platform': IMPLEMENTATION_TARGETS[self.platform][lang],
            'method': self.method[lang]
        }

class CheckTool:
    all_tools = {}

    def __init__(self, tool_id, names):
        self.id = tool_id
        self.names = names
        self.examples = []
        CheckTool.all_tools[tool_id] = self

    def add_example(self, example):
        self.examples.append(example)

    def get_name(self, lang):
        if lang in self.names:
            return self.names[lang]
        return self.names['ja']

    def get_dependency(self):
        dependency = []
        for example in self.examples:
            dependency.append(example.check_src_path)
        return uniq(dependency)

    def example_template_data(self, lang):
        examples = {}
        for example in self.examples:
            check_id = example.check_id
            if check_id not in examples:
                examples[check_id] = {
                    'check_id': check_id,
                    'check_text': example.check_text[lang],
                    'tool': self.id,
                    'procedures': []
                }
            examples[check_id]['procedures'].append(example.procedure.template_data(lang))
        return sorted(examples.values(), key=lambda item: item['check_id'])

    @classmethod
    def list_all(cls):
        return cls.all_tools.values()

    @classmethod
    def list_all_ids(cls):
        return cls.all_tools.keys()

    @classmethod
    def get_by_id(cls, tool_id):
        return cls.all_tools.get(tool_id)

class AxeRule:
    all_rules = {}
    timestamp = None
    version = None
    major_version = None
    deque_url = None

    def __init__(self, rule, messages_ja):
        rule_id = rule['id']
        if rule_id in AxeRule.all_rules:
            raise ValueError(f'Duplicate rule ID: {rule_id}')
        self.id = rule_id
        self.object_type = 'axe_rule'
        if not rule_id in messages_ja['rules']:
            msg_ja = {
                'help': rule['metadata']['help'],
                'description': rule['metadata']['description']
            }
            self.translated = None
        else:
            msg_ja = messages_ja['rules'][rule_id]
            self.translated = True
        self.message = {
            'help': {
                'en': rule['metadata']['help'],
                'ja': msg_ja['help']
            },
            'description': {
                'en': rule['metadata']['description'],
                'ja': msg_ja['description']
            }
        }
        self.has_wcag_sc = None
        self.has_guideline = None
        wcag_scs = [tag2sc(tag) for tag in rule['tags'] if re.match(r'wcag\d{3,}', tag) ]
        rel = RelationshipManager()
        for sc in wcag_scs:
            if sc not in WcagSc.all_scs:
                continue
            rel.associate_objects(self, WcagSc.get_by_id(sc))
            self.has_wcag_sc = True
            for guideline in rel.get_sc_to_guidelines(WcagSc.get_by_id(sc)):
                rel.associate_objects(self, guideline)
                self.has_guideline = True
        AxeRule.all_rules[rule_id] = self

    def template_data(self, lang):
        rel = RelationshipManager()
        data = {
            'id': self.id,
            'help': self.message['help'],
            'description': self.message['description']
        }
        if self.translated:
            data['translated'] = True
        if self.has_wcag_sc:
            scs = sorted(rel.get_axe_to_wcagsc(self), key=lambda item: item.sort_key)
            data['scs'] = [sc.template_data() for sc in scs]
        if self.has_guideline:
            guidelines = sorted(rel.get_axe_to_guidelines(self), key=lambda item: item.sort_key)
            data['guidelines'] = [guideline.get_category_and_id(lang) for guideline in guidelines]
        return data

    @classmethod
    def list_all(cls):
        sorted_all_rules = sorted(cls.all_rules, key=lambda rule: cls.all_rules[rule].id)
        with_guidelines = []
        with_sc = []
        without_sc = []
        for rule_id in sorted_all_rules:
            rule = cls.all_rules[rule_id]
            if rule.has_guideline:
                with_guidelines.append(rule)
            elif rule.has_wcag_sc:
                with_sc.append(rule)
            else:
                without_sc.append(rule)
        return with_guidelines + with_sc + without_sc

# Utility functions
def join_items(items, lang):
    if lang == 'ja':
        separator = '、'
    else:
        separator = ', '
    return separator.join([PLATFORM_NAMES[item][lang] for item in items])

def uniq(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

def tag2sc(tag):
    return re.sub(r'wcag(\d)(\d)(\d+)', r'\1.\2.\3', tag)
