#===============================================================================
# Train a model with whale data and save it to a pickle
#===============================================================================

import csv
from sklearn.ensemble import * #Random forest
from sklearn import svm #Support vector machine
import pickle
import time

FOLDER_PATH = r'c:/Erik/Projekt/Kaggle/Save the Whales/data'


#------------------------------------------------------------------------------ 
# Functions
def save_model(trained_model,name):
    """Save the trained model to a pickle file"""
    pickleFileName = FOLDER_PATH + r'/trained_' + name + r'.pickle'
    
    pickleFile = open(pickleFileName, 'wb')
    
    pickle.dump(trained_model, pickleFile, pickle.HIGHEST_PROTOCOL)
    
    pickleFile.close()


def train_random_forest(training_data,answer):
    """
    Train a random forest
    http://scikit-learn.org/dev/modules/generated/sklearn.ensemble.RandomForestClassifier.html
    """
    
    #No big difference between gini and entropy http://stats.stackexchange.com/questions/19639/which-is-a-better-cost-function-for-a-random-forest-tree-gini-index-or-entropy
    forest = RandomForestClassifier(n_estimators=1000) #500 -> 150 estimators for large datasets http://nymetro.chapter.informs.org/prac_cor_pubs/RandomForest_SteinbergD.pdf

    time_start = time.time()
    
    forest.fit(training_data,answer) #(training set, target set)
    
    #632 seconds to train n=150
    #1958 seconds to train n=500
    #4568 seconds to train n=1000
    print 'It took ', time.time()-time_start, ' seconds to train the forest!'
    
    #Save the trained model
    save_model(forest, r'forest_zoomed_best_n1000') 


def train_svm(training_data,answer):
    """Train a support vector machine"""
    
    # C is the cost to the SVM when it mis-classifies one of your training examples. If you increase it, 
    # the SVM will try very hard to fit all your data, which may be good if you strongly trust your data.
    # http://www.svms.org/parameters/
    clf = svm.SVC(C=1,probability=True,cache_size=1000) #http://scikit-learn.org/stable/modules/svm.html
    
    time_start = time.time()
    
    clf.fit(training_data,answer)
    
    #2313 seconds to train C=1, cache_size=200
    #2108 seconds to train C=1, cache_size=1000
    #3319 seconds to train C=10, cache_size=1000
    #3300 seconds to train C=100, cache_size=1000
    #14224 seconds to train C=1, cache_size=1000, probability=True
    print 'It took ', time.time()-time_start, ' seconds to train the svm!'
    
    #Save the trained model
    save_model(clf, r'svm') 


#------------------------------------------------------------------------------ 
# Read the training data

#One file
"""
file_name = FOLDER_PATH + r'/train_data_256_64.csv'

#Open up the csv file in to an object
csv_file_object = csv.reader(open(file_name, 'r'))

#Run through each row in the csv file adding each row to the data variable
train_data = []
answer = []
for counter,row in enumerate(csv_file_object):
    train_data.append([float(number) for number in row[1::]]) #From str to float
    answer.append(int(row[0])) #From str to int
    
    #Limit the data to test
    #if counter == 10:
        #break
"""

#Multiple files
file_name1 = FOLDER_PATH + r'/train_data1_zoomed_best.csv'
file_name2 = FOLDER_PATH + r'/train_data2_zoomed_best.csv'

#Open up the csv file in to an object
csv_file_object = csv.reader(open(file_name1, 'r'))

#Run through each row in the csv file adding each row to the data variable
train_data = []
answer = []
for counter,row in enumerate(csv_file_object):
    train_data.append([float(number) for number in row[1::]]) #From str to float
    answer.append(int(row[0])) #From str to int


#Open up the csv file in to an object
csv_file_object = csv.reader(open(file_name2, 'r'))

#Run through each row in the csv file adding each row to the data variable
for counter,row in enumerate(csv_file_object):
    train_data.append([float(number) for number in row[1::]]) #From str to float
    answer.append(int(row[0])) #From str to int

 
#------------------------------------------------------------------------------ 
# Train the model and save the trained object in a pickle file
print 'Start training!'
#Random forest
train_random_forest(train_data,answer)

#Support vector machine
#train_svm(train_data,answer)


