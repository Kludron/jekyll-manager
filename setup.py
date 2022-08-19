#!/usr/bin/env python

from setuptools import setup

import os

README = open('README.md', 'r').read()
DEPENDENCIES = open(os.path.join(os.getenv('HOME'), 'Documents/Projects/jekyll-manager', 'requirements.txt'), 'r').read()

long_description = """
A command line interface for your Jekyll Blog.

There are multiple ways to run after installself.

1. Traverse to the directory of your jekyll blog and type `jekyll-manager`. 
2. Type in `jekyll-manager </path/to/jekyll_blog>`. 
3. Set the environment variable 'JEKYLL_ROOT' to point to your directory, and type in `jekyll-manager` from anywhere!.

For more information, visit my github repo: https://github.com/kludron/jekyll-manager
"""

setup(
    name='jekyll-manager',
    description="A command line interface for managing your Jekyll Blog",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Kludron",
    author_email="kludron@lukewarmsecurityinfo.com",
    documentation="https://gitbu.com/kludron/jekyll-manager",
    url="https://github.com/kludron/jekyll-manager",
    packages=['jekyll_manager'],
    version='1.0.2',
    install_requires=DEPENDENCIES,
    entry_points={'console_scripts': ['jekyll-manager=jekyll_manager.__main__:main']}
)
