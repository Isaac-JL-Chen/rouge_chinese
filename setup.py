import os
import re

from setuptools import setup, find_packages


def get_version():
    path = os.path.join(os.path.dirname(__file__), 'rouge_chinese', '__init__.py')
    with open(path, 'r') as f:
        content = f.read()
    m = re.search(r'__version__\s*=\s*"(.+)"', content)
    assert m is not None
    return m.group(1)


def long_description():
    this_directory = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()


version = get_version()

setup(
    name="rouge_chinese",
    version=version,
    description="Python ROUGE Score Implementation for Chinese Language Task (official rouge score)",
    url="https://github.com/Isaac-JL-Chen/rouge_chinese.git",
    # download_url="https://github.com/pltrdy/rouge/archive/%s.tar.gz" % version,
    author="Isaac-JL-Chen",
    author_email="chn.jianlin@gmail.com",
    keywords=["NL", "CL", "natural language processing",
              "computational linguistics", "summarization","chinese"],
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Linguistic"
    ],
    license="LICENCE.txt",
    long_description=long_description(),
    long_description_content_type='text/markdown',
    test_suite="nose.collector",
    tests_require=['nose'],
    install_requires=['six'],
    entry_points={
        'console_scripts': [
            'rouge_chinese=bin.rouge_cmd:main'
        ]
    }
)
