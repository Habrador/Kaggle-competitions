#===============================================================================
# Kaggle: Visualize the State of Public Education in Colorado
#===============================================================================

import csv as csv 
import numpy as np

#Plot
#import matplotlib
#matplotlib.use('Agg') #To make svg work???

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt



#===============================================================================
# Functions
#===============================================================================

#------------------------------------------------------------------------------ 
# Import csv file, remove first row, turn it into an array
def import_csv_turninto_array(filename):
    #Read the data
    file_path = r'c:\Erik\Projekt\Kaggle\Public education in Colorado\ColoradoSchoolGrades'
    filename = file_path + filename
    
    #Open up the csv file in to a Python object
    csv_file_object = csv.reader(open(filename, 'rU')) #open the file with universal newline mode enabled
    
    #The next() command just skips the first line which is a header
    csv_file_object.next()
    
    data = []
    
    #Run through each row in the csv file adding each row to the data variable
    for row in csv_file_object:
        data.append(row)
    
    #Convert from a list to an array (to make it easier to do math with numpy). Each item is currently a string in this format
    data = np.array(data)
    
    return data



#===============================================================================
# Experiment functions
#===============================================================================


#===============================================================================
# Display all the A schools on a map
#===============================================================================

def display_schools_on_map():
    #Choose all A schools >10
    data_2010_a = data_2010[data_2010[0::,15].astype(np.float) > 10]
    data_2011_a = data_2011[data_2011[0::,14].astype(np.float) > 10]
    data_2012_a = data_2012[data_2012[0::,9].astype(np.float) > 10]
    
    #Read the coordinates files
    data_coordinates = import_csv_turninto_array(r'\school_gps_coordinates.csv')
    
    print data_coordinates[0][0]
    
    #Remove the coordinates that doesnt belong to an A school
    #print data_2012_a[0::,3]
    
    #This array will be smaller since some A-schools are present many times because of they are high-schools, kindergarten etc 
    print 'A school coordinates:' 
    
    data_coordinates_a = []
    for i in data_coordinates:
        if i[0].astype(np.float) in data_2010_a[0::,5].astype(np.float):
        #if i[0].astype(np.float) in data_2011_a[0::,5].astype(np.float):
        #if i[0].astype(np.float) in data_2012_a[0::,3].astype(np.float):
            #print i
            data_coordinates_a.append(i)
        #else:
            #print 'Not in array'
    
    data_coordinates_a = np.array(data_coordinates_a)
    print data_coordinates_a
    print len(data_coordinates_a)
    
    
    #------------------------------------------------------------------------------ 
    # Display on a map (l is low, f is best)
    map = Basemap(
                    width=800000,
                    height=600000,
                    projection='lcc',
                    resolution='l',
                    lat_1=45.,
                    lat_2=55,
                    lat_0=39,
                    lon_0=-106.
                    )
    
    #map.bluemarble()
    #map.drawlsmask()
    
    # draw the edge of the map projection region (the projection limb)
    #map.drawmapboundary()
    #map.drawstates() #Display the states
    
    # draw lat/lon grid lines every 30 degrees.
    #map.drawmeridians(np.arange(0, 360, 30))
    #map.drawparallels(np.arange(-90, 90, 30))
    
    # lat/lon coordinates of five cities.
    lats = data_coordinates_a[0::,2]
    lons = data_coordinates_a[0::,3]
    cities = data_coordinates_a[0::,1]
    # compute the native map projection coordinates for cities.
    x,y = map(lons,lats)
    # plot filled circles at the locations of the cities.
    #map.plot(x,y,'bo')
    # plot the names of the cities
    #for name,xpt,ypt in zip(cities,x,y):
        #plt.text(xpt+50000,ypt+50000,name)
        

