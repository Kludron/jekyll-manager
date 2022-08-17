
import sys
import os
import platform
import yaml

import colorama
from colorama import Fore, Style

from datetime import datetime

from pprint import pprint

JEKYLL_ROOT = os.getcwd()

colorama.init(autoreset=True)

# TODO: Change this to first read user input, then check _config.yml, then _config.toml
# Documentation: https://jekyllrb.com/docs/configuration/

try:
    JEKYLL_CONFIG_NAME = sys.argv[1]
except IndexError:
    JEKYLL_CONFIG_NAME = '_config.yml'

JEKYLL_CONFIG = os.path.join(JEKYLL_ROOT, JEKYLL_CONFIG_NAME)

if not os.path.isfile(JEKYLL_CONFIG_NAME):
    sys.stderr.write('Usage: {} [config-filename(if different)]\n'.format(sys.argv[0]))
    exit()

if os.path.dirname(JEKYLL_CONFIG) != os.path.dirname(JEKYLL_ROOT):
    # Change into the jekyll directory
    # NOTE: This always assumes that the config file is at the root of the jekyll directory
    # As per the documentation, this is not always the case: https://jekyllrb.com/docs/configuration/
    JEKYLL_ROOT = os.path.dirname(JEKYLL_CONFIG)

# This should always be correct, as per the documentation: https://jekyllrb.com/docs/posts/
JEKYLL_POSTS = os.path.join(JEKYLL_ROOT, '_posts')

# This seems to be a globally identified YAML header delimiter
YAML_DELIMITER = '---'

