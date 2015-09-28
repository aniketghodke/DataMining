__author__ = ‘Aniket’

'''
Main.py : This is the main project code. It is a python script which reads several
text file that created before hand during information analysis and create in memory
maps for each of them.
Then it run our User Guided Search algorithm with ranking functions to find predictions
for a given test paper or set of test paper.

IMPORTANT: KEEP ALL FILES INTACT AND DON'T DELETE ANY FILES. JUST PASTE THESE TWO FILES
FROM DATA PRE PROCESSING JAVA CODE. THE TWO FILES TO BE PASTED ARE:
Train_Data_Matrix.txt
Test_Data_Matrix.txt
'''

#Import statement
import operator


#Global constants and parameters

#Number of predictions to be made for a paper
prediction_paper_set_size = 10
#Counter to check how many test papers have been processed.
count = 1

#--------------------------Data Definition and Processing Section Begins-------------------------------#


            #--------------Create Citation count Map---------------------------#

'''
Data Structure for storing the citation counts of papers from training data. It is a
map with keys as paper indices from Training data and values as citations of each paper.
'''
citation_map = {}

'''
File handler for reading the citation information for training papers from text file.
'''
citation_map_handler = open("Citations.txt", "r")

'''
Here we read the citation file and create a citation map
Code to create citation map
'''
for line in citation_map_handler:
    line = line.strip()
    current_data_point = line.split(';')
    paper_index = int(current_data_point[0])
    paper_citation_count = (len(current_data_point[1]))
    if paper_citation_count > 1:
        citation_map[paper_index] = paper_citation_count
print "Length of Citation Map is: " + str(len(citation_map))

            #--------------Create Citation count Map Done---------------------------#

            #--------------------Code to create h-index map-------------------------#

'''
Data structure for storing the H Index of all the authors from training and testing
data. It is also a pre processed file made during information analysis of the problem
It is a map with keys as Author names strings and values as their H Index.
'''
h_index_map = {}

'''
File handler for reading the H index file and storing info in the map.
'''
#Here we read the the H Index file and create a H index map
h_index_map_handler = open("H_index.txt", "r")


for line in h_index_map_handler:
    line = line.strip()
    current_data_point = line.split(';')
    author_name = current_data_point[0]
    paper_h_index = int(current_data_point[1])
    if paper_h_index > 1:
        h_index_map[author_name] = paper_h_index
print "Length of H-Index Map is: " + str(len(h_index_map))

             #--------------------Code to create h-index map---------------------------#


            #--------------------Code to create the test paper to its bucket_id map----#

'''
Data structure to store the paper index as key and values as bucket id of the buckets formed
in Generate_Bucket.py file.
'''
paper_to_bucket_id_map = {}

'''
File handler for reading the paper_to_bucket_id file. Here paper is test paper
'''
paper_to_bucket_id_map_handler = open("paperid_bucketid.txt", "r")

#Here we read the Test Paper to Bucket Id file and create a map for it
for line in paper_to_bucket_id_map_handler:
    line = line.strip()
    current_data_point = line.split('\t')
    current_test_paper = int(current_data_point[0])
    current_test_paper_bucket_id = int(current_data_point[1])
    paper_to_bucket_id_map[current_test_paper] = current_test_paper_bucket_id
print "Length of Test paper to Bucket Id Map is: " + str(len(paper_to_bucket_id_map))

        #--------------------Code to create the test paper to its bucket_id map----#


        #--------------------Code to create bucket_id to bucket map----------------#

'''
Data structure Map for storing mapping of bucket_id to paper list of buckets.
'''
bucket_id_to_papers_map = {}

'''
File Handler to read the id to paper list mapping file.
'''
bucket_id_to_papers_map_handler = open("Final_Term_Buckets.txt", "r")

for line in bucket_id_to_papers_map_handler:
    line = line.strip()
    line = line.split('\t')
    current_bucket_id = int(line[0])
    current_buckets_papers = list(line[1].split(' '))
    bucket_id_to_papers_map[current_bucket_id] = current_buckets_papers
print "Length of Bucket Id to Papers Map is: " + str(len(bucket_id_to_papers_map))

        #--------------------Code to create bucket_id to bucket map----------------#

        #--------------------Code to write the references map----------------------#

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

