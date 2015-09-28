CS6220
Group Information:
Team Name� Dark Knights
Team Id � 10

Team Members -
Aniket Ghodke (ghodke.a@husky.neu.edu)
Akshay Sawant (sawant.ak@husky.neu.edu)
Chintan Pathak (pathak.c@husky.neu.edu)
Kunal Bohra (bohra.k@husky.neu.edu)

Project's README File
Approach : Topic and Document Similarity combined with User Guided Search 
Language: Python 

System Requirements to run the code
1. Python 2.x or more running on system
2. 8GB or more RAM
3. 50 GB or more HDD space
4. Intel Pentitum Processor i5 or higher


How to run the code:

1. First go to folder named PreProcessing - Matrix_Creation in the current directory of this file. 
2. Follow all the instructions there, and the code would generate two processed files for training data and test data. 
3. Copy these two files in the folder Main_Project. 
4. There are already other pre processed data files there along with 3 python scripts which contain the code. 
5. Now change your current working directory to Main_Project.
6. There you should see several text file and 2 new files for testing and training data copied by you. Don't change or delete any other file. 
   As they are used by Main.py (main project script) to run and generate output
7. From command line under this present working directory run following command:
   Let's assumer your current working is Main_Project which is under home, then run following scripts in given order only

   NOTE: FOR EXISTING TEST AND TRAIN DATA GIVEN TO US, JUST RUN 3 COMMAND BELOW. FOR NEW TEST DATASET, RUN 1, 2 AND 3. PLEASE
   ALLOW SUFFICIENT TIME FOR PROCESSING.

1   ~Main_Project$python Create_Author_Maps.py : Take 5 minutes
2   ~Main_Project$python Generate_Buckets.py   : Takes 3 hours approx to create term bukcet file named "Final_Term_Buckets.txt"
3   ~Main_Project$python Main.py               : Takes 25 seconds to generate final result set for approx 6205 test papers.

IMPORTANT NOTE: IF YOUR TESTING NEW TEST DATASET THAN THAT GIVEN TO US, THEN YOU MUST WAIT FOR 3 HOURS TO LET Generate_Buckets.py
CREATE THE BUKCET FILE. WITHOUT BUCKET FILE, ANSWER CANNOT BE GENERATED.
SO FOR FIRST RUN OF COMPLETE CODE, APPROX 3 HOURS ARE NEEDED.
WE HAVE ALREADY SUPPLIED PREDICTIONS FOR TEST DATA GIVEN TO US IN Predictions_Guided_Search.txt
   
IMPORTANT NOTE: All the 3 script above take testing and training data files with exact names only. Please change the names of test and train data
files you get from pre processing and paste them with same name here in folder Main_Project.

Training Data: Train_Data_Matrix.txt
Testing Data: Test_Data_Matrix.txt
  
8. After 15-25 seconds, a text file named Predictions_Guided_Search is created in current working directory which contains
   the final results. Currently the file has 6205 predictions for given test data. 
