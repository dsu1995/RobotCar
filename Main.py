from myro import *
from IsObstacleMet import *
from FindColour import *
from Constants import *

initialize(PORT)
manualCamera(0,50,100) #manually adjusts camera settings

#used to set the colour of the garbage we are looking for by 
def calibrateGarbage():   
    #user presses enter to begin
    raw_input("Calibrating garbage. Press enter to begin...")  
    
    r_sum = 0
    g_sum = 0
    b_sum = 0
    pixelCount = 0
    
    pic=takePicture()
    show(pic)
    
    #only considers rectangle bounded by 2/5 width on left, 3/5 width on right
    #3/5 height on top, and 4/5 height on the bottom
    for i in xrange(WIDTH/5*2, WIDTH/5*3): 
        for j in xrange(HEIGHT/5*3, HEIGHT/5*4):  
            R, G, B = getRGB(getPixel(pic, i, j))
            #accumulates RGB values
            r_sum += R
            g_sum += G
            b_sum += B
            pixelCount += 1
    
    if pixelCount == 0:
        pixelCount = 1    
    
    #returns the average colour in the bounded region, 
    #to be used as the colour of the garbage we are looking for
    colour = (r_sum/pixelCount, g_sum/pixelCount, b_sum/pixelCount)
    print 'Garbage colour:', colour    
    return colour
    
#similar to calibrateGarbage(), but instead this function
#sets the colour of the garbage bin we are looking for
def calibrateGarbageBin():  
    raw_input("Calibrating garbage bin. Press enter to continue...")      
    r_sum = 0
    g_sum = 0
    b_sum = 0
    pixelCount = 0
    
    pic=takePicture()
    show(pic)
    
    for i in xrange(WIDTH/3, WIDTH/3*2): 
        for j in xrange(HEIGHT/5*3, HEIGHT/5*4):  
            R,G,B = getRGB(getPixel(pic,i,j))
            r_sum += R
            g_sum += G
            b_sum += B
            pixelCount += 1
    
    if pixelCount == 0:
        pixelCount = 1
    
    colour = (r_sum/pixelCount, g_sum/pixelCount, b_sum/pixelCount)
    print 'Garbage bin colour:', colour    
    return colour

#turns the robot to the left repeatedly until one of the garbage colours is found
#returns the colour of the garbage found
def initialFind(colours):
    while 1:
        for i in xrange(len(colours)):
            if findColour(colours[i][0])[0]:
                return colours.pop(i)
        turnLeft(ADJUST_TURN_SPEED, ADJUST_TURN_TIME) 
        
#turns the robot until the robot is directly facing the garbage
def find(colour):
    while 1:
        output = findColour(colour)[0]
        print'location:', output
        if(output == False or output == "left"):
            turnLeft(ADJUST_TURN_SPEED, ADJUST_TURN_TIME)
        elif(output == "right"):
            turnRight(ADJUST_TURN_SPEED, ADJUST_TURN_TIME)
        else:
            break       

#called to move the garbage
def moveToGarbage(colours):
    currentColour=initialFind(colours)
            
    find(currentColour[0])        
        
    #instantiates obstacle sensor readings class
    readings = Readings()
    
    while 1:
        forward(0.5) #moves the robot forward
        output, pixelCount = findColour(currentColour[0])
        print "location:", output
        
        #if the number of pixels matching the garbage exceeds a threshold, 
        #the robot is close enough and stops moving forward
        #or, if the obstacle sensor detects that the robot is close enough to 
        #the obstacle, the robot will stop as well        
        if pixelCount>2000 or readings.takeReading()>DISTANCE_THRESHOLD: 
            stop() 
            break          
        #if garbage is no longer centered, use find() function to recenter it
        elif(output != "centre"):           
            find(currentColour[0])        
    
    #returns the colour found
    return currentColour
    
def turn180():
    turnRight(TURN_SPEED, TURN_TIME)

def putGarbageInBin(colour):
    #because arms are mounted on back of robot to prevent the garbage 
    #from obstructing the view of the sensors on the fluke board,
    #the robot must carry the garbage behind it
    turn180()        
    backward(1,3)
    
    while 1:
        find(colour[1])  #centres garbage bin on screen
           
        #turns 180 so that garbage is between the robot and bin
        turn180()
        #and backs the garbage into the garbage bin
        backward()
        
        for _ in timer(8):
            #if the line sensor detects the tape in front of the garbage bin
            if 0 in getLine() and 0 in getLine():
                #goes forward to exit the garbage bin and returns from the function
                #garbage has now been successfully placed into the bin
                forward(1,3)
                return
            
        #else if 8 seconds elapses and the robot still has not placed the garbage in the bin
        #the robot will turn around and recenter the garbage bin in its view
        turn180()
        backward(1,0.5)
        
def main():     
    #calibrates colours first
    colours=[[calibrateGarbage(), calibrateGarbageBin()], [calibrateGarbage(), calibrateGarbageBin()]]
    
    raw_input("Done calibrating. Press enter to start...")
    
    #finds each garbage and places them in the appropriate bin
    colourFound=moveToGarbage(colours)
    putGarbageInBin(colourFound)
    
    colourFound2=moveToGarbage(colours)
    putGarbageInBin(colourFound2)
        
main()
