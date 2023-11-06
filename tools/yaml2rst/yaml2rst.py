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

LANG = 'ja'
GUIDELINES_SRCDIR = 'data/yaml/gl'
INFO_SRC = 'data/json/info.json'
CHECKS_SRCDIR = 'data/yaml/checks'
SCHEMA_SRCDIR = 'data/json/schemas'
DESTDIR = 'source/inc'
MAKEFILE_FILENAME = 'incfiles.mk'
ALL_CHECKS_FILENAME = "allchecks.rst"
ALL_CHECKS_PATH = os.path.join(os.getcwd(), DESTDIR, ALL_CHECKS_FILENAME)
WCAG_MAPPING_FILENAME = "wcag21-mapping.rst"
WCAG_MAPPING_PATH = os.path.join(os.getcwd(), DESTDIR, WCAG_MAPPING_FILENAME)
PRIORITY_DIFF_FILENAME = "priority-diff.rst"
PRIORITY_DIFF_PATH = os.path.join(os.getcwd(), DESTDIR, PRIORITY_DIFF_FILENAME)
MISCDEFS_FILENAME = "misc-defs.txt"
MISCDEFS_PATH = os.path.join(os.getcwd(), DESTDIR, MISCDEFS_FILENAME)
WCAG_SC = 'data/json/wcag-sc.json'
GUIDELINE_CATEGORIES = 'data/json/guideline-categories.json'
TEMPLATE_DIR = 'templates'
GUIDELINES_SCHEMA = 'guideline.json'
CHECKS_SCHEMA = 'check.json'
COMMON_SCHEMA = 'common.json'

