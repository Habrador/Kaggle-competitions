#===============================================================================
# Hilbert Curve
#===============================================================================

import numpy as np
import math
import csv as csv

class HilbertCurve:
    
    #------------------------------------------------------------------------------ 
    #Generates the coordinates for the Hilbert curve
    def generate_hilbert_coordinates(self,x0, y0, xi, xj, yi, yj, n):
        coordinates=[]
        #x0 and y0 are the coordinates of the bottom left corner
        #xi & xj are the i & j components of the unit x vector of the frame similarly yi and yj
        #http://www.fundza.com/algorithmic/space_filling/hilbert/basics/index.html
        def hilbert(x0, y0, xi, xj, yi, yj, n):
            if n <= 0:
                X = x0 + (xi + yi)/2
                Y = y0 + (xj + yj)/2
                coordinates.append([X,Y])
                # Output the coordinates of the cv
                #print '%s %s 0' % (X, Y)
            else:
                hilbert(x0,               y0,               yi/2, yj/2, xi/2, xj/2, n - 1)
                hilbert(x0 + xi/2,        y0 + xj/2,        xi/2, xj/2, yi/2, yj/2, n - 1)
                hilbert(x0 + xi/2 + yi/2, y0 + xj/2 + yj/2, xi/2, xj/2, yi/2, yj/2, n - 1)
                hilbert(x0 + xi/2 + yi,   y0 + xj/2 + yj,  -yi/2,-yj/2,-xi/2,-xj/2, n - 1)
            
            return coordinates
        
        #Run the loop
        coordinates = hilbert(x0, y0, xi, xj, yi, yj, n)
        
        return coordinates
    
    
    
    #------------------------------------------------------------------------------ 
    # Calculate the euclidean distance between 2 coordinates
    def calculate_distance(self,start_coordinates,next_coordinates):
        distance = math.sqrt(
                              math.pow(
                                      start_coordinates[0]
                                      - 
                                      next_coordinates[1].astype(np.float)
                                      ,2) 
                              + 
                              math.pow(
                                      start_coordinates[1]
                                      -
                                      next_coordinates[2].astype(np.float)
                                      ,2)
                             )
        
        return distance
    
    
    
    #------------------------------------------------------------------------------ 
    #Takes a given path and calculates the distance from the path and returns the distance
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
    # Main method
    def hilbert_curve(self,data):
        """
        #Find the size of the box to know the size of the hilbert curve - needed once
        x = data[(data[0::,1].astype(np.float)).argsort()]
        y = data[(data[0::,1].astype(np.float)).argsort()]
        
        xmin = x[0][1] #71
        xmax = x[-1][1] #19989
        ymin = y[0][1] #71
        ymax = y[-1][1] #19989
        
        #print xmax,xmin,ymax,ymin
        """
        
        #Generate the hilbert coordinates - Grade 6 is best?
        hilbert_coordinates = self.generate_hilbert_coordinates(0,0,20000.,0,0,20000.,6.)
        #print hilbert_coordinates
        
        #Half side of the loop-box
        side = hilbert_coordinates[0][0] #If the bottom left coordinates are 0
        #print side
        
        #------------------------------------------------------------------------------ 
        #Loop through the hilbert coordinates
        start_coordinates = [0,0] #Assume start in the corner
        travel_path = []
        counter = len(hilbert_coordinates)
        distance_total = 0
        for i in hilbert_coordinates:
            #Select the data coordinates inside the current box
            #This is only working if there is no coordinate at 20000, if so modify the way data_small is calculated
            data_small = data[
                          (data[0::,1].astype(np.float) <  float(i[0]+side)) & #x+
                          (data[0::,1].astype(np.float) >= float(i[0]-side)) & #x-
                          (data[0::,2].astype(np.float) <  float(i[1]+side)) & #y+
                          (data[0::,2].astype(np.float) >= float(i[1]-side)) #y-
                          ]
            
            #Find the next coordinate point by pint
            distances = [] #Store all the distances temporarily
            length = len(data_small) #Faster than while len(data_small) > 0?
            counter_data = 0
            while counter_data < length:                           
                
                #Calculate all the distances possible with euclidean
                for i in data_small:
                    distance = self.calculate_distance(start_coordinates,i)
                    distances.append([i[0],distance,i[1],i[2]]) #waypoint, distance, x, y
                
                #Sort the array to find the best solution
                distances = sorted(distances, key=lambda path: path[1])
                
                #Add the shortest distance to the travel path (calculate the travel distance later)
                travel_path.append(distances[0][0])
                
                #Add the distance - not needed but got to see if the distances are the same
                if start_coordinates != [0,0]:
                    distance_total += distances[0][1]
                
                #Remove the waypoint from small_data
                data_small = data_small[data_small[0::,0] != distances[0][0]]
                
                #Not faster:
                #index = np.where(data_small[0::,0] == distances[0][0])
                #np.delete(data_small,[index[0][0]],0)
                
                #Replace the start coordinates
                start_coordinates = [float(distances[0][2]),float(distances[0][3])]
                
                #Reset distances
                distances = []
                
                counter_data += 1
            
            #Counter
            counter -= 1
            if counter % 100 == 0:
                print 'Hilbert boxes to go: ', counter, ' Distance: ',distance_total
        
        
        #------------------------------------------------------------------------------ 
        #Save the finished path
        save = True
        if save == True:
            file_path = r'c:\Erik\Projekt\Kaggle\Traveling Santa\santa_path.csv'
            open_file_object = csv.writer(open(file_path,'wb'))
        
            for i in range(len(travel_path)):
                open_file_object.writerow([travel_path[i]])
        
                print 'Save the path finished'
        
        #------------------------------------------------------------------------------ 
        #Create a path with coordinates to make is faster to calculate the distance
        data = data.tolist()
        travel_path = list(travel_path)
        
        path_with_coordinates = []
        for i in travel_path:
            coordinates = data[int(i)]
            path_with_coordinates.append(coordinates)
        
        #print path_with_coordinates
        
        #Calculate the distance traveled from the path
        distance_from_path = self.calculate_distance_from_path(path_with_coordinates)
        
        print ''
        print 'The total distance is: ', distance_from_path
        print 'The total distance is: ', distance_total
        print 'The number of waypoints: ', len(travel_path)
        #print 'The travel path is: ', travel_path
        
        return travel_path,hilbert_coordinates