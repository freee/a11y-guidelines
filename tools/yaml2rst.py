import os
import sys
import re
import yaml
import json

GUIDELINES_SRCDIR = 'data/yaml/gl'
CHECKS_SRCDIR = 'data/yaml/checks'
DESTDIR = 'source/inc'
MAKEFILE_FILENAME = 'incfiles.mk'

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
def main():
    args = sys.argv
    argc = len(args)
    if argc == 1:
        build_all = True
    else:
        build_all = False
        targets = args[1:argc]

    if build_all or not MAKEFILE_FILENAME in targets:
        build_allchecks = True
    else:
        build_allchecks = False

    build_examples = []

    guidelines = read_yaml(os.path.join(os.getcwd(), GUIDELINES_SRCDIR))
    checks = read_yaml(os.path.join(os.getcwd(), CHECKS_SRCDIR))

    allcheck_text = ''
    check_examples = {}
    for key in CHECK_TOOLS:
        check_examples[key] = ''

    for key in sorted(checks):
        check = checks[key]
        check['glref'] = []
        check['info'] = []
        for glkey in guidelines:
            gl = guidelines[glkey]
            if key in gl['checks']:
                check['glref'].append(glkey)
                if 'info' in gl:
                    check['info'].extend(gl['info'])

        allcheck_info = ''
        if len(check['info']) > 0:
            check['info'] = uniq(check['info'])
            allcheck_info = mkheader('参考情報', '=')
            for info in check['info']:
                if re.match(r'(https?://|\|.+\|)', info):
                    allcheck_info += f'*  {info}\n'
                else:
                    allcheck_info += f'*  :ref:`{info}`\n'

        target = TARGET_NAMES[check['target']]
        gl_check_title = mkheader(f':ref:`check-{key}`', '-')
        allcheck_title = mkheader(f'チェックID：{key}', '*', True)

        glref_text = '関連ガイドライン\n'
        for ref in check['glref']:
            glcat = _get_category(ref)
            glref_text += f'   *  {glcat}： :ref:`{ref}`\n'

        gl_check_details = ''
        allcheck_details = ''
        if check['target'] == 'code' and 'implementation' in check:
            for detail in check['implementation']:
                gl_check_details += mkheader('実装方法の例：' + detail['title'], '^')
                allcheck_details += mkheader('実装方法の例：' + detail['title'], '=')

                for impl in detail:
                    if impl == 'title':
                        continue
                    str = detail.get(impl)
                    gl_check_details += IMPLEMENTATION_NAMES[impl] + "\n" + indent(str, 3)
                    allcheck_details += impl + "\n" + indent(str, 3)
        elif check['target'] == 'product' and 'checkMeans' in check:
            for means in check['checkMeans']:
                check_example_title = mkheader(f':ref:`check-{check["id"]}`', '*', True)
                gl_check_details += mkheader(f'{CHECK_TOOLS[means]}によるチェック実施方法の例', '^') + check['checkMeans'][means] + '\n'
                allcheck_details += mkheader(f'{CHECK_TOOLS[means]}によるチェック実施方法の例', '=') + check['checkMeans'][means] + '\n'
                check_examples[means] += '''\
.. _check-example-{means}-{id}:
{title}
{check}
{example}

'''.format(means = means, id = check['id'], title = check_example_title, check = indent(check['check'], 3), example = check['checkMeans'][means])

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
{title}{metainfo}{glref}
{check}
{info}
{details}
""".format(id = key, title = allcheck_title, metainfo = metainfo, glref = glref_text, check = check['check'], details = allcheck_details, info = allcheck_info)

    intent_title = mkheader('意図', '=')
    check_title = mkheader('チェック内容', '=')
    sc_title = mkheader('対応するWCAG 2.1の達成基準', '=')
    info_title = mkheader('参考情報', '=')
    guidelines_rst = []
    guidelines_rst_depends = []

    for key in guidelines:
        gl = guidelines[key]
        gl['depends'] = [gl['srcpath']]
        glstr = {
            'title': mkheader(gl['priority'] + gl['title'], "*", True),
            'intent': intent_title + gl['intent'],
            'id': key,
            'priority': gl['priority'],
            'guideline': gl['guideline'],
            'info': ''
        }

        if 'info' in gl:
            glstr['info'] = info_title
            for ref in gl['info']:
                if re.match(r'(https?://|\|.+\|)', ref):
                    glstr['info'] += f'*  {ref}\n'
                else:
                    glstr['info'] += f'*  :ref:`{ref}`\n'

        glstr['checks'] = check_title
        gl['examples'] = []
        for check in gl['checks']:
            if 'checkMeans' in checks[check]:
                gl['examples'].extend(list(checks[check]['checkMeans'].keys()))
            glstr['checks'] += checks[check]['gl_check_text']
            gl['depends'].append(checks[check]['srcpath'])
        glstr['scs'] = sc_title
        for sc in gl['sc']:
            glstr['scs'] += """\