#===============================================================================
# Distribution of grades = how many A+, A, etc - and difference since 2010
#===============================================================================
def distribution_of_grades(data_2010,data_2011,data_2012):
    print 'Distribution of grades'
    
    distribtion_grades_2010 = []
    distribtion_grades_2011 = []
    distribtion_grades_2012 = []
    grade = 13 #Highest grade
    
    #Calculate the amount of schools with a certain grade
    while grade > 0:
        number_of_schools_with_grade_grade = len(data_2010[data_2010[0::,15].astype(np.float) == grade])
        distribtion_grades_2010.append(number_of_schools_with_grade_grade)
        
        number_of_schools_with_grade_grade = len(data_2011[data_2011[0::,14].astype(np.float) == grade])
        distribtion_grades_2011.append(number_of_schools_with_grade_grade)
        
        number_of_schools_with_grade_grade = len(data_2012[data_2012[0::,9].astype(np.float) == grade])
        distribtion_grades_2012.append(number_of_schools_with_grade_grade)
        
        
        grade -= 1
    
    print distribtion_grades_2010
    print len(data_2010)
    
    print distribtion_grades_2011
    print len(data_2011)
    
    print distribtion_grades_2012
    print len(data_2012)
    
    
    #Calculate the percentage and turn into %
    distribtion_grades_2010_p = [(x/float(len(data_2010)))*100 for x in distribtion_grades_2010]
    distribtion_grades_2011_p = [(x/float(len(data_2011)))*100 for x in distribtion_grades_2011]
    distribtion_grades_2012_p = [(x/float(len(data_2012)))*100 for x in distribtion_grades_2012]
    
    print distribtion_grades_2010_p
    print distribtion_grades_2011_p
    print distribtion_grades_2012_p
    
    change_2012_2010 = [i - j for i, j in zip(distribtion_grades_2012_p, distribtion_grades_2010_p)]
    print change_2012_2010
    
    #plt.bar(range(1), distribtion_grades_2010_p[0])
    #plt.bar(range(1), distribtion_grades_2010_p[1], bottom=distribtion_grades_2010_p[0])
    #plt.bar(range(1), distribtion_grades_2010_p[2], bottom=distribtion_grades_2010_p[0]+distribtion_grades_2010_p[1])
    
    width = 0.6
    ind = np.arange(13)
    
    plt.subplot(2,1,1)
    #plt.bar(ind, distribtion_grades_2012_p, width, color='r')
    #plt.bar(ind, distribtion_grades_2011_p, width, color='g')
    plt.bar(ind, distribtion_grades_2010_p, width, color='#002768')
    plt.xticks(ind + width/2., ('A+', 'A', 'A-', 'B+', 'B', 'B-','C+', 'C', 'C-','D+', 'D', 'D-','F'), fontsize=15)
    plt.yticks(fontsize=15)
    
    #Remove top and right axis
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    #Difference since 2010
    plt.subplot(2,1,2)
    plt.bar(ind, change_2012_2010, width, color='#d72e39')
    plt.xticks(ind + width/2., ('A+', 'A', 'A-', 'B+', 'B', 'B-','C+', 'C', 'C-','D+', 'D', 'D-','F'), fontsize=15)
    plt.yticks(fontsize=15)
    
    #Remove top and right axis
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    plt.show()


#===============================================================================
# In which cities are the A schools located?
#===============================================================================
def where_are_the_a_schools_located(data_2012):
    #All the a schools
    data_2012_a = data_2012[data_2012[0::,9].astype(np.float) > 10]
    
    print 'Number of A schools 2012: ', len(data_2012_a)
    
    #In which cities are these A schools located?
    #Read address files. Columns: 2 is school code, 6 is city 
    school_address = import_csv_turninto_array(r'\2012_school_address.csv')
    
    #This array will be smaller since some A-schools are present many times because of they are high-schools, kindergarten etc 
    print 'A school cities:' 
    
    city_a = []
    for i in school_address:
        if i[1].astype(np.float) in data_2012_a[0::,3].astype(np.float):
            city_a.append(i[5]) #Add the city to the array
        #else:
            #print 'Not in array'
    
    print city_a
    print len(city_a)
    
    #Clean duplicates http://www.peterbe.com/plog/uniqifiers-benchmark
    cities = []
    for e in city_a:
        if e not in cities:
            cities.append(e)
    
    print cities
    print len(cities)
    
    #Write to file
    file_path = r'c:\Erik\Projekt\Kaggle\Public education in Colorado\cities_with_a_schools.csv'
    open_file_object = csv.writer(open(file_path,'wb'),delimiter=' ')
    
    for i in range(len(cities)):
        open_file_object.writerow(cities[i])
 


