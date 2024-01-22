import os
import sys
import re
import yaml
import json
import unicodedata
import copy
from jsonschema import validate, ValidationError, RefResolver
import argparse
from jinja2 import Template, Environment, FileSystemLoader
import datetime
from config import AVAILABLE_LANGUAGES

GUIDELINES_SRCDIR = 'data/yaml/gl'
INFO_SRC = 'data/json/info.json'
CHECKS_SRCDIR = 'data/yaml/checks'
FAQ_SRCDIR = 'data/yaml/faq'
SCHEMA_SRCDIR = 'data/json/schemas'
DESTDIR = 'source/inc'
GUIDELINES_DESTDIR = DESTDIR + '/gl'
CHECKS_DESTDIR = DESTDIR + '/checks'
FAQ_DESTDIR = 'source/faq'
FAQ_INDEX_FILENAME = 'index.rst'
FAQ_INDEX_PATH = os.path.join(os.getcwd(), FAQ_DESTDIR, FAQ_INDEX_FILENAME)
FAQ_ARTICLES_DESTDIR = FAQ_DESTDIR + '/articles'
FAQ_ARTICLE_INDEX_PATH = os.path.join(os.getcwd(), FAQ_ARTICLES_DESTDIR, FAQ_INDEX_FILENAME)
FAQ_TAGPAGES_DESTDIR = FAQ_DESTDIR + '/tags'
FAQ_TAG_INDEX_PATH = os.path.join(os.getcwd(), FAQ_TAGPAGES_DESTDIR, FAQ_INDEX_FILENAME)
INFO_TO_GL_DESTDIR = DESTDIR + '/info2gl'
INFO_TO_FAQ_DESTDIR = DESTDIR + '/info2faq'
MISC_DESTDIR = DESTDIR + '/misc'
MAKEFILE_FILENAME = 'incfiles.mk'
ALL_CHECKS_FILENAME = "allchecks.rst"
ALL_CHECKS_PATH = os.path.join(os.getcwd(), CHECKS_DESTDIR, ALL_CHECKS_FILENAME)
WCAG_MAPPING_FILENAME = "wcag21-mapping.rst"
WCAG_MAPPING_PATH = os.path.join(os.getcwd(), MISC_DESTDIR, WCAG_MAPPING_FILENAME)
PRIORITY_DIFF_FILENAME = "priority-diff.rst"
PRIORITY_DIFF_PATH = os.path.join(os.getcwd(), MISC_DESTDIR, PRIORITY_DIFF_FILENAME)
MISCDEFS_FILENAME = "defs.txt"
MISCDEFS_PATH = os.path.join(os.getcwd(), MISC_DESTDIR, MISCDEFS_FILENAME)
WCAG_SC = 'data/json/wcag-sc.json'
GUIDELINE_CATEGORIES = 'data/json/guideline-categories.json'
FAQ_TAGS = 'data/json/faq-tags.json'
TEMPLATE_DIR = 'templates'
GUIDELINES_SCHEMA = 'guideline.json'
CHECKS_SCHEMA = 'check.json'
FAQS_SCHEMA = 'faq.json'
COMMON_SCHEMA = 'common.json'

# Values which needs to be changed if there are some changes in the checklist/item structure:
CHECK_TOOLS = {
    'nvda': 'NVDA',
    'macos-vo': 'macOS VoiceOver',
    'axe': 'axe DevTools',
    'ios-vo': 'iOS VoiceOver',
    'android-tb': 'Android TalkBack',
    'keyboard': 'キーボード操作',
    'misc': 'その他のツール'
}
IMPLEMENTATION_NAMES = {
    'web': 'Web',
    'ios': 'iOS',
    'android': 'Android'
}
TARGET_NAMES = {
    'design': 'デザイン',
    'code': 'コード',
    'product': 'プロダクト'
}
PLATFORM_NAMES = {
    'web': 'Web',
    'mobile': 'モバイル',
    'general': 'Web、モバイル'
}


