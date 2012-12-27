#===============================================================================
# Random path
#===============================================================================

import random
import math
import numpy as np

#Euclidean distance to calculate the distance between 2 points sqrt((x1-x2)^2 + (y1-y2)^2)

class RandomPath:
    
    def random_path(self,data):
        distance = 0
        travel_path = []
        
        #print len(data)
        
        #Choose a random starting point
        starting_point = random.randrange(len(data)) #Generates a random int between 0 and 9 if the length of the list is 10
        start_coordinates = data[starting_point]
        travel_path.append(start_coordinates[0])
        #Remove the starting_point from the array
        data = np.delete(data,[starting_point],0) #0 means row
        
        limiter = 0
        while len(data) > 0:
            
            #Generate the next point randomly
            next_point = random.randrange(len(data)) 
            #Generate the next point by finding the smallest euclidean distance?
            #next_point = min_euclidean_distance(data,start_coordinates)
            
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