#===============================================================================
# How have individual schools improved since 2010
#===============================================================================
def how_have_individual_schools_improved(data_2010,data_2011,data_2012):
    
    grade_3_years_2010 = []
    grade_3_years_2011 = []
    grade_3_years_2012 = []
    
    #Standardize the data
    
    #Insert the data needed
    for i in data_2010:
        grade_3_years_2010.append([i[0],i[5].astype(np.float),i[3],i[4],i[15].astype(np.float)])
    
    for i in data_2011:
        grade_3_years_2011.append([i[0],i[5].astype(np.float),i[3],i[4],i[14].astype(np.float)])
    
    for i in data_2012:
        grade_3_years_2012.append([i[4],i[3].astype(np.float),i[5],i[6],i[9].astype(np.float)])
    
    print grade_3_years_2010[1]
    print grade_3_years_2011[1]
    print grade_3_years_2012[1]
    
    grade_3_years_2010 = np.array(grade_3_years_2010)
    grade_3_years_2011 = np.array(grade_3_years_2011)
    grade_3_years_2012 = np.array(grade_3_years_2012)
    
    #print len(grade_3_years_2010)
    #print len(grade_3_years_2011)
    #print len(grade_3_years_2012)
    
    grade_improvement = []
    grade_improvement_with_name = []
    for i in grade_3_years_2012:
        grade_2010 = grade_3_years_2010[(grade_3_years_2010[0::,1] == i[1]) & (grade_3_years_2010[0::,2] == i[2])] #First is code, 2nd is type
        grade_2011 = grade_3_years_2011[(grade_3_years_2011[0::,1] == i[1]) & (grade_3_years_2011[0::,2] == i[2])]
        
        #print grade_2010[0][4]
        
        #Check if the arrays are not empty = the school haven't existed for 3 years
        if grade_2010.size and grade_2011.size: 
            grade_10 = grade_2010[0][4]
            grade_11 = grade_2011[0][4]
            grade_12 = i[4]
        
            grade_improvement.append([grade_10,grade_11,grade_12])
            grade_improvement_with_name.append([grade_10,grade_11,grade_12,i[0]])
        
        #break
    
    print 'Number of schools that have existed for 3 years: ', len(grade_improvement)
    
    grade_improvement = np.array(grade_improvement)
    
    #Divide the array into arrays with the different grades
    #grade_improvement_a = grade_improvement[grade_improvement[0::,0].astype(np.float) > 12]
    grade_improvement_a = grade_improvement[(grade_improvement[0::,0].astype(np.float) < 13) & (grade_improvement[0::,0].astype(np.float) > 11)]
    grade_improvement_b = grade_improvement[(grade_improvement[0::,0].astype(np.float) < 10) & (grade_improvement[0::,0].astype(np.float) > 8)]
    grade_improvement_c = grade_improvement[(grade_improvement[0::,0].astype(np.float) < 7) & (grade_improvement[0::,0].astype(np.float) > 5)]
    grade_improvement_d = grade_improvement[(grade_improvement[0::,0].astype(np.float) < 4) & (grade_improvement[0::,0].astype(np.float) > 2)]
    
    #Plot the results ABCD only = less messy:
    def axis():
        #plt.yticks(np.arange(14),('','F','D-', 'D', 'D+', 'C-', 'C', 'C+','B-', 'B', 'B+','A-', 'A', 'A+'), fontsize=15, color='#444444')
        plt.yticks(np.arange(14),('','F','', 'D', '', '', 'C', '','', 'B', '','', 'A', ''), fontsize=15, color='#444444')
        plt.xticks(np.arange(3),(2010,2011,2012), fontsize=15, color='#444444')
    
    color = '#d72e39'
    
    i=0
    while i < len(grade_improvement_a):
        plt.subplot(2,2,1)
        #plt.plot(grade_improvement_a[i],color)
        plt.fill(grade_improvement_a[i], color)
        i += 1
    axis()
    
    i=0
    while i < len(grade_improvement_b):
        plt.subplot(2,2,2)
        #plt.plot(grade_improvement_b[i],color)
        plt.fill(grade_improvement_b[i],color)
        i += 1
    axis()
    
    i=0
    while i < len(grade_improvement_c):
        plt.subplot(2,2,3)
        #plt.plot(grade_improvement_c[i],color)
        plt.fill(grade_improvement_c[i],color)
        i += 1
    axis()
    
    i=0
    while i < len(grade_improvement_d):
        plt.subplot(2,2,4)
        #plt.plot(grade_improvement_d[i],color)
        plt.fill(grade_improvement_d[i],color)
        i += 1
    axis()
    
        
    #------------------------------------------------------------------------------ 
    # Percentage of schools that improved/worsened
    
    def display_percentage(grade,improved,worsened,total):
        print ''
        print '% of', grade, 'schools with higher grade: ', (float(improved)/float(total))*100
        print '% of', grade, 'schools with lower grade: ', (float(worsened)/float(total))*100
    
    #A    
    total = len(grade_improvement_a)
    improved = len(grade_improvement_a[grade_improvement_a[0::,2].astype(np.float) > 12])
    worsened = len(grade_improvement_a[grade_improvement_a[0::,2].astype(np.float) < 12])
    display_percentage('A',improved,worsened,total)
    
    #B    
    total = len(grade_improvement_b)
    improved = len(grade_improvement_b[grade_improvement_b[0::,2].astype(np.float) > 9])
    worsened = len(grade_improvement_b[grade_improvement_b[0::,2].astype(np.float) < 9])
    display_percentage('B',improved,worsened,total)
    
    #C
    total = len(grade_improvement_c)
    improved = len(grade_improvement_c[grade_improvement_c[0::,2].astype(np.float) > 6])
    worsened = len(grade_improvement_c[grade_improvement_c[0::,2].astype(np.float) < 6])
    display_percentage('C',improved,worsened,total)
    
    #D    
    total = len(grade_improvement_d)
    improved = len(grade_improvement_d[grade_improvement_d[0::,2].astype(np.float) > 3])
    worsened = len(grade_improvement_d[grade_improvement_d[0::,2].astype(np.float) < 3])
    display_percentage('D',improved,worsened,total)
    
    
    #------------------------------------------------------------------------------
    # Display the best/worst schools = that made the larges jumps in grades
    
    print grade_improvement_with_name[0]
    
    grade_change_array = []
    for i in grade_improvement_with_name:
        #print i[0].astype(np.float)
        difference = i[2].astype(np.float)-i[0].astype(np.float)
        grade_change_array.append([difference,i[3],i[0],i[2]])
    
    print grade_change_array[0:5]
    
    #Sort the list
    from operator import itemgetter
    sorted_array = sorted(grade_change_array, key=itemgetter(0))
    
    print sorted_array
    
    #plt.show()



