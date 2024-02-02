import datetime
import re
from urllib.parse import quote as url_encode
from config import CHECK_TARGETS, PLATFORM_NAMES, SEVERITY_TAGS, IMPLEMENTATION_TARGETS

class Guideline:
    all_guidelines = {}

    def __init__(self, gl):
        self.id = gl['id']
        self.sortKey = gl['sortKey']
        self.title = gl['title']
        self.platform = gl['platform']
        self.guideline = gl['guideline']
        self.intent = gl['intent']
        self.src_path = gl['src_path']
        self.category = None
        Category.get_by_id(gl['category']).add_guideline(self)
        self.checks = []
        self.faqs = []
        for check_id in gl['checks']:
            self.add_check(Check.get_by_id(check_id))
        self.sc = []
        for sc in gl['sc']:
            self.add_sc(WCAG_SC.get_by_id(sc))

        self.info = []
        if 'info' in gl:
            for info in gl['info']:
                self.add_info(InfoRef(info))

        Guideline.all_guidelines[self.id] = self

    def set_category(self, category):
        self.category = category
        category.add_guideline(self)

    def add_check(self, check):
        if check in self.checks:
            return
        self.checks.append(check)
        check.add_guideline(self)

    def add_faq(self, faq):
        if faq in self.faqs:
            return
        self.faqs.append(faq)
        faq.add_guideline(self)

    def add_sc(self, sc):
        if sc in self.sc:
            return
        self.sc.append(sc)
        sc.add_guideline(self)

    def add_info(self, info):
        if info in self.info:
            return
        self.info.append(info)
        for check in self.checks:
            check.add_info(info)
        if not info.internal:
            return
        info.add_guideline(self)

    def get_category_and_id(self, lang):
        return {
            'category': self.category.get_name(lang),
            'guideline': self.id
        }

    def template_object(self, lang):
        template_object = {
            'id': self.id,
            'title': self.title[lang],
            'platform': join_items(self.platform, lang),
            'guideline': self.guideline[lang],
            'intent': self.intent[lang],
            'category': self.category.names[lang],
            'checks': [check.template_object(lang, platform=self.platform) for check in self.checks],
            'scs': [sc.template_object(lang) for sc in self.sc]
        }
        if len(self.faqs):
            template_object['faqs'] = [faq.id for faq in sorted(self.faqs, key=lambda item: item.sortKey)]
        if len(self.info):
            template_object['info'] = [inforef.refstring() for inforef in self.info]
        return template_object

    @classmethod
    def get_by_id(cls, id):
        return cls.all_guidelines.get(id)

class Check:
    all_checks = {}

    def __init__(self, check):
        self.id = check['id']
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
        self.guidelines = []
        self.faqs = []
        self.info = []
        Check.all_checks[self.id] = self

    def add_guideline(self, guideline):
        if guideline in self.guidelines:
            return
        self.guidelines.append(guideline)

    def add_faq(self, faq):
        if faq in self.faqs:
            return
        self.faqs.append(faq)
        faq.add_check(self)

    def add_info(self, info):
        if info in self.info:
            return
        self.info.append(info)
        if not info.internal:
            return
        info.add_check(self)

    def procedure_platforms(self):
        return sorted(list(set([procedure.platform for procedure in self.procedures])))

    def template_object(self, lang, **kwargs):
        if 'platform' in kwargs:
            gl_platform = kwargs['platform']
        else:
            gl_platform = []
        template_object = {
            'id': self.id,
            'check': self.check[lang],
            'severity': SEVERITY_TAGS[self.severity][lang],
            'target': CHECK_TARGETS[self.target][lang],
            'platform': join_items(self.platform, lang),
            'guidelines': []
        }
        if len(self.procedures) > 0:
            if len(gl_platform) == 0:
                template_object['procedures'] = [procedure.template_object(lang) for procedure in self.procedures]
            else:
                template_object['procedures'] = []
                for proc in self.procedures:
                    proc_platform = proc.platform
                    if proc_platform == 'general' or proc_platform in gl_platform:
                        template_object['procedures'].append(proc.template_object(lang))
        if len(self.implementations) > 0:
            template_object['implementations'] = [implementation.template_object(lang) for implementation in self.implementations]
        if len(self.info) > 0:
            template_object['info_refs'] = [inforef.refstring() for inforef in self.info]
        if len(self.faqs) > 0:
            template_object['faqs'] = [faq.id for faq in sorted(self.faqs, key=lambda item: item.sortKey)]
        sorted_guidelines = sorted(self.guidelines, key=lambda item: item.sortKey)
        for gl in sorted_guidelines:
            template_object['guidelines'].append(gl.get_category_and_id(lang))
        return template_object

    @classmethod
    def get_by_id(cls, id):
        return cls.all_checks.get(id)

    @classmethod
    def template_object_all(cls, lang):
        sorted_checks = sorted(cls.all_checks, key=lambda x: cls.all_checks[x].id)
        return [cls.all_checks[check_id].template_object(lang) for check_id in sorted_checks]

