#===============================================================================
# Split a csv into smaller csvs
#===============================================================================

import csv

FOLDER_PATH = r'c:/Erik/Projekt/Kaggle/Save the Whales/data'


def read_csv(file_name,start,end):
    """Read the file with test data"""
    file_path = FOLDER_PATH + file_name
    
    #Open up the csv file in to an object
    csv_file_object = csv.reader(open(file_path, 'r'))
    
    #Run through each row in the csv file adding each row to the data variable
    data = []
    for counter,row in enumerate(csv_file_object):
        
        if counter == end:
            break
        
        if counter >= start:
            data.append([row[0],[float(number) for number in row[1::]]]) #From str to float
    
    return data


def print_to_csv(data,file_name):
    """Print everything to csv"""
    file_path = FOLDER_PATH + file_name
    open_file_object = csv.writer(open(file_path,'wb'),delimiter=',')
    
    for i in range(len(data)):
        #From [x,[1,2,3]] -> [z,1,2,3] to easier write to csv file
        standardized = [data[i][0]]
        #standardized.append(data[i][0])
        standardized.extend(data[i][1]) #Same as append but add an entire list
        #for item in data[i][1]:
            #standardized.append(item)
        
        open_file_object.writerow(standardized)
        

#------------------------------------------------------------------------------ 
#Main

#data = read_csv(r'/test_data2_zoomed_smooth_temp.csv',0,20000)
data = read_csv(r'/test_data2_zoomed_smooth_temp.csv',20000,100000)
#print data[0]
print_to_csv(data,r'/test_data3_zoomed_smooth.csv')
