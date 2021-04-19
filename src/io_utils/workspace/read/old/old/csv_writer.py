# -*- coding: utf-8 -*-

import os
import csv

'''
This module is used to read / write data from dictionaries as csv files and 
contains functions for data manipulation.
'''

class dict_csv_wrapper(object):

    def __init__(self, data):
        '''
        Initialize the csv handler class.
        Either takes a dictionary of the correct form or uses the input as a path

        The csv file look like this:
            header: var1, var2, ...
            data:   val1, val2, ...
                    ...   ...

        Parameters
        ----------
        data : dict or str
            if data is an existing file, open this file as an existing csv file
            if data is a dictionary, create a log file from the passed data
        '''
        if isinstance(data, dict):
            self.content = data
        else:
            self.content = self._read(data) #type: dict
        self.header = sorted(self.content.keys()) #type: list

    @staticmethod
    def merge_dicts(*dict_args):
        '''
        Merge the content of multiple dictionaries into one.
        Parameters
        ----------
        dict_args : dict
            Input dictionaries to merge

        Returns
        -------
        merged : dict
            The merged dictionary
        '''
        merged = None
        for dictionary in dict_args:
            if not merged:
                merged = dictionary
            else:
                for key, cont in dictionary.items():
                    merged[key] += cont
        return merged

    def asint(self):
        '''
        Maps the content of a csv object to integers

        Returns
        -------
        '''
        for n, d in self.content.items():
            self.content[n] = map(int, self.content[n])


    def asfloat(self):
        '''
        Maps the content of a csv object to floats

        Returns
        -------
        '''
        for n, d in self.content.items():
            self.content[n] = map(float, self.content[n])

    def __int__(self):
        '''
        Maps the content of a csv object to integers

        Returns
        -------
        '''
        for n, d in self.content.items():
            self.content[n] = map(int, self.content[n])


    def __float__(self):
        '''
        Maps the content of a csv object to floats

        Returns
        -------
        '''
        for n, d in self.content.items():
            self.content[n] = map(float, self.content[n])


    def check_headers(self, other):
        '''
        Checks if headers of 2 csv objects are equal, raises Exception if not
        Parameters
        ----------
        other : dict_csv_wrapper
            another csv object

        Returns
        -------
        isequal : bool
            is True (otherwise an exception is thrown)

        '''
        for key in other.header:
            if key not in self.header:
                raise Exception("%s only exists in one file header" % key)
        return True

    def join_files(self, output_file=None, remove_old=True,  *others):
        for other in others:
            self.append(other)
            if remove_old:
                os.remove(other)
        if output_file:
            self.write(output_file)

        return self.content


    def _read(self, file_to_read):
        '''
        Reads data from an existing csv file

        Parameters
        ----------
        file_to_read : str
            full path to file that should be read

        Returns
        -------
        file_data : list
            File content in list form
        '''

        with open(file_to_read, mode='r') as infile:
            reader = csv.reader(infile)
            header = None
            file_data = {}
            for i, row in enumerate(reader):
                if i == 0:
                    header = row
                    for var in header:
                        file_data[var] = []
                else:
                    for h, r in zip(header, row):
                        if r:
                            file_data[h].append(r)
        return file_data

    def append(self, other):
        '''
        Appends the content of one csv object to this one.

        Parameters
        ----------
        other : dict or str
            The other csv object (existing or from dict)

        Returns
        -------

        '''
        other_file = dict_csv_wrapper(other)
        if self.check_headers(other_file):
            self.content = self.merge_dicts(self.content, other_file.content)

    def write(self, output_file):
        '''
        Write content of this object to a .csv file
        Parameters
        ----------
        output_file : str
            path to the file that should be written

        Returns
        -------

        '''
        with open(output_file, 'wb') as outfile:
            w = csv.writer(outfile, delimiter = ",")
            w.writerow(self.header)
            w.writerows(zip(*[self.content[key] for key in self.header]))


if __name__ == '__main__':
    file = dict_csv_wrapper({'var1':[1,2,3], 'var2':[1,2,3], 'var3': [1,2,3]})
    joined = file.join_files(r"C:\Temp\csv\merged.csv", True, r"C:\Temp\csv\test2.csv",
                             r"C:\Temp\csv\test3.csv")



