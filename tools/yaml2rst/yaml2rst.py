import os
import app_initializer
from a11y_guidelines import Category, WcagSc, InfoRef, Guideline, Check, Faq, FaqTag, CheckTool, AxeRule, RelationshipManager
import a11y_guidelines_initializer

def main():
    settings = app_initializer.setup_parameters()
    DEST_DIRS, STATIC_FILES, MAKEFILE_VARS = app_initializer.setup_constants(settings)
    templates = app_initializer.setup_templates()
    makefile_vars, makefile_vars_list = app_initializer.setup_variables()
    a11y_guidelines_initializer.setup_instances(settings)

    for directory in DEST_DIRS.values():
        os.makedirs(directory, exist_ok=True)

    generate_files(DEST_DIRS['guidelines'], templates['category_page'], get_category_pages, settings['build_all'], settings['targets'], settings['lang'])
    generate_files(STATIC_FILES['all_checks'], templates['allchecks_text'], get_allchecks, settings['build_all'], settings['targets'], settings['lang'])
    generate_files(DEST_DIRS['checks'], templates['tool_example'], get_example_pages, settings['build_all'], settings['targets'], settings['lang'])
    generate_files(DEST_DIRS['faq_articles'], templates['faq_article'], get_faq_articles, settings['build_all'], settings['targets'], settings['lang'])
    generate_files(DEST_DIRS['faq_tags'], templates['faq_tagpage'], get_faq_tagpages, settings['build_all'], settings['targets'], settings['lang'])
    generate_files(STATIC_FILES['faq_index'], templates['faq_index'], get_faq_index, settings['build_all'], settings['targets'], settings['lang'])
    generate_files(STATIC_FILES['faq_tag_index'], templates['faq_tag_index'], get_faq_tag_index, settings['build_all'], settings['targets'], settings['lang'])
    generate_files(STATIC_FILES['faq_article_index'], templates['faq_article_index'], get_faq_article_index, settings['build_all'], settings['targets'], settings['lang'])
    generate_files(DEST_DIRS['info2gl'], templates['info_to_gl'], get_info_to_guidelines, settings['build_all'], settings['targets'], settings['lang'])
    generate_files(DEST_DIRS['info2faq'], templates['info_to_faq'], get_info_to_faqs, settings['build_all'], settings['targets'], settings['lang'])
    generate_files(STATIC_FILES['wcag21mapping'], templates['wcag21mapping'], get_wcag21mapping, settings['build_all'], settings['targets'], settings['lang'])
    generate_files(STATIC_FILES['priority_diff'], templates['priority_diff'], get_priority_diff, settings['build_all'], settings['targets'], settings['lang'])
    generate_files(STATIC_FILES['miscdefs'], templates['miscdefs'], get_miscdefs, settings['build_all'], settings['targets'], settings['lang'])
    generate_files(STATIC_FILES['makefile'], templates['makefile'], get_makefile, settings['build_all'], settings['targets'], settings['lang'], {
        'DEST_DIRS': DEST_DIRS,
        'MAKEFILE_VARS': MAKEFILE_VARS,
        'makefile_vars': makefile_vars,
        'makefile_vars_list': makefile_vars_list
    })
    generate_files(STATIC_FILES['axe_rules'], templates['axe_rules'], get_axe_rules, settings['build_all'], settings['targets'], settings['lang'])

def get_category_pages(lang):
    rel = RelationshipManager()
    for category, guidelines in rel.get_guidelines_to_category().items():
        yield {
            'filename': category,
            'guidelines': [gl.template_object(lang) for gl in guidelines]
        }

def get_allchecks(lang):
    allchecks = Check.template_object_all(lang)
    return [{'allchecks': allchecks}]

def get_example_pages(lang):
    for tool in CheckTool.list_all():
        yield {**tool.example_template_object(lang), **{'filename': f'examples-{tool.id}'}}

def get_faq_articles(lang):
    for faq in Faq.list_all():
        yield {'filename': faq.id, **faq.template_object(lang)}

def get_faq_tagpages(lang):
    rel = RelationshipManager()
    for tag in FaqTag.list_all():
        if tag.article_count() == 0:
            continue
        yield {
            'filename': tag.id,
            'tag': tag.id,
            'label': tag.names[lang],
            'articles': [faq.id for faq in rel.get_tag_to_faqs(tag)]
        }

def get_faq_index(lang):
    sorted_tags = sorted(FaqTag.list_all(), key=lambda x: x.names[lang])
    tags = [tag.template_object(lang) for tag in sorted_tags if tag.article_count() > 0]
    articles = [article.template_object(lang) for article in Faq.list_all(sort_by='date')]
    return [{'articles': articles, 'tags': tags}]

def get_faq_tag_index(lang):
    sorted_tags = sorted(FaqTag.list_all(), key=lambda x: x.names[lang])
    tagpages = [tagpage.template_object(lang) for tagpage in sorted_tags if tagpage.article_count() > 0]
    return [{'tags': tagpages}]

def get_faq_article_index(lang):
    articles = [article.template_object(lang) for article in Faq.list_all(sort_by='sortKey')]
    return [{'articles': articles}]

def get_info_to_guidelines(lang):
    rel = RelationshipManager()
    for info in InfoRef.list_has_guidelines():
        if not info.internal:
            continue
        sorted_guidelines = sorted(rel.get_info_to_guidelines(info), key=lambda item: item.sort_key)
        guidelines = [guideline.get_category_and_id(lang) for guideline in sorted_guidelines]
        yield {'filename': info.ref, 'guidelines': guidelines}

