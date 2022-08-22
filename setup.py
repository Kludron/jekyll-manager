#!/usr/bin/env python

from setuptools import setup

README = open('README.md', 'r').read()
DEPENDENCIES = open('requirements.txt', 'r').read().split('\n')

setup(
    name='jekyll-manager',
    description="A command line interface for managing your Jekyll Blog",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Kludron",
    author_email="kludron@lukewarmsecurityinfo.com",
    url="https://github.com/kludron/jekyll-manager",
    version='1.2.0',
    install_requires=DEPENDENCIES,
    entry_points={'console_scripts': ['jekyll-manager=jekyll_manager.__main__:main']}
)
