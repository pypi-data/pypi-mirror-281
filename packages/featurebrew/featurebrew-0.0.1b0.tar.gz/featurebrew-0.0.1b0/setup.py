#!/usr/bin/env python
import codecs
import os.path
import re
import sys

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


install_requires = [
    'click==8.1.7',
    'PyYAML==6.0.1',
    'asyncio==3.4.3',
    'boto3==1.34.132',
    'chromadb==0.4.24',
    'fastapi==0.110.1',
    'langchain==0.2.1',
    'langchain-openai==0.1.8',
    'langchainhub==0.1.17',
    'langchain-experimental==0.0.59',
    'langgraph==0.0.60',
    'langsmith==0.1.67',
    'neo4j==5.19.0',
    'numpy==1.26.4',
    'openai==1.30.5',
    'opentelemetry-api==1.24.0',
    'pandas==2.2.2',
    'pydantic==2.7.0',
    'uvicorn==0.29.0',
    'python-docx==1.1.0',
    'python-dotenv==1.0.1',
    'psycopg2-binary==2.9.9',
    'google-cloud-bigquery==3.24.0',
    'func_timeout==4.3.5',
    'torch==2.3.0',
    'scikit-learn==1.4.2',
    'openai-multi-tool-use-parallel-patch==0.2.0'
]


setup_options = dict(
    name='featurebrew',
    version=find_version("chicory_cli", "__init__.py"),
    description='Universal Command Line Environment for Chicory.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Chicory.AI',
    url='http://chicory.ai',
    packages=find_packages(),
    install_requires=install_requires,
    license="Apache License 2.0",
    python_requires=">= 3.9",
    entry_points={
        'console_scripts': [
            'featurebrew=chicory_cli.clidriver:main',
        ],
    },
)

setup(**setup_options)