def main():
    args = parse_args()
    settings = process_arguments(args)
    build_all = settings.get('build_all')
    targets = settings.get('targets')
    LANG = settings.get('lang')

    template_env = setup_template_environment()
    templates = load_templates(template_env)

    build_examples = []

    if not args.no_check:
        common_schema_path = os.path.join(os.getcwd(), SCHEMA_SRCDIR, COMMON_SCHEMA)
        try:
            file_content = read_file_content(common_schema_path)
            common_schema = json.loads(file_content)
        except Exception as e:
            handle_file_error(e, common_schema_path)
        schema_path = 'file://{}/'.format(os.path.join(os.getcwd(), SCHEMA_SRCDIR))
        resolver = RefResolver(schema_path, common_schema)

    files = ls_dir(os.path.join(os.getcwd(), GUIDELINES_SRCDIR))
    guidelines = []
    for f in files:
        guidelines.append(process_yaml_file(f, os.path.join(os.getcwd(), SCHEMA_SRCDIR), GUIDELINES_SCHEMA, args.no_check, resolver))

    guidelines = sorted(guidelines, key=lambda x: x['sortKey'])

    files = ls_dir(os.path.join(os.getcwd(), CHECKS_SRCDIR))
    checks = []
    for f in files:
        checks.append(process_yaml_file(f, os.path.join(os.getcwd(), SCHEMA_SRCDIR), CHECKS_SCHEMA, args.no_check, resolver))

    files = ls_dir(os.path.join(os.getcwd(), FAQ_SRCDIR))
    faqs = []
    for f in files:
        faqs.append(process_yaml_file(f, os.path.join(os.getcwd(), SCHEMA_SRCDIR), FAQS_SCHEMA, args.no_check, resolver))

    faqs = sorted(faqs, key=lambda x: x['sortKey'])

    if not args.no_check:
        check_duplicate_values(guidelines, 'id', 'Guideline ID')
        check_duplicate_values(guidelines, 'sortKey', 'Guideline sortKey')
        check_duplicate_values(checks, 'id', 'Check ID')
        check_duplicate_values(faqs, 'id', 'FAQ ID')
        check_duplicate_values(faqs, 'sortKey', 'FAQ sortKey')

    try:
        file_content = read_file_content(WCAG_SC)
        wcag_sc = json.loads(file_content)
    except Exception as e:
        handle_file_error(e, WCAG_SC)

    try:
        file_content = read_file_content(GUIDELINE_CATEGORIES)
        category_names = json.loads(file_content)
    except Exception as e:
        handle_file_error(e, GUIDELINE_CATEGORIES)

    try:
        file_content = read_file_content(FAQ_TAGS)
        faq_tags = json.loads(file_content)
    except Exception as e:
        handle_file_error(e, FAQ_TAGS)

    for sc in wcag_sc:
        wcag_sc[sc]['gls'] = []
        wcag_sc[sc]['en']['linkCode'] = f'`{wcag_sc[sc]["en"]["title"]} <{wcag_sc[sc]["en"]["url"]}>`_'
        wcag_sc[sc]['ja']['linkCode'] = f'`{wcag_sc[sc]["ja"]["title"]} <{wcag_sc[sc]["ja"]["url"]}>`_'

    category_pages = {}
    guideline_category_target = []
    for cat in category_names:
        category_pages[cat] = {
            'guidelines': [],
            'dependency': []
        }
        guideline_category_target.append(os.path.join(GUIDELINES_DESTDIR, f'{cat}.rst'))

    gl_categories = {}
    info_to_gl = {}
    for gl in guidelines:
        gl_categories[gl['id']] = category_names[gl['category']][LANG]
        for sc in gl['sc']:
            wcag_sc[sc]['gls'].append(gl['id'])

        if not 'info' in gl:
            continue
        for info in gl['info']:
            if re.match(r'(https?://|\|.+\|)', info):
                continue
            if info not in info_to_gl:
                info_to_gl[info] = []
            info_to_gl[info].append({
                'id': gl['id'],
                'category': gl_categories[gl['id']],
                'sortKey': gl['sortKey']
            })

        for faq in faqs:
            if not 'guidelines' in faq:
                continue
            if gl['id'] in faq['guidelines']:
                if 'faqrefs' not in gl:
                    gl['faq_ref'] = []
                gl['faq_ref'].append(faq["id"])

    allchecks = []
    check_examples = {}
    for key in CHECK_TOOLS:
        check_examples[key] = []

    for check in sorted(checks, key=lambda x: x['id']):
        if f'data/yaml/checks/{check["target"]}/{check["id"]}.yaml' != check['src_path']:
            raise Exception(f'The file path does not match the ID and/or the target in {check["src_path"]}')

        check['severity'] = f"[{check['severity'].upper()}]"
        check['gl_ref'] = []
        check['info'] = []
        for gl in guidelines:
            if check["id"] in gl['checks']:
                check['gl_ref'].append(gl["id"])
                if 'info' in gl:
                    check['info'].extend(gl['info'])

        if len(check['gl_ref']) == 0:
            raise Exception(f'The check {check["id"]} is not referred to from any guideline.')

        check['faq_ref'] = []
        for faq in faqs:
            if not 'checks' in faq:
                continue
            if check["id"] in faq['checks']:
                check['faq_ref'].append(faq["id"])

        check_str = {
            'target': TARGET_NAMES[check['target']],
            'platform': '、'.join(list(map(lambda item: PLATFORM_NAMES[item], check['platform']))),
            'id': check['id'],
            'severity': check['severity'],
            'check': check['check'][LANG],
        }
        if len(check['info']) > 0:
            check['info'] = uniq(check['info'])
            check_str['inforefs'] = []
            for info in check['info']:
                if re.match(r'(https?://|\|.+\|)', info):
                    check_str['inforefs'].append(info)
                else:
                    check_str['inforefs'].append(f':ref:`{info}`')

        if len(check['faq_ref']) > 0:
            check_str['faqrefs'] = []
            for faq in check['faq_ref']:
                check_str['faqrefs'].append(f':ref:`faq-{faq}`')

        check_str['gl_refs'] = []
        for ref in check['gl_ref']:
            check_str['gl_refs'].append({
                'category': gl_categories[ref],
                'glref': ref
                })

        if check['target'] == 'code' and 'implementations' in check:
            check_str['implementations'] = []
            for detail in check['implementations']:
                implementation = {
                    'title': detail['title'],
                    'examples': []
                }

                for impl in detail['methods']:
                    implementation['examples'].append({
                        'platform': IMPLEMENTATION_NAMES[impl['platform']],
                        'method': impl['method']
                    })
                check_str['implementations'].append(implementation)
        elif check['target'] == 'product' and 'procedures' in check:
            check_str['procedures'] = []
            for procedure in check['procedures']:
                procedure_str_obj = {}
                procedure_str_obj = {
                    'platform': PLATFORM_NAMES[procedure['platform']],
                    'text': procedure['procedure'][LANG]
                }

                if 'techniques' in procedure:
                    procedure_str_obj['techniques'] = []
                    if 'checkTools' not in check:
                        check['checkTools'] = []
                    for technique in procedure['techniques']:
                        if technique['tool'] in CHECK_TOOLS:
                            tool_basename = technique['tool']
                            tool_display_name = CHECK_TOOLS[technique['tool']]
                        else:
                            tool_basename = 'misc'
                            tool_display_name = technique['tool']

                        str_obj = {
                            'tool_display_name': tool_display_name,
                            'technique': technique['technique'][LANG],
                            'tool': tool_basename,
                            'id': check['id'],
                            'check': check['check'][LANG],
                        }
                        if 'note' in technique:
                            str_obj['note'] = technique['note'][LANG]
                        if 'YouTube' in technique:
                            str_obj['YouTube'] = technique['YouTube']
                        check['checkTools'].append(tool_basename)
                        procedure_str_obj['techniques'].append(str_obj)
                        check_examples[tool_basename].append(str_obj)

                check_str['procedures'].append(procedure_str_obj)

        allchecks.append(check_str)
        check['check_str'] = check_str

    info_to_faq = {}
    for faq in faqs:
        if not 'info' in faq:
            continue
        for info in faq['info']:
            if not info in info_to_faq:
                info_to_faq[info] = []
            info_to_faq[info].append({
                'id': faq['id'],
                'label': f'faq-{faq["id"]}',
                'sortKey': faq['sortKey']
            })

    for gl in guidelines:
        category_pages[gl['category']]['dependency'].append(gl['src_path'])
        gl_str = {
            'title': gl['title'][LANG],
            'intent': gl['intent'][LANG],
            'id': gl['id'],
            'platform': '、'.join(list(map(lambda item: PLATFORM_NAMES[item], gl['platform']))),
            'guideline': gl['guideline'][LANG]
        }

        if 'info' in gl:
            gl_str['info'] = []
            for ref in gl['info']:
                if re.match(r'(https?://|\|.+\|)', ref):
                    gl_str['info'].append(ref)
                else:
                    gl_str['info'].append(f':ref:`{ref}`')

        if 'faq_ref' in gl:
            gl_str['faqrefs'] = []
            for faq in gl['faq_ref']:
                gl_str['faqrefs'].append(f':ref:`faq-{faq}`')

        gl_str['checks'] = []
        gl['examples'] = []
        for check in gl['checks']:
            _check = [x for x in checks if x["id"] == check][0]
            _check_str = copy.deepcopy(_check['check_str'])
            if 'checkTools' in _check:
                gl['examples'].extend(list(_check['checkTools']))
            if 'procedures' in _check:
                for i, proc in enumerate(_check['procedures']):
                    if proc['platform'] == 'general' or proc['platform'] in gl['platform']:
                        continue
                    del _check_str['procedures'][i]

            gl_str['checks'].append(_check_str)
            category_pages[gl['category']]['dependency'].append(_check['src_path'])

        gl_str['scs'] = []
        for sc in gl['sc']:
            gl_str['scs'].append({
                'sc': sc,
                'sc_en': wcag_sc[sc]['en']['linkCode'],
                'sc_ja': wcag_sc[sc]['ja']['linkCode'],
                'sc_level': wcag_sc[sc]['level']
            })

        category_pages[gl['category']]['guidelines'].append(gl_str)
        if len(gl['examples']) > 0:
            build_examples.extend(gl['examples'])
        build_examples = uniq(build_examples)

    os.makedirs(os.path.join(os.getcwd(), GUIDELINES_DESTDIR), exist_ok=True)
    for cat in category_pages:
        filename = f'{cat}.rst'
        destfile = os.path.join(os.getcwd(), GUIDELINES_DESTDIR, filename)
        if build_all or destfile in targets:
            write_rst(templates['category_page'], {'guidelines': category_pages[cat]['guidelines']}, destfile)

    os.makedirs(os.path.join(os.getcwd(), INFO_TO_GL_DESTDIR), exist_ok=True)
    for info in info_to_gl:
        filename = f'{info}.rst'
        destfile = os.path.join(os.getcwd(), INFO_TO_GL_DESTDIR, filename)
        if build_all or destfile in targets:
            write_rst(templates['info_to_gl'], {'guidelines': sorted(info_to_gl[info], key=lambda x: x['sortKey'])}, destfile)

    os.makedirs(os.path.join(os.getcwd(), INFO_TO_FAQ_DESTDIR), exist_ok=True)
    for info in info_to_faq:
        filename = f'{info}.rst'
        destfile = os.path.join(os.getcwd(), INFO_TO_FAQ_DESTDIR, filename)
        if build_all or destfile in targets:
            write_rst(templates['info_to_faq'], {'faqs': sorted(info_to_faq[info], key=lambda x: x['sortKey'])}, destfile)

    os.makedirs(os.path.join(os.getcwd(), FAQ_ARTICLES_DESTDIR), exist_ok=True)
    faq_articles = []
    faq_tagpages = {}
    for faq in faqs:
        faq_updated = datetime.datetime.fromisoformat(faq['updated'])
        faq_articles.append({
            'id': faq['id'],
            'sortKey': faq['sortKey'],
            'updated': faq_updated,
            'updated_year': faq_updated.year,
            'updated_month': faq_updated.month,
            'updated_day': faq_updated.day
        })
        article_filename = f'{faq["id"]}.rst'
        destfile = os.path.join(os.getcwd(), FAQ_ARTICLES_DESTDIR, article_filename)
        if build_all or destfile in targets:
            faq_obj = {
                'id': faq['id'],
                'title': faq['title'][LANG],
                'updated_year': faq_updated.year,
                'updated_month': faq_updated.month,
                'updated_day': faq_updated.day,
                'tags': faq['tags'],
                'problem': faq['problem'][LANG],
                'solution': faq['solution'][LANG],
                'explanation': faq['explanation'][LANG]
            }
            if 'checks' in faq:
                faq_obj['checks'] = []
                for c in faq['checks']:
                    faq_obj['checks'].append({
                        'id': c,
                        'check': [x for x in checks if x["id"] == c][0]['check'][LANG],
                    })
            if 'info' in faq:
                faq_obj['info'] = faq['info']
            if 'guidelines' in faq:
                faq_obj['guidelines'] = []
                for gl in faq['guidelines']:
                    faq_obj['guidelines'].append({
                        'id': gl,
                        'category': gl_categories[gl]
                    })
            faq['destpath'] = os.path.join(FAQ_ARTICLES_DESTDIR, article_filename)
            write_rst(templates['faq_article'], faq_obj, destfile)

        for tag in faq['tags']:
            try:
                if not tag in faq_tags:
                    raise ValueError(f'FAQ tag {tag} in {faq["id"]} is not defined in {FAQ_TAGS}')
            except ValueError as e:
                print(e, file=sys.stderr)
                sys.exit(1)
            if not tag in faq_tagpages:
                faq_tagpages[tag] = {
                    'tag': tag,
                    'label': faq_tags[tag][LANG],
                    'articles': [],
                    'count': 0
                }
            faq_tagpages[tag]['articles'].append(faq["id"])
            faq_tagpages[tag]['count'] += 1

    faq_tagpage_list = sorted(faq_tagpages.values(), key=lambda x: x['label'])

    os.makedirs(os.path.join(os.getcwd(), FAQ_TAGPAGES_DESTDIR), exist_ok=True)
    for page in faq_tagpage_list:
        filename = f'{page["tag"]}.rst'
        destfile = os.path.join(FAQ_TAGPAGES_DESTDIR, filename)
        if build_all or destfile in targets:
            write_rst(templates['faq_tagpage'], page, destfile)

    if build_all or FAQ_INDEX_PATH in targets:
        write_rst(templates['faq_index'], {'files': sorted(faq_articles, key=lambda x: x['updated'], reverse=True), 'tags': faq_tagpage_list}, FAQ_INDEX_PATH)

    if build_all or FAQ_TAG_INDEX_PATH in targets:
        write_rst(templates['faq_tag_index'], {'tags': faq_tagpage_list}, FAQ_TAG_INDEX_PATH)

    if build_all or FAQ_ARTICLE_INDEX_PATH in targets:
        write_rst(templates['faq_article_index'], {'files': sorted(faq_articles, key=lambda x: x['sortKey'])}, FAQ_ARTICLE_INDEX_PATH)

    os.makedirs(os.path.join(os.getcwd(), MISC_DESTDIR), exist_ok=True)
    if build_all or WCAG_MAPPING_PATH in targets:
        sc_mapping = []
        for sc in wcag_sc:
            if len(wcag_sc[sc]['gls']) == 0:
                continue
            gls = []
            for gl in wcag_sc[sc]['gls']:
                gls.append(f'*  {gl_categories[gl]}： :ref:`{gl}`')
            gls_str = '\n   '.join(gls)
            mapping = {
                'sc': sc,
                'sc_en': wcag_sc[sc]['en']['linkCode'],
                'sc_ja': wcag_sc[sc]['ja']['linkCode'],
                'level': wcag_sc[sc]['level'],
                'gls': gls_str
            }
            sc_mapping.append(mapping)
        write_rst(templates['wcag21mapping'], {'mapping': sc_mapping}, WCAG_MAPPING_PATH)

    if build_all or PRIORITY_DIFF_PATH in targets:
        diffs = []
        for sc in wcag_sc:
            if wcag_sc[sc]['level'] == wcag_sc[sc]['localPriority']:
                continue
            diff = {
                'sc': sc,
                'sc_en': wcag_sc[sc]['en']['linkCode'],
                'sc_ja': wcag_sc[sc]['ja']['linkCode'],
                'level': wcag_sc[sc]['level'],
                'LocalLevel': wcag_sc[sc]['localPriority']
            }
            diffs.append(diff)
        write_rst(templates['priority_diff'], {'diffs': diffs}, PRIORITY_DIFF_PATH)

    os.makedirs(os.path.join(os.getcwd(), CHECKS_DESTDIR), exist_ok=True)
    if build_all or ALL_CHECKS_PATH in targets:
        write_rst(templates['allchecks_text'], {'allchecks': allchecks}, ALL_CHECKS_PATH)

    if build_all or MISCDEFS_PATH in targets:
        try:
            file_content = read_file_content(INFO_SRC)
            info_links = json.loads(file_content)
        except Exception as e:
            handle_file_error(e, INFO_SRC)

        external_info_links = []
        for link in info_links:
            external_info_links.append({
                'label': link,
                'text': info_links[link]['text'][LANG],
                'url': info_links[link]['url'][LANG]
            })
        write_rst(templates['miscdefs'], {'links': external_info_links}, MISCDEFS_PATH)

    if build_all or len(build_examples):
        for tool in check_examples:
            if check_examples[tool] == '' or not tool in build_examples:
                continue
            filename = f'examples-{tool}.rst'
            destfile = os.path.join(os.getcwd(), CHECKS_DESTDIR, filename)
            write_rst(templates['tool_example'], {'examples': check_examples[tool]}, destfile)

    if build_all or MAKEFILE_FILENAME in targets:
        gl_yaml = []
        for obj in guidelines:
            gl_yaml.append(obj['src_path'])
        check_yaml = []
        for obj in checks:
            check_yaml.append(obj['src_path'])
        faq_yaml = []
        for obj in faqs:
            faq_yaml.append(obj['src_path'])
        all_yaml = gl_yaml + check_yaml + faq_yaml

        other_deps = []
        for cat in category_pages:
            target = os.path.join(GUIDELINES_DESTDIR, f'{cat}.rst')
            deps = " ".join(uniq(category_pages[cat]['dependency']))
            other_deps.append({
                'dep': f'{target}: {deps}',
                'target': target
            })
        check_example_target = []
        for tool in check_examples:
            if check_examples[tool] == '' or not tool in build_examples:
                continue
            target = os.path.join(CHECKS_DESTDIR, f'examples-{tool}.rst')
            check_example_target.append(target)
            _deps = []
            for ex in check_examples[tool]:
                _deps.append([x for x in checks if x["id"] == ex['id']][0]['src_path'])
            deps = " ".join(_deps)
            other_deps.append({
                'dep': f'{target}: {deps}',
                'target': target
            })
        faq_article_target = []
        for faq in faqs:
            target = os.path.join(FAQ_ARTICLES_DESTDIR, f'{faq["id"]}.rst')
            faq_article_target.append(target)
            _deps = []
            _deps.append(faq["src_path"])
            if 'guidelines' in faq:
                for gl in faq['guidelines']:
                    _deps.append([x for x in guidelines if x["id"] == gl][0]['src_path'])
            if 'checks' in faq:
                for c in faq['checks']:
                    _deps.append([x for x in checks if x["id"] == c][0]['src_path'])
            deps = " ".join(_deps)
            other_deps.append({
                'dep': f'{target}: {deps}',
                'target': target
            })
        faq_tagpage_target = []
        for tag in faq_tagpages:
            target = os.path.join(FAQ_TAGPAGES_DESTDIR, f'{tag}.rst')
            faq_tagpage_target.append(target)
            _deps = []
            for faq in faq_tagpages[tag]['articles']:
                _deps.append([x for x in faqs if x["id"] == faq][0]['src_path'])
            deps = " ".join(_deps)
            other_deps.append({
                'dep': f'{target}: {deps}',
                'target': target
            })

        info_to_faq_target = []
        for info in info_to_faq:
            target = os.path.join(INFO_TO_FAQ_DESTDIR, f'{info}.rst')
            deps = " ".join([faq['src_path'] for faq in faqs for id in [x['id'] for x in info_to_faq[info]] if faq.get('id') == id])
            info_to_faq_target.append(target)
            other_deps.append({
                'dep': f'{target}: {deps}',
                'target': target
            })
            
        info_to_gl_target = []
        for info in info_to_gl:
            target = os.path.join(INFO_TO_GL_DESTDIR, f'{info}.rst')
            deps = " ".join([guideline['src_path'] for guideline in guidelines for id in [x['id'] for x in info_to_gl[info]] if guideline.get('id') == id])
            info_to_gl_target.append(target)
            other_deps.append({
                'dep': f'{target}: {deps}',
                'target': target
            })
        faq_index_pages = []
        faq_index_pages.append(os.path.join(FAQ_DESTDIR, FAQ_INDEX_FILENAME))
        faq_index_pages.append(os.path.join(FAQ_ARTICLES_DESTDIR, FAQ_INDEX_FILENAME))        
        faq_index_pages.append(os.path.join(FAQ_TAGPAGES_DESTDIR, FAQ_INDEX_FILENAME))

        makefile_data = {
            'guideline_category_target': " ".join(guideline_category_target),
            'check_example_target': " ".join(check_example_target),
            'faq_tagpage_target': " ".join(faq_tagpage_target),
            'faq_article_target': " ".join(faq_article_target),
            'faq_index_target': " ".join(faq_index_pages),
            'wcag_mapping_target': os.path.join(MISC_DESTDIR, WCAG_MAPPING_FILENAME),
            'priority_diff_target': os.path.join(MISC_DESTDIR, PRIORITY_DIFF_FILENAME),
            'all_checks_target': os.path.join(CHECKS_DESTDIR, ALL_CHECKS_FILENAME),
            'wcag_sc': WCAG_SC,
            'gl_yaml': " ".join(gl_yaml),
            'check_yaml': " ".join(check_yaml),
            'faq_yaml': " ".join(faq_yaml),
            'all_yaml': " ".join(all_yaml),
            'info_to_gl_target': " ".join(info_to_gl_target),
            'info_to_faq_target': " ".join(info_to_faq_target),
            'other_deps': other_deps,
            'miscdefs_target': os.path.join(MISC_DESTDIR, MISCDEFS_FILENAME),
            'info_src': INFO_SRC
        }
        destfile = os.path.join(os.getcwd(),  MAKEFILE_FILENAME)
        write_rst(templates['makefile'], makefile_data, destfile)

