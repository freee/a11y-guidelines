import sys
import os
import json
import re
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import initializer as app_initializer
from a11y_guidelines import setup_instances, Category, WcagSc, InfoRef, Guideline, Check, Faq, FaqTag, CheckTool, AxeRule, RelationshipManager

def main():
    settings = app_initializer.setup_parameters()
    version_info = app_initializer.version_info(settings['basedir'])
    setup_instances(settings['basedir'])

    info_links = app_initializer.get_info_links(settings['basedir'], settings['base_url'])
    for info in InfoRef.list_all_internal():
        if info.ref in info_links:
            info.set_link(info_links[info.ref])
    checks = Check.object_data_all(settings['base_url'])
    for key in checks:
        if 'conditions' in checks[key]:
            checks[key]['conditions'] = [deRST(condition, info_links) for condition in checks[key]['conditions']]

    data = {
        'publish': settings['publish'],
        'version': version_info['checksheet_version'],
        'checks': checks
    }
    with open(settings['output_file'], mode="w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def deRST(condition, info):

    def reRST_str(str, info, lang):
        ref = re.compile(r':ref:`([-a-z0-9]+)`')
        text = ref.sub(lambda m: info[m.group(1)]['text'][lang], str)
        kbd = re.compile(r':kbd:`(.+)`')
        text = kbd.sub(lambda m: m.group(1), text)

        # Remove leading and trailing whitespaces
        text = text.strip()

        # Define regexp for half and full width chars
        fullwidth_chars = r'[\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]'
        halfwidth_chars = r'[\u0000-\u007F\uFF61-\uFFDC\uFFE8-\uFFEE]'

        # Remove whitespaces between fullwidth chars
        text = re.sub(f'({fullwidth_chars})\s+({fullwidth_chars})', r'\1\2', text)

        # Remove whitespaces between halfwidth chars and full width chars
        text = re.sub(f'({fullwidth_chars})\s+({halfwidth_chars})', r'\1\2', text)
        text = re.sub(f'({halfwidth_chars})\s+({fullwidth_chars})', r'\1\2', text)

        return text

    if condition['type'] == 'simple':
        if 'procedure' in condition:
            for lang in condition['procedure']['procedure']:
                condition['procedure']['procedure'][lang] = reRST_str(condition['procedure']['procedure'][lang], info, lang)
        return condition
    for i in range(len(condition['conditions'])):
        condition['conditions'][i] = deRST(condition['conditions'][i], info)
    return condition

if __name__ == "__main__":
    main()
