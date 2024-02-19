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
        self.category_to_guidelines = {}
        self.guideline_to_category = {}
        self.guideline_to_scs = {}
        self.sc_to_guidelines = {}
        self.guideline_to_checks = {}
        self.check_to_guidelines = {}
        self.guideline_to_info = {}
        self.info_to_guidelines = {}
        self.faq_to_guidelines = {}
        self.guideline_to_faqs = {}
        self.faq_to_checks = {}
        self.check_to_faqs = {}
        self.faq_to_tags = {}
        self.tag_to_faqs = {}
        self.info_to_checks = {}
        self.check_to_info = {}
        self.faq_to_info = {}
        self.info_to_faqs = {}
        self._initialized = True

    def set_guideline_category(self, guideline):
        category = guideline.category
        if category.id not in self.category_to_guidelines:
            self.category_to_guidelines[category.id] = []
        self.category_to_guidelines[category.id].append(guideline)
        self.guideline_to_category[guideline.id] = category

    def get_guidelines_to_category(self):
        mapping = {}
        for category, guidelines in self.category_to_guidelines.items():
            sorted_guidelines = sorted(guidelines, key=lambda item: item.sort_key)
            mapping[category] = sorted_guidelines
        return mapping

    def get_category_to_guidelines(self, category):
        return sorted(self.category_to_guidelines[category.id], key=lambda item: item.sort_key)

    def associate_guideline_with_check(self, guideline, check):
        if guideline.id not in self.guideline_to_checks:
            self.guideline_to_checks[guideline.id] = []
        if check not in self.guideline_to_checks[guideline.id]:
            self.guideline_to_checks[guideline.id].append(check)
        if check.id not in self.check_to_guidelines:
            self.check_to_guidelines[check.id] = []
        if  guideline not in self.check_to_guidelines[check.id]:
            self.check_to_guidelines[check.id].append(guideline)

    def get_check_to_guidelines(self, check):
        return sorted(self.check_to_guidelines[check.id], key=lambda item: item.sort_key)

    def get_guideline_to_checks(self, guideline):
        return sorted(self.guideline_to_checks[guideline.id], key=lambda item: item.id)

    def associate_guideline_with_sc(self, guideline, sc):
        if guideline.id not in self.guideline_to_scs:
            self.guideline_to_scs[guideline.id] = []
        if sc not in self.guideline_to_scs[guideline.id]:
            self.guideline_to_scs[guideline.id].append(sc)
        if sc.id not in self.sc_to_guidelines:
            self.sc_to_guidelines[sc.id] = []
        if guideline not in self.sc_to_guidelines[sc.id]:
            self.sc_to_guidelines[sc.id].append(guideline)

    def get_guideline_to_scs(self, guideline):
        return sorted(self.guideline_to_scs[guideline.id], key=lambda item: item.sort_key)

    def get_sc_to_guidelines(self, sc):
        if sc.id not in self.sc_to_guidelines:
            return []
        return sorted(self.sc_to_guidelines[sc.id], key=lambda item: item.sort_key)

    def associate_guideline_with_info(self, guideline, info):
        if guideline.id not in self.guideline_to_info:
            self.guideline_to_info[guideline.id] = []
        if info not in self.guideline_to_info[guideline.id]:
            self.guideline_to_info[guideline.id].append(info)
        if info.id not in self.info_to_guidelines:
            self.info_to_guidelines[info.id] = []
        if info.internal and guideline not in self.info_to_guidelines[info.id]:
            self.info_to_guidelines[info.id].append(guideline)
        for check in self.guideline_to_checks.get(guideline.id):
            if check.id not in self.check_to_info:
                self.check_to_info[check.id] = []
            if info not in self.check_to_info.get(check.id):
                self.check_to_info[check.id].append(info)

    def get_guideline_to_info(self, guideline):
        if guideline.id in self.guideline_to_info:
            return self.guideline_to_info.get(guideline.id)
        return []

    def get_info_to_guidelines(self, info):
        if info.id in self.info_to_guidelines:
            return self.info_to_guidelines.get(info.id)
        return []

    def get_check_to_info(self, check):
        if check.id in self.check_to_info:
            return self.check_to_info.get(check.id)
        return []

    def associate_faq_with_guideline(self, faq, guideline):
        if faq.id not in self.faq_to_guidelines:
            self.faq_to_guidelines[faq.id] = []
        if guideline not in self.faq_to_guidelines[faq.id]:
            self.faq_to_guidelines[faq.id].append(guideline)
        if guideline.id not in self.guideline_to_faqs:
            self.guideline_to_faqs[guideline.id] = []
        if faq not in self.guideline_to_faqs[guideline.id]:
            self.guideline_to_faqs[guideline.id].append(faq)

    def get_guideline_to_faqs(self, guideline):
        if guideline.id in self.guideline_to_faqs:
            return self.guideline_to_faqs.get(guideline.id)
        return []

    def get_faq_to_guidelines(self, faq):
        if faq.id in self.faq_to_guidelines:
            return self.faq_to_guidelines.get(faq.id)
        return []

    def associate_faq_with_check(self, faq, check):
        if faq.id not in self.faq_to_checks:
            self.faq_to_checks[faq.id] = []
        if check not in self.faq_to_checks[faq.id]:
            self.faq_to_checks[faq.id].append(check)
        if check.id not in self.check_to_faqs:
            self.check_to_faqs[check.id] = []
        if faq not in self.check_to_faqs[check.id]:
            self.check_to_faqs[check.id].append(faq)

    def get_faq_to_checks(self, faq):
        if faq.id in self.faq_to_checks:
            return self.faq_to_checks.get(faq.id)
        return []

    def get_check_to_faqs(self, check):
        if check.id in self.check_to_faqs:
            return self.check_to_faqs.get(check.id)
        return []

    def associate_faq_with_tag(self, faq, tag):
        if faq.id not in self.faq_to_tags:
            self.faq_to_tags[faq.id] = []
        if tag not in self.faq_to_tags[faq.id]:
            self.faq_to_tags[faq.id].append(tag)
        if tag.id not in self.tag_to_faqs:
            self.tag_to_faqs[tag.id] = []
        if faq not in self.tag_to_faqs[tag.id]:
            self.tag_to_faqs[tag.id].append(faq)

    def get_faq_to_tags(self, faq):
        if faq.id in self.faq_to_tags:
            return sorted(self.faq_to_tags.get(faq.id), key=lambda item: item.id)
        return []

    def get_tag_to_faqs(self, tag):
        if tag.id in self.tag_to_faqs:
            return self.tag_to_faqs.get(tag.id)
        return []

    def associate_faq_with_info(self, faq, info):
        if faq.id not in self.faq_to_info:
            self.faq_to_info[faq.id] = []
        if info not in self.faq_to_info[faq.id]:
            self.faq_to_info[faq.id].append(info)
        if info.id not in self.info_to_faqs:
            self.info_to_faqs[info.id] = []
        if faq not in self.info_to_faqs[info.id]:
            self.info_to_faqs[info.id].append(faq)

    def get_faq_to_info(self, faq):
        if faq.id in self.faq_to_info:
            return self.faq_to_info.get(faq.id)
        return []

    def get_info_to_faqs(self, info):
        if info.id in self.info_to_faqs:
            return self.info_to_faqs.get(info.id)
        return []

