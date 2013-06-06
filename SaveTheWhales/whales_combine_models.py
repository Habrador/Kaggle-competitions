#===============================================================================
# Whales - combine finished models
#===============================================================================

import csv

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
        data.append(float(row[0])) #From str to float
    
    return data


data1 = read_csv(r'/final_forest_zoomed_smooth+zoomed_10_4.csv')
data2 = read_csv(r'/final_forest_zoomed_best_n1000.csv')
#data3 = read_csv(r'/final_forest_zoomed_smooth_n2000_part3.csv')
#print data1
combined_data=[]
for counter,item in enumerate(data1):
    combined_data.append((data1[counter]+data2[counter])/2)
    
#combined_data.extend(data1)
#combined_data.extend(data2)
#combined_data.extend(data3)


#------------------------------------------------------------------------------ 
# Print the results to a file
file_path = FOLDER_PATH + r'\final_forest_zoomed_smooth+zoomed_10_4+best.csv'

open_file_object = csv.writer(open(file_path,'wb'),delimiter=',')

for i in range(len(combined_data)):
    open_file_object.writerow([combined_data[i]])