#===============================================================================
# Optimize the path
#===============================================================================

import csv
import numpy as np
import math
import random
import itertools
import collections


class OptimizePath:
    
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
    #Calculate distance
    def calculate_distance(self,data,travel_path):
        
        path_with_coordinates = []
        
        for i in travel_path:
            coordinates = data[int(i)]
            path_with_coordinates.append(coordinates)
        
        distance = self.calculate_distance_from_path(path_with_coordinates)
        
        return distance
    
    
    
    #------------------------------------------------------------------------------ 
    # Mutation
    def mutation(self,travel_path,data):
        tp = list(travel_path) #Make a copy - Important or travel_path will be different in the main program
        
        #Generate 2 different random numbers
        random1 = random.randrange(0,len(tp))
        
        random2 = random.randrange(0,len(tp))
        while random1 == random2:
            random2 = random.randrange(0,len(tp))
        
        #Make the switch
        point1 = tp[random1]
        point2 = tp[random2]
        
        tp[random1] = point2
        tp[random2] = point1
        
        #Calculate the distance of the new solution
        distance = self.calculate_distance(data,tp)
        
        return distance,tp
        
    
    
    #------------------------------------------------------------------------------ 
    #Crossover between 2 solutions
    def crossover(self,pop_elite,data):
        
        #Pick 2 parents randomly from the top elite
        parent1 = random.choice(pop_elite)
        parent2 = random.choice(pop_elite)
        
        parent1_distance = parent1[0]
        parent2_distance = parent2[0]
        
        parent1_path = parent1[1]
        parent2_path = parent2[1]
        
        #Crossover (mate) to make 2 new children Ox2 from "New Variations of Order Crossover for Travelling Salesman Problem" (pdf)
        length = 3
        substart = random.randrange(0,len(parent1_path)-length)
        
        #Get the sub-lists that we are going to switch between the lists
        subsequence1 = parent1_path[substart:substart+length]
        subsequence2 = parent2_path[substart:substart+length]
        
        child1 = parent1_path
        child2 = parent2_path
        
        #print ''
        #print 'Before: ',child1,parent1_distance,child2,parent2_distance
        #print 'Path: ',subsequence1,subsequence2
        
        if child1 != child2:
            #print 'Crossover between different children'
            
            #Remove all the values in subsequence from each child
            for i in subsequence1:
                child2.remove(i)
            for i in subsequence2:
                child1.remove(i)
            
            #Create the new children
            for i in subsequence1:
                child2.insert(substart+subsequence1.index(i),i)
            for i in subsequence2:
                child1.insert(substart+subsequence2.index(i),i)
            
            #Calculate the distance of the new children
            child1_distance = self.calculate_distance(data,child1)
            child2_distance = self.calculate_distance(data,child2)
        else:
            child1_distance = parent1_distance
            child2_distance = parent2_distance
        
        #print 'After: ',child1,child1_distance,child2,child2_distance
        
        return child1_distance,child1,child2_distance,child2



    #------------------------------------------------------------------------------ 
    # Generate random path
    def generate_random_path(self,travel_path,data):
        travel_path_random = list(travel_path)
        
        random.shuffle(travel_path_random)
        
        #Calculate the distance of the new solution
        distance = self.calculate_distance(data,travel_path_random)
        
        return distance,travel_path_random



    #------------------------------------------------------------------------------ 
    # Genetic algorithm to improve the path
    def genetic_algorithm(self,data,travel_path,distance):
        population_size = 20
        mutation_prob = 0.2 #The prob that a mutation will occur
        elite = 0.2 #How many (%) in the group that will not be replaced each generation
    
        #Create the population with mutated solutions - these are the random solutions if normal genetic 
        population = []
        
        #Add the first solution
        population.append([distance,travel_path])
        
        #Generate the rest of the population
        for i in range(population_size-1):
            #distance, mutated_path = self.mutation(travel_path,data)
            distance, random_path = self.generate_random_path(travel_path,data)
            
            population.append([distance,random_path])
            
            #if i % 10 == 0:
            print 'Initial population: ', i+1
        
        #Sort the list - shortest path first
        population = sorted(population, key=lambda path: path[0])
        
        #------------------------------------------------------------------------------ 
        #Loop until we have a good solution or a number of iterations (max_generations)
        max_generations = 0
        nr_solutions = 0
        best_distance = math.pow(1000,100)
        
        #Get the best results and generate new solutions from them
        top_elite = int(elite*population_size)
        if top_elite < 2:
            top_elite = 2
        
        while max_generations < 1000 and nr_solutions < 50:
            current_distance = population[0][0]
            
            if current_distance == best_distance:
                nr_solutions += 1
            else:
                nr_solutions = 0
            
            print max_generations, nr_solutions, current_distance, population[-1][0]
            
            #Pick the elite from the total population
            population = population[0:top_elite]
            pop_elite = list(population[0:top_elite])
            #print pop_elite
            
            #Add mutated and bred(crossover) forms of the winners
            while len(population) < population_size:
                
                #Crossover
                child1_distance,child1,child2_distance,child2 = self.crossover(pop_elite,data)
                
                #Add these new children to the old array - need to check it here as well?
                if len(population) < population_size:
                    population.append([child1_distance,child1])
                if len(population) < population_size:
                    population.append([child2_distance,child2])
                
                
                #Mutation
                if random.random() < mutation_prob:
                    
                    parent_mutate = random.choice(pop_elite)
                    
                    parent_mutate_path = parent_mutate[1]
                
                    distance,mutated_path = self.mutation(parent_mutate_path,data)
                    
                    #Insert into the population_array
                    if len(population) < population_size:
                        population.append([distance,mutated_path])
            
            #Sort the list shortest path first
            population = sorted(population, key=lambda path: path[0]) #Lambda is an anonymous function

            #Save the best distance
            if current_distance <= best_distance:
                best_distance = current_distance
            
            max_generations += 1
        
        #Get the best distance and travel path
        distance = population[0][0]
        travel_path = population[0][1]
       
        return distance,travel_path


        
    #------------------------------------------------------------------------------ 
    # Main method    
    def optimize_path(self):
        
        data = self.read_data_file('\santa_cities.csv',True) #city,x,y
        travel_path = self.read_data_file('\santa_path.csv',False) #city
        
        data = data[0:len(travel_path)]
        
        print len(data), len(travel_path)
        
        travel_path = list(itertools.chain.from_iterable(travel_path)) #2d list to 1d list
        
        #Calculate the distance of the initial travel path
        distance = self.calculate_distance(data,travel_path)
        
        print 'The total distance of the original path is: ',distance
        
        
        #------------------------------------------------------------------------------ 
        #Improve the original path with a genetic algorithm
        improved_distance,improved_path = self.genetic_algorithm(data,travel_path,distance)
        
        print 'The total distance of the improved path is: ',improved_distance
        
        #Save it to file
        improved_path = list(itertools.chain.from_iterable(improved_path))
        #print travel_path
        if improved_distance < distance:
            file_path = r'c:\Erik\Projekt\Kaggle\Traveling Santa\santa_path_optimized.csv'
            open_file_object = csv.writer(open(file_path,'wb'))
        
            for i in range(len(improved_path)):
                open_file_object.writerow([improved_path[i]])
        
            print 'Save the path finished'
        