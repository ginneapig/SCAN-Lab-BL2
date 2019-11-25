'''This program creates objects for each directory encountered using directory.py,
meant for ease of accessing attributes about a directory. It (should) then 
organizes and creates an Excel sheet of all directories with subdirectories 
and subfiles in a horizontal format.

This script must exist directly inside of the starting/root directory. 
It accesses all items inside using the os.listdir(path) function.

Apparently os.scandir() is fastest and least expensive. Personally 
found difficulty in accessing root directory, however, unless script is placed 
outside of root directory -- in which case there then needs to be more
maneuvering to locate the correct directory this script should target.'''

from directory import Directory # imports Directory class

import os

def main():
    dir_path = os.getcwd()
    root_name = os.path.basename(dir_path)
    root_dir = Directory(root_name) # initialize root Directory object

    check_directory(dir_path, root_dir)
    structure_spaces(root_dir)

def check_directory(dir_path, root_dir):
    '''Takes in a Directory object to traverse all items within it 
    and call this function recursively until all Directory objects
    are initialized and completed.'''
    for entry in os.listdir(dir_path): # "entry" is a String
        entry_path = os.path.join(dir_path, entry)
        if (not entry.startswith('.')):
            if (os.path.isdir(entry_path)): 
                new_dir = Directory(entry, root_dir)
                root_dir.add_subdir(new_dir)
                check_directory(entry_path, new_dir) # directories recursively created
            elif (os.path.isfile(entry_path)):
                root_dir.add_subfile(entry)

def structure_spaces(root_dir):
    if (not root_dir.subdirs()): # subdirectory list is empty
        root_dir.set_filelines(root_dir.num_items - 1)
        return root_dir.num_items() - 1
    else:
        pass
        # figure out recursion dude.

main()