class Guideline:
    all_guidelines = {}

    def __init__(self, gl):
        self.id = gl['id']
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
        rel.set_guideline_category(self)
        for check_id in gl['checks']:
            rel.associate_guideline_with_check(self, Check.get_by_id(check_id))
        for sc in gl['sc']:
            rel.associate_guideline_with_sc(self, WcagSc.get_by_id(sc))

        if 'info' in gl:
            for info in gl['info']:
                rel.associate_guideline_with_info(self, InfoRef(info))

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
            'checks': [check.template_object(lang, platform=self.platform) for check in rel.guideline_to_checks.get(self.id)],
            'scs': [sc.template_object(lang) for sc in rel.get_guideline_to_scs(self)],
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
        return [guideline.src_path for guideline in cls.all_guidelines.values()]
class Check:
    all_checks = {}

    def __init__(self, check):
        self.id = check['id']
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
        # if 'platform' in kwargs:
        gl_platform = kwargs.get('platform')
        # else:
            # gl_platform = []
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
        return [cls.all_checks[check_id].template_object(lang) for check_id in sorted_checks]

    @classmethod
    def list_all_src_paths(cls):
        return [check.src_path for check in cls.all_checks.values()]

class Faq:
    all_faqs = {}

    def __init__(self, faq):
        self.id = faq['id']
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
                rel.associate_faq_with_guideline(self, Guideline.get_by_id(guideline_id))

        for tag in faq['tags']:
            rel.associate_faq_with_tag(self, FaqTag.get_by_id(tag))

        if 'checks' in faq:
            for check_id in faq['checks']:
                rel.associate_faq_with_check(self, Check.get_by_id(check_id))

        if 'info' in faq:
            for info in faq['info']:
                rel.associate_faq_with_info(self, InfoRef(info))

        Faq.all_faqs[self.id] = self

    def get_dependency(self):
        rel = RelationshipManager()
        dependency = [self.src_path]
        guidelines = rel.get_faq_to_guidelines(self)
        if len(guidelines):
            dependency.extend([guideline.src_path for guideline in guidelines])
        checks = rel.get_faq_to_checks(self)
        if len(checks):
            dependency.extend([check.src_path for check in checks])
        return uniq(dependency)

    def template_object(self, lang):
        rel = RelationshipManager()
        tags = rel.get_faq_to_tags(self)
        template_object = {
            'id': self.id,
            'updated': self.updated,
            'updated_year': self.updated.year,
            'updated_month': self.updated.month,
            'updated_day': self.updated.day,
            'title': self.title[lang],
            'problem': self.problem[lang],
            'solution': self.solution[lang],
            'explanation': self.explanation[lang],
            'tags': [tag.id for tag in tags],
        }
        guidelines = rel.get_faq_to_guidelines(self)
        if len(guidelines):
            sorted_guidelines = sorted(guidelines, key=lambda item: item.sort_key)
            template_object['guidelines'] = [guideline.get_category_and_id(lang) for guideline in sorted_guidelines]
        checks = rel.get_faq_to_checks(self)
        if len(checks):
            sorted_checks = sorted(checks, key=lambda item: item.id)
            template_object['checks'] = [{'id': check.id, 'check': check.check[lang]} for check in sorted_checks]
        info = rel.get_faq_to_info(self)
        if len(info):
            template_object['info'] = [inforef.refstring() for inforef in info]
        return template_object

    @classmethod
    def list_all(cls, **kwargs):
        if 'sort_by' in kwargs:
            if kwargs['sort_by'] == 'date':
                return sorted(cls.all_faqs.values(), key=lambda faq: faq.updated, reverse=True)
        return sorted(cls.all_faqs.values(), key=lambda faq: faq.sort_key)

    @classmethod
    def list_all_src_paths(cls):
        return [faq.src_path for faq in cls.all_faqs.values()]

class Category:
    all_categories = {}

    def __init__(self, category_id, names):
        self.id = category_id
        self.names = names
        self.guidelines = []
        Category.all_categories[category_id] = self

    def add_guideline(self, guideline):
        if guideline in self.guidelines:
            return
        self.guidelines.append(guideline)
        guideline.set_category(self)

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

    def template_object(self, lang):
        rel = RelationshipManager()
        template_object =  {
            'sc': self.scnum,
            'level': self.level,
            'LocalLevel': self.local_priority,
            'sc_en_title': self.title['en'],
            'sc_ja_title': self.title['ja'],
            'sc_en_url': self.url['en'],
            'sc_ja_url': self.url['ja']
        }
        guidelines = rel.get_sc_to_guidelines(self)
        if len(guidelines) > 0:
            template_object['guidelines'] = [guideline.get_category_and_id(lang) for guideline in guidelines]
        return template_object

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
        return [inforef for inforef in cls.all_inforefs.values() if not inforef.internal]


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
