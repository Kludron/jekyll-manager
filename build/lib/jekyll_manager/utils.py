
import yaml
import os

# This seems to be a globally identified YAML header delimiter
YAML_DELIMITER = '---'

# This only returns the title, date, categories and tags
# is this needed?
def grabinfo(filepath) -> dict:
    postdata = parseYAML(filepath)

    # Following the filename structure of YYYY-MM-DD-name.md
    filename = os.path.basename(filepath)
    f_info = filename.strip('.md').split('-')

    # Grab the date from the header, or from the filename
    try:
        date = postdata.pop('date')
    except KeyError:
        f_date = '-'.join(f_info[:3])
        date = f_date

    # Grab the title from the header, or from the filename
    try:
        title = postdata.pop('title')
    except KeyError:
        f_title = ' '.join(f_info[3:])
        title = f_title.title()

    return {
        "title" : title,
        "date"  : date,
        "metadata" : postdata, 
    }


def parseYAML(filepath) -> dict:
    """
    :params:
        filepath: path to file.
    :description:
        This should (theoretically) parse the yaml header data from the top of
        markdown files, where the yaml content is enclosed with ---, which is 
        the global identifier for the start (and end) of a YAML file

        NOTE: This only reads the first delimited YAML region of the file
    """
    with open(filepath, 'r') as filedata:
        start = False
        data = ""
        for line in filedata.readlines():
            if line.strip() == YAML_DELIMITER:
                if start: break
                else: start = True
                continue
            data += line
        # NOTE: This does not load the data in the same order it was typed
        #   this wouldn't be suitable for editing the _config.yml file.
        return yaml.load(data, Loader=yaml.FullLoader)

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
