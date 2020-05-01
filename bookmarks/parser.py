import re
import json

class BookmarkParser():

    def __init__(self, infile):
        # Read input file, lines to list, strip each line.
        # Utf8 because spanish
        self.file_lines = []

        with open(infile, encoding='utf8') as f:

            self.file_lines = f.read().splitlines()

            for i in range(len(self.file_lines)):

                self.file_lines[i] = self.file_lines[i].strip()


        # self.tree: dict with the whole structure
        # root: key that holds all the structure in its value, it's used
        # to have a root directory that is not the tree itself
        self.tree = {'root':{}}

        # list to store the path of the current directory through the iteration,
        # used by change_folder
        self.path = ['root']

        # reference to the tree used by change_folder
        self.folder = self.tree

        self.change_folder()
        self.iterate()
        self.save()

    def change_folder(self):
        # change the folder reference to the last folder in path
        self.folder = self.tree[self.path[-1]]

    def iterate(self):
        # Iterate html lines to parse structure from <DT H3 and </DL, and data from <DT H3 and <DT A
        for line in self.file_lines:

            # If the first tag is DT
            if line[1:3] == 'DT':

                # And if the second tag is A
                if line[5] == 'A':
                    # Its a link: get its parameters and append to current folder
                    self.handle_link(line)
                    

                # If the second tag is H3
                elif line[5:7] == 'H3':
                    # Its a folder: get its parameters, append to current folder,
                    # create this folder with meta subfolder, and set current folder to this
                    self.handle_folder(line)

            # If tag is /DL we closed current folder: pop it from self.path and change folder
            elif line[1:4] == '/DL':

                self.path.pop()
                self.change_folder()

    def handle_link(self, line):
        name = re.findall('(?<=>).*?(?=<)', line)[1]
        href = re.search('(?<=HREF=").*?(?=")', line).group()
        add_date = re.search('(?<=ADD_DATE=").*?(?=")', line).group()
        icono = re.search('(?<=ICON=").*?(?=")', line)
        icon=''

        if icono:

            # Not all links have one
            icon = icono.group()

        info = {
            'url':href,
            'add_date':add_date,
            'icon':icon
        }

        self.folder.update({name:info})
    
    def handle_folder(self, line):
        name = re.findall('(?<=>).*?(?=<)', line)[1]
        # last_modified = re.search('(?<=LAST_MODIFIED=").*?(?=")', line).group()
        # add_date = re.search('(?<=ADD_DATE=").*?(?=")', line).group()

        # info = {
        #     'add_date':add_date,
        #     'last_modified':last_modified
        # }

        self.folder.update({name:{'meta':info}})
        self.path.append(name)
        self.change_folder()
    
    def save(self):
        # Save the tree dict to a json file. Using utf8 here because spanish.
        with open('parsed_bookmarks.json','w',encoding='utf8') as outfile:

            json.dump(self.tree, outfile, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    
    parser = BookmarkParser('bookmarks_chrome.html')
