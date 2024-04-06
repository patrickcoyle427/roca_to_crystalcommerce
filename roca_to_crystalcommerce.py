!/usr/bin/env python3

'''
Takes a CSV from the ROCA sorter output file and converts it into a CSV that can be uploaded into Crystal Commerce to add nev inventory

ROCA Sorter output files are sorted lists of MTG or Pokemon cards that the ROCA Sorter arranged by set and then alphabetically

Crystal Commerce is a service primarily for trading card games such as Magic the Gathering and Pokemon Trading Card game that syncs your inventory across several
online marketplaces such as TCGPlayer, ManaPool, and eBay

USAGE:

    REQUIRED DATA: ROCA Sorter Output CSV file

    On first run of this script, two directories will be created in the same directiory as this file
        Directory names: to_parse and parsed_data

    Place ROCA sorter CSV files into the to_parse folder

'''

# TO DO:
# Actually program everything lol
# IDEA: ADD 'CC_Ready_' and keep the rest of the name the same for CC ready files that were Roca files
# 

import csv, os, os.path

# csv - reads the data from the ROCA sorter output and also used for creating the new csv to upload
# os - used for creating directories and checking directory contents
# os.path - used for thecking if the 'to_convert' and 'converted_files' directories exist

def start():

    # Runs script through each step of the conversion process

    file_names = find_csv_names()

    # Loop over files, don't combine them into 1?

def dir_check():

    # Will create necessary directories on first launch of script,
    # then will pass each other time. Gives a message to let the user know
    # what to do with the created directories

    if os.path.isdir('to_parse') and os.path.isdir('parsed_files'):

        return True

    else:

        create_these = ('to_convert', 'converted_files')

        for i in create_these:

            if not os.path.isdir(i):

                os.makedirs(i)

        print('Folders for ROCA files created in the same location as this script.',
              'Please place all files that need to be converted',
              'to Crystal Commerce files into the "to_convert" folder, then run this script again.')

        return False

def find_csv_names():

    # Finds the names of the files to be parsed.

    return [file for file in os.listdire('to_parse') if file.endswith('.csv')]

def move_files(names):

    # Moves ROCA csvfiles that were used for creating crystal commerce files to a
    # new folder so the user knows they have been processed
    
    # names - a list of file names that have been parsed

    for file in names:

        os.replace(f'to_parse/{file}', f'parsed_files/{file}')

if __name == '__main__':

    start()
