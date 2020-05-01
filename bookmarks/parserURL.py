""" Little script to get all the urls from a chrome bookmarks export file.
First step for a simple cli program to clean/manage bookmarks.
TODO 
CLI menu to choose values for pattern, path, fileNames and debug print options (with defaults) before instantiating
Error handle: invalid or nonexistent files
FUTURE
- iterate over urls showing name and place inside bookmarks directory tree:
open in browser, change place in directory tree, delete, change name
- firefox support, test usability of current methods in other setups
"""


import re
import pathlib
import logging

# Set logger
logger = logging.getLogger("URLExtractor")
logging.basicConfig(level=logging.INFO, format="[%(name)s] [%(levelname)s] - %(message)s")

class URLExtractor():

    def __init__(self, pattern, file_path, dump_file, parsed_file):

        # Regex URL pattern
        self.pattern = pattern
        # Path for bookmarks dump input and collected urls output files
        self.file_path = file_path
        # Bookmarks export html file name
        self.dump_file = dump_file
        # Parsed urls output file name
        self.parsed_file = parsed_file

        # List to store each line from the bookmarks file
        self.file_lines = []
        # list to store only lines with <a> tag
        self.a_tags=[]
        # list to store the urls found by the pattern in each line
        self.urls=[]

        # separated stages for fine tuning each one according to own needs
        self.load_dump()
        self.filter_tag()
        self.filter_url()
        self.save_output()
        
        # parameters: debug_print(r, n) (default = 0, 0)
        # r: print raw output  n: print number of urls found
        self.debug_print(0, 1)

    def load_dump(self):
        """ Open dump_file in file_path, read lines to list and strip them """
        with open(self.file_path / self.dump_file, encoding="utf8") as f:

            self.file_lines = f.read().splitlines()

        # strip each line (so pattern matches)
        for i in range(len(self.file_lines)):

            self.file_lines[i] = self.file_lines[i].strip()

    def filter_tag(self):
        """ Filter lines starting with '<dt><a'
        (because chrome stores each bookmark (<a> tag and content
        plus other info) inside description list terms (<dt>))
        """
        for line in self.file_lines:

            if line[0:6] == '<DT><A':

                self.a_tags.append(line)

    def filter_url(self):
        """ Filter urls from tag filtered lines """
        for line in self.a_tags:

            s = re.search(self.pattern,line)
            if s:

                self.urls.append(s.group())

    def save_output(self):
         """ Output an url per line to parsed_file """
         with open(self.file_path / self.parsed_file,'w') as f:

            for url in self.urls: f.write(url + "\n")

         logger.info("File written")

    def debug_print(self, r=0, n=0):
        """ Logs raw output and/or number of urls found """
        if r:

            # console raw print
            for url in self.urls: logger.info(url)
                
        if n:

            # console print number of urls found
            logger.info("Urls found: "+str(len(self.urls)))



if __name__ == "__main__":
    pattern = r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
    file_path = pathlib.Path("F:\\bookmarkParser\\")
    dump_file = "bookmarks_chrome.html"
    parsed_file = "urls.txt"
    ext = URLExtractor(pattern, file_path, dump_file, parsed_file)

def create_parser():
    """ cli menu [WIP] """
    pass