def ls_dir(dir):
    files = []
    for currentDir, dirs, fs in os.walk(dir):
        for f in fs:
            files.append(os.path.join(currentDir, f))
    return files

def read_file_content(file_path):
    """
    Read and return the content of a file.

    Args:
        file_path: Path to the file.

    Returns:
        The content of the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise e

def handle_file_error(e, file_path):
    """
    Handle file-related errors.

    Args:
        e: The exception object.
        file_path: Path to the file that caused the error.
    """
    print(f"Error with file {file_path}: {e}", file=sys.stderr)
    sys.exit(1)

def read_yaml_file(file):
    try:
        with open(file, encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        print(f'Exception occurred while loading YAML {file}...', file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

    return data

def validate_data(data, schema_file, common_resolver=None):
    try:
        with open(schema_file) as f:
            schema = json.load(f)
    except Exception as e:
        print(f'Exception occurred while loading schema {schema_file}...', file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

    try:
        validate(data, schema, resolver=common_resolver)
    except ValidationError as e:
        raise ValueError("Validation failed.") from e

def process_yaml_file(file_path, schema_dir, schema_file, no_check, resolver):
    """
    Read, validate, and process a YAML file.

    Args:
        file_path: The path to the YAML file.
        schema_dir: The directory containing the schema file.
        schema_file: The schema file for validation.
        no_check: Boolean indicating whether to skip validation.
        resolver: The resolver for schema validation.

    Returns:
        The processed YAML data with an additional source path.
    """
    data = read_yaml_file(file_path)
    
    if not no_check:
        try:
            validate_data(data, os.path.join(schema_dir, schema_file), resolver)
        except ValueError as e:
            print(f'Exception occurred while validating {file_path}...', file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)

    data['src_path'] = os.path.relpath(file_path, start=os.getcwd())
    return data

def uniq(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

def make_heading(title, level, className=""):
    
    def _isMultiByte(c):
        return unicodedata.east_asian_width(c) in ['F', 'W', 'A']
        
    def _width(c):
        return 2 if _isMultiByte(c) else 1

    def width(s):
        return sum([_width(c) for c in s])
        
    # Modify heading_styles accordingly
    heading_styles = [('#', True), ('*', True), ('=', False), ('-', False), ('^', False), ('"', False)]
    
    if not 1 <= level <= len(heading_styles):
        raise ValueError(f'Invalid level: {level}. Must be between 1 and {len(heading_styles)}')

    char, overline = heading_styles[level - 1]
    line = char * width(title)

    heading_lines = []

    if className:
        heading_lines.append(f'.. rst-class:: {className}\n')

    if overline:
        heading_lines.append(line)

    heading_lines.append(title)
    heading_lines.append(line)

    return '\n'.join(heading_lines)

def check_duplicate_values(lst, key, dataset):
    # Extract the values for the given key across the list of dictionaries
    values = [d[key] for d in lst]

    # Find the non-unique values
    non_unique_values = [value for value in values if values.count(value) > 1]

    # Convert to set to remove duplicates
    non_unique_values = set(non_unique_values)

    # Check if there are any non-unique values and raise error if so
    if non_unique_values:
        raise ValueError(f"Duplicate values in {dataset}: {non_unique_values}")

def parse_args():
    parser = argparse.ArgumentParser(description="Process YAML files into rst files for the a11y-guidelines.")
    parser.add_argument('--no-check', action='store_true', help='Do not run various checks of YAML files')
    parser.add_argument('--lang', '-l', type=str, choices=AVAILABLE_LANGUAGES, default='ja', help=f'the language of the output file ({" ".join(AVAILABLE_LANGUAGES)})')
    parser.add_argument('files', nargs='*', help='Filenames')
    return parser.parse_args()

def process_arguments(args):
    """
    Process the command-line arguments to determine the build mode, target files, and other options.

    Args:
        args: The parsed command-line arguments.

    Returns:
        A dictionary containing settings derived from the command-line arguments.
    """
    settings = {
        'build_all': not args.files,
        'targets': args.files if args.files else [],
        'lang': args.lang
    }

    # 例：新しいオプション 'verbose' の処理
    # if hasattr(args, 'verbose'):
    #     settings['verbose'] = args.verbose

    return settings

def setup_template_environment():
    """
    Set up the Jinja2 template environment.

    Returns:
        The configured Jinja2 environment object.
    """
    template_env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), TEMPLATE_DIR))
    )
    template_env.filters['make_heading'] = make_heading
    return template_env

def load_templates(template_env):
    """
    Load the necessary templates using the provided Jinja2 environment.

    Args:
        template_env: The Jinja2 environment object.

    Returns:
        A dictionary of Jinja2 templates.
    """
    template_filenames = {
        'tool_example': 'checks/examples-tool.rst',
        'allchecks_text': 'checks/allchecks.rst',
        'category_page': 'gl-category.rst',
        'info_to_gl': 'info_to_gl.rst',
        'info_to_faq': 'info_to_faq.rst',
        'faq_article': 'faq/article.rst',
        'faq_tagpage': 'faq/tagpage.rst',
        'faq_index': 'faq/index.rst',
        'faq_tag_index': 'faq/tag-index.rst',
        'faq_article_index': 'faq/article-index.rst',
        'wcag21mapping': WCAG_MAPPING_FILENAME,
        'priority_diff': PRIORITY_DIFF_FILENAME,
        'makefile': MAKEFILE_FILENAME,
        'miscdefs': 'misc-defs.txt'
    }

    templates = {name: template_env.get_template(filename) for name, filename in template_filenames.items()}
    return templates

def write_rst(template, data, output_path):
    """
    Render a Jinja2 template with provided data and write the output to an RST file.

    Args:
        template: Jinja2 template object.
        data: Data to be used in the template.
        output_path: Path to the output RST file.

    Returns:
        None
    """
    rendered_content = template.render(data)
    with open(output_path, mode='w', encoding='utf-8', newline='\n') as file:
        file.write(rendered_content)

if __name__ == "__main__":
    main()
