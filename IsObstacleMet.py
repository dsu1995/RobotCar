from Constants import *
from myro import *

class Readings:
    def __init__(self):
        self.readings=map(list,zip(*[getObstacle() for _ in xrange(5)]))     
            
    def takeReading(self):
        temp=getObstacle()
        for i in xrange(3):
            del self.readings[i][0]
            self.readings[i].append(temp[i]) 
        a=map(lambda x:sum(x)/len(x), self.readings)
        print "distance:",max(a)
        return max(a)   