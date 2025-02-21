# setup.py
from setuptools import setup, find_packages

setup(
    name="get_yaml_data",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'yaml2json=get_yaml_data.cli:main',
        ],
    },
    python_requires='>=3.8',
)
