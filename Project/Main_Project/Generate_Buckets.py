__author__ = ‘Aniket’

'''
This python script is used to main paper buckets file that is to be used
by the Main.py (main project script) to generate results. In this script
we read training and testing data files (pre processed) and output a paper
bucket file for each testing paper.

Input: Three text files
Train_Data_Matrix.txt which is complete training data after pre processing.
Test_Data_Matrix.txt which is compete testing data after pre processing.
References_Map.txt which is already in current working directory containing
the paper citation relations from training data

Output: One text file named New_term_buckets.txt which holds author and paper
information used by Main.py to generate final results.
'''

#Import statement
import operator

#--------------------------Data Definition Section Begins-------------------------------#

'''
Data structure for storing the citation relations from References.txt file. It's a map
with keys as papers and values as list of papers that cites other papers in the training
data.
'''
references_map = {}

'''
File handler to read teh References Map file created earlier during pre processing and
information analysis of the project.
'''
references_map_handler = open("References_Map.txt", "r")

'''
Data structure for storing topic/title terms for a given paper from the
training data. This map has keys as paper index and values for these keys
are set of term that form the title/topic of the paper.
'''
training_papers_term_map = {}

'''
Data structure for storing topic/title terms for a given paper from the
testing data. This map has keys as paper index and values for these keys
are set of term that form the title/topic of the paper.
'''
test_papers_term_map = {}

'''
File handler for writing the Term/topic paper buckets created for a given
test paper.
'''
test_paper_bucket_handler = open("Final_Term_Buckets.txt", "w")

'''
File handler for reading the training data file we get after pre processing.
'''
training_data_file_handler = open("Train_Data_Matrix.txt", "r")

'''
File handler for reading the testing data file we get after pre processing.
'''
testing_data_file_handler = open("Test_Data_Matrix.txt", "r")

'''
Counter variable to keep track of number of entries processed so for. 25 denotes
that 25 buckets for 25 test papers have been formed and written to the text file.
'''
count = 0
#--------------------------Data Definition Section Ends-------------------------------#


'''
Here we read the references map file and create a map for it.
Code to write the references map
'''
for line in references_map_handler:
    line = line.strip()
    line = line.split('\t')
    paper = int(line[0])
    references = (line[1].split(','))
    references_map[paper] = references
print "Length of References Map is: " + str(len(references_map))


#---------------------------------------------------------------------------------------#
'''
Here we read the training data and create a map for paper index, terms as
described above in data definitions section.
'''
#First read training data and fill the map with key as paper index and value as the author name/s
for line in training_data_file_handler:
    line = line.strip()
    current_data_point = line.split(';')
    paper_index = current_data_point[0]
    paper_title_terms = set(current_data_point[1].split(' '))
    training_papers_term_map[paper_index] = paper_title_terms
print "Length of Paper Term of Train is: " + str(len(training_papers_term_map))

#---------------------------------------------------------------------------------------#

'''
Here we read the testing data and create a map for paper index, terms as
described above in data definitions section.
'''
# Do the same above process for test data just like training data
for line in testing_data_file_handler:
    line = line.strip()
    current_data_point = line.split(';')
    paper_index = current_data_point[0]
    paper_title_terms = set(current_data_point[1].split(' '))
    test_papers_term_map[paper_index] = paper_title_terms
print "Length of Paper Term of Test is: " + str(len(test_papers_term_map))


#-------------------------------Algorithm Begins Here-----------------------------------#
'''
Main Algorithm to create buckets for test papers. The number of buckets are
equal to number of papers in testing file.
'''
#Now we loop N^2 to find best 500 approx. papers bucket for a given test paper
for test_paper in test_papers_term_map:
    #Count to see progress
    count += 1
    print "Number of testing papers processed so far is: " + str(count) + "..."

    #Temp storage for scores
    temp_train_paper_dict = {}
    current_test_paper_terms = test_papers_term_map[test_paper]

    #Now we loop over all train papers
    for train_paper in training_papers_term_map:
        current_train_paper_terms = training_papers_term_map[train_paper]
        #Now we find set intersection
        common_terms_set_length = len(current_test_paper_terms.intersection(current_train_paper_terms))
        temp_train_paper_dict[train_paper] = common_terms_set_length

    #Here we have a temp dict with scores of match. We sort this dict.
    sorted_temp_score_list = sorted(temp_train_paper_dict.items(), key=operator.itemgetter(1), reverse=True)

    #Clear up the memory
    temp_train_paper_dict.clear()

    #Declare the bucket data structure
    bucket_for_current_test_paper = set()

    #Fetch the papers and separate them from their scores
    for paper in sorted_temp_score_list:

        #Stop when bucket size is 500 papers
        if len(bucket_for_current_test_paper) > 500:
            break

        #Here our Main logic for creating Buckets comes into picture
        '''
        Algorithm:
        1. Take the top ranked paper where top ranked paper is whose maximum terms in topic
           match with topic of test paper.
        2. Take this paper and find it's citation relations from the references_map. Add this
           current paper and all it's citation relation papers to bucket.
           Similarly, take second paper and it's references and so on.
        3. Do this until we have a bucket of size 500.
        4. This is our PCP meta path based bucket creation.
        '''
        if paper != '' and paper[1] != 0:
            best_train_paper = int(paper[0])

            if best_train_paper in references_map:
                current_paper_references = set(references_map[best_train_paper])
                bucket_for_current_test_paper = bucket_for_current_test_paper.union(current_paper_references)
                bucket_for_current_test_paper.add(best_train_paper)

    #Convert the 500 papers bucket to string to write to a file
    bucket_for_current_test_paper = ' '.join(map(str, bucket_for_current_test_paper))
    #Write output to file
    test_paper_bucket_handler.write(str(test_paper)+"\t"+bucket_for_current_test_paper+"\n")

#-------------------------------Algorithm Ends Here-------------------------------------#