for line in references_map_handler:
    line = line.strip()
    line = line.split('\t')
    paper = int(line[0])
    references = (line[1].split(','))
    references_map[paper] = references

print "Length of References Map is: " + str(len(references_map))

        #--------------------Code to write the references map----------------------#


        #--------------------Code to create the author map--------------------------------#

'''
Data structure map to store author names as keys and paper written by them as
the values.
'''
author_to_paper_list_map = {}

'''
File handler to read the file of auhtor-paper written file.
'''
author_to_paper_list_map_handler = open("Author_Paper.txt", "r")


for line in author_to_paper_list_map_handler:
    line = line.strip()
    line = line.split(';')
    current_author = str(line[0])
    paper_written_by_this_author = (line[1].split(','))
    author_to_paper_list_map[current_author] = paper_written_by_this_author
print "Length of author_to_paper_list_map is: " + str(len(author_to_paper_list_map))

        #--------------------Code to create the author map--------------------------------#


        #--------------------Code to create the paper to author map-----------------------#

'''
Data structure map to store paper index as key and name of author for that paper as
value.
'''
paper_to_author_name_map = {}

'''
File handler to read the file to create above map of paper-author names.
'''
paper_to_author_name_map_handler = open("Paper_To_Author.txt", "r")


for line in paper_to_author_name_map_handler:
    line = line.strip()
    line = line.split('\t')
    if len(line) == 2:
        if line[0] != '' and line[1] != '':
            paper = int(line[0])
            if len(line[1]) > 1:
                papers_author = (line[1].split(','))
            else:
                papers_author =line[1]
            paper_to_author_name_map[paper] = papers_author
print "Length of paper_to_author_name_map is: " + str(len(paper_to_author_name_map))

         #--------------------Code to create the paper to author map-----------------------#

#Here we read the input from Part_1
partial_citations_map = {}
part_1_input_file_handler = open("Part_1.txt", "r")

#Code for reading and creating the map
for line in part_1_input_file_handler:
    line = line.strip()
    line = line.split(',')
    test_paper = int(line[0])
    partial_citations = (line[1].split(' '))
    partial_citations_map[test_paper] = partial_citations
print "Length of Partial Citation Map from Intermediate Stage is: " + str(len(partial_citations_map))

'''
Code to read bucket file from Generate_Buckets.py and store it in the map
'''
test_paper_to_bucket_map_handler = open("Final_Term_Buckets.txt", "r")
test_paper_to_bucket_map = {}

for line in test_paper_to_bucket_map_handler:
    line = line.strip()
    line = line.split('\t')
    current_test_paper = int(line[0])
    current_test_paper_bucket = list(line[1].split(' '))
    test_paper_to_bucket_map[current_test_paper] = current_test_paper_bucket

#Here we write the answer or predictions for one query paper to a final_output file
'''
File handler for writing final prediction results
'''
final_output_file = open("Predictions_Guided_Search.txt", "w")
#Write the first line as per Kaggle submission
final_output_file.write("Id, References\n")
#--------------------------Data Definition and Processing Section Ends---------------------------------#


