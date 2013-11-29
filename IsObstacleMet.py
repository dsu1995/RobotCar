from Constants import *
from myro import *

#obstacle sensor class that filters out anomalous readings
class Readings:
    def __init__(self):
        #takes 5 readings from the obstacle sensor to begin, and stores it in an array
        self.readings=map(list,zip(*[getObstacle() for _ in xrange(5)]))     
            
    def takeReading(self):
        #takes a reading of left, centre, and right obstacle sensors
        temp = getObstacle()
        
        for i in xrange(3):
            del self.readings[i][0] #deletes oldest reading at the front of the queue
            self.readings[i].append(temp[i]) #adds newest reading to the back of the queue
            
        #takes the average of the past 5 readings for left, centre, and right sensors
        a = map(lambda x:sum(x)/len(x), self.readings)
        print "distance:", max(a)
        #returns the maximum reading of the 3 sensors
        return max(a)   