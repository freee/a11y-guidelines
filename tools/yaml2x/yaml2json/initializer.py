import os
import argparse
import pickle

LANGUAGES = ['ja', 'en']
PICKLE_PATH = 'build/doctrees/environment.pickle'

def setup_parameters():
    args = parse_args()
    return process_arguments(args)

def parse_args():
    parser = argparse.ArgumentParser(description="Process YAML files and generate a JSON file containing checklist items.")
    parser.add_argument('--basedir', '-b', type=str, default='.', help='Base directory where the data directory is located.')
    parser.add_argument('--output-file', '-o', type=str, default='data.json', help='Output file path.')
    parser.add_argument('--base-url', '-u', type=str, default='', help='Base URL for the links to related information.')
    parser.add_argument('--publish', '-p', action='store_true', help='Generate for publishing')
    return parser.parse_args()

def process_arguments(args):
    """
    Process the command-line arguments to determine the build mode, target files, and other options.

    Args:
        args: The parsed command-line arguments.

    Returns:
        A dictionary containing settings derived from the command-line arguments.
    """
    basedir = os.path.abspath(args.basedir)
    if os.path.isabs(args.output_file):
        output_file = args.output_file
    elif not os.path.dirname(args.output_file):
        output_file = os.path.join(basedir, args.output_file)
    else:
        output_file = os.path.abspath(args.output_file)
    return {
        'basedir': basedir,
        'output_file': output_file,
        'base_url': args.base_url,
        'publish': args.publish
    }

def get_info_links(basedir, baseurl = ''):
    """
    Extract the labels from the environment pickle file.

    Args:
        basedir: The project root directory where the data directory is located for each language.
        baseurl: The base URL for the links to related information.

    Returns:
        A dictionary containing the labels extracted from the environment pickle file.
    """
    info = {}
    path_prefix = {
        'ja': '',
        'en': 'en/'
    }
    for lang in LANGUAGES:
        pickle_file = os.path.abspath(os.path.join(basedir, lang, PICKLE_PATH))
        try:
            with open(pickle_file, 'rb') as f:
                doctree = pickle.load(f)
        except Exception as e:
            raise Exception(f'Error loading environment pickle file: {pickle_file}') from e
        labels = doctree.domaindata['std']['labels']
        for label in labels:
            if labels[label][0] == '' or labels[label][1] == '' or labels[label][2] == '':
                continue
            if label not in info:
                info[label] = {
                    'text': {},
                    'url': {}
                }
            info[label]['text'][lang] = labels[label][2]
            info[label]['url'][lang] = f'{baseurl}/{path_prefix[lang]}{labels[label][0]}.html#{labels[label][1]}'

    return info

def version_info(basedir):
    version_info = {}
    with open(os.path.join(basedir, 'version.py'), encoding='utf-8') as f:
        exec(f.read(), version_info)
    return version_info