class Manager:
    def __init__(self):
        with open(JEKYLL_CONFIG, 'r') as config_file:
            self.config = yaml.load(config_file, Loader=yaml.FullLoader)
        
        self.posts = list()
        for root,dir,posts in os.walk(JEKYLL_POSTS):
            for post in posts:
                self.posts.append(os.path.join(root, post))

    def __call__(self):
        self.start()

    def start(self):
        while True:
            try:
                self.__menu(input('jm> '))
            except (KeyboardInterrupt, EOFError):
                print()
                break

    def __menu(self, selection, display=False):
        """
        Options:
            - Create posts
            - View posts
            - Edit posts
            - Delete posts
        """

        def printMenu():
            optSize  = max([len(key) for key in menu.keys()]) + 2
            descSize = max([len(item.get("Description")) for item in menu.values()]) + 2
            line = '-' * (4 + optSize + 5 + descSize + 2)
            header = f'{"":<4}{Style.BRIGHT}{"Option":<{optSize}}{Style.RESET_ALL}{" |":<5}{Style.BRIGHT}{"Description":<{descSize}}'

            print(header)
            print(line)
            for key in menu.keys():
                print(f'| + {Style.BRIGHT + Fore.RED}{key:<{optSize}}{Style.RESET_ALL}{" :":<5}{menu.get(key)["Description"]:<{descSize}} |')
            print(line)

        menu = {
            "create" :  {
                "Description" : "Create a post",
                "Function" : self.__createPost,
            },
            "view"   :  {
                "Description" : "View a post",
                "Function" : self.__viewPost,
            },
            "edit"   :  {
                "Description" : "Edit a post",
                "Function" : self.__editPost,
            },
            "delete" :  {
                "Description" : "Delete a post",
                "Function" : self.__deletePost,
            },
            "list"   :  {
                "Description" : "List all posts",
                "Function" : self.__listPosts,
            },
            "menu"   :  {
                "Description" : "Display this menu",
                "Function" : printMenu
            },
            "exit"  :   {
                "Description" : "Exit the program",
                "Function" : self.__exit
            },
        }

        if not menu.get(selection.lower()):
            print('option unknown. type \'menu\' for a list of options')
        else:
            print()
            menu.get(selection.lower()).get('Function')()
        
    def __exit(self):
        sys.exit()

    def __createPost(self):
        # TODO: How do I add more items that they can add in the creation
        """
        Needs to select:
            - Date
            - Title
            - Categories
            - Tags

        Then, open in editor
        """
        prompt = 'jc> '
        
        # Grab the title of the post
        print("What would you like the post title to be?")
        title = input(prompt)

        # Check if that title already exists
        for post in self.posts:
            if title.lower() == self.__grabInfo(post)['Title'].lower():
                # Prompt to edit the post
                print("This post already exists!")
                edit = input("Would you like to edit the post [Y/n]? ")
                if edit.lower() == 'y':
                    self.__openInEditor(post)
                return
        
        # Grab the date for the post
        print('What date would you like to assign to the post?')
        print('Format: Day Month Year (e.g. 12 2 2022)')
        date = ''
        while not date:
            try:
                date = datetime.strptime(input(prompt), '%d %m %Y').strftime('%Y-%m-%d')
            except Exception:
                print("Invalid date format")
                if not input("Try again [y/n]? ").lower()[0] == 'y':
                    return

        # Grab categories
        # TODO
        categories = []

        # Grab tags
        # TODO
        tags = []

        filename = date + '-' + '-'.join(title.lower().split()) + '.md'
        filepath = os.path.join(JEKYLL_POSTS, filename)

        if not os.path.exists(filepath):
            with open(filepath, 'w') as new_post:
                metadata = {
                    "title" : title,
                    "date" : date,
                    "categories" : f'[{",".join([c for c in categories])}]',
                    "tags" : f'[{",".join([t for t in tags])}]'
                }
                header = '\n'.join([YAML_DELIMITER, yaml.dump(metadata).strip(), YAML_DELIMITER])
                new_post.write(header)
            
            self.__openInEditor(filepath)

        # Regenerate posts list
        self.__init__()
    
    def __openInEditor(self, post):
        # Assumes Linux & MacOS have EDITOR env variable set
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            os.system('%s %s' % (os.getenv('EDITOR'), post))
        elif platform.system() == 'Windows':
            os.system(post)

    def __editPost(self):
        self.__displayPosts()

        print('\nWhich post would you like to edit?')
        postnum = input('je> ')
        
        try:
            post = self.posts[int(postnum)]
        except Exception:
            print("That post doesn't exist!")
            return

        self.__openInEditor(post)

    def __displayPosts(self):
        for i, file in enumerate(self.posts):
            print(f'{Fore.RED}{i:<3}{Style.RESET_ALL}{self.__grabInfo(file)["Title"]}')

    def __viewPost(self):
        self.__displayPosts()
        
        print('\nWhich post would you like to view?')
        postnum = input('jv> ')
        
        try:
            post = self.posts[int(postnum)]
        except Exception:
            print("That post doesn't exist!")
            return

        print("This is still in progress. Opening in your editor...")
        self.__openInEditor(post)

    def __grabInfo(self, post) -> dict:
        postdata = self.__grabYAML(post)
        # Grab the title from the header, or from the filename
        title = postdata.get('title')
        date = postdata.get('date')
        categories = postdata.get('categories')
        tags = postdata.get('tags')

        # Following the filename structure of YYYY-MM-DD-name.md
        filename = os.path.basename(post)
        f_info = filename.strip('.md').split('-')
        f_date = '-'.join(f_info[:3])
        f_title = ' '.join(f_info[3:])

        # Assign file-found date and title if one is not specified in header
        if not date:
            date = f_date

        if not title:
            # Maybe some people won't want it to be displayed in title case?
            title = f_title.title()

        # Check for 'category' name also
        if not categories:
            categories = postdata.get('category')

        # Create the view
        return {
            "Title" : title,
            "Date"  : date,
            "Categories" : categories,
            "Tags" : tags,
        }


    def __listPosts(self) -> None:
        # TODO: Maybe make this dynamic? Where you can pass in what you'd like to grab...
        """
        Should be able to view:
            - title
            - date
            - categories
            - tags
        """
        postviews = {}
        for post in self.posts:
            info = self.__grabInfo(post)
            postviews[info['Title']] = {
                'Date'       : info['Date'],
                'Categories' : info['Categories'],
                'Tags'       : info['Tags']
            }

        for i, name in enumerate(postviews.keys()):
            print(f'{Fore.RED}{i:<4}{Style.RESET_ALL + Style.BRIGHT}{name}')
            for dname, value in postviews[name].items():
                print(f'{"":<6}{Style.BRIGHT + Fore.GREEN}{dname:<15}', end="")
                if isinstance(value, list):
                    print(f'{", ".join(value):<15}')
                elif value is None:
                    print(f'{"None":<15}')
                else:
                    print(f'{value:<15}')
                
    def __deletePost(self):
        self.__displayPosts()

        prompt = 'jd> '
        print('\nWhich post would you like to delete?')
        postnum = input(prompt)
        
        try:
            post_title = self.__grabInfo(self.posts[int(postnum)])['Title']
            print(f"Please confirm by typing '{post_title.upper()}' in uppercase.")
        except Exception as e:
            print(e)
            print("That post doesn't exist!")
            return

        confirmation = input(prompt)
        if confirmation == post_title.upper():
            print(f"Deleting post: {post_title}")
            os.remove(self.posts[int(postnum)])
        else:
            print("Confirmation unsuccessful. Not deleting...")

        # Regenerate posts
        self.__init__()

    def __grabYAML(self, file) -> dict:
        """
        :params:
            file: open() return value
        :description:
            This should (theoretically) parse the yaml header data from the top of
            markdown files, where the yaml content is enclosed with ---, which is 
            the global identifier for the start (and end) of a YAML file

            NOTE: This only reads the first delimited YAML region of the file
        """
        with open(file, 'r') as filedata:
            start = False
            data = ""
            for line in filedata.readlines():
                if line.strip() == YAML_DELIMITER:
                    if start: break
                    else: start = True
                    continue
                data += line
            return yaml.load(data, Loader=yaml.FullLoader)

if __name__ == '__main__':
    m = Manager()
    m()