#===============================================================================
# 2012: Poor students plots how many at the different school grades are receiving discounted lunch
#===============================================================================
def poor_people(data_2010,data_2011,data_2012):
    #Read the file with discounted lunch
    poor_people = import_csv_turninto_array(r'\2012_k_12_FRL.csv')
    
    #Remove the last 3 rows in the array = unneeded junk
    poor_people = np.delete(poor_people,np.s_[-3:],0)
    
    #print poor_people[len(poor_people)-1]
    
    #Change the hard-coded percentage to a number
    
    for i in xrange(np.size(poor_people[0::,4])):
        #Reads something like 69.42%
        percentage = poor_people[i,4]
        #Remove percentage sign
        percentage = percentage.replace('%','')
        
        poor_people[i,4] = float(percentage)
    
    print poor_people[0]
    
    #Connect the poor_people_array with original data
    poor = []
    for i in data_2012:
        percentage_poor = poor_people[poor_people[0::,2] == i[3]]
        
        #Add to the poor list
        #if len(percentage_poor) != 0: 
        poor.append([i[9],percentage_poor[0][4],i[4],percentage_poor[0][3]])
    
    print poor[0:5]
    print len(poor)
    
    poor = np.array(poor)
    
    poor_a = poor[poor[0::,0].astype(np.float) > 10]
    poor_b = poor[(poor[0::,0].astype(np.float) < 11) & (poor[0::,0].astype(np.float) > 7)]
    poor_c = poor[(poor[0::,0].astype(np.float) < 8) & (poor[0::,0].astype(np.float) > 4)]
    poor_d = poor[(poor[0::,0].astype(np.float) < 5) & (poor[0::,0].astype(np.float) > 1)]
    poor_f = poor[poor[0::,0].astype(np.float) < 2]
    
    def poor_average(poor):
        return np.mean(poor[0::,1].astype(np.float)) #mean or median?
    
    print poor_average(poor_b)
    #print poor_a_average
    
    #Plot the graph!
    poor_average_list=[
                       poor_average(poor_a),
                       poor_average(poor_b),
                       poor_average(poor_c),
                       poor_average(poor_d),
                       poor_average(poor_f)
                       ]
    
    print poor_average_list
    
    width = 0.6
    ind = np.arange(5)
    
    #plt.subplot(111,axisbg='#cccccc')
    plt.subplot(111,alpha=0)
    plt.bar(ind, poor_average_list, width, color='#002768')
    plt.xticks(ind + width/2., ('A', 'B', 'C', 'D', 'F'), fontsize=15)
    plt.yticks(fontsize=15)
    
    #Remove top and right axis
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    #plt.show()