class FAQ:
    all_faqs = {}

    def __init__(self, faq):
        self.id = faq['id']
        self.sortKey = faq['sortKey']
        self.updated = datetime.datetime.fromisoformat(faq['updated'])
        self.title = faq['title']
        self.problem = faq['problem']
        self.solution = faq['solution']
        self.explanation = faq['explanation']
        self.src_path = faq['src_path']
        self.guidelines = []
        if 'guidelines' in faq:
            for guideline_id in faq['guidelines']:
                self.add_guideline(Guideline.get_by_id(guideline_id))

        self.tags = []
        for tag in faq['tags']:
            self.add_tag(FAQ_Tag.get_by_id(tag))

        self.checks = []    
        if 'checks' in faq:
            for check_id in faq['checks']:
                self.add_check(Check.get_by_id(check_id))

        self.info = []
        if 'info' in faq:
            for info in faq['info']:
                self.add_info(InfoRef(info))

        FAQ.all_faqs[self.id] = self

    def add_guideline(self, guideline):
        if guideline in self.guidelines:
            return
        self.guidelines.append(guideline)
        guideline.add_faq(self)

    def add_check(self, check):
        if check in self.checks:
            return
        self.checks.append(check)
        check.add_faq(self)

    def add_tag(self, tag):
        if tag in self.tags:
            return
        self.tags.append(tag)
        tag.add_faq(self)



    def add_info(self, info):
        if info in self.info:
            return
        self.info.append(info)
        if not info.internal:
            return
        info.add_faq(self)

    def get_dependency(self):
        dependency = [self.src_path]
        if len(self.guidelines):
            dependency.extend([guideline.src_path for guideline in self.guidelines])
        if len(self.checks):
            dependency.extend([check.src_path for check in self.checks])
        return uniq(dependency)

    def template_object(self, lang):
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
            'tags': [tag.id for tag in sorted(self.tags, key=lambda item: item.id)],
        }
        if len(self.guidelines):
            sorted_guidelines = sorted(self.guidelines, key=lambda item: item.sortKey)
            template_object['guidelines'] = [guideline.get_category_and_id(lang) for guideline in sorted_guidelines]
        if len(self.checks):
            sorted_checks = sorted(self.checks, key=lambda item: item.id)
            template_object['checks'] = [{'id': check.id, 'check': check.check[lang]} for check in sorted_checks]
        if len(self.info):
            template_object['info'] = [inforef.refstring() for inforef in self.info]
        return template_object

    @classmethod
    def list_all(cls, **kwargs):
        if 'sort_by' in kwargs:
            if kwargs['sort_by'] == 'date':
                return sorted(cls.all_faqs.values(), key=lambda faq: faq.updated, reverse=True)
            elif kwargs['sort_by'] == 'sortKey':
                return sorted(cls.all_faqs.values(), key=lambda faq: faq.sortKey)
        return sorted(cls.all_faqs.values(), key=lambda faq: faq.sortKey)

class Category:
    all_categories = {}

    def __init__(self, id, names):
        self.id = id
        self.names = names
        self.guidelines = []
        Category.all_categories[id] = self

    def add_guideline(self, guideline):
        if guideline in self.guidelines:
            return
        self.guidelines.append(guideline)
        guideline.set_category(self)

    def get_name(self, lang):
        if lang in self.names:
            return self.names[lang]
        else:
            return self.names['ja']

    def get_guidelines(self):
        return sorted(self.guidelines, key=lambda item: item.sortKey)

    def get_dependency(self):
        dependency = []
        for guideline in self.guidelines:
            dependency.append(guideline.src_path)
            dependency.extend([check.src_path for check in guideline.checks])
            dependency.extend([faq.src_path for faq in guideline.faqs])
        return uniq(dependency)

    @classmethod
    def get_by_id(cls, id):
        return cls.all_categories.get(id)

    @classmethod
    def list_all(cls):
        return cls.all_categories.values()

class FAQ_Tag:
    all_tags = {}

    def __init__(self, id, names):
        self.id = id
        self.names = names
        self.faqs = []
        FAQ_Tag.all_tags[id] = self

    def article_count(self):
        return len(self.faqs)

    def add_faq(self, faq):
        if faq in self.faqs:
            return
        self.faqs.append(faq)
        faq.add_tag(self)

    def get_name(self, lang):
        if lang in self.names:
            return self.names[lang]
        else:
            return self.names['en']

    def get_faqs_ids(self):
        return sorted([str(faq.id) for faq in self.faqs])

    def get_dependency(self):
        dependency = [faq.src_path for faq in self.faqs]
        return uniq(dependency)

    def template_object(self, lang):
        if len(self.faqs) == 0:
            return None
        sorted_faqs = sorted(self.faqs, key=lambda item: item.sortKey)
        return {
            'tag': self.id,
            'label': self.names[lang],
            'articles': [faq.id for faq in sorted_faqs],
            'count': len(self.faqs)
        }

    @classmethod
    def get_by_id(cls, id):
        return cls.all_tags.get(id)

    @classmethod
    def list_all(cls, **kwargs):
        if 'sort_by' in kwargs:
            if kwargs['sort_by'] == 'count':
                return sorted(cls.all_tags.values(), key=lambda tag: tag.article_count(), reverse=True)
            elif kwargs['sort_by'] == 'label':
                return sorted(cls.all_tags.values(), key=lambda tag: tag.names['en'])
        return cls.all_tags.values()

