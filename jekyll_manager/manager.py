
# NOTE: This is not being used...

import os
import sys
import yaml
from colorama import (
    Fore, 
    Style,
)
from datetime import datetime

from post import Post

from utils import (
    makeBright,
    makeRed
)

class Manager:

    def __init__(self, root):
        self.root = root
        self.posts = list()
        
        # Grab all posts (should be in _posts folder as per jekyll spec)
        counter = 0
        for blogroot,dir,posts in os.walk(os.path.join(self.root, '_posts')):
            for post in posts:
                path = os.path.join(blogroot, post)
                self.posts.append(Post(path, counter))
                counter += 1

        # Set of functions that the manager can do
        self.functions = {
            "list"   :  {
                "Description" : "List all posts",
                "Function" : self.listPosts,
            },
            "menu"   :  {
                "Description" : "Display this menu",
                "Function" : self.printMenu
            },
            "exit"  :   {
                "Description" : "Exit the program",
                "Function" : sys.exit
            },
        }

    def __call__(self):
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
        counter = 0
        # Iterate through a copy of the posts list
        for post in self.posts[:]:
            if not os.path.exists(post.getPath()):
                self.posts.remove(post)
                continue
            post.setIndex(counter)
            counter += 1

    def listPosts(self):
        for post in self.posts:
            post.display()

    def printMenu(self) -> None:
        padding  = 2
        # Get maximum option size
        optSize  = padding + max([len(key) for key in self.functions.keys()])
        # Get maximum description size
        descSize = padding + max([len(item.get("Description")) for item in self.functions.values()])
        offset  = 2  #TODO: Calculate this so it's dynamic
        #                           What is this hard-coded 5?!
        seperator = '-' * (padding + optSize + 5 + descSize + offset)
        # Create header
        header  = ' '*offset
        header += f'{makeBright("Option"):<{optSize}}'
        header += f'{" |":<5}'
        header += f'{makeBright("Description"):<{descSize}}'

        # Print header of table
        print(header)
        print(seperator)

        for key in self.functions.keys():
            row  = f'| + {makeBright(makeRed(key)):<{optSize}}'
            row += f'{" :":<5}'
            row += f'{self.functions.get(key)["Description"]:<{descSize}} |'
            # Print row
            print(row)
        # Print end of table seperator 
        print(seperator)

    def parseSelection(self, selection):
        pass
    
# For testing
if __name__ == '__main__':
    m = Manager('/home/turd/Documents/Projects/LukewarmWebsite')
    m.printMenu()
    m.listPosts()
    # import colorama
    # def maker(text):
    #     return f'{colorama.Fore.RED}{text}{colorama.Style.RESET_ALL}'
    #
    # output = maker(str(4)).ljust(5)
    # output += "example"
    # print(output)