#===============================================================================
# 2010: Poor students plots how many at the different school grades are 
# receiving discounted lunch (almost same as above)
#===============================================================================
def poor_people_2010(data_2010,data_2011,data_2012):
    #Read the file with discounted lunch
    poor_people = import_csv_turninto_array(r'\2010_k_12_FRL.csv')
    
    #Remove the last 3 rows in the array = unneeded junk
    poor_people = np.delete(poor_people,np.s_[-3:],0)
    #remove the 2nd last row
    poor_people = np.delete(poor_people,[len(poor_people)-2],0)
    #remove the 5nd last row
    poor_people = np.delete(poor_people,[len(poor_people)-5],0)
    
    #print poor_people[len(poor_people)-1]
    
    #Change the hard-coded percentage to a number
    
    for i in xrange(np.size(poor_people[0::,4])):
        #Reads something like 69.42%
        percentage = poor_people[i,4]
        #Remove percentage sign
        percentage = percentage.replace('%','')
        
        poor_people[i,4] = float(percentage)
    
    print poor_people[0]
    print data_2010[0]
    
    #Connect the poor_people_array with original data
    poor = []
    for i in data_2010:
        percentage_poor = poor_people[poor_people[0::,2].astype(np.float) == i[5].astype(np.float)]
        #print i
        #print i[0]
        #break
        #Add to the poor list
        # grade, percentage, school, school
        if len(percentage_poor) != 0: 
            poor.append([i[15],percentage_poor[0][4],i[0],percentage_poor[0][3]])
    
    print poor[0:10]
    print len(poor)
    
    poor = np.array(poor)
    
    poor_a = poor[poor[0::,0].astype(np.float) > 10]
    poor_b = poor[(poor[0::,0].astype(np.float) < 11) & (poor[0::,0].astype(np.float) > 7)]
    poor_c = poor[(poor[0::,0].astype(np.float) < 8) & (poor[0::,0].astype(np.float) > 4)]
    poor_d = poor[(poor[0::,0].astype(np.float) < 5) & (poor[0::,0].astype(np.float) > 1)]
    poor_f = poor[poor[0::,0].astype(np.float) < 2]
    
    def poor_average(poor):
        return np.mean(poor[0::,1].astype(np.float)) #mean or median?
    
    print poor_average(poor_b)
    #print poor_a_average
    
    #Plot the graph!
    poor_average_list=[
                       poor_average(poor_a),
                       poor_average(poor_b),
                       poor_average(poor_c),
                       poor_average(poor_d),
                       poor_average(poor_f)
                       ]
    
    print poor_average_list
           


