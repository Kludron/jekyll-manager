#!/usr/bin/env python

import sys
import os
import logging

from jekyll_manager.exceptions import JekyllRootException
from jekyll_manager.manager import Manager

filename = os.path.basename(__file__)
cliname = 'jekyll-manager'
env_variable = 'JEKYLL_ROOT'

usage = f'''
There are multiple ways to run {cliname}.
1. Traverse into your jekyll blog directory and run '{cliname}'
2. Set the environment variable '{env_variable}' to point to your jekyll blog directory and run '{cliname}'
3. Run '{cliname} <path/to/jekyll-blog>'
'''

def main():
    # Grab jekyll root directory
    if len(sys.argv) < 2:
        # Check if current directory is Jekyll Blog directory
        try:
            manager = Manager(os.path.abspath(os.getcwd()))
        except JekyllRootException:
            # Check if user has JEKYLL_ROOT in their environment variables
            try:
                root = os.getenv(env_variable)
                manager = Manager(root)
            except JekyllRootException as e:
                logging.error(e)
                print(usage)
                sys.exit()
    else:
        try:
            manager = Manager(sys.argv[1])
        except JekyllRootException as e:
            logging.error(e)
            print(usage)
            sys.exit()

    print(f'Opening jekyll blog @ {manager.root}')
    manager()

if __name__ == '__main__':
    main()
