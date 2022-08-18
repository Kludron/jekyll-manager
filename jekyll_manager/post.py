
import os
import logging as log

import utils

# Remove in production
from pprint import pprint

class Post():

    def __init__(self, path: str, index: int) -> None:
        
        self.index = index

        # Ensure file exists
        if not os.path.exists(path):
            log.error("File not found")
            return

        self.path = path
        info = utils.grabinfo(self.path)

        # Title and Date are the only required parameters for a post
        self.title = info.get('title')
        self.date = info.get('date')
        self.metadata = info.get('metadata')

    def edit(self):
        """
        description:
            This function allows the post to be opened in the system editor.
        """
        pass

    def view(self):
        pass

    def display(self) -> None:
        from colorama import Fore, Style
        from utils import makeRed, makeBright
        # Generate output
        # output  = utils.makeRed(str(self.index)).ljust(4)
        # output = f'{Fore.RED}{self.index}{Style.RESET_ALL}'.ljust(4)
        output  = f'{makeBright(self.index)}'
        output += ' ' * (4-len(output))
        output += self.title
        # output += "sample"
        # Print output
        print(output)
        # import sys
        # sys.stdout.write('{}\n'.format(output))

    def getTitle(self) -> str:
        return self.title

    def getDate(self) -> str:
        return self.date

    def getPath(self) -> str:
        return self.path

    def getIndex(self) -> int:
        return self.index

    def setTitle(self, title) -> bool:
        # Change title in filename NOTE: This is on hold. might not be needed
        # Change title inside file
        # Grab info from new path (to ensure that it was updated)

        # Considerations:
        #   - How do you keep the ordering in the header the same
        #   - How do you keep comments / anything else there the same
        #   - Only want to change the title, absolutely NOTHING else
        pass

    def setIndex(sel, number) -> bool:
        self.index = number

# For testing
if __name__ == '__main__':
    p = Post('/home/turd/Documents/Projects/LukewarmWebsite/_posts/2022-08-10-template.md')
    p.printdata()
