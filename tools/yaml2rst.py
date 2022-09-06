import os
import sys
import re
import yaml
import json
from jsonschema import validate, ValidationError

GUIDELINES_SRCDIR = 'data/yaml/gl'
CHECKS_SRCDIR = 'data/yaml/checks'
DESTDIR = 'source/inc'
MAKEFILE_FILENAME = 'incfiles.mk'
ALL_CHECKS_FILENAME = "allchecks.rst"
ALL_CHECKS_PATH = os.path.join(os.getcwd(), DESTDIR, ALL_CHECKS_FILENAME)
WCAG_MAPPING_FILENAME = "wcag21-mapping.rst"
WCAG_MAPPING_PATH = os.path.join(os.getcwd(), DESTDIR, WCAG_MAPPING_FILENAME)
PRIORITY_DIFF_FILENAME = "priority-diff.rst"
PRIORITY_DIFF_PATH = os.path.join(os.getcwd(), DESTDIR, PRIORITY_DIFF_FILENAME)
GUIDELINES_SCHEMA = 'data/json/schema/guideline.json'
CHECKS_SCHEMA = 'data/json/schema/check.json'
WCAG_SC = 'data/json/wcag-sc.json'

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
    'mobile': 'モバイル'
}
CATEGORY_NAMES = {
    'dynamic_content': '動的コンテンツ',
    'form': 'フォーム',
    'icon': 'アイコン',
    'image': '画像',
    'images_of_text': '画像化されたテキスト',
    'input_device': '入力ディバイス',
    'link': 'リンク',
    'login_session': 'ログイン・セッション',
    'markup': 'マークアップと実装',
    'multimedia': '音声・映像コンテンツ',
    'page': 'ページ全体',
    'text': 'テキスト'
}


