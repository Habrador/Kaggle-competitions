#===============================================================================
# Create the second path
#===============================================================================

import csv
import numpy as np
import itertools
import math


class SecondPath:
    
    #------------------------------------------------------------------------------ 
    # Read the data file and turn into array
    def read_data_file(self,data_file,has_heading):
        #Read the data
        file_path = r'c:\Erik\Projekt\Kaggle\Traveling Santa'
        filename = file_path + data_file
        
        #Open up the csv file in to a Python object
        csv_file_object = csv.reader(open(filename, 'r')) #open the file with universal newline mode enabled
        
        #The next() command just skips the first line which is a header
        if has_heading == True:
            csv_file_object.next()
        
        #Run through each row in the csv file adding each row to the data variable
        data = []
        for row in csv_file_object:
            data.append(row)
        
        return data
    
    
    
    #------------------------------------------------------------------------------ 
    #Takes a given path with coordinates and calculates the distance from the path and returns the distance
    def calculate_distance_from_path(self,data):        
        
        data = np.array(data)
        
        #starting_point = data[0][0].astype(np.float)
        start_coordinates = data[0][1:3].astype(np.float)
        data = np.delete(data,[0],0)
                
        #Calculates the distance
        counter = 0
        distance = 0
        length = len(data)
        while counter < length:
            next_coordinates = data[counter][1:3].astype(np.float)
            
            #Calculate the distance with euclidean and add it to the total distance
            distance += math.sqrt(
                                  math.pow(
                                          start_coordinates[0]
                                          - 
                                          next_coordinates[0]
                                          ,2) 
                                  + 
                                  math.pow(
                                          start_coordinates[1]
                                          -
                                          next_coordinates[1]
                                          ,2)
                                 )
                   
            counter += 1
            
            #Next_coordinates is the start_coordinates the next iteration
            start_coordinates = next_coordinates

        return distance
    
    
    
    #------------------------------------------------------------------------------ 
    #Calculate distance
    def calculate_distance(self,data,travel_path):
        
        path_with_coordinates = []
        
        for i in travel_path:
            coordinates = data[int(i)]
            path_with_coordinates.append(coordinates)
        
        distance = self.calculate_distance_from_path(path_with_coordinates)
        
        return distance
    
    
    
    #------------------------------------------------------------------------------ 
    # Generate a second travel_path
    def generate_second_path_from_original(self,travel_path):
        counter = 0
        first = []
        second = []
        for i in travel_path:
            if counter % 2 == 0:
                first.append(i)
            else:
                second.append(i)
            
            counter += 1
        
        final = first + second
        
        return final
    
    
    #------------------------------------------------------------------------------ 
    # Generate the second path
    def generate_second_path(self):
        
        data = self.read_data_file('\santa_cities.csv',True) #city,x,y
        travel_path = self.read_data_file('\santa_path.csv',False) #city
        
        data = data[0:len(travel_path)]
        
        print len(data), len(travel_path)
        
        travel_path = list(itertools.chain.from_iterable(travel_path)) #2d list to 1d list
        
        #Calculate the distance of the initial travel path
        distance = self.calculate_distance(data,travel_path)
        
        print 'The total distance of the original path is: ',distance
        
        
        #------------------------------------------------------------------------------
        # Generate a second path
        second_travel_path = self.generate_second_path_from_original(travel_path)
        
        #Calculate the distance of the initial travel path
        distance = self.calculate_distance(data,second_travel_path)
        
        print 'The total distance of the second path is: ',distance
        
        #print travel_path
        #print second_travel_path
        
        
        #------------------------------------------------------------------------------ 
        # Print the paths to a file
        print_path = False
        if print_path == True:
            #Combine the paths into one list
            combined = []
            for i in range(len(travel_path)):
                combined.append([travel_path[i],second_travel_path[i]])
            
            file_path = r'c:\Erik\Projekt\Kaggle\Traveling Santa\santa_path_combined.csv'
            open_file_object = csv.writer(open(file_path,'wb'),delimiter=',')
        
            for i in range(len(combined)):
                open_file_object.writerow(combined[i])
        
            print 'Save the path finished'
                