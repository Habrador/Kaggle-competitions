#===============================================================================
# Genetic Algorithm - this class doesnt work yet - use the one on Optimize_path
#===============================================================================

import random
import math
import numpy as np

class GeneticAlgorithm:
    
    #------------------------------------------------------------------------------ 
    #Takes a given path and calculates the distance from the path and returns the distance
    def calculate_distance(self,child,data):
        distance = 0
        
        child = np.array(child)
        
        starting_point = child[0].astype(np.float)
        start_coordinates = data[starting_point]
        child = np.delete(child,[0],0)
                
        #Calculates the distance
        while len(child) > 0:
            next_point = child[0].astype(np.float)
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
            child = np.delete(child,[0],0) #0 means row
            
            #Next_coordinates is the start_coordinates the next iteration
            start_coordinates = next_coordinates
            
        return distance
    
    
    
    #------------------------------------------------------------------------------ 
    #generates a random path through the data and calculates the distance
    def generate_random_path(self,data):
        distance = 0
        travel_path = []
        
        #print len(data)
        
        #Choose a random starting point
        starting_point = random.randrange(len(data)) #Generates a random int between 0 and 9 if the length of the list is 10
        start_coordinates = data[starting_point]
        travel_path.append(start_coordinates[0])
        #Remove the starting_point from the array
        data = np.delete(data,[starting_point],0) #0 means row
        
        while len(data) > 0:
            
            #Generate the next point randomly
            next_point = random.randrange(len(data)) 
                        
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
                        
        return distance,travel_path
    
    
    
    #------------------------------------------------------------------------------ 
    #Crossover between 2 solutions
    def crossover(self,pop_elite,data):
        #pick 2 parents randomly from the top elite
        parent1 = pop_elite[random.randrange(0,len(pop_elite))]
        parent2 = pop_elite[random.randrange(0,len(pop_elite))]
        
        parent1_distance = parent1[0]
        parent1 = parent1[1]
        parent2_distance = parent2[0]
        parent2 = parent2[1]
        
        #print 'Before: ',parent1_distance,parent2_distance
                
        #Crossover (mate) to make 2 new children Ox2 from "New Variations of Order Crossover for Travelling Salesman Problem" (pdf)
        length = 3
        substart = random.randrange(0,len(parent1)-length)
        
        subsequence1 = parent1[substart:substart+length]
        subsequence2 = parent2[substart:substart+length]
        
        child1 = parent1
        child2 = parent2
        if child1 != child2:
            #Remove all the values in subsequence from each child
            for i in subsequence1:
                #print i, child2
                child2.remove(i)
            for i in subsequence2:
                #print i, child1
                child1.remove(i)
            
            #Create the new children
            for i in subsequence1:
                child2.insert(substart+subsequence1.index(i),i)
            for i in subsequence2:
                child1.insert(substart+subsequence2.index(i),i)
            
            #Calculate the distance of the new children
            child1_distance = self.calculate_distance(child1,data)
            child2_distance = self.calculate_distance(child2,data)
        else:
            child1_distance = parent1_distance
            child2_distance = parent2_distance
        
        return child1_distance,child1,child2_distance,child2
    
    
    
    #------------------------------------------------------------------------------ 
    # Mutation
    def mutation(self,pop_elite,data):
        best_solution = pop_elite[random.randrange(0,len(pop_elite))][1]
        
        #Generate 2 random numbers
        random1 = random.randrange(0,len(best_solution))
        
        random2 = random.randrange(0,len(best_solution))
        while random1 == random2:
            random2 = random.randrange(0,len(best_solution))
            
        #Make the switch
        point1 = best_solution[random1]
        point2 = best_solution[random2]
        
        best_solution[random1] = point2
        best_solution[random2] = point1
        
        #Calculate the distance of the new solution
        distance = self.calculate_distance(best_solution,data)
        
        return distance,best_solution
    
    
    
    #------------------------------------------------------------------------------ 
    #Main algorithm
    def genetic_algorithm(self,data):
        
        population_size = 500
        mutation_prob = 0.2 #The prob that a mutation will occur
        elite = 0.2 #How many (%) in the group that will not be replaced each generation
        
        #Create the population of random solutions
        population = []
        for i in range(population_size):
            
            #Generate a random path
            distance,random_path = self.generate_random_path(data)
            
            #Add the variables to the population
            population.append([distance,random_path])
            
            #population_size -= 1
        
        #Sort the list shortest path first
        population = sorted(population, key=lambda path: path[0]) #Lambda is an anonymous function
        print len(population), population
        #Loop until we have a good solution or a number of iterations (max_generations)
        max_generations = 0
        nr_solutions = 0
        best_distance = math.pow(1000,100)
        
        top_elite = int(elite*population_size)
        if top_elite < 2:
            top_elite = 2
        
        while max_generations < 1000 and nr_solutions < 50:
                        
            current_distance = population[0][0]
            
            if current_distance == best_distance:
                nr_solutions += 1
            else:
                nr_solutions = 0
            
            print max_generations, nr_solutions, current_distance
            
            #Pick the elite from the total population
            population = population[0:top_elite]
            pop_elite = population
            
            #Add mutated and bred(crossover) forms of the winners
            while len(population) < population_size:
                
                #Crossover
                child1_distance,child1,child2_distance,child2 = self.crossover(pop_elite,data)
                
                #Add these new children to the old array - need to check it here as well?
                if len(population) < population_size:
                    population.append([child1_distance,child1])
                    population.append([child2_distance,child2])
                
                #print 'Crossover distance: ', child1_distance, child2_distance
                
                #Mutation
                if random.random() < mutation_prob:
                    #print 'Mutation'
                    
                    distance,best_solution = self.mutation(pop_elite,data)
                    #print 'Mutation: ', distance
                    #Insert into the population_array
                    if len(population) < population_size:
                        population.append([distance,best_solution])
            
            #Sort the list shortest path first
            population = sorted(population, key=lambda path: path[0]) #Lambda is an anonymous function
            
            #Save the best distance
            if current_distance <= best_distance:
                best_distance = current_distance
            
            max_generations += 1
            
        #Return the optimal path
        print len(population),population
        distance = population[0][0]
        travel_path = population[0][1]
        print 'The total distance is: ', distance
        print 'The traveling path is: ', travel_path
            
        return travel_path 
        