def main():
    args = sys.argv
    argc = len(args)
    if argc == 1:
        build_all = True
    else:
        build_all = False
        targets = args[1:argc]

    build_examples = []

    guidelines = read_yaml(os.path.join(os.getcwd(), GUIDELINES_SRCDIR), os.path.join(os.getcwd(), GUIDELINES_SCHEMA))
    guidelines = sorted(guidelines, key=lambda x: x['sortKey'])
    checks = read_yaml(os.path.join(os.getcwd(), CHECKS_SRCDIR), os.path.join(os.getcwd(), CHECKS_SCHEMA))

    try:
        with open(WCAG_SC) as f:
            wcag_sc = json.load(f)
    except Exception as e:
        print(f'Exception occurred while reading {WCAG_SC}...', file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

    for sc in wcag_sc:
        wcag_sc[sc]['gls'] = []
        wcag_sc[sc]['en']['linkCode'] = f'`{wcag_sc[sc]["en"]["title"]} <{wcag_sc[sc]["en"]["url"]}>`_'
        wcag_sc[sc]['ja']['linkCode'] = f'`{wcag_sc[sc]["ja"]["title"]} <{wcag_sc[sc]["ja"]["url"]}>`_'

    gl_categories = {}
    for gl in guidelines:
        gl_categories[gl['id']] = CATEGORY_NAMES[gl['category']]
        for sc in gl['sc']:
            wcag_sc[sc]['gls'].append(gl['id'])

    allcheck_text = ''
    check_examples = {}
    for key in CHECK_TOOLS:
        check_examples[key] = ''

    for check in sorted(checks, key=lambda x: x['id']):
        if f'data/yaml/checks/{check["target"]}/{check["id"]}.yaml' != check['src_path']:
            raise Exception(f'The file path does not match the ID and/or the target in {check["src_path"]}')

        check['gl_ref'] = []
        check['info'] = []
        for gl in guidelines:
            if check["id"] in gl['checks']:
                check['gl_ref'].append(gl["id"])
                if 'info' in gl:
                    check['info'].extend(gl['info'])

        if len(check['gl_ref']) == 0:
            raise Exception(f'The check {check["id"]} is not referred to from any guideline.')

        allcheck_info = ''
        if len(check['info']) > 0:
            check['info'] = uniq(check['info'])
            allcheck_info = make_header('参考情報', '=')
            for info in check['info']:
                if re.match(r'(https?://|\|.+\|)', info):
                    allcheck_info += f'*  {info}\n'
                else:
                    allcheck_info += f'*  :ref:`{info}`\n'

        target = TARGET_NAMES[check['target']]
        gl_check_title = make_header(f':ref:`check-{check["id"]}`', '-')
        allcheck_title = make_header(f'チェックID：{check["id"]}', '*', True)

        gl_ref_text = '関連ガイドライン\n'
        for ref in check['gl_ref']:
            gl_category = gl_categories[ref]
            gl_ref_text += f'   *  {gl_category}： :ref:`{ref}`\n'

        gl_check_details = ''
        allcheck_details = ''
        if check['target'] == 'code' and 'implementation' in check:
            for detail in check['implementation']:
                gl_check_details += make_header('実装方法の例：' + detail['title'], '^')
                allcheck_details += make_header('実装方法の例：' + detail['title'], '=')

                for impl in detail:
                    if impl == 'title':
                        continue
                    str = detail.get(impl)
                    gl_check_details += IMPLEMENTATION_NAMES[impl] + "\n" + indent(str, 3)
                    allcheck_details += impl + "\n" + indent(str, 3)
        elif check['target'] == 'product' and 'checkMeans' in check:
            check['checkMeansTools'] = []
            for means in check['checkMeans']:
                tool = means['tool']
                check['checkMeansTools'].append(tool)
                check_example_title = make_header(f':ref:`check-{check["id"]}`', '*', True)
                gl_check_details += make_header(f'{CHECK_TOOLS[tool]}によるチェック実施方法の例', '^') + means['means'] + '\n'
                allcheck_details += make_header(f'{CHECK_TOOLS[tool]}によるチェック実施方法の例', '=') + means['means'] + '\n'
                check_examples[tool] += '''\
.. _check-example-{means}-{id}:
{title}
{check}
{example}

'''.format(means = tool, id = check['id'], title = check_example_title, check = indent(check['check'], 3), example = means['means'])

        metainfo = f'対象\n   {target}\n'
        if 'platform' in check:
            platforms = list(map(lambda item: PLATFORM_NAMES[item], check['platform']))
            platform_str = '、'.join(platforms)
            metainfo += f'対象プラットフォーム\n   {platform_str}\n'
        if 'severity' in check:
            metainfo += f'重篤度\n   {check["severity"]}\n'
        metainfo += '\n'

        check['gl_check_text'] = """\
{title}{metainfo}
{check}
{details}
""".format(title = gl_check_title, metainfo = metainfo, check = check['check'], details = gl_check_details)

        allcheck_text += """\
.. _check-{id}:
{title}{metainfo}{gl_ref}
{check}
{info}
{details}
""".format(id = check["id"], title = allcheck_title, metainfo = metainfo, gl_ref = gl_ref_text, check = check['check'], details = allcheck_details, info = allcheck_info)

    intent_title = make_header('意図', '=')
    check_title = make_header('チェック内容', '=')
    sc_title = make_header('対応するWCAG 2.1の達成基準', '=')
    info_title = make_header('参考情報', '=')
    guidelines_rst = []
    guidelines_rst_depends = []

    for gl in guidelines:
        gl['depends'] = [gl['src_path']]
        gl_str = {
            'title': make_header(gl['title'], "*", True),
            'intent': intent_title + gl['intent'],
            'id': gl["id"],
            'guideline': gl['guideline'],
            'info': ''
        }

        gl_platforms = list(map(lambda item: PLATFORM_NAMES[item], gl['platform']))
        gl_platform_str = '、'.join(gl_platforms)
        gl_str['metainfo'] = f'優先度\n   {gl["priority"]}\n対象プラットフォーム\n   {gl_platform_str}\n\n'

        if 'info' in gl:
            gl_str['info'] = info_title
            for ref in gl['info']:
                if re.match(r'(https?://|\|.+\|)', ref):
                    gl_str['info'] += f'*  {ref}\n'
                else:
                    gl_str['info'] += f'*  :ref:`{ref}`\n'

        gl_str['checks'] = check_title
        gl['examples'] = []
        for check in gl['checks']:
            _check = [x for x in checks if x["id"] == check][0]
            if 'checkMeans' in _check:
                gl['examples'].extend(list(_check['checkMeansTools']))
            gl_str['checks'] += _check['gl_check_text']
            gl['depends'].append(_check['src_path'])
        gl_str['scs'] = sc_title
        for sc in gl['sc']:
            gl_str['scs'] += """\
SC {sc}：
   -  {linkCode_en}
   -  {linkCode_ja}
""".format(
           sc=sc,
           linkCode_en = wcag_sc[sc]['en']['linkCode'],
           linkCode_ja = wcag_sc[sc]['ja']['linkCode']
        )

        output = """\
.. _{0[id]}:
{0[title]}{0[metainfo]}{0[guideline]}

{0[intent]}
{0[scs]}
{0[info]}
{0[checks]}\
""".format(gl_str)

        filename = gl["id"] + '.rst'
        make_target = os.path.join(DESTDIR, filename)
        guidelines_rst.append(make_target)
        guidelines_rst_depends.append("{0}: {1}".format(make_target, " ".join(gl['depends'])))
        if build_all or make_target in targets:
            os.makedirs(os.path.join(os.getcwd(), DESTDIR), exist_ok=True)
            destfile = os.path.join(os.getcwd(), DESTDIR, filename)
            with open(destfile, mode="w", encoding="utf-8", newline="\n") as f:
                f.write(output)
            if len(gl['examples']):
                build_examples.extend(gl['examples'])

            build_examples = uniq(build_examples)

    if build_all or os.path.join(DESTDIR, WCAG_MAPPING_FILENAME) in targets:
        sc_mapping = []
        for sc in wcag_sc:
            if len(wcag_sc[sc]['gls']) == 0:
                continue
            gls = []
            for gl in wcag_sc[sc]['gls']:
                gls.append(f'*  {gl_categories[gl]}： :ref:`{gl}`')
            mapping = [
                f'"{sc}"',
                '"' + wcag_sc[sc]['en']['linkCode'] + '"',
                '"' + wcag_sc[sc]['ja']['linkCode'] + '"',
                '"' + wcag_sc[sc]['level'] + '"'
            ]
            mapping_str = ','.join(mapping)
            gls_str = '\n   '.join(gls)
            sc_mapping.append(f'   {mapping_str},"{gls_str}"')

        csv_table_header = """\
.. csv-table:: WCAG 2.1の達成基準との対応一覧
   :widths: auto
   :header: "達成基準","原文","日本語訳","適合レベル","対応するガイドライン"

"""
    
        sc_mapping_text = csv_table_header + '\n'.join(sc_mapping) + "\n"
        with open(WCAG_MAPPING_PATH, mode="w", encoding="utf-8", newline="\n") as f:
            f.write(sc_mapping_text)

    if build_all or os.path.join(DESTDIR, PRIORITY_DIFF_FILENAME) in targets:
        diffs = []
        for sc in wcag_sc:
            if wcag_sc[sc]['level'] == wcag_sc[sc]['localPriority']:
                continue
            diff = []
            diff = [
                f'"{sc}"',
                '"' + wcag_sc[sc]['en']['linkCode'] + '"',
                '"' + wcag_sc[sc]['ja']['linkCode'] + '"',
                '"' + wcag_sc[sc]['level'] + '"',
                '"' + wcag_sc[sc]['localPriority'] + '"'
            ]
            diffs.append('   ' + ','.join(diff))

        csv_table_header = """\
.. csv-table:: 適合レベルを見直した達成基準一覧
   :widths: auto
   :header: "達成基準","原文","日本語訳","見直し前","見直し後"

"""
    
        diffs_text = csv_table_header + '\n'.join(diffs) + "\n"
        with open(PRIORITY_DIFF_PATH, mode="w", encoding="utf-8", newline="\n") as f:
            f.write(diffs_text)

    if build_all or os.path.join(DESTDIR, ALL_CHECKS_FILENAME) in targets:
        with open(ALL_CHECKS_PATH, mode="w", encoding="utf-8", newline="\n") as f:
            f.write(allcheck_text)

    if build_all or len(build_examples):
        for tool in check_examples:
            if check_examples[tool] == '' or not tool in build_examples:
                continue
            filename = 'check-examples-' + tool + '.rst'
            destfile = os.path.join(os.getcwd(), DESTDIR, filename)
            with open(destfile, mode="w", encoding="utf-8", newline="\n") as f:
                f.write(check_examples[tool])

    if build_all or MAKEFILE_FILENAME in targets:
        gl_yaml = []
        for obj in guidelines:
            gl_yaml.append(obj['src_path'])
        all_yaml = []
        for obj in guidelines+checks:
            all_yaml.append(obj['src_path'])

        makefile_str = '''
guidelines_rst = {guidelines_rst}

incfiles: $(guidelines_rst)

%.yaml: ;

{wcag_mapping_target}: {gl_yaml} {wcag_sc}
	@$(YAML2RST) {wcag_mapping_target}

{priority_diff_target}: {gl_yaml} {wcag_sc}
	@$(YAML2RST) {priority_diff_target}

{all_checks_target}: {all_yaml}
	@$(YAML2RST) {all_checks_target}

'''.format(
    guidelines_rst = " ".join(guidelines_rst),
    wcag_mapping_target = os.path.join(DESTDIR, WCAG_MAPPING_FILENAME),
    priority_diff_target = os.path.join(DESTDIR, PRIORITY_DIFF_FILENAME),
    all_checks_target = os.path.join(DESTDIR, ALL_CHECKS_FILENAME),
    wcag_sc = os.path.join(DESTDIR, WCAG_SC),
    gl_yaml = " ".join(gl_yaml),
    all_yaml = " ".join(all_yaml)
)

        for dep in guidelines_rst_depends:
            makefile_str += '''
{0}
	@$(YAML2RST) {1}
'''.format(dep, dep.split(":")[0])
        destfile = os.path.join(os.getcwd(),  MAKEFILE_FILENAME)
        with open(destfile, mode="w", encoding="utf-8", newline="\n") as f:
            f.write(makefile_str)

def read_yaml(dir, schema_file):
    src_files = []
    for currentDir, dirs, files in os.walk(dir):
        for f in files:
            src_files.append(os.path.join(currentDir, f))

    try:
        with open(schema_file) as f:
            schema = json.load(f)
    except Exception as e:
        print(f'Exception occurred while loading schema {schema_file}...', file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

    obj = []
    for src in src_files:
        try:
            with open(src, encoding="utf-8") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(f'Exception occurred while loading YAML {src}...', file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)
        try:
            validate(data, schema)
        except ValidationError as e:
            print(f'Error occurred while validating {src}', file=sys.stderr)
            print(e.message, file=sys.stderr)
            sys.exit(1)
        data['src_path'] = src.replace(os.getcwd() + "/", "")
        obj.append(data)
    return obj

def uniq(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

def indent(para, level):
    lines = para.split('\n')
    for i in range(len(lines)):
        lines[i] = ' ' * level + lines[i]

    return '\n'.join(lines) + '\n'

def make_header(title, char, overline = False):
    line = char * width(title)
    if overline:
        return f'\n{line}\n{title}\n{line}\n\n'
    else:
        return f'\n{title}\n{line}\n\n'

def width(s):
    return sum([_width(c) for c in s])

def _width(c):
    return 2 if _isMultiByte(c) else 1

def _isMultiByte(c):
    import unicodedata
    return unicodedata.east_asian_width(c) in ['F', 'W', 'A']

if __name__ == "__main__":
    main()
