
import os
import logging as log
import platform
import datetime

import frontmatter

import jekyll_manager.utils as utils
from jekyll_manager.utils import (
    grabinfo,
    makeRed,
    makeBright,
    markdownCount,
)

class Post():

    def __init__(self, path: str, index: int) -> None:
        
        self.index = index

        # Ensure file exists
        if not os.path.exists(path):
            log.error("File not found")
            return

        self.path = path
        with open(self.path, 'r') as post:
            self.data = post.read()

        self.postfix = '.md'    # Default
        self.delimiter = '-'    # Default

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
            os.system('%s %s %s' % (editor, self.path, viewonly.get(editor,'')))
        elif platform.system() == 'Windows':
            os.system(post)
        else:
            print("This operating system is not yet supported.")

    def display(self) -> None:
        """
        :description:
            Prints out the index and title of a post
        """
        # Generate output (allows for 4 digit numbers)
        output  = utils.makeRed(self.index).ljust(9 + 4)
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

    def printInfo(self) -> None:
        """
        :description:
            Prints out information about the post such as:
                - Title
                - Date
                - Index
                - Word Count
        """
        title = self.getTitle()
        date  = self.getDate()
        index = self.getIndex()
        words = self.getWordCount()

        info_len = 22

        linestart = "".ljust(5)
        output  = linestart + makeBright("Title:").ljust(info_len) + title + '\n'
        output += linestart + makeBright("Date:").ljust(info_len) + date + '\n'
        for key in self.metadata:
            output += linestart + makeBright(key.title()+":").ljust(info_len) + str(self.metadata.get(key)) + '\n'
        output += linestart + makeBright("Index:").ljust(info_len) + str(index) + '\n'
        output += linestart + makeBright("Word Count:").ljust(info_len) + str(words)

        print(output)

    def getTitle(self) -> str:
        return self.title

    def getDate(self) -> str:
        return self.date

    def getPath(self) -> str:
        return self.path

    def getIndex(self) -> int:
        return self.index

    def getWordCount(self) -> int:
        with open(self.path, 'r') as post:
            data = frontmatter.load(post)
            content = data.content
            return markdownCount(content)

    def setTitle(self, title: str) -> bool:
        # Change title in filename NOTE: This is on hold. might not be needed
        # Change title inside file
        # Grab info from new path (to ensure that it was updated)

        # Considerations:
        #   - How do you keep the ordering in the header the same
        #   - How do you keep comments / anything else there the same
        #   - Only want to change the title, absolutely NOTHING else
        """
        :params:
            title: str 
        :description:
            Sets the new title in the files metadata (if there previously), as 
            well as alters the filename to match.
        """

        # Grab the date from the filename
        f_name  = os.path.basename(self.getPath()).strip(self.postfix).split(self.delimiter)
        # This assumes that the filename follows the correct pattern (i.e. YYYY-MM-DD-title.md)
        f_date = f_name[:3]
        new_name = self.delimiter.join(f_date) + self.delimiter + self.delimiter.join(title.split()) + self.postfix
        # Check if the file already exists
        f_path = os.path.join(os.path.dirname(self.getPath()), new_name)
        if os.path.exists(f_path):
            return False
        
        # Try rename the file
        try:
            os.rename(self.path, f_path)
            # Set the new path
            self.path = f_path
        except FileNotFoundError:
            return False

        # Load metadata from the file
        post = frontmatter.loads(self.data)
        # If the post attribute is in the metadata, change it
        if post.metadata.get('title', False):
            # Change the post metadata
            post.metadata['title'] = title

            # Save the new post metadata
            with open(self.path, 'w') as postfile:
                postfile.write(frontmatter.dumps(post))

        self.title = title
        return True

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

    def setDate(self, date: str) -> bool:
        """
        :params:
            date: str in isoformat (i.e. YYYY-MM-DD)
        :description:
            Sets the new date in the files metadata (if there previously), as 
            well as alters the filename to match.
        """
        # Ensure date is in correct format (i.e. YYYY-MM-DD)
        try:
            date = datetime.date.fromisoformat(str(date))
        except ValueError:
            return False

        # Grab the date from the filename
        f_name  = os.path.basename(self.getPath()).strip(self.postfix).split(self.delimiter)
        # This assumes that the filename follows the correct pattern (i.e. YYYY-MM-DD-title.md)
        f_title = f_name[3:]
        new_name = str(date) + self.delimiter + self.delimiter.join(f_title) + self.postfix
        # Check if the file already exists
        f_path = os.path.join(os.path.dirname(self.getPath()), new_name)
        if os.path.exists(f_path):
            return False
        
        # Try rename the file
        try:
            os.rename(self.path, f_path)
            # Set the new path
            self.path = f_path
        except FileNotFoundError:
            return False

        # Load metadata from the file
        post = frontmatter.loads(self.data)
        # If the post attribute is in the metadata, change it
        if post.metadata.get('date', False):
            # Change the post metadata
            post.metadata['date'] = date

            # Save the new post metadata
            with open(self.path, 'w') as postfile:
                postfile.write(frontmatter.dumps(post))
        self.date = date
        return True

    def setPath(self, path) -> bool:
        """
        :params:
            path : str = path that already exists.
        """
        if os.path.exists(path):
            self.path = path
            return True
        return False

