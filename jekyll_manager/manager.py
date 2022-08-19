
# NOTE: This is not being used...

import os
import sys
import yaml
from colorama import (
    Fore, 
    Style,
)
from datetime import datetime

from jekyll_manager.exceptions import JekyllRootException
from jekyll_manager.post import Post
from jekyll_manager.utils import (
    makeBright,
    makeRed,
    makeBlue,
    YAML_DELIMITER,
)

COUNTER_START = 1

class Manager:

    def __init__(self, root) -> None:
        self.root = root
        self.posts = list()

        try:
            # This should always be correct, as per the documentation: https://jekyllrb.com/docs/posts/
            self.posts_path = os.path.join(self.root, '_posts')
        except TypeError:
            if not root: raise JekyllRootException("Root directory not specified")
            raise JekyllRootException(f"Root directory: '{root}' is invalid")

        if not os.path.isdir(self.posts_path):
            raise JekyllRootException('_posts directory not found')
        
        # Grab all posts (should be in _posts folder as per jekyll spec)
        counter = COUNTER_START
        for blogroot,dir,posts in os.walk(self.posts_path):
            for post in posts:
                path = os.path.join(blogroot, post)
                self.posts.append(Post(path, counter))
                counter += 1

        # Set of functions that the manager can do
        self.functions = {
            "list"   :  {
                "Description" : "List all posts",
                "Function"    : self.listPosts,
            },
            "view"   :  {
                "Description" : "View a posts",
                "Function"    : self.viewPosts,
            },
            "edit"   :  {
                "Description" : "Edit a post",
                "Function"    : self.editPosts,
            },
            "create"   :  {
                "Description" : "Create a post",
                "Function"    : self.createPosts,
            },
            "delete"   :  {
                "Description" : "Delete a posts",
                "Function"    : self.deletePosts,
            },
            "menu"   :  {
                "Description" : "Display this menu",
                "Function"    : self.printMenu
            },
            "help"   :  {
                "Description" : "Display this menu",
                "Function"    : self.printMenu
            },
            "quit"  :   {
                "Description" : "Exit the program",
                "Function"    : sys.exit
            },
        }

    def __call__(self) -> None:
        # Start the prompt
        prompt = 'jm> '
        while True:
            try:
                self.parseSelection(input(prompt))
            except (KeyboardInterrupt, EOFError):
                # Print a newline so it looks nice(r)
                print()
                break

    def regeneratePosts(self) -> None:
        counter = COUNTER_START
        # Iterate through a copy of the posts list
        for post in self.posts[:]:
            if not os.path.exists(post.getPath()):
                self.posts.remove(post)
                continue
            post.setIndex(counter)
            counter += 1

    ### Menu Functions ###

    def printMenu(self) -> None:
        padding  = 2
        # Get maximum option size
        optSize  = padding + max([len(makeBright(makeRed(key))) for key in self.functions.keys()])
        # Get maximum description size
        descSize = padding + max([len(item.get("Description")) for item in self.functions.values()])
        # Set some variables
        listprefix  = '| + '
        listpostfix = ' |'
        rowdelim    = ' :'
        offset  = len(listprefix)
        delimpadding = 5

        # Create header
        header  = ' '*offset
        header += f'{makeBright(makeBlue("Option")):<{optSize}}'
        header += f'{" |":<{delimpadding}}'
        header += f'{makeBright(makeBlue("Description")):<{descSize}}'

        # NOTE: Not sure why a constant 5 is needed here, but it's needed.
        seperator = '-' * (len(header) - optSize + (optSize-descSize) - 5)

        # Print header of table
        print(header)
        # Print seperator
        print(seperator)

        for key in self.functions.keys():
            row  = listprefix.ljust(offset)
            row += makeBright(makeRed(key)).ljust(optSize)
            row += rowdelim.ljust(delimpadding)
            row += self.functions.get(key)["Description"].ljust(descSize)
            row += listpostfix
            # Print row
            print(row)
        # Print end of table seperator 
        print(seperator)

    def parseSelection(self, selection) -> None:
        if selection in self.functions.keys():
            self.functions.get(selection).get('Function')()
        else:
            # Allow for shorthand calls. 
            # NOTE: This needs to be reviewed whenever a new funtion is added
            for key in self.functions.keys():
                if key.startswith(selection):
                    function = self.functions.get(key)
                    function.get('Function')()
                    return
            print("Invalid option. Type 'menu' for a list of options")

    ### Post functions ###

    def listPosts(self) -> None:
        for post in self.posts:
            post.display()

    def editPosts(self) -> None:
        # Print all posts available to edit
        self.listPosts()
        # Prompt for post number to edit
        prompt = 'Post number to edit: '
        postnum = input(prompt)
        try:
            # Edit the post with the corresponding post number
            self.posts[int(postnum)-COUNTER_START].edit()
        except (IndexError, ValueError):
            print('Invalid post number.')

    def viewPosts(self) -> None:
        # Print all posts available to view
        self.listPosts()
        # Prompt for post number to view
        prompt = 'Post number to view: '
        postnum = input(prompt)
        try:
            # View the post with the corresponding post number
            self.posts[int(postnum)-COUNTER_START].view()
        except (IndexError, ValueError):
            print('Invalid post number.')
    
    def deletePosts(self) -> None:
        # Print all posts available to view
        self.listPosts()
        # Prompt for post number to view
        prompt = 'Post to delete: '
        postnum = input(prompt)
        try:
            post = self.posts[int(postnum)-COUNTER_START]
            title = post.getTitle()
            print(f"To verify, please type '{title.upper()}'")
            confirmation = input('confirmation: ')
            if confirmation != title.upper():
                print('Verificaiton failed. Not deleting...')
            else:
                print('Verification successful. Deleting post...')
                if not post.delete():
                    print('An error occured while deleting')
            self.regeneratePosts()
        except (IndexError, ValueError):
            print('Invalid post number.')

    def createPosts(self) -> None:
        # TODO: How do I add more items that they can add in the creation
        """
        Needs to select:
            - Date
            - Title
            - Categories
            - Tags

        Then, open in editor
        """
        # Grab the title of the post
        title = input('Post title: ')

        # Check if that title already exists
        for post in self.posts:
            if post.getTitle().lower() == title.lower():
                print('This post already exists.')
                isEdit = input('Would you like to edit the post [Y/N]: ')
                if isEdit.lower() == 'y':
                    post.edit()
                return

        while True:
            try:
                # Grab the date for the post
                print('Date format: YYYY MM DD')
                date = input('Post date: ')
                date = datetime.strptime(date, '%Y %m %d').strftime(f'%Y-%m-%d ')
                break
            except ValueError:
                prompt = 'Invalid date. Try again [y/n]: '
                reattempt = input(prompt)
                if reattempt.lower().startswith('y'):
                    continue
                else:
                    return

        file_extension = '.md'
        filename_delim = '-'

        filename = date + title.lower()
        filename = filename_delim.join(filename.strip().split()) + file_extension
        filepath = os.path.join(self.posts_path, filename)

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
            
            post = Post(filepath, -1)
            self.posts.append(post)
            self.regeneratePosts()
            post.edit()
            print('Post created')

