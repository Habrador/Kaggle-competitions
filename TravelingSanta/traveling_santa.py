#===============================================================================
# Kaggle: Traveling Santa Problem
#===============================================================================

import csv as csv 
import numpy as np #@UnusedImport
import matplotlib.pyplot as plt

#Classes
from _class.RandomPath import * #@UnusedWildImport
from _class.NearestNeighbor import * #@UnusedWildImport
from _class.GeneticAlgorithm import * #@UnusedWildImport
from _class.HilbertCurve import * #@UnusedWildImport
from _class.OptimizePath import * #@UnusedWildImport
from _class.SecondPath import * #@UnusedWildImport



#------------------------------------------------------------------------------ 
# Read the data file and turn into array
def read_data_file(data_file):
    #Read the data
    file_path = r'c:\Erik\Projekt\Kaggle\Traveling Santa'
    filename = file_path + data_file
    
    #Open up the csv file in to a Python object
    csv_file_object = csv.reader(open(filename, 'r')) #open the file with universal newline mode enabled
    
    #The next() command just skips the first line which is a header
    csv_file_object.next()
    
    #Run through each row in the csv file adding each row to the data variable
    data = []
    for row in csv_file_object:
        data.append(row)
    
    #Convert from a list to an array (to make it easier to do math with numpy). Each item is currently a string in this format
    data = np.array(data)
    
    return data
   

#===============================================================================
# Main program
#===============================================================================

data = read_data_file('\santa_cities.csv') #id, x, y

#print data[0]
#print len(data)

#limit the data
#data = data[0:10]


# Traveling salesman problem (best length of path from Kaggle: 6,575,231)


#Experiment 1: Random path
Experiment1 = RandomPath()
#travel_path = Experiment1.random_path(data)


#Experiment 2: Nearest-neighbor
Experiment2 = NearestNeighbor()
#travel_path = Experiment2.nearest_neighbor(data)


#Experiment 3: Genetic algorithm
Experiment3 = GeneticAlgorithm()
#travel_path = Experiment3.genetic_algorithm(data)


#Experiment 4: Hilbert Curve with random, or eucliden
Experiment4 = HilbertCurve()
travel_path,hilbert_curve = Experiment4.hilbert_curve(data)

#Calculate the length of the path and optimize it with a genetic algorithm
Optimize = OptimizePath()
#Optimize.optimize_path()

#Generate a second path
Second = SecondPath()
#Second.generate_second_path()


#------------------------------------------------------------------------------ 
# Plot
plot = False
if plot == True:
    #Plot the waypoints data
    plt.plot(data[0::,1],data[0::,2],'.', ms=1)
    
    #Plot the travelpath
    plt.plot(
             [data[float(i)][1] for i in travel_path],
             [data[float(i)][2] for i in travel_path]
             )  
    
    #Plot the start and endpoints
    plt.plot(
              data[float(travel_path[0])][1],
              data[float(travel_path[0])][2],
              'o',color='b',alpha=0.75,ms=20)
    
    plt.plot(
              data[float(travel_path[len(travel_path)-1])][1],
              data[float(travel_path[len(travel_path)-1])][2],
              'o',color='r',alpha=0.75,ms=10)
    
    #Plot the hilbert curve
    plt.plot(
             [hilbert_curve[i][0] for i in range(len(hilbert_curve))],
             [hilbert_curve[i][1] for i in range(len(hilbert_curve))],
             '-',color='r',alpha=0.5
             )
    
    plt.axis('equal')
    plt.show()
