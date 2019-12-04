'''This program creates objects for each directory encountered using directory.py,
meant for ease of accessing attributes about a directory. It (should) then 
organizes and creates an Excel sheet of all directories with subdirectories 
and subfiles in a horizontal format.

This script must exist directly inside of the starting/root directory. 
It accesses all items inside using the os.listdir(path) function.

Apparently os.scandir() is fastest and least expensive. Personally 
found difficulty in accessing root directory, however, unless script is placed 
outside of root directory -- in which case there then needs to be more
maneuvering to locate the correct directory this script must target.'''

import os
import csv
from directory import Directory # imports Directory class
# from xlsxwriter import Workbook #v1.2.5 

def main():
    dir_path = os.getcwd()
    root_name = os.path.basename(dir_path)
    root_dir = Directory(root_name) # initialize root Directory object

    check_directory(dir_path, root_dir)
    # structure_spaces(root_dir) # currently unnecessary 

    # root_dir.print_tree(0, True) # uncomment for printing to terminal

    count_names = {}
    csv_file = open(root_name + '.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=',')
    create_csv(csv_writer, root_dir, 0, count_names)
    
    # show_counts(count_names)

def check_directory(dir_path, root_dir):
    '''Takes in a path and a Directory object to traverse all items within it 
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
    ##may remove
    '''Recursively adds counts of items to each directory with use
    of a helper function. Removes one line at the end to account for one item
    being on the same line as the directory name.
    PARAM: Directory object'''
    if (not root_dir.subdirs()): # subdirectory list is empty
        to_add = root_dir.num_items()
        # root_dir.add_filelines(root_dir.num_items - 1)
        add_upwards(root_dir, to_add)
    else:
        for subdir in root_dir.subdirs():
            structure_spaces(subdir)
        if (root_dir.num_items() != 0):
            root_dir.remove_filelines(1)    # after loop, added all subdirectories' counts

def add_upwards(curr_dir, to_add):
    ##may remove
    '''Helper function for structure_spaces(root_dir).
    Recursively adds the same number of items to each super directory.
    PARAM: current Directory object, int representing number of items'''
    curr_dir.add_filelines(to_add)
    while (not curr_dir.super_dir()): # if super directory exists
        add_upwards(curr_dir.super_dir(), to_add)

def create_csv(csv_writer, root_dir, count, count_names):
    '''Writes the CSV file. Recursively passes in each subdirectory.
    PARAM: CSV writer tool from csv library, Directory object representing root
        directory, int representing level at which file or folder is at in the tree.
    RETURN: none'''
    curr_line = []
    curr_line.extend(['' for i in range(count)])
    curr_line.append(root_dir.name() + '/')
    csv_writer.writerow(curr_line)   # holds only one directory name

    for subdir in root_dir.subdirs():
        counting_helper(count_names, subdir.name() + '/')
        # recursive call allows for items in each folder written immediately after folder name
        create_csv(csv_writer, subdir, count + 1, count_names) 

    for subfile in root_dir.subfiles():
        counting_helper(count_names, subfile)
        file_line = []
        file_line.extend(['' for i in range(count+1)]) # files always one indent more
        file_line.append(subfile)
        csv_writer.writerow(file_line) # holds only one file name

def counting_helper(count_names, name):
    '''Helps count number of times a name occurs.
    PARAM: dictionary to hold counts, string for directory or file name.
    RETURN: none'''
    if name in count_names:
        count_names[name] += 1
    else: 
        count_names[name] = 1

def show_counts(count_names):
    '''Creates a second CSV for showing the count of all repeated items.
    May make it print the whole file pathway, unsure how that's going to go.
    PARAM: dictionary holding names and counts.
    RETURN: none'''
    csv_file2 = open('counts.csv', 'w')
    csv_writer = csv.writer(csv_file2, delimiter=',')

    repeat = input('Display all files/folders or only those repeated? ')
    if ('all' in repeat.lower()):
        for item in count_names.items():
            csv_writer.writerow([item[0], item[1]])

    else: # only print repeated ones
        for item in count_names.items():
            if (item[1] > 1):
                csv_writer.writerow([item[0], item[1]])

main()
