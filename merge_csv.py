""" BESKRIVELSE AV SCRIPT """
""" 
For at dette scriptet skal fungere må filene som skal konverteres og settes sammen eksistere i samme mappe som denne filen. 
Etter kjøring vil en ny fil bli lagt til i mappen med navn: "combined_csv".
"""

import time
import os
import glob
import pandas as pd
from csv import reader
from csv import writer

#timing
start = time.time()

prefix = 'eco'
prefix_output = 'converted'
new_column_header = 'Source.Name'
extension = 'csv'

all_input_filenames = [i for i in glob.glob(f'{prefix}*.{extension}')]

print('Lenght: ',len(all_input_filenames))

# input_file: file path / name of the input csv file, it will read the contents of this csv file
# output_file: file path / name of the output csv file, it will write modified contents in this csv file
# transform_row: A callback function, that receives a list and modifies that list
def add_column_in_csv(input_file, output_file, transform_row):
    """ Append a column in existing csv using csv.reader / csv.writer classes"""
    # Open the input_file in read mode and output_file in write mode
    with open(input_file, 'r') as read_obj, \
            open(output_file, 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = reader(read_obj)
        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)
        # Read each row of the input csv file as list
        for row in csv_reader:
            # Pass the list / row in the transform function to add column text for this row
            transform_row(row, csv_reader.line_num)
            # Write the updated row / list to the output file
            csv_writer.writerow(row)

for file in all_input_filenames:
    transformLambda = lambda row, line_num: row.insert(0, new_column_header) if line_num == 1 else row.insert(0,file)
    add_column_in_csv(file, 'converted_' + file,transformLambda)
    

#List of converted files
all_output_filenames = [i for i in glob.glob(f'{prefix_output}*.{extension}')]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_output_filenames ])
#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

#delete converted files
for file in all_output_filenames:
    if os.path.exists(file):
        os.remove(file)

#timing
end = time.time()
total_time = end - start
print("\n"+ str(total_time))
