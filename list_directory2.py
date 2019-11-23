# list_directory2.py that creates objects for each directory encountered.
# meant for ease of accessing attributes about a directory.
# This script must exist directly inside of the starting directory.

from directory import Directory # imports Directory class

import os

def main():
    directory = os.getcwd()
    root_name = os.path.basename(directory.strip('/'))

    root_dir = Directory(root_name)
    check_directory(root_dir)

    print(root_dir.subdirs())


def get_root_dir():
    script_path = os.getcwd()
    script_dir = os.path.basename

def check_directory(root_dir):
    '''Takes in the root Directory object to traverse all items
    within it and call this function recursively until all Directory objects
    have been created and implemented.'''
    for entry in os.scandir(root_dir.name()): 
        if (not entry.name.startswith('.')):
            if(entry.is_dir()):
                new_dir = Directory(entry.name, root_dir)
                root_dir.add_subdir()
                check_directory(new_dir) # recursive call
            elif (entry.is_file()):
                root_dir.add_subfile(entry.name)


main()
