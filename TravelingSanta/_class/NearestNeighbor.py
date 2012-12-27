#===============================================================================
# Nearest Neighbor
#===============================================================================

import random
import math
import numpy as np

class NearestNeighbor:
    
    def min_euclidean_distance(self,data,start_coordinates):
        data_original = data
    
        distance = math.pow(1000,100)
        counter = 0
        
        #print data[0]
        #Create a box around the point we are going from to speed up the calculation process
        box = 500 #The half-size of the box
        data_small = data[
                          (data[0::,1].astype(np.float) < start_coordinates[1].astype(np.float)+box) & #x+
                          (data[0::,1].astype(np.float) > start_coordinates[1].astype(np.float)-box) & #x-
                          (data[0::,2].astype(np.float) < start_coordinates[2].astype(np.float)+box) & #y+
                          (data[0::,2].astype(np.float) > start_coordinates[2].astype(np.float)-box) #y-
                          ]
        #print len(data_small)
        if len(data_small) != 0:
            data = data_small
        
        #Random inside of the small box
        #next_point = random.randrange(len(data)) 
        
        
        #Euclidean distance
        for i in data:
            #Calculate the distance with euclidean and add it
            distance_new = math.sqrt(
                                  math.pow(
                                          start_coordinates[1].astype(np.float)
                                          - 
                                          i[1].astype(np.float)
                                          ,2) 
                                  + 
                                  math.pow(
                                          start_coordinates[2].astype(np.float)
                                          -
                                          i[2].astype(np.float)
                                          ,2)
                                 )
            
            if distance_new < distance:
                next_point = i[0].astype(np.float)
                #next_point = counter
                #print i[0].astype(np.float)
                distance = distance_new
            
            counter += 1
            #print counter
        
        #Find the position of the best point in the original data array
        next_point = np.where(data_original[0::,0].astype(np.float) == next_point)
        
        next_point = next_point[0][0].astype(np.float)
        """
        print next_point_new
        print 'counter ',next_point
        print next_point
        print ''
        """
        #next_point = random.randrange(len(data))
        return next_point #This is a number
    
    def nearest_neighbor(self,data):
        distance = 0
        travel_path = []
        
        #print data
        
        #Choose a random starting point
        starting_point = random.randrange(len(data)) #Generates a random int between 0 and 9 if the length of the list is 10
        start_coordinates = data[starting_point]
        travel_path.append(start_coordinates[0])
        #Remove the starting_point from the array
        data = np.delete(data,[starting_point],0) #0 means row
        
        limiter = 0
        while len(data) > 0:
            
            #Generate the next point randomly
            #next_point = random.randrange(len(data)) 
            #Generate the next point by finding the smallest euclidean distance?
            next_point = self.min_euclidean_distance(data,start_coordinates)
            
            next_coordinates = data[next_point]
            
            #Calculate the distance with euclidean and add it
            distance += math.sqrt(
                                  math.pow(
                                          start_coordinates[1].astype(np.float)
                                          - 
                                          next_coordinates[1].astype(np.float)
                                          ,2) 
                                  + 
                                  math.pow(
                                          start_coordinates[2].astype(np.float)
                                          -
                                          next_coordinates[2].astype(np.float)
                                          ,2)
                                 )
                   
            #Remove the starting_point from the array
            data = np.delete(data,[next_point],0) #0 means row
            
            travel_path.append(next_coordinates[0])
            
            #Next_coordinates is the start_coordinates the next iteration
            start_coordinates = next_coordinates
            
            if len(data) % 10 == 0:
                print 'Iteration:', len(data)
            
            """   
            #To save computer time
            limiter += 1
            if limiter == 1000:
                break
            """ 
        #print starting_point
        
        print 'The total distance is: ', distance
        print 'The traveling path is: ', travel_path
        
        return travel_path
    