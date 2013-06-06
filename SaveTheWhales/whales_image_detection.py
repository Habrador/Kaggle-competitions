#===============================================================================
# Whales - using image detection
#===============================================================================

import csv

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm #Colors for the average plots
from sklearn.decomposition import RandomizedPCA #Get eigenfaces
from sklearn.ensemble import * #Random forest
import time
import pickle

FOLDER_PATH = r'c:/Erik/Projekt/Kaggle/Save the Whales/data'


#------------------------------------------------------------------------------ 
#Functions
def read_csv(file_name):
    """Read csv file return data and answer"""
    file_path = FOLDER_PATH + file_name
    
    #Open up the csv file in to an object
    csv_file_object = csv.reader(open(file_path, 'r'))
    
    #Run through each row in the csv file adding each row to the data variable
    train_data = []
    answer = []
    for counter,row in enumerate(csv_file_object):
        train_data.append([float(number) for number in row[1::]]) #From str to float
        answer.append(int(row[0])) #From str to int
        
        #limit
        #if counter == 10:
            #break
    
    return train_data,answer

def save_model(trained_model,name):
    """Save the trained model to a pickle file"""
    pickleFileName = FOLDER_PATH + r'/trained_' + name + r'.pickle'
    
    pickleFile = open(pickleFileName, 'wb')
    
    pickle.dump(trained_model, pickleFile, pickle.HIGHEST_PROTOCOL)
    
    pickleFile.close()

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
#Main program
train_data,answer_data = read_csv(r'/train_data1_256_128_zoomed.csv')

#print train_data[0]

#Limit
#train_data = train_data[0:10]
#answer_data = answer_data[0:10]


#------------------------------------------------------------------------------ 
#Get the eigenfaces
n_components = 20 #How many eigenfaces - Higher number gives better result? n_components <= w*h (size of the image) or smaples?
h = 18
w = 8

#Extracting the top n_components eigenfaces from total number of faces, maximum 10 in this case becuse the image is not a square?
pca = RandomizedPCA(n_components=n_components, whiten=True) 

pca.fit(train_data)

#print len(pca.components_),len(pca.components_[0]) #From n_components up to 10,h*w

eigenfaces = pca.components_.reshape((len(pca.components_), h, w)) #Get the components with maximum variance

print 'Eigenfaces finished!'

#------------------------------------------------------------------------------ 
#Plot
eigenface = eigenfaces[0]
#Reverse
eigenface = eigenface[::-1]

#print eigenface

face = eigenface.reshape((h,w))

#plt.imshow(eigenface, cmap=plt.cm.gray_r, interpolation=None, aspect='auto')

#plt.show()

#Projecting the input data on the eigenfaces orthonormal basis
data_train_pca = pca.transform(train_data)



#------------------------------------------------------------------------------ 
# Predict
predict = True
if predict == True:    
    #Get predictions with random forest
    forest = RandomForestClassifier(n_estimators=150)
    
    time_start = time.time()
        
    forest.fit(data_train_pca,answer_data) #(training set, target set)
    
    #632 seconds to train n=150
    #1958 seconds to train n=500
    #4568 seconds to train n=1000
    print 'It took ', time.time()-time_start, ' seconds to train the forest!'
    
    #Save the trained model as a pickle if it wins
    save_model(forest,r'forest_image_18_8_n150')


#------------------------------------------------------------------------------ 
#Test
test = True
if test == True:
    data_test1,answer = read_csv(r'/test_data1_256_128_zoomed.csv') #answer is not need but will produce error if not there
    data_test2,asnwer = read_csv(r'/test_data2_256_128_zoomed.csv')
    #print data_test1[0][0]
    #Projecting the input data on the eigenfaces orthonormal basis
    data_test1_pca = pca.transform(data_test1)
    data_test2_pca = pca.transform(data_test2)
    
    test_data1 = predict_data(data_test1_pca,r'/trained_forest_image_18_8_n150.pickle')
    test_data2 = predict_data(data_test2_pca,r'/trained_forest_image_18_8_n150.pickle')
    #test_data3 = predict_data(test_data3,r'/trained_forest_256_192.pickle')
    
    print 'Prediction finished!'
    
    #Combine the two data lists
    for item in test_data2:
        test_data1.append(item)
        
    #Save the file as csv
    file_path = FOLDER_PATH + r'\final_forest_256_128_zoomed_18_8_n150_image.csv'

    open_file_object = csv.writer(open(file_path,'wb'),delimiter=',')
    
    for i in range(len(test_data1)):
        open_file_object.writerow([test_data1[i]])
    
