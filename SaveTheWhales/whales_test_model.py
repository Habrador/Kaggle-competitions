#===============================================================================
# Get the predicted results from loaded pickle model
#===============================================================================

import csv
from sklearn.ensemble import *
import pickle

FOLDER_PATH = r'c:/Erik/Projekt/Kaggle/Save the Whales/data'


#------------------------------------------------------------------------------ 
# Functions
def read_csv(filename):
    """Read the file with test data"""
    file_path = FOLDER_PATH + filename
    
    #Open up the csv file in to an object
    csv_file_object = csv.reader(open(file_path, 'r'))
    
    #Run through each row in the csv file adding each row to the data variable
    data = []
    for counter,row in enumerate(csv_file_object):
        data.append([float(number) for number in row[1::]]) #From str to float
        
        #Limit the data to test
        """
        if counter == 10:
            break
        """
    
    return data


def predict_data(data,model_name):
    """Load pickle file and get the predicted results"""

    pickleFileName = FOLDER_PATH + model_name
    
    pickleFile = open(pickleFileName, 'rb')
    
    trained_model = pickle.load(pickleFile)
    
    pickleFile.close()
    
    #Test the loaded pickle
    #final_data = forest.predict(test_data)
    #We need probabilities that its a right whale = prob that its 1
    final_data = trained_model.predict_proba(data) #[prob that its 0, prob that its 1]
    
    final_data = [item[1] for item in final_data]
    
    #final_data_prob = []
    #for item in final_data:
        #final_data_prob.append(item[1])
    
    return final_data


#------------------------------------------------------------------------------ 
# Main program

#Get the test data - needed 2 files to avoid memory error
test_data1 = read_csv(r'/test_data1_zoomed_best.csv')
test_data2 = read_csv(r'/test_data2_zoomed_best.csv')
test_data3 = read_csv(r'/test_data3_zoomed_best.csv')
#test_data2 = read_csv(r'/test_data2_zoomed_smooth.csv')
#test_data3 = read_csv(r'/test_data3_zoomed_smooth.csv')

print 'Load data finished!'

#Get the predicted numbers
model_name = r'/trained_forest_zoomed_best_n1000.pickle'
test_data1 = predict_data(test_data1,model_name)
test_data2 = predict_data(test_data2,model_name)
test_data3 = predict_data(test_data3,model_name)

print 'Prediction finished!'

#Combine the two data lists
#for item in test_data2:
    #test_data1.append(item)
test_data1.extend(test_data2)
test_data1.extend(test_data3)

#for item in test_data3:
    #test_data1.append(item)


#------------------------------------------------------------------------------ 
# Print the results to a file
file_path = FOLDER_PATH + r'\final_forest_zoomed_best_n1000.csv'

open_file_object = csv.writer(open(file_path,'wb'),delimiter=',')

for i in range(len(test_data1)):
    open_file_object.writerow([test_data1[i]])
