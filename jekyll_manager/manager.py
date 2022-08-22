
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
                "args"        : False,
            },
            "info"   :  {
                "Description" : "Display post information",
                "Function"    : self.infoPosts,
                "args"        : True,
            },
            "view"   :  {
                "Description" : "View a posts",
                "Function"    : self.viewPosts,
                "args"        : True,
            },
            "edit"   :  {
                "Description" : "Edit a post",
                "Function"    : self.editPosts,
                "args"        : True,
            },
            "create"   :  {
                "Description" : "Create a post",
                "Function"    : self.createPosts,
                "args"        : False,
            },
            "delete"   :  {
                "Description" : "Delete a posts",
                "Function"    : self.deletePosts,
                "args"        : True,
            },
            "menu"   :  {
                "Description" : "Display this menu",
                "Function"    : self.printMenu,
                "args"        : False,
            },
            "help"   :  {
                "Description" : "Display this menu",
                "Function"    : self.printMenu,
                "args"        : False,
            },
            "quit"  :   {
                "Description" : "Exit the program",
                "Function"    : sys.exit,
                "args"        : False,
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
        print(descSize)
        print(optSize)
        print(len(makeBlue(makeBright("Description"))))
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
        seperator = '-' * (len(header) - len(makeBright(makeBlue(''))))

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
        """
        :params:
            selection: str = the input from the user
        :description:
            This should be able to satisfy the following:
                - Shorthand calls (i.e., just typing in e for edit, or q for quit)
                - Handling multiple arguments (i.e., e 3, or edit 4)
        """
        # Split the users input, space delimited
        selection = selection.strip().split(' ')
        # Seperate the command
        command = selection[0]

        # Ensure command is non-empty
        if len(command) < 1:
            return 

        # Seperate out the arguments
        if len(selection) > 1:
            arguments = selection[1:]
        else:
            arguments = None

        # Check if command matches / is a substring of any of the menu options
        #   If it's a substring of more than one menu function, then fail. 

        possibilities = []

        for fkey in self.functions:
            if fkey.find(command) == 0:
                possibilities.append(fkey)
                
        if len(possibilities) != 1:
            print("Invalid option. Type 'menu' for a list of options.")
            return

        menu_item = self.functions.get(possibilities[0])

        # Grab the function 
        func = menu_item.get("Function")

        # Grab args
        func_args = menu_item.get("args")

        # Pass arguments through if there are any
        if func_args:
            func(arguments)
        else:
            func()
        return

    ### Post functions ###

    def getPost(self, postnum) -> Post:
        try: postnum = int(postnum)
        except ValueError: return None

        if postnum < COUNTER_START or postnum >= (len(self.posts)+COUNTER_START):
            return None

        try: return self.posts[postnum-COUNTER_START]
        except IndexError: return None

    def listPosts(self) -> None:
        for post in self.posts:
            post.display()

    def infoPosts(self, args:list) -> None:
        # Check if user put in post number in command-line argument
        if not args:
            # Prompt for post number to edit
            prompt = 'Post number to view info: '
            postnum = input(prompt)
        else:
            # Else, grab the postnum from arguments supplied
            postnum = args[0]

        post = self.getPost(postnum)
        if post:
            post.printInfo()
        else:
            print('Invalid post number')

    def editPosts(self, args:list) -> None:
        # Check if user put in post number in command-line argument
        if not args:
            # Prompt for post number to edit
            prompt = 'Post number to edit: '
            postnum = input(prompt)
        else:
            # Else, grab the postnum from arguments supplied
            postnum = args[0]

        post = self.getPost(postnum)
        if post:
            post.edit()
        else:
            print('Invalid post number')

    def viewPosts(self, args:list) -> None:
        # Check if user put in post number in command-line argument
        if not args:
            # Prompt for post number to edit
            prompt = 'Post number to edit: '
            postnum = input(prompt)
        else:
            # Else, grab the postnum from arguments supplied
            postnum = args[0]

        post = self.getPost(postnum)
        if post:
            post.view()
        else:
            print('Invalid post number')
    
    def deletePosts(self, args:list) -> None:
        # Check if user put in post number in command-line argument
        if not args:
            # Prompt for post number to edit
            prompt = 'Post number to edit: '
            postnum = input(prompt)
        else:
            # Else, grab the postnum from arguments supplied
            postnum = args[0]
        try:
            post = self.getPost(postnum)
            if not post:
                pass
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
                date = datetime.strptime(date, '%Y %m %d').strftime('%Y %m %d')
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

        filename = date + filename_delim + title.lower()
        filename = filename_delim.join(filename.strip().split()) + file_extension
        filepath = os.path.join(self.posts_path, filename)

        if not os.path.exists(filepath):
            with open(filepath, 'w') as new_post:
                metadata = {
                    "title" : title,
                    "date" : date,
                }
                header = '\n'.join([YAML_DELIMITER, yaml.dump(metadata).strip(), YAML_DELIMITER])
                new_post.write(header)
            
            post = Post(filepath, -1)
            self.posts.append(post)
            self.regeneratePosts()
            post.edit()
            print('Post created')

