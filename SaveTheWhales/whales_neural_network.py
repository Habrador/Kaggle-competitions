#===============================================================================
# Whales Neural Network
#===============================================================================

#NN stuff
from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers.backprop import BackpropTrainer

from pylab import * # Display charts
from sklearn import preprocessing #Convert input to between 0->1
import csv
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
    

def load_model(model_name):
    """Load pickle file and get the predicted results"""

    pickleFileName = FOLDER_PATH + model_name
    
    pickleFile = open(pickleFileName, 'rb')
    
    trained_model = pickle.load(pickleFile)
    
    pickleFile.close()
    
    return trained_model


def read_csv(file_name):
    path = FOLDER_PATH + file_name
    
    #Open up the csv file in to an object
    csv_file_object = csv.reader(open(path, 'r'))
    
    #Run through each row in the csv file adding each row to the data variable
    train_data = []
    answer = []
    for counter,row in enumerate(csv_file_object):
        train_data.append([float(number) for number in row[1::]]) #From str to float
        answer.append(int(row[0])) #From str to int
    
    return train_data,answer


#------------------------------------------------------------------------------ 
# Train NN
train = False
if train == True:
    #Get the training data
    train_data,answer = read_csv(r'/train_data_zoomed_19_8.csv')
    
    #Limit the data
    #train_data = train_data[0:10]
    #answer = answer[0:10]
    
    
    #Standardize the input data (0-1 only in NN)
    min_max_scaler = preprocessing.MinMaxScaler()
    train_data = min_max_scaler.fit_transform(train_data)
    
    
    #Create the training data
    D = SupervisedDataSet(len(train_data[0]),1) #input, target
    
    for counter,item in enumerate(train_data):
        D.addSample(train_data[counter], answer[counter])
        
    #print D['target']
    
    
    #Create the NN
    N = buildNetwork(len(train_data[0]),200,1, bias=True) #152 76=(152+1)/2
    
    
    #Train the NN with backpropagation
    T = BackpropTrainer(N, D, learningrate = 0.1, momentum = 0.9)
    
    i=0
    error = []
    time_before = time.time()
    while i < 50 and T.testOnData(D) > 0.001:
        errordata = T.testOnData(D)
        
        if i % 1 == 0:
            print i, '\tMSE:', round(errordata,6), '\tTime:', round(time.time()-time_before,6)
        
        #Store the error in a list to plot
        error.append(errordata)
        
        T.train()
        i += 1
    
    #print 'It took ', time.time()-time_before, ' seconds to train the NN'
    
    #Display the error in a chart
    plot(error)
    show()
    
    
    #------------------------------------------------------------------ 
    #Test the NN
    #for counter,item in enumerate(train_data):
        #print 'Real:', answer[counter], ' NN:', N.activate(item)[0]
    
    
    #------------------------------------------------------------------------------ 
    #Save the trained network to a pickle
    save_model(N, r'neural_network_i50_276_200_1')


#------------------------------------------------------------------------------ 
# Predict NN
predict = True
if predict == True:
    #Load trained model    
    trained_model = load_model(r'/trained_neural_network_i50_276_200_1.pickle')
    
    #Get the test data - needed 2 files to avoid memory error
    test_data1,answer = read_csv(r'/test_data1_256_128_zoomed_19_8.csv')
    test_data2,answer = read_csv(r'/test_data2_256_128_zoomed_19_8.csv')
    
    #Standardize the input data (0-1 only in NN)
    min_max_scaler = preprocessing.MinMaxScaler()
    test_data1 = min_max_scaler.fit_transform(test_data1)
    test_data2 = min_max_scaler.fit_transform(test_data2)
    
    #Predict
    predictions = []
    for item in test_data1:
        prediction = trained_model.activate(item)[0]
        #Max 1 and min 0
        if prediction > 1: prediction = 1
        if prediction < 0: prediction = 0
        
        predictions.append(prediction)
    
    for item in test_data2:
        prediction = trained_model.activate(item)[0]
        #Max 1 and min 0
        if prediction > 1: prediction = 1
        if prediction < 0: prediction = 0
        
        predictions.append(prediction)
        
    
    #Print to csv
    file_path = FOLDER_PATH + r'\final_forest_256_128_zoomed_19_8_NN_i50_276_200_1.csv'

    open_file_object = csv.writer(open(file_path,'wb'),delimiter=',')
    
    for i in range(len(predictions)):
        open_file_object.writerow([predictions[i]])
        
        
        
        