'''
Here the main Algorithm is implemented.
Outer loop on every test paper
Algo:
1. Loop on every test paper
2. Find predictions using ranking functions
3. Repeat
'''
for test_paper in test_paper_to_bucket_map:
    #Loop variable
    count += 1
    print count

    test_paper = int(test_paper)
    #Find the first test paper and it's bucket
    #current_test_paper_bucket_id = int(paper_to_bucket_id_map[test_paper])
    #Now we have id, find the bucket/list of papers from second map
    #if current_test_paper_bucket_id in bucket_id_to_papers_map:
    #    current_test_paper_bucket = set(bucket_id_to_papers_map[current_test_paper_bucket_id])

    current_test_paper_bucket = set(test_paper_to_bucket_map[test_paper])

    '''
    Here we define our temporary data structures for the current test paper and use below
    mentioned ranking functions to find top 10 citations for it.
    '''

    #Final prediction set of papers for current test paper
    current_test_paper_predictions = set()

    #Find current test paper's author
    current_test_paper_author = (paper_to_author_name_map[test_paper])
    current_test_paper_author = ','.join(map(str, current_test_paper_author))
    current_test_paper_author_list = current_test_paper_author.split(',')

    #Find all papers written by this author from train data if any.
    paper_written_by_author = set()

    for author in current_test_paper_author_list:
        #Check to see if author in map
        if author in author_to_paper_list_map:
            #Find all papers writtern by this author
            temp_paper_written = set(author_to_paper_list_map[author])
            paper_written_by_author = paper_written_by_author.union(temp_paper_written)


    #Now we use our first Ranking function to find predictions
    '''
    Algo: Append partial results obtained from intermediate PCP Meta Path and
    add them to final prediction list
    '''
    partial_citations = set(partial_citations_map[test_paper])
    temp_set = partial_citations.intersection(current_test_paper_bucket)
    current_test_paper_predictions = current_test_paper_predictions.union(temp_set)

    '''
    Ranking function 1.1
    If the author of current test paper has written some previous papers and they are in
    this 500 papers bucket, then he is likely to cite his own papers.
    Algo:
    1. Find current test paper's author
    2. Find all papers written by this author from train data if any.
    3. Check if there are any papers by this same author in the 500 paper bucket we have.
    4. If we have any papers, add all of them to final prediction paper set.
    5. If not, do nothing and move ahead, use further ranking functions to fill the 10 papers list
    '''

    if len(paper_written_by_author) > 0:
        temp_set = current_test_paper_bucket.intersection(paper_written_by_author)
        for paper in temp_set:
        #for paper in paper_written_by_author:
            if len(current_test_paper_predictions) < 10:
                current_test_paper_predictions.add(paper)

        #Do second round to add more that do not intersect with 500 paper bucket
        for paper in paper_written_by_author:
            if len(current_test_paper_predictions) < 10 and paper not in current_test_paper_predictions:
                current_test_paper_predictions.add(paper)

    #Now we use our second Ranking function to find predictions
    '''
    Use Ranking function 2 only if length of final prediction set is less than 10
    Ranking function 2
    If the author of current test paper has has written some papers earlier and referred some
    papers already, then this author is likely to cite again those papers which he has already
    cited.
    Algo
    1. Find the current test paper's author
    2. Find all papers written by this author already.
    3. Find the papers referred by this author in his previous papers using references map
    4. Check if any of the papers from step 3 are in 500 papers bucket, if yes, add them to
    final prediction. If not, take all such papers and add them to final prediction set.
    '''

    if len(paper_written_by_author) > 0:
        #Temp set of papers according to PCP Meta Path
        for previous_paper in paper_written_by_author:
            previous_paper = int(previous_paper)
            if previous_paper in references_map:
                previous_paper_references = set(references_map[previous_paper])
                for paper in previous_paper_references:
                    if len(current_test_paper_predictions) < prediction_paper_set_size:
                        current_test_paper_predictions.add(paper)

    #Now we use of third Ranking function to find predictions
    '''
    Use Ranking function 3 only if length of final prediction set is less than 10
    Ranking function 3
    A author is likely to cite papers who have citation count and are of same area.
    Similarly, a author is likely to cite paper's of author's whose H index is high
    since High Index denotes good credibility.
    Algo:
    1. Find the all the papers whose citation count is more than threshold value and
    add them to final prediction set.
    2. Find all the papers whose authors have a high H index than a given threshold and
    add them to final prediction set.
    '''

    if len(current_test_paper_predictions) < prediction_paper_set_size:
        current_length = prediction_paper_set_size - len(current_test_paper_predictions)
        #Find citations of all 500 papers and create a temp dict
        temp_cit_dict = {}
        for paper in current_test_paper_bucket:
            paper = int(paper)
            if paper in citation_map:
                current_bucket_paper_citation_count = citation_map[paper]
                temp_cit_dict[paper] = current_bucket_paper_citation_count
        sorted_temp_cit_list = sorted(temp_cit_dict.items(), key=operator.itemgetter(1), reverse=True)
        for i in xrange(current_length):
            current_tuple = sorted_temp_cit_list[i]
            paper_to_add = int(current_tuple[0])
            #Add the paper with highest citation count to prediction set
            current_test_paper_predictions.add(paper_to_add)

    #final_output_file.write(str(test_paper)+","+str(len(current_test_paper_predictions))+"\n")
    current_test_paper_predictions = ' '.join(map(str, current_test_paper_predictions))
    final_output_file.write(str(test_paper)+","+current_test_paper_predictions+"\n")

#--------------------------------------Algorithm Ends--------------------------------------------------#