class WCAG_SC:
    all_scs = {}

    def __init__(self, sc):
        self.id = sc['id']
        self.sortKey = sc['sortKey']
        self.level = sc['level']
        self.localPriority = sc['localPriority']
        self.title = {
            'ja': sc['ja']['title'],
            'en': sc['en']['title']
        }
        self.url = {
            'ja': sc['ja']['url'],
            'en': sc['en']['url']
        }
        self.guidelines = []
        WCAG_SC.all_scs[self.id] = self
       

    def add_guideline(self, guideline):
        if guideline in self.guidelines:
            return
        self.guidelines.append(guideline)
        guideline.add_sc(self)

    def template_object(self, lang):
        template_object =  {
            'sc': self.id,
            'sc_level': self.level,
            'LocalLevel': self.localPriority,
            'sc_en_title': self.title['en'],
            'sc_ja_title': self.title['ja'],
            'sc_en_url': self.url['en'],
            'sc_ja_url': self.url['ja']
        }
        if len(self.guidelines):
            sorted_guidelines = sorted(self.guidelines, key=lambda item: item.sortKey)
            template_object['guidelines'] = [guideline.get_category_and_id(lang) for guideline in sorted_guidelines]
        return template_object

    @classmethod
    def get_by_id(cls, id):
        return cls.all_scs.get(id)

    @classmethod
    def get_all(cls):
        sorted_keys = sorted(cls.all_scs.keys(), key=lambda sc: cls.all_scs[sc].sortKey)
        return {key: cls.get_by_id(key) for key in sorted_keys}

class InfoRef:
    all_inforefs = {}

    def __new__(cls, id, *args, **kwargs):
        if id in cls.all_inforefs:
            return cls.all_inforefs[id]
        else:
            instance = super(InfoRef, cls).__new__(cls)
            cls.all_inforefs[id] = instance
            return instance

    def __init__(self, inforef):
        if not hasattr(self, 'initialized'):
            self.ref = inforef
            self.id = url_encode(self.ref)
            self.internal = False if re.match(r'(https?://|\|.+\|)', self.ref) else True
            self.guidelines = []
            self.checks = []
            self.faqs = []
            self.initialized = True


    def add_guideline(self, guideline):
        if guideline in self.guidelines:
            return
        self.guidelines.append(guideline)
        guideline.add_info(self)

    def add_faq(self, faq):
        if faq in self.faqs:
            return
        self.faqs.append(faq)
        faq.add_info(self)

    def add_check(self, check):
        if check in self.checks:
            return
        self.checks.append(check)
        check.add_info(self)

    def refstring(self):
        if self.internal:
            return f':ref:`{self.ref}`'
        else:
            return self.ref

    def get_guidelines(self, lang):
        sorted_guidelines = sorted(self.guidelines, key=lambda item: item.sortKey)
        return [guideline.get_category_and_id(lang) for guideline in sorted_guidelines]

    def get_faqs(self):
        sorted_faqs = sorted(self.faqs, key=lambda item: item.sortKey)
        return [faq.id for faq in sorted_faqs]

    @classmethod
    def get_all_internals(cls):
        return [info for info in cls.all_inforefs.values() if info.internal]

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
            self.YouTube = YouTube(**kwargs['YouTube'])
        else:
            self.YouTube = None

    def template_object(self, lang):
        if not self.tool_display_name:
            self.tool_display_name = self.tool.get_name(lang)
        template_object = {
            'tool_display_name': self.tool_display_name,
            'technique': self.technique[lang]
        }
        if self.note:
            template_object['note'] = self.note[lang]        
        if self.YouTube:
            template_object['YouTube'] = self.YouTube.template_object()
        return template_object

class YouTube:
    def __init__(self, id, title):
        self.id = id
        self.title = title

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
            'title': self.title,
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
            'method': self.method
        }
    
class CheckTool:
    all_tools = {}

    def __init__(self, id, names):
        self.id = id
        self.names = names
        self.examples = []
        CheckTool.all_tools[id] = self

    def add_example(self, example):
        self.examples.append(example)

    def get_name(self, lang):
        if lang in self.names:
            return self.names[lang]
        else:
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
    def get_by_id(cls, id):
        return cls.all_tools.get(id)

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
