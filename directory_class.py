# This file declares the Directory class for ease of accessing
# various attributes about directories when creating a CSV file.

import os

class Directory:
    def __init__(self, name, pathway, super_dir=None):
        '''Initializes Directory object. Super directory optional.
        PARAM: string for name of directory, Directory object for 
        name of super directory. 
        ## may change the ints to linked lists or lists.
        '''
        self._name = name
        self._subfiles = [] # holds File objects
        self._subdirs = []  # holds Directory objects
        self._pathway = pathway
        self._super_dir = super_dir
        
    def name(self):
        '''Returns string of directory name with a backslash.'''
        return self._name + '/'

    def num_items(self):
        '''Returns integer representing number of files and folders in the directory.'''
        return len(self._subfiles) + len(self._subdirs)

    def num_files(self):
        '''Returns integer representing number of files in the directory.'''
        return len(self._subfiles)
    
    def subfiles(self):
        '''Returns list of subfiles.'''
        return [subfile for subfile in self._subfiles]
    
    def add_subfile(self, subfile):
        '''Takes a string name of subfile and adds it to the list.'''
        self._subfiles.append(subfile)

    def remove_subfile(self, subfile):
        '''Takes a string name of subfile and removes it.
        Unlikely to be used.'''
        self._subfiles.remove(subfile)

    def num_subdirs(self):
        '''Returns integer representing number of subdirectories.'''
        return len(self._subdirs)
    
    def subdirs(self):
        '''Returns list of subdirectory objects.'''
        return [subdir for subdir in self._subdirs]

    def subdir_names(self):
        '''Returns list of strings of the names of subdirectories.'''
        return [subdir.name() for subdir in self._subdirs]

    def add_subdir(self, subdir):
        '''Takes Directory object and adds it to the list.'''
        self._subdirs.append(subdir)

    def remove_subdir(self, subdir):
        '''Takes Directory object and removes it from the list.'''
        self._subdirs.remove(subdir)

    def has_subdir(self, subdir):
        '''Takes name of subdir and returns a boolean value if 
        this subdirectory is present in this directory or not.'''
        for subdir_obj in self._subdirs:
            if (subdir == subdir_obj.name()):
                return True

    def pathway(self):
        '''Returns string of directory pathway.'''
        return self._pathway

    def super_dir(self):
        '''Returns super directory object.'''
        return self._super_dir

    def print_tree(self, count, files=False):
        '''Prints directory tree into terminal. Unless indicated by user, 
        does not print files.
        PARAM: count for tabbing, boolean for printing files or not'''
        os.system('tabs -4') # sets tabs for homogeneity
        print(count, '\t'*count, self._name + '/')
        for subdir in self._subdirs:
            subdir.print_tree(count + 1, files)
        if (files): # want to print files
            for fil in self._subfiles:
                print(count, '\t'*(count+1), fil)
