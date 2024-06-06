import os

DATA_DIR = 'data'
YAML_DIR = 'yaml'
JSON_DIR = 'json'

def get_src_path(basedir):
    data_basedir = os.path.join(basedir, DATA_DIR)
    yaml_basedir = os.path.join(data_basedir, YAML_DIR)
    json_basedir = os.path.join(data_basedir, JSON_DIR)

    src_path = {
        'guidelines': os.path.join(yaml_basedir, "gl"),
        'checks': os.path.join(yaml_basedir, 'checks'),
        'faq': os.path.join(yaml_basedir, 'faq'),
        'wcag_sc': os.path.join(json_basedir, 'wcag-sc.json'),
        'gl_categories': os.path.join(json_basedir, 'guideline-categories.json'),
        'faq_tags': os.path.join(json_basedir, 'faq-tags.json'),
        'info': os.path.join(json_basedir, 'info.json')
    }
    return src_path