#===============================================================================
# Can the students continue to college - 2012 only
#===============================================================================
def continue_to_college(data_2010,data_2011,data_2012):
    #Read the file with college readiness data 1=yes 2=no
    college_readiness = import_csv_turninto_array(r'\2012_COACT.csv')
    
    #Connect college readiness with school grades
    grade_readiness = []
    for i in data_2012:
        if i[5] == 'H': #If the school is an high-school
            readiness = college_readiness[college_readiness[0::,3]==i[3]]
            #Change from 2 to 0 = not ready
            
            if readiness[0][4] == '2': read_en = 0
            else: read_en = 1
            if readiness[0][5] == '2': read_math = 0 
            else: read_math = 1
            if readiness[0][6] == '2': read_read = 0
            else: read_read = 1
            if readiness[0][7] == '2': read_sci = 0
            else: read_sci = 1
            
            grade_readiness.append([
                                    i[9],
                                    read_en, #eng
                                    read_math, #math
                                    read_read, #read
                                    read_sci, #sci
                                    i[4],
                                    readiness[0][1]
                                    ])
    
    print grade_readiness[0]
    
    grade_readiness = np.array(grade_readiness)
    
    #Choose the ABCD grades
    grade_readiness_a = grade_readiness[grade_readiness[0::,0].astype(np.float) > 10]
    grade_readiness_b = grade_readiness[(grade_readiness[0::,0].astype(np.float) < 11) & (grade_readiness[0::,0].astype(np.float) > 7)]
    grade_readiness_c = grade_readiness[(grade_readiness[0::,0].astype(np.float) < 8) & (grade_readiness[0::,0].astype(np.float) > 4)]
    grade_readiness_d = grade_readiness[(grade_readiness[0::,0].astype(np.float) < 5) & (grade_readiness[0::,0].astype(np.float) > 1)]
    
    print grade_readiness_a[0]
    
    #Turn into array
    grade_readiness_a = np.array(grade_readiness_a)
    grade_readiness_b = np.array(grade_readiness_b)
    grade_readiness_c = np.array(grade_readiness_c)
    grade_readiness_d = np.array(grade_readiness_d)
    
    #Turn into percentage
    grade_readiness_a_percent = [
                                 sum(grade_readiness_a[0::,1].astype(np.float))/len(grade_readiness_a)*100,
                                 sum(grade_readiness_a[0::,2].astype(np.float))/len(grade_readiness_a)*100,
                                 sum(grade_readiness_a[0::,3].astype(np.float))/len(grade_readiness_a)*100,
                                 sum(grade_readiness_a[0::,4].astype(np.float))/len(grade_readiness_a)*100
                                 ]
    
    grade_readiness_b_percent = [
                                 sum(grade_readiness_b[0::,1].astype(np.float))/len(grade_readiness_b)*100,
                                 sum(grade_readiness_b[0::,2].astype(np.float))/len(grade_readiness_b)*100,
                                 sum(grade_readiness_b[0::,3].astype(np.float))/len(grade_readiness_b)*100,
                                 sum(grade_readiness_b[0::,4].astype(np.float))/len(grade_readiness_b)*100
                                 ]
    
    grade_readiness_c_percent = [
                                 sum(grade_readiness_c[0::,1].astype(np.float))/len(grade_readiness_c)*100,
                                 sum(grade_readiness_c[0::,2].astype(np.float))/len(grade_readiness_c)*100,
                                 sum(grade_readiness_c[0::,3].astype(np.float))/len(grade_readiness_c)*100,
                                 sum(grade_readiness_c[0::,4].astype(np.float))/len(grade_readiness_c)*100
                                 ]
    
    grade_readiness_d_percent = [
                                 sum(grade_readiness_d[0::,1].astype(np.float))/len(grade_readiness_d)*100,
                                 sum(grade_readiness_d[0::,2].astype(np.float))/len(grade_readiness_d)*100,
                                 sum(grade_readiness_d[0::,3].astype(np.float))/len(grade_readiness_d)*100,
                                 sum(grade_readiness_d[0::,4].astype(np.float))/len(grade_readiness_d)*100
                                 ]
  
    print grade_readiness_a_percent
    print grade_readiness_b_percent
    print grade_readiness_c_percent
    print grade_readiness_d_percent
    
    #Create arrays to plot
    en      = [grade_readiness_a_percent[0],grade_readiness_b_percent[0],grade_readiness_c_percent[0],grade_readiness_d_percent[0]]
    math    = [grade_readiness_a_percent[1],grade_readiness_b_percent[1],grade_readiness_c_percent[1],grade_readiness_d_percent[1]]
    read    = [grade_readiness_a_percent[2],grade_readiness_b_percent[2],grade_readiness_c_percent[2],grade_readiness_d_percent[2]]
    sci     = [grade_readiness_a_percent[3],grade_readiness_b_percent[3],grade_readiness_c_percent[3],grade_readiness_d_percent[3]]
    
    size = 10
    a = 0.75
    plt.plot(en,    range(4),'o', ms=size*2, alpha=a, color='#bf0a30')
    plt.plot(math,  range(4),'o', ms=size*3, alpha=a, color='#002868')
    plt.plot(read,  range(4),'o', ms=size*4, alpha=a, color='green')
    plt.plot(sci,   range(4),'o', ms=size*5, alpha=a, color='#ffd700')
    
    plt.yticks(range(4), ('A', 'B', 'C', 'D'), fontsize=15)
    plt.xticks(fontsize=15)
    plt.xlim([0,100])
    plt.ylim([-1,4])
    
    #Remove top and right axis
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    plt.show()
 


