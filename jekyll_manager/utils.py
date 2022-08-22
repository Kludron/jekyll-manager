
import yaml
import os
import re

import frontmatter

# This seems to be a globally identified YAML header delimiter
YAML_DELIMITER = '---'

# This only returns the title, date, categories and tags
# is this needed?
def grabinfo(filepath) -> dict:

    postdata = frontmatter.load(filepath)

    # Following the filename structure of YYYY-MM-DD-name.md
    filename = os.path.basename(filepath)
    f_info = filename.strip('.md').split('-')

    # Grab the date from the header, or from the filename
    try:
        date = postdata.metadata.pop('date')
    except KeyError:
        f_date = '-'.join(f_info[:3])
        date = f_date

    # Grab the title from the header, or from the filename
    try:
        title = postdata.metadata.pop('title')
    except KeyError:
        f_title = ' '.join(f_info[3:])
        title = f_title.title()

    return {
        "title" : title,
        "date"  : date,
        "metadata" : postdata.metadata, 
    }


def markdownCount(content) -> int:
    """
    :NOTE:
        This is forked from https://github.com/gandreadis/markdown-word-count
        (NOT ORIGINAL CONTENT).
    """
    # Comments
    content = re.sub(r'<!--(.*?)-->', '', content, flags=re.MULTILINE)
    # Tabs to spaces
    content = content.replace('\t', '    ')
    # More than 1 space to 4 spaces
    content = re.sub(r'[ ]{2,}', '    ', content)
    # Footnotes
    content = re.sub(r'^\[[^]]*\][^(].*', '', content, flags=re.MULTILINE)
    # Indented blocks of code
    content = re.sub(r'^( {4,}[^-*]).*', '', content, flags=re.MULTILINE)
    # Custom header IDs
    content = re.sub(r'{#.*}', '', content)
    # Replace newlines with spaces for uniform handling
    content = content.replace('\n', ' ')
    # Remove images
    content = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', content)
    # Remove HTML tags
    content = re.sub(r'</?[^>]*>', '', content)
    # Remove special characters
    content = re.sub(r'[#*`~\-–^=<>+|/:]', '', content)
    # Remove footnote references
    content = re.sub(r'\[[0-9]*\]', '', content)
    # Remove enumerations
    content = re.sub(r'[0-9#]*\.', '', content)

    return len(content.split())

#####################
#
# Printing functions
#
#####################

from colorama import Fore, Style
import colorama
colorama.init(autoreset=True)

def makeBright(text: str) -> str:
    return f'{Style.BRIGHT}{text}{Style.RESET_ALL}'

def makeRed(text: str) -> str:
    return f'{Fore.RED}{text}{Style.RESET_ALL}'

def makePurple(text: str) -> str:
    return f'{Fore.PURPLE}{text}{Style.RESET_ALL}'

def makeBlue(text: str) -> str:
    return f'{Fore.BLUE}{text}{Style.RESET_ALL}'
