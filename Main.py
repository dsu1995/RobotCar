from myro import *
from IsObstacleMet import *
from FindColour import *
from Constants import *

initialize(PORT)
manualCamera(0,50,100)

def calibrateGarbage():   
    raw_input("Calibrating garbage. Press enter to begin...")  
    r_sum=0
    g_sum=0
    b_sum=0
    pixelCount=0
    
    pic=takePicture()
    show(pic)
    for i in xrange(WIDTH/5*2, WIDTH/5*3): 
        for j in xrange(HEIGHT/5*3, HEIGHT/5*4):  
            R,G,B = getRGB(getPixel(pic,i,j))
            r_sum+=R
            g_sum+=G
            b_sum+=B
            pixelCount+=1
    
    if pixelCount==0:
        pixelCount=1    
    
    colour=(r_sum/pixelCount, g_sum/pixelCount, b_sum/pixelCount)
    print 'Garbage colour:', colour    
    return colour
    
def calibrateGarbageBin():  
    raw_input("Calibrating garbage bin. Press enter to continue...")      
    r_sum=0
    g_sum=0
    b_sum=0
    pixelCount=0
    
    pic=takePicture()
    show(pic)
    for i in xrange(WIDTH/3, WIDTH/3*2): 
        for j in xrange(HEIGHT/5*3, HEIGHT/5*4):  
            R,G,B = getRGB(getPixel(pic,i,j))
            r_sum+=R
            g_sum+=G
            b_sum+=B
            pixelCount+=1
    
    if pixelCount==0:
        pixelCount=1
    
    colour=(r_sum/pixelCount, g_sum/pixelCount, b_sum/pixelCount)
    print 'Garbage bin colour:', colour    
    return colour

def initialFind(colours):
    while 1:
        for i in xrange(len(colours)):
            if findColour(colours[i][0])[0]:
                return colours.pop(i)
        turnLeft(ADJUST_TURN_SPEED,ADJUST_TURN_TIME) 
        
def find(colour):
    while 1:
        output = findColour(colour)[0]
        print'location:', output
        if(output == False or output == "left"):
            turnLeft(ADJUST_TURN_SPEED,ADJUST_TURN_TIME)
        elif(output == "right"):
            turnRight(ADJUST_TURN_SPEED,ADJUST_TURN_TIME)
        else:
            break       

def moveToGarbage(colours):
    currentColour=initialFind(colours)
            
    find(currentColour[0])
        
        
    readings = Readings()
    
    while 1:
        forward(0.5)
        output, pixelCount = findColour(currentColour[0])
        print "location:", output
        if pixelCount>2000:
            stop() 
            break          
        elif max(getObstacle())>THRESHOLD:
            stop()
            wait(1)
            
            if max(getObstacle())>THRESHOLD:
                wait(2)
                
                if max(getObstacle())>THRESHOLD:
                    break
            
        elif(output != "centre"):           
            find(currentColour[0])        
    
    return currentColour
    
def turn180():
    turnRight(TURN_SPEED, TURN_TIME)

def putGarbageInBin(colour):
    turn180()        
    backward(1,3)
    
    while 1:
        find(colour[1])      
        turn180()
        backward()
        
        for _ in timer(8):
            if 0 in getLine() and 0 in getLine():
                forward(1,3)
                return
            
        turn180()
        backward(1,0.5)
        
def main():     
    colours=[[calibrateGarbage(), calibrateGarbageBin()], [calibrateGarbage(), calibrateGarbageBin()]]
    
    raw_input("Done calibrating. Press enter to start")
    
    colourFound=moveToGarbage(colours)
    putGarbageInBin(colourFound)
    
    colourFound2=moveToGarbage(colours)
    putGarbageInBin(colourFound2)
        
main()
