# This file declares the File class for ease of accessing
# various attributes about files when creating a CSV file.

class File:
    def __init__(self, name, pathway, super_dir):
        '''Initializes File object. Super directory not optional.
        PARAM: string for name of directory, string for 
        name of super directory, string for path. 
        '''
        self._name = name
        self._super_dir = super_dir
        self._pathway = pathway

    def name(self):
        '''Returns string of file name.'''
        return self._name

    def pathway(self):
        '''Returns string of directory pathway.'''
        return self._pathway
        
    def super_dir(self):
        '''Returns string of super directory name.'''
        return self._super_dir