SC {sc}：
   -  |SC {sc}|
   -  |SC {sc}ja|
""".format(sc=sc)
        output = """\
.. _{0[id]}:
{0[title]}{0[guideline]}

{0[intent]}
{0[scs]}
{0[info]}
{0[checks]}\
""".format(glstr)

        filename = key + '.rst'
        make_target = os.path.join(DESTDIR, filename)
        guidelines_rst.append(make_target)
        guidelines_rst_depends.append("{0}: {1}".format(make_target, " ".join(gl['depends'])))
        if build_all or make_target in targets:
            os.makedirs(os.path.join(os.getcwd(), DESTDIR), exist_ok=True)
            destfile = os.path.join(os.getcwd(), DESTDIR, filename)
            with open(destfile, mode="w", encoding="utf-8", newline="\n") as f:
                f.write(output)
            if len(guidelines[key]['examples']):
                build_examples.extend(guidelines[key]['examples'])

            build_examples = uniq(build_examples)

    if build_allchecks:
        filename = 'allchecks.rst'
        destfile = os.path.join(os.getcwd(), DESTDIR, filename)
        with open(destfile, mode="w", encoding="utf-8", newline="\n") as f:
            f.write(allcheck_text)

    if build_all or len(build_examples):
        for means in check_examples:
            if check_examples[means] == '' or not means in build_examples:
                continue
            filename = 'check-examples-' + means + '.rst'
            destfile = os.path.join(os.getcwd(), DESTDIR, filename)
            with open(destfile, mode="w", encoding="utf-8", newline="\n") as f:
                f.write(check_examples[means])

    if build_all or MAKEFILE_FILENAME in targets:
        makefile_str = '''
guidelines_rst = {guidelines_rst}

incfiles: $(guidelines_rst)

%.yaml: ;
'''.format(guidelines_rst = " ".join(guidelines_rst))

        for dep in guidelines_rst_depends:
            makefile_str += '''
{0}
	@$(YAML2RST) {1}
'''.format(dep, dep.split(":")[0])
        destfile = os.path.join(os.getcwd(),  MAKEFILE_FILENAME)
        with open(destfile, mode="w", encoding="utf-8", newline="\n") as f:
            f.write(makefile_str)

def read_yaml(dir):
    srcs = []
    for currDir, dirs, files in os.walk(dir):
        for f in files:
            srcs.append(os.path.join(currDir, f))

    obj = {}
    for src in srcs:
        try:
            with open(src, encoding="utf-8") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print('Exception occurred while loading YAML...', file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)
        data['srcpath'] = src.replace(os.getcwd() + "/", "")
        obj[data['id']] = data
    return obj

def uniq(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

def indent(para, level):
    lines = para.split('\n')
    for i in range(len(lines)):
        lines[i] = ' ' * level + lines[i]

    return '\n'.join(lines) + '\n'

def mkheader(title, char, overline = False):
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

def _get_category(id):
    category_names = {
        'dynamic': '動的コンテンツ',
        'form': 'フォーム',
        'icon': 'アイコン',
        'image': '画像',
        'iot': '画像化されたテキスト',
        'input': '入力ディバイス',
        'link': 'リンク',
        'login': 'ログイン・セッション',
        'markup': 'マークアップ全般',
        'multimedia': '音声・映像コンテンツ',
        'page': 'ページ全体',
        'text': 'テキスト'
    }
    return category_names[id.split('-')[1]]

if __name__ == "__main__":
    main()