#===============================================================================
# Which districts have improved / worsened?
#===============================================================================
def districts_improved_or_not(data_2010,data_2011,data_2012):
    
    #Remove the schools that havent existed 2010->2012
    grade_3_years_2010 = []
    grade_3_years_2011 = []
    grade_3_years_2012 = []
    
    #Insert the data needed in standardized lists
    #School name
    #School code
    #EMH
    #EMH Combined
    #Grade
    #District
    for i in data_2010:
        grade_3_years_2010.append([i[0],i[5].astype(np.float),i[3],i[4],i[15].astype(np.float),i[2]])
    
    for i in data_2011:
        grade_3_years_2011.append([i[0],i[5].astype(np.float),i[3],i[4],i[14].astype(np.float),i[2]])
    
    for i in data_2012:
        grade_3_years_2012.append([i[4],i[3].astype(np.float),i[5],i[6],i[9].astype(np.float),i[2]])
    
    print grade_3_years_2010[1]
    print grade_3_years_2011[1]
    print grade_3_years_2012[1]
    
    grade_3_years_2010 = np.array(grade_3_years_2010)
    grade_3_years_2011 = np.array(grade_3_years_2011)
    grade_3_years_2012 = np.array(grade_3_years_2012)
    
    #print len(grade_3_years_2010)
    #print len(grade_3_years_2011)
    #print len(grade_3_years_2012)
    
    grade_improvement = []
    grade_improvement_with_district = []
    for i in grade_3_years_2012:
        #Removes the schools that doesnt exist in 2012
        grade_2010 = grade_3_years_2010[(grade_3_years_2010[0::,1] == i[1]) & (grade_3_years_2010[0::,2] == i[2])] #First is code, 2nd is type
        grade_2011 = grade_3_years_2011[(grade_3_years_2011[0::,1] == i[1]) & (grade_3_years_2011[0::,2] == i[2])]
        
        #print grade_2010[0][4]
        
        #Check if the arrays are not empty = the school haven't existed for 3 years
        if grade_2010.size and grade_2011.size: 
            grade_10 = grade_2010[0][4]
            grade_11 = grade_2011[0][4]
            grade_12 = i[4]
        
            grade_improvement.append([grade_10,grade_11,grade_12])
            grade_improvement_with_district.append([grade_10,grade_12,i[-1]])
        
        #break
    
    print 'Number of schools that have existed for 3 years: ', len(grade_improvement)
    print grade_improvement_with_district
    
    #For each district calculate how many schools improved,worsened, didnt change
    district_change = []
    improved = 0
    worsened = 0
    unchanged = 0
    for i in grade_improvement_with_district:
        #Improved or not
        if i[1] > i[0]:
            improved = 1
            worsened = 0
            unchanged = 0
        if i[1] < i[0]:
            improved = 0
            worsened = 1
            unchanged = 0
        if i[1] == i[0]:
            improved = 0
            worsened = 0
            unchanged = 1
        
        #Check if the district has already been added to the list
        def m_array_index(arr, searchItem):
            for i,x in enumerate(arr):
                for j,y in enumerate(x):
                    if y == searchItem:
                        return i,j #j is not needed here
            return -1,-1 #not found
        
        location = m_array_index(district_change,i[2])
        
        if location[0] != -1:
            #Update the values
            district_change[location[0]] = [
                                    i[2],
                                    district_change[location[0]][1]+improved,
                                    district_change[location[0]][2]+improved,
                                    district_change[location[0]][3]+improved
                                    ]
        else:
            district_change.append([i[2],improved,worsened,unchanged])
    
    print district_change
    print len(district_change)
    
    district_change_percentage = []
    for i in district_change:
        total = sum(i[1:4])
        improved = (float(i[1])/total)*100
        worsened = (float(i[2])/total)*100
        unchanged = 100 - improved - worsened
        
        district_change_percentage.append([
                                           i[0],
                                           improved,
                                           worsened,
                                           unchanged,
                                           total
                                          ])
    
    #print district_change_percentage
    
    #Sort the array by improved schools
    from operator import itemgetter
    
    district_change_percentage = sorted(district_change_percentage, key=itemgetter(3))
    district_change_percentage = sorted(district_change_percentage, key=itemgetter(1))
    
    
    #Reverse
    district_change_percentage.reverse()
    
    print district_change_percentage
    
    #Plot. The bar is fatter the more schools in the district
    district_change_percentage = np.array(district_change_percentage)
    
    ind = np.arange(len(district_change_percentage))
    width = 0.6
    
    counter = 0
    for i in district_change_percentage:
        #worsened
        plt.bar(
                counter,
                i[1].astype(np.float) + i[2].astype(np.float) + i[3].astype(np.float),
                (i[4].astype(np.float)/len(district_change_percentage))*width,
                color='#d72e39',
                edgecolor='#d72e39'
                ) #worsened
        
        #unchanged
        plt.bar(
                counter,
                i[1].astype(np.float) + i[3].astype(np.float),
                (i[4].astype(np.float)/len(district_change_percentage))*width,
                color='w',
                edgecolor='w'
                )
        
        #improved
        plt.bar(
                counter,
                i[1].astype(np.float),
                (i[4].astype(np.float)/len(district_change_percentage))*width,
                color='#002768',
                edgecolor='#002768'
                ) #improved
        
        counter += 1
    
    plt.xlim([0,len(district_change_percentage)])
    plt.ylim([0,100])
    
    #Remove top and right axis
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    plt.show()
    