# Values which needs to be changed if there are some changes in the checklist/item structure:
CHECK_TOOLS = {
    'nvda': 'NVDA',
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
    if not args.files:
        build_all = True
    else:
        build_all = False
        targets = args.files

    template_env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), TEMPLATE_DIR))
        )
    template_env.filters['make_heading'] = make_heading

    tool_example_template = template_env.get_template('check-examples-tool.rst')
    allchecks_text_template = template_env.get_template('allchecks.rst')
    category_page_template = template_env.get_template('gl-category.rst')
    info_to_gl_template = template_env.get_template('info_to_gl.rst')
    wcag21mapping_template = template_env.get_template(WCAG_MAPPING_FILENAME)
    priority_diff_template = template_env.get_template(PRIORITY_DIFF_FILENAME)
    makefile_template = template_env.get_template(MAKEFILE_FILENAME)
    miscdefs_template = template_env.get_template("misc-defs.txt")

    build_examples = []

    if not args.no_check:
        try:
            with open(os.path.join(os.getcwd(), SCHEMA_SRCDIR, COMMON_SCHEMA)) as f:
                common_schema = json.load(f)
        except Exception as e:
            print(f'Exception occurred while reading {COMMON_SCHEMA}...', file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)

        schema_path = 'file://{}/'.format(os.path.join(os.getcwd(), SCHEMA_SRCDIR))
        resolver = RefResolver(schema_path, common_schema)

    files = ls_dir(os.path.join(os.getcwd(), GUIDELINES_SRCDIR))
    guidelines = []
    for f in files:
        guidelines.append(read_yaml_file(f))
        if not args.no_check:
            try:
                validate_data(guidelines[-1], os.path.join(os.getcwd(), SCHEMA_SRCDIR, GUIDELINES_SCHEMA), resolver)
            except ValueError as e:
                print(f'Exception occurred while validating {f}...', file=sys.stderr)
                print(e, file=sys.stderr)
                sys.exit(1)
        guidelines[-1]['src_path'] = f.replace(os.getcwd() + "/", "")

    guidelines = sorted(guidelines, key=lambda x: x['sortKey'])

    files = ls_dir(os.path.join(os.getcwd(), CHECKS_SRCDIR))
    checks = []
    for f in files:
        checks.append(read_yaml_file(f))
        if not args.no_check:
            try:
                validate_data(checks[-1], os.path.join(os.getcwd(), SCHEMA_SRCDIR, CHECKS_SCHEMA), resolver)
            except ValueError as e:
                print(f'Exception occurred while validating {f}...', file=sys.stderr)
                print(e, file=sys.stderr)
                sys.exit(1)
        checks[-1]['src_path'] = f.replace(os.getcwd() + "/", "")

    if not args.no_check:
        check_duplicate_values(guidelines, 'id', 'Guideline ID')
        check_duplicate_values(guidelines, 'sortKey', 'Guideline sortKey')
        check_duplicate_values(checks, 'id', 'Check ID')

    try:
        with open(WCAG_SC) as f:
            wcag_sc = json.load(f)
    except Exception as e:
        print(f'Exception occurred while reading {WCAG_SC}...', file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

    try:
        with open(GUIDELINE_CATEGORIES) as f:
            category_names = json.load(f)
    except Exception as e:
        print(f'Exception occurred while reading {GUIDELINE_CATEGORIES}...', file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

    for sc in wcag_sc:
        wcag_sc[sc]['gls'] = []
        wcag_sc[sc]['en']['linkCode'] = f'`{wcag_sc[sc]["en"]["title"]} <{wcag_sc[sc]["en"]["url"]}>`_'
        wcag_sc[sc]['ja']['linkCode'] = f'`{wcag_sc[sc]["ja"]["title"]} <{wcag_sc[sc]["ja"]["url"]}>`_'

    category_pages = {}
    guideline_category_rst = []
    for cat in category_names:
        category_pages[cat] = {
            'guidelines': [],
            'dependency': []
        }
        guideline_category_rst.append(os.path.join(DESTDIR, f'gl-category-{cat}.rst'))

    gl_categories = {}
    info_to_gl = {}
    for gl in guidelines:
        gl_categories[gl['id']] = category_names[gl['category']][LANG]
        for sc in gl['sc']:
            wcag_sc[sc]['gls'].append(gl['id'])

        if 'info' in gl:
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

    for gl in guidelines:
        category_pages[gl['category']]['dependency'].append(gl['src_path'])
        gl_str = {
            'title': gl['title'][LANG],
            'intent': gl['intent'],
            'id': gl['id'],
            'platform': '、'.join(list(map(lambda item: PLATFORM_NAMES[item], gl['platform']))),
            'guideline': gl['guideline']
        }

        if 'info' in gl:
            gl_str['info'] = []
            for ref in gl['info']:
                if re.match(r'(https?://|\|.+\|)', ref):
                    gl_str['info'].append(ref)
                else:
                    gl_str['info'].append(f':ref:`{ref}`')

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

        if len(gl['examples']):
            build_examples.extend(gl['examples'])

        build_examples = uniq(build_examples)

    os.makedirs(os.path.join(os.getcwd(), DESTDIR), exist_ok=True)

    for cat in category_pages:
        filename = f'gl-category-{cat}.rst'
        if build_all or os.path.join(DESTDIR, filename) in targets:
            output = category_page_template.render(guidelines = category_pages[cat]['guidelines'])
            destfile = os.path.join(os.getcwd(), DESTDIR, filename)
            with open(destfile, mode="w", encoding="utf-8", newline="\n") as f:
                f.write(output)

    for info in info_to_gl:
        filename = f'{info}.rst'
        if build_all or os.path.join(DESTDIR, filename) in targets:
            output = info_to_gl_template.render(guidelines = sorted(info_to_gl[info], key=lambda x: x['sortKey']))
            destfile = os.path.join(os.getcwd(), DESTDIR, filename)
            with open(destfile, mode="w", encoding="utf-8", newline="\n") as f:
                f.write(output)

    if build_all or os.path.join(DESTDIR, WCAG_MAPPING_FILENAME) in targets:
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

        sc_mapping_text = wcag21mapping_template.render({'mapping': sc_mapping})
        with open(WCAG_MAPPING_PATH, mode="w", encoding="utf-8", newline="\n") as f:
            f.write(sc_mapping_text)

    if build_all or os.path.join(DESTDIR, PRIORITY_DIFF_FILENAME) in targets:
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

        diffs_text = priority_diff_template.render({'diffs': diffs})
        with open(PRIORITY_DIFF_PATH, mode="w", encoding="utf-8", newline="\n") as f:
            f.write(diffs_text)

    if build_all or os.path.join(DESTDIR, ALL_CHECKS_FILENAME) in targets:
        allcheck_text = allchecks_text_template.render({'allchecks': allchecks})
        with open(ALL_CHECKS_PATH, mode="w", encoding="utf-8", newline="\n") as f:
            f.write(allcheck_text)

    if build_all or os.path.join(DESTDIR, MISCDEFS_FILENAME) in targets:
        try:
            with open(INFO_SRC, encoding='utf-8') as f:
                info_links = json.load(f)
        except Exception as e:
            print(f'Exception occurred while reading {INFO_SRC}...', file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)

        external_info_links = []
        for link in info_links:
            external_info_links.append({
                'label': link,
                'text': info_links[link]['text'][LANG],
                'url': info_links[link]['url'][LANG]
            })
        miscdefs_text = miscdefs_template.render({'links': external_info_links})
        with open(MISCDEFS_PATH, mode="w", encoding="utf-8", newline="\n") as f:
            f.write(miscdefs_text)

    if build_all or len(build_examples):
        for tool in check_examples:
            if check_examples[tool] == '' or not tool in build_examples:
                continue
            filename = f'check-examples-{tool}.rst'
            destfile = os.path.join(os.getcwd(), DESTDIR, filename)
            with open(destfile, mode="w", encoding="utf-8", newline="\n") as f:
                f.write(tool_example_template.render({'examples': check_examples[tool]}))

    if build_all or MAKEFILE_FILENAME in targets:
        gl_yaml = []
        for obj in guidelines:
            gl_yaml.append(obj['src_path'])
        all_yaml = []
        for obj in guidelines+checks:
            all_yaml.append(obj['src_path'])

        other_deps = []
        for cat in category_pages:
            target = os.path.join(DESTDIR, f'gl-category-{cat}.rst')
            deps = " ".join(uniq(category_pages[cat]['dependency']))
            other_deps.append({
                'dep': f'{target}: {deps}',
                'target': target
            })
        all_info = []
        for info in info_to_gl:
            target = os.path.join(DESTDIR, f'{info}.rst')
            deps = " ".join([guideline['src_path'] for guideline in guidelines for id in [x['id'] for x in info_to_gl[info]] if guideline.get('id') == id])
            all_info.append(target)
            other_deps.append({
                'dep': f'{target}: {deps}',
                'target': target
            })
        makefile_data = {
            'guideline_category_rst': " ".join(guideline_category_rst),
            'wcag_mapping_target': os.path.join(DESTDIR, WCAG_MAPPING_FILENAME),
            'priority_diff_target': os.path.join(DESTDIR, PRIORITY_DIFF_FILENAME),
            'all_checks_target': os.path.join(DESTDIR, ALL_CHECKS_FILENAME),
            'wcag_sc': WCAG_SC,
            'gl_yaml': " ".join(gl_yaml),
            'all_yaml': " ".join(all_yaml),
            'all_info': " ".join(all_info),
            'other_deps': other_deps,
            'miscdefs_target': os.path.join(DESTDIR, MISCDEFS_FILENAME),
            'info_src': INFO_SRC
        }
        makefile_str = makefile_template.render(makefile_data)

        destfile = os.path.join(os.getcwd(),  MAKEFILE_FILENAME)
        with open(destfile, mode="w", encoding="utf-8", newline="\n") as f:
            f.write(makefile_str)

def ls_dir(dir):
    files = []
    for currentDir, dirs, fs in os.walk(dir):
        for f in fs:
            files.append(os.path.join(currentDir, f))
    return files

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
    parser.add_argument('files', nargs='*', help='Filenames')
    return parser.parse_args()

if __name__ == "__main__":
    main()
