from setuptools import setup

setup(
    name='jekyll-manager',
    description='A command line interface for managing your Jekyll Blog',
    long_description ="""
    A command line interface for your Jekyll Blog. 
    Find out more information on my github repo: https://github.com/kludron/jekyll-manager.
    """,
    author="Kludron",
    author_email="kludron@lukewarmsecurityinfo.com",
    readme="README.md",
    documentation='https://gitbu.com/kludron/jekyll-manager',
    url='https://github.com/kludron/jekyll-manager',
    packages=['jekyll_manager'],
    version='0.0.2',
    install_requires=[
        'colorama',
        'pyyaml',
    ],
    scripts=['bin/jekyll-manager'],
)
