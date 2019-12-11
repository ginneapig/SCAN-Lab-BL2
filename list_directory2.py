'''This program creates objects for each directory encountered using directory.py,
meant for ease of accessing attributes about a directory. It (should) then
organizes and creates an Excel sheet of all directories with subdirectories
and subfiles in a horizontal format.

This script must exist directly inside of the starting/root directory.
It accesses all items inside using the os.listdir(path) function.

Apparently os.scandir() is fastest and least expensive. Personally
found difficulty in accessing root directory, however, unless script is placed
outside of root directory -- in which case there then needs to be more
maneuvering to locate the correct directory this script must target.

Helper functions are always listed underneath the function they're called by.'''

import os
import csv
import string   # may not need, was orig. using for detecting symbols

# from xlsxwriter import Workbook #v1.2.5

from directory_class import Directory # imports Directory class
from file_class import File


def main():
    dir_path = os.getcwd()
    root_name = fix_root_name(dir_path)
    root_dir = Directory(root_name, dir_path) # initialize root Directory object

    check_directory(dir_path, root_dir)

    method = input('1 - Print to the terminal\n2 - Print to a CSV\nSelect an option: ')
    if (method == '1'):
        root_dir.print_tree(0, True) # uncomment for printing to terminal
    elif (method == '2'):
        counts_dict = {} # only stores strings, not objects
        # initialize file and writer outside of recursive writing fxn
        csv_file = open(root_name + '.csv', 'w') 
        csv_writer = csv.writer(csv_file, delimiter=',') 
        write_tree_csv(csv_writer, root_dir, 0, counts_dict)
        
        # sort_method = input('1 - Print alphabetically.\n2 - idk. Select an option: ')
        sort_method = '1' #temp
        if (sort_method == '1'):
            alpha_counts_dict = alphabet_sort(root_name, counts_dict)
            counts_file(root_name, alpha_counts_dict)
    else:
        print('Incorrect input. Please run the program again.')


def fix_root_name(dir_path):
    '''Pulls root name from os library basename() function and lowercases
    as well as adds underscores between words.
    PARAM: directory path
    RETURN: string representing CSV tree file name'''
    root_name = os.path.basename(dir_path).split()
    fixed_root = ''
    for word in root_name:
        word = word.lower()
        fixed_root += word + '-'

    return fixed_root.strip('-')


def check_directory(dir_path, root_dir):
    '''Takes in a path and a Directory object to traverse all items within it
    and call this function recursively until all Directory objects
    are initialized and completed.'''
    for entry in os.listdir(dir_path): # "entry" is a String
        entry_path = os.path.join(dir_path, entry)
        if (not entry.startswith('.')):
            if (os.path.isdir(entry_path)):
                new_dir = Directory(entry, entry_path, root_dir)
                root_dir.add_subdir(new_dir)
                check_directory(entry_path, new_dir) # directories recursively created
            elif (os.path.isfile(entry_path)):
                new_file = File(entry, entry_path, root_dir)
                root_dir.add_subfile(new_file)


def write_tree_csv(csv_writer, root_dir, level, counts_dict):
    '''Recursive: writes the tree CSV file. Recursively passes in each subdirectory.
    PARAM: CSV writer tool from csv library, Directory object representing root
        directory, int representing level at which file or folder is at in the tree.
    RETURN: none'''
    root_dir_name = get_string_name(root_dir) 
    curr_line = []
    curr_line.extend(['' for i in range(level)])
    curr_line.append(root_dir_name + '/')
    csv_writer.writerow(curr_line)   # holds only one directory name

    for subdir in root_dir.subdirs():
        counting_helper(counts_dict, subdir) # not part of main CSV creation
        write_tree_csv(csv_writer, subdir, level + 1, counts_dict) # recursive call

    for subfile in root_dir.subfiles():
        counting_helper(counts_dict, subfile)
        subfile_name = get_string_name(subfile) # calls helper
        file_line = []
        file_line.extend(['' for i in range(level+1)]) # files always one indent more
        file_line.append(subfile_name)
        csv_writer.writerow(file_line) # holds only one file name

def get_string_name(entry):
    '''Helper function: for write_tree_csv(), both Directory and File classes 
    have .name() function to return String of Directory or File name. Checks symbol(s).
    PARAM: Directory or File object
    RETURN: string name of object'''
    if (entry.name().startswith('-')):
        entry_name = '\'' + entry.name() # prevents Excel from reading as operation
    else:
        entry_name = entry.name()
    return entry_name

def counting_helper(counts_dict, entry):
    '''Helper function: for write_tree_csv(), add object to string key.
    Note: directory names have '/' appended automatically when .name() called.
    PARAM: dictionary to hold names keyed to list of objects, Directory or File object.
    RETURN: none'''
    if entry.name() in counts_dict:
        counts_dict[entry.name()].append(entry)
    else:
        counts_dict[entry.name()] = [entry]


def alphabet_sort(root_name, counts_dict):
    '''Sorts dictionary of file and directory names alphabetically.
    Calls counts_file() to create the CSV.
    PARAM: string name of root to pass to counts_file(), dictionary of counts.
    RETURN: none'''
    dirs = {}
    files = {}
    for name in counts_dict:
        if (name[-1] == '/'):
            dirs[name] = counts_dict[name] # still string keyed to lists
        else:
            files[name] = counts_dict[name]

    # separate dictionaries, sorted
    sorted_dirs = {k:v for k,v in sorted(dirs.items(), key=lambda item:item[0])}
    sorted_files = {k:v for k,v in sorted(files.items(), key=lambda item:item[0])}
    
    sorted_dirs.update(sorted_files)    # combine separate dictionaries again
    return sorted_dirs


def counts_file(root_name, counts_dict):
    '''Helper: for all sorting fxns, creates a CSV for showing the count of all 
    repeated items. Option to print all items or option to print items with greater than 
    one repetition, which also prints the pathways of all objects with the same name.
    PARAM: dictionary holding names and counts, sorted in different ways.
    RETURN: none'''
    csv_file2 = open(root_name + '_counts.csv', 'w')
    csv_writer = csv.writer(csv_file2, delimiter=',')

    repeat = input('1 - Display all files/folders\n2 - Display only those repeated\nSelect an option: ')
    if (repeat == '1'):
        for item in counts_dict.items():
            csv_writer.writerow([item[0], len(item[1])])

    elif (repeat == '2'): # only print repeated ones with pathways
        for item in counts_dict.items():
            if (len(item[1]) > 1):
                csv_writer.writerow([item[0], len(item[1])])
                for entry in item[1]:
                    csv_writer.writerow(['', entry.pathway()])


main()