def get_info_to_faqs(lang):
    rel = RelationshipManager()
    for info in InfoRef.list_has_faqs():
        if not info.internal:
            continue
        faqs = [faq.id for faq in rel.get_info_to_faqs(info)]
        yield {'filename': info.ref, 'faqs': faqs}

def get_wcag21mapping(lang):
    rel = RelationshipManager()
    mappings = []
    for sc in WcagSc.get_all().values():
        sc_object = sc.template_object()
        guidelines = rel.get_sc_to_guidelines(sc)
        if len(guidelines) > 0:
            sc_object['guidelines'] = [guideline.get_category_and_id(lang) for guideline in guidelines]
        mappings.append(sc_object)
    return [{'mapping': mappings}]

def get_priority_diff(lang):
    diffs = [sc.template_object() for sc in WcagSc.get_all().values() if sc.level != sc.local_priority]
    return [{'diffs': diffs}]

def get_miscdefs(lang):
    data = []
    for info in InfoRef.list_all_external():
        data.append({
            'label': info.refstring(),
            'text': info.text[lang],
            'url': info.url[lang]
        })
    return [{'links': data}]

def get_makefile(lang, DEST_DIRS, MAKEFILE_VARS, makefile_vars, makefile_vars_list):
    rel = RelationshipManager()
    build_depends = []
    makefile_vars['check_yaml'] = ' '.join(Check.list_all_src_paths())
    makefile_vars['gl_yaml'] = ' '.join(Guideline.list_all_src_paths())
    makefile_vars['faq_yaml'] = ' '.join(Faq.list_all_src_paths())
    for cat in Category.list_all():
        filename = f'{cat.id}.rst'
        target = os.path.join(DEST_DIRS['guidelines'], filename)
        makefile_vars_list['guideline_category_target'].append(target)
        build_depends.append({'target': target, 'depends': ' '.join(cat.get_dependency())})

    for tool in CheckTool.list_all():
        filename = f'examples-{tool.id}.rst'
        target = os.path.join(DEST_DIRS['checks'], filename)
        makefile_vars_list['check_example_target'].append(target)
        build_depends.append({'target': target, 'depends': ' '.join(tool.get_dependency())})

    for faq in Faq.list_all():
        filename = f'{faq.id}.rst'
        target = os.path.join(DEST_DIRS['faq_articles'], filename)
        makefile_vars_list['faq_article_target'].append(target)
        build_depends.append({'target': target, 'depends': ' '.join(faq.get_dependency())})

    for tag in FaqTag.list_all():
        if tag.article_count() == 0:
            continue
        filename = f'{tag.id}.rst'
        target = os.path.join(DEST_DIRS['faq_tags'], filename)
        makefile_vars_list['faq_tagpage_target'].append(target)
        dependency = []
        for faq in rel.get_tag_to_faqs(tag):
            dependency.extend(faq.get_dependency())
        build_depends.append({'target': target, 'depends': ' '.join(dependency)})

    for info in InfoRef.list_has_guidelines():
        if not info.internal:
            continue
        filename = f'{info.ref}.rst'
        target = os.path.join(DEST_DIRS['info2gl'], filename)
        makefile_vars_list['info_to_gl_target'].append(target)
        build_depends.append({'target': target, 'depends': ' '.join([guideline.src_path for guideline in rel.get_info_to_guidelines(info)])})

    for info in InfoRef.list_has_faqs():
        filename = f'{info.ref}.rst'
        target = os.path.join(DEST_DIRS['info2faq'], filename)
        makefile_vars_list['info_to_faq_target'].append(target)
        build_depends.append({'target': target, 'depends': ' '.join([faq.src_path for faq in rel.get_info_to_faqs(info)])})

    for key, value in makefile_vars_list.items():
        makefile_vars[key] = ' '.join(value)
        makefile_vars['depends'] = build_depends
    return [{**makefile_vars, **MAKEFILE_VARS}]

def get_axe_rules(lang):
    return [{
        'version': AxeRule.version,
        'major_version': AxeRule.major_version,
        'deque_url': AxeRule.deque_url,
        'timestamp': AxeRule.timestamp,
        'rules': [rule.template_object(lang) for rule in AxeRule.list_all()]
    }]

def generate_file(dest_path, template, data):
    """
    Generate a single file based on provided data and template.

    Args:
    - dest_path: Destination path for the file. This can be a directory or a specific file path.
    - template: Template to use for file generation.
    - data: Data to pass to the template.
    """
    # Determine if dest_path is a directory or a file path
    if os.path.isdir(dest_path):
        filename = f"{data['filename']}.rst"  # Assume data contains 'filename' key for directory output
        dest_file_path = os.path.join(dest_path, filename)
    else:
        dest_file_path = dest_path  # dest_path is already a file path

    # Use the template to write the data to the destination file
    template.write_rst(data, dest_file_path)

def generate_files(dest_path, template, get_data_func, build_all, targets, lang, extra_args=None):
    """
    Generate files (or a single file) based on provided data, conditions, and destination path.

    Args:
    - dest_path: Destination directory or specific file path for the output.
    - template: Template to use for file generation.
    - get_data_func: Function to get data for file generation. It should yield dictionaries containing data and optionally 'filename' key for multiple files.
    - build_all: Flag to indicate whether to build all files.
    - targets: List of specific targets to build.
    - lang: Language for content generation.
    - extra_args: Additional arguments for get_data_func, if any.
    """
    extra_args = extra_args or {}
    for data in get_data_func(lang=lang, **extra_args):
        if build_all or dest_path in targets or ('filename' in data and os.path.join(dest_path, f'{data["filename"]}.rst') in targets):
            data['lang'] = lang
            generate_file(dest_path, template, data)

if __name__ == "__main__":
    main()
