
import os
import logging as log
import platform

import jekyll_manager.utils as utils
from jekyll_manager.utils import (
    grabinfo,
    makeRed,
)

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

    def edit(self) -> None:
        """
        :description:
            This function allows the post to be opened in the system editor.
        """
        # Assumes Linux & MacOS have EDITOR env variable set
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            os.system('%s %s' % (os.getenv('EDITOR'), self.path))
        elif platform.system() == 'Windows':
            os.system(post)
        else:
            print("This operating system is not yet supported.")

    def view(self) -> None:
        """
        :description:
            To seperate this from the normal 'edit' function, the post
            is opened in read-only mode. 

            To achieve this, the file is duplicated as a read-only document 
            in the users temporary directory, and opened from there.
        """
        # Linux only - limited view-only support
        viewonly = {
            "nvim"  : '-R',
            "vi"    : '-R',
            "vim"   : '-R',
            "nano"  : '-v',
        }
        # Assumes Linux & MacOS have EDITOR env variable set
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            # Open in view-only mode (if known)
            # Otherwise open like normal
            editor = os.getenv('EDITOR')
            os.system('%s %s %s' % (editor, self.path, viewonly.get(editor)))
        elif platform.system() == 'Windows':
            os.system(post)
        else:
            print("This operating system is not yet supported.")

    def display(self) -> None:
        """
        :description:
            Prints out the index and title of a post
        """
        # Generate output
        output  = utils.makeRed(self.index)
        output  = output.ljust(len(output)+3)
        output += self.title
        # Print output
        print(output)

    def delete(self) -> bool:
        """
        :description:
            Removes a post and returns True on success, otherwise False
        """
        try:
            os.remove(self.getPath())
            return True
        except (FileNotFoundError, TypeError):
            return False

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

    def setIndex(self, number) -> bool:
        """
        :params:
            number: int = posts index value
        :description:
            Sets the post index value to the given number.
        """
        if isinstance(number, int):
            self.index = number
            return True
        return False

    def setDate(self, date) -> bool:
        pass

    def setPath(self, path) -> bool:
        """
        :params:
            path : str = path that already exists.
        """
        if os.path.exists(path):
            self.path = path
            return True
        return False

            

# For testing
if __name__ == '__main__':
    p = Post('/home/turd/Documents/Projects/LukewarmWebsite/_posts/2022-08-10-template.md')
    p.printdata()
