import datetime
import re
from urllib.parse import quote as url_encode
from constants import PLATFORM_NAMES, SEVERITY_TAGS, CHECK_TARGETS, IMPLEMENTATION_TARGETS

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
            return self._data['check'][check.id]['faq']
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

    def template_object(self, lang):
        rel = RelationshipManager()
        template_object = {
            'id': self.id,
            'title': self.title[lang],
            'platform': join_items(self.platform, lang),
            'guideline': self.guideline[lang],
            'intent': self.intent[lang],
            'category': self.category.names[lang],
            'checks': [check.template_object(lang, platform=self.platform) for check in rel.get_guideline_to_checks(self)],
            'scs': [sc.template_object() for sc in rel.get_guideline_to_scs(self)],
        }
        faqs = rel.get_guideline_to_faqs(self)
        if len(faqs):
            template_object['faqs'] = [faq.id for faq in sorted(faqs, key=lambda item: item.sort_key)]
        info = rel.get_guideline_to_info(self)
        if len(info):
            template_object['info'] = [inforef.refstring() for inforef in info]
        return template_object

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
        self.check = check['check']
        self.severity = check['severity']
        self.target = check['target']
        self.platform = check['platform']
        self.src_path = check['src_path']
        self.procedures = []
        self.implementations = []
        if 'procedures' in check:
            for proc in check['procedures']:
                self.procedures.append(Procedure(proc, self))
        if 'implementations' in check:
            self.implementations = [Implementation(**implementation) for implementation in check['implementations']]
        Check.all_checks[self.id] = self

    def procedure_platforms(self):
        return sorted({procedure.platform for procedure in self.procedures})

    def template_object(self, lang, **kwargs):
        rel = RelationshipManager()
        gl_platform = kwargs.get('platform')
        template_object = {
            'id': self.id,
            'check': self.check[lang],
            'severity': SEVERITY_TAGS[self.severity][lang],
            'target': CHECK_TARGETS[self.target][lang],
            'platform': join_items(self.platform, lang),
            'guidelines': []
        }
        if len(self.procedures) > 0:
            if not gl_platform:
                template_object['procedures'] = [procedure.template_object(lang) for procedure in self.procedures]
            else:
                template_object['procedures'] = []
                for proc in self.procedures:
                    proc_platform = proc.platform
                    if proc_platform == 'general' or proc_platform in gl_platform:
                        template_object['procedures'].append(proc.template_object(lang))
        if len(self.implementations) > 0:
            template_object['implementations'] = [implementation.template_object(lang) for implementation in self.implementations]
        info = rel.get_check_to_info(self)
        if len(info) > 0:
            template_object['info_refs'] = [inforef.refstring() for inforef in info]
        faqs = rel.get_check_to_faqs(self)
        if len(faqs) > 0:
            template_object['faqs'] = [faq.id for faq in sorted(faqs, key=lambda item: item.sort_key)]
        for gl in rel.get_check_to_guidelines(self):
            template_object['guidelines'].append(gl.get_category_and_id(lang))
        return template_object

    @classmethod
    def get_by_id(cls, check_id):
        return cls.all_checks.get(check_id)

    @classmethod
    def template_object_all(cls, lang):
        sorted_checks = sorted(cls.all_checks, key=lambda x: cls.all_checks[x].id)
        for check_id in sorted_checks:
            yield cls.all_checks[check_id].template_object(lang)

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

    def template_object(self, lang):
        rel = RelationshipManager()
        tags = rel.get_faq_to_tags(self)
        if lang == 'ja':
            date_format = "%Y年%-m月%-d日"
        else:
            date_format = "%B %-d, %Y"
        template_object = {
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
            template_object['guidelines'] = [guideline.get_category_and_id(lang) for guideline in sorted_guidelines]
        checks = rel.get_faq_to_checks(self)
        if len(checks) > 0:
            sorted_checks = sorted(checks, key=lambda item: item.id)
            template_object['checks'] = [{'id': check.id, 'check': check.check[lang]} for check in sorted_checks]
        info = rel.get_faq_to_info(self)
        if len(info):
            template_object['info'] = [inforef.refstring() for inforef in info]
        related_faqs = rel.get_related_faqs(self)
        if len(related_faqs) > 0:
            template_object['related_faqs'] = [faq.id for faq in related_faqs]
        return template_object

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

    # def add_guideline(self, guideline):
    #     if guideline in self.guidelines:
    #         return
    #     self.guidelines.append(guideline)
    #     guideline.set_category(self)

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

    def template_object(self, lang):
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

    def template_object(self):
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

    @classmethod
    def get_by_id(cls, ref_id):
        return cls.all_inforefs.get(ref_id)

    @classmethod
    def list_all_external(cls):
        for inforef in cls.all_inforefs.values():
            if not inforef.internal:
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

class Procedure:
    def __init__(self, procedure, check):
        self.platform = procedure['platform']
        self.procedure = procedure['procedure']
        self.techniques = []
        if 'techniques' in procedure:
            for tech in procedure['techniques']:
                tech_tool = tech['tool']
                if tech_tool in CheckTool.list_all_ids():
                    basename = tech_tool
                else:
                    basename = 'misc'
                    tech['tool_display_name'] = tech_tool
                tech['tool'] = CheckTool.get_by_id(basename)
                tech_obj = Technique(**tech)
                example = {
                    'tool': CheckTool.get_by_id(basename),
                    'check': check,
                    'technique': tech_obj
                }
                CheckTool.get_by_id(basename).add_example(Example(**example))
                self.techniques.append(tech_obj)
        else:
            self.techniques = None

    def get_platform(self):
        return self.platform

    def template_object(self, lang):
        template_object = {
            'platform': PLATFORM_NAMES[self.platform][lang],
            'procedure': self.procedure[lang]
        }
        if self.techniques:
            template_object['techniques'] = [technique.template_object(lang) for technique in self.techniques]
        return template_object

class Technique:
    def __init__(self, tool, technique, **kwargs):
        self.tool = tool
        if 'tool_display_name' in kwargs:
            self.tool_display_name = kwargs['tool_display_name']
        else:
            self.tool_display_name = None
        self.technique = technique
        if 'note' in kwargs:
            self.note = kwargs['note']
        else:
            self.note = None
        if 'YouTube' in kwargs:
            self.youtube = YouTube(**kwargs['YouTube'])
        else:
            self.youtube = None

    def template_object(self, lang):
        if not self.tool_display_name:
            self.tool_display_name = self.tool.get_name(lang)
        template_object = {
            'tool_display_name': self.tool_display_name,
            'technique': self.technique[lang]
        }
        if self.note:
            template_object['note'] = self.note[lang]
        if self.youtube:
            template_object['YouTube'] = self.youtube.template_object()
        return template_object

class YouTube:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.title = kwargs['title']

    def template_object(self):
        return {
            'id': self.id,
            'title': self.title
        }

class Implementation:
    def __init__(self, title, methods):
        self.title = title
        self.methods = [Method(**method) for method in methods]

    def template_object(self, lang):
        return {
            'title': self.title[lang],
            'methods': [method.template_object(lang) for method in self.methods]
        }

class Example:
    def __init__(self, tool, check, technique):
        self.tool = tool
        self.check_id = check.id
        self.check_text = check.check
        self.check_src_path = check.src_path
        self.technique = technique

    def template_object(self, lang):
        template_object = self.technique.template_object(lang)
        template_object['tool'] = self.tool.id
        template_object['check_id'] = self.check_id
        template_object['check_text'] = self.check_text[lang]
        return template_object

class Method:
    def __init__(self, platform, method):
        self.platform = platform
        self.method = method

    def template_object(self, lang):
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

    def example_template_object(self, lang):
        template_object = {
            'tool': self.id
        }
        example_objects = []
        for example in self.examples:
            example_objects.append(example.template_object(lang))
        template_object['examples'] = sorted(example_objects, key=lambda item: item['check_id'])
        return template_object

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

    def template_object(self, lang):
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
            data['scs'] = [sc.template_object() for sc in scs]
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
