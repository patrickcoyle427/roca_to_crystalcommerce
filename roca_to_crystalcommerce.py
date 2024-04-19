#!/usr/bin/env python3

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

    dir_exist = dir_check()

    if dir_exist:

        file_names = find_csv_names()

        if len(file_names) == 0:

            # Won't run script if there are no files to scan

            print('No files found. Please put any files to convert in the "to_convert" directory')
            user_response = input('Press enter to exit...')

            while user_response != '':

                user_response = input('Press enter to exit... ')

                continue
                
            exit()
            
        for name in file_names:

            # Goes through each file individually to create Crystal Commerce .csv files
            # Lets the user upload based on sort rather than forcing them to sort
            # each box together before uploading

            pull_data(name)

        move_files(file_names)
        
        print('Files converted! They are found in the same directory as this script!')
        user_response = input('Press enter to exit...')

        while user_response != '':

            user_response = input('Press enter to exit...')

            continue

def dir_check():

    # Will create necessary directories on first launch of script,
    # then will pass each other time. Gives a message to let the user know
    # what to do with the created directories

    if os.path.isdir('to_convert') and os.path.isdir('converted_files'):

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

    return [file for file in os.listdir('to_convert') if file.endswith('.csv')]

def move_files(names):

    # Moves ROCA csvfiles that were used for creating crystal commerce files to a
    # new folder so the user knows they have been processed
    
    # names - a list of file names that have been converted
    
    for file in names:

        os.replace(f'to_convert/{file}', f'converted_files/{file}')

def pull_data(f_name):

    # f_name - .csv file to be loaded

    data = []
    # will hold csv data after being loaded

    # Condition, old_price, and old_sku are columns on the Crystal Commerce csv
    # These values will always be added in for those columns
    # Condition default is Near Mint. It's the most likely condition for cards being added
    # old_sku is not used by CC but the csv has it so it's added here

    condition = 'Near Mint'
    old_sku = 'abcde'

    with open(f'to_convert/{f_name}', newline='') as csvfile:

        reader = csv.reader(csvfile, delimiter=',')

        next(reader, None)
        # Skips the header line

        for row in reader:

            name = row[0]
            category = row[1]
            old_price = row[2]
            language = row[4]
            qty = row[5]

            quote_removal_check = (name, category)

            for i in quote_removal_check:

                if i[0] == '"' or i[0] == "'":
                    # Remove quotation marks

                    length = len(i)

                    to_switch = i[1:length-1]

                    if i == name:

                        name = to_switch

                    else:

                        category = to_switch

            column_data = (name, qty, condition, category, old_price, old_sku, language)
            
            data.append(column_data)

        write_file(data, f_name)

def write_file(data, old_file_name):

    # Writes the csv file to put into crystal commerce

    # data - the csv data read from ROCA sorter output
    # old_file_name - the ROCA sorter output file name

    new_file_name = 'CC_READY_' + old_file_name[:len(old_file_name)-4] + '.csv'
    # Builds the new file name

    with open(new_file_name, 'w', newline='\n') as csvfile:
        
        writer = csv.writer (csvfile, delimiter=',')

        writer.writerow(['Product Name', 'Add Qty', 'Condition', 'Category', 'OLDPRICE', 'OLDSKU', 'Language'])

        for row in data:

            writer.writerow(row)

    print(f'{new_file_name} has been created')
                                               
if __name__ == '__main__':

    start()
