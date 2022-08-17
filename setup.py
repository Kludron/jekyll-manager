from setuptools import setup

setup(
    name='jekyll-manager',
    description='A command line interface for managing your Jekyll Blog',
    author = "Kludron",
    author_email = "kludron@lukewarmsecurityinfo.com",
    readme = "README.md",
    url='https://github.com/kludron/jekyll-manager',
    packages=['jekyll_manager'],
    version='0.0.1',
    install_requires=[
        'colorama',
        'pyyaml',
    ],
    scripts=['bin/jekyll-manager'],
)
