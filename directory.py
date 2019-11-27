# This file declares the Directory class for ease of accessing
# various attributes about directories when creating an Excel file.

import os

class Directory:
    def __init__(self, name, super_dir=None):
        '''Initializes Directory object. Super directory optional.
        PARAM: string for name of directory, integer for number of files
        in directory, integer for number of subdirectories, string for 
        name of super directory. 
        ## may change the ints to linked lists or lists.
        '''
        self._name = name
        self._subfiles = [] # holds String objects
        self._subdirs = []  # holds Directory objects
        self._super_dir = super_dir
        self._filelines = 0 # for Excel sheet
    
    def name(self):
        '''Returns string of directory name.'''
        return self._name

    def num_items(self):
        '''Returns integer representing number of files and folders in the directory.'''
        return len(self._subfiles) + len(self._subdirs)

    def num_files(self):
        '''Returns integer representing number of files in the directory.'''
        return len(self._subfiles)
    
    def subfiles(self):
        '''Returns list of subfiles.'''
        return [subfile_name for subfile in self._subfiles]
    
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

    def super_dir(self):
        '''Returns string of super directory name, or None if there is no
        super directory.'''
        if (self._super_dir != None):
            return self._super_dir
        return None

    def filelines(self):
        '''Return the attribute referring to the number of empty lines
        that go below this directory's name to allow for proper spacing
        between directories in the sheet.'''
        return self._filelines

    def add_filelines(self, count):
        '''Add to the number of empty filelines that will go below 
        this directory name in the Excel.'''
        self._filelines += count

    def remove_filelines(self, count):
        '''Remove any number of filelines.'''
        self._filelines -= count

    def print_tree(self, count):
        os.system('tabs -4')
        print(count, '\t'*count, self._name)
        for subdir in self._subdirs:
            subdir.print_tree(count + 1)

