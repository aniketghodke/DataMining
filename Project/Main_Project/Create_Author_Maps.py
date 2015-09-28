__author__ = ‘Aniket’

'''
This file is used to generate Author related information from
Training and Testing Data.

Input: Two text files
Train_Data_Matrix.txt which is complete training data after pre processing.
Test_Data_Matrix.txt which is compete testing data after pre processing.

Output: One text file named Paper_To_Author.txt which holds author and paper
information used by Main.py
'''

#---------------------------Data Definitions Section------------------------------------#

'''
Data structure to store author and paper information. It's a dictionary where
keys are paper indexes from testing as well training data and values of these
keys are author list. This author list denotes that paper denoted by key is written
by authors in the list.
'''
author_info_map = {}

'''
File handler for writing the author info map to a text file to be used by Main.py
'''
paper_to_author_name_map_handler = open("Paper_To_Author.txt", "w")

'''
File handler to read the Training data file.
'''
input_train_file = open("Train_Data_Matrix.txt", "r")

'''
File handler to read the Testing data file.
'''
input_test_file = open("Test_Data_Matrix.txt", "r")

#---------------------------Data Definitions Section Ends------------------------------#


#---------------------------Main script begins-----------------------------------------#

#First read training data and fill the map with key as paper index and value as the author name/s
for line in input_train_file:
    #Read the current line of file and remove newline
    line = line.strip()
    #Split the line into two parts, paper index and paper's author list
    current_data_point = line.split(';')
    paper_index = current_data_point[0]
    paper_to_author = current_data_point[2].split(',')
    #Add entry to the map
    author_info_map[paper_index] = paper_to_author


# Do the same above process for test data
for line in input_test_file:
    #Read the current line of file and remove newline
    line = line.strip()
    #Split the line into two parts, paper index and paper's author list
    current_data_point = line.split(';')
    paper_index = current_data_point[0]
    paper_to_author = current_data_point[2].split(',')
    #Add entry to the map
    author_info_map[paper_index] = paper_to_author


# Now write the map to a text file
for paper in author_info_map:
    #Convert the list representation to a , separated string.
    author_list = ','.join(map(str, author_info_map[paper]))
    paper_to_author_name_map_handler.write(paper+"\t"+author_list+"\n")


print "Length of Final Map is: " + str(len(author_info_map))

#---------------------------Main script ends-----------------------------------------#