#===============================================================================
# Main program
#===============================================================================
data_2010 = import_csv_turninto_array(r'\2010_final_grade.csv')
data_2011 = import_csv_turninto_array(r'\2011_final_grade.csv')
data_2012 = import_csv_turninto_array(r'\2012_final_grade.csv')

#Remove unnecessary columns messy if remove can check with csv file
#data = np.delete(data,[6,7,8,9,10,11,12,13,14],1) #1 is direction 0=row 1=column  
#print data_2012[0]
#print len(data_2012)

#Remove schools with no rating (school grade is not in the same column in each file)
data_2010 = data_2010[data_2010[0::,15] != '']
data_2011 = data_2011[data_2011[0::,14] != '']
data_2012 = data_2012[data_2012[0::,9] != '']

#print data_2012[0]
#print len(data_2012)

#print data_2012_a[0::,4]
#print len(data_2012_a)


#------------------------------------------------------------------------------
# Experiments

#Plot the distribution of grades and change since 2010
#distribution_of_grades(data_2010,data_2011,data_2012)

#Get all the A schools and their cities
#where_are_the_a_schools_located(data_2012)

#How have individual schools improved since 2010
#how_have_individual_schools_improved(data_2010,data_2011,data_2012)

#Poor students plots how many at the different school grades are receiving discounted lunch
#poor_people(data_2010,data_2011,data_2012)
#poor_people_2010(data_2010,data_2011,data_2012)

#Can the students continue to college
#continue_to_college(data_2010,data_2011,data_2012)

#Which districts have improved / worsened?
districts_improved_or_not(data_2010,data_2011,data_2012)
 




