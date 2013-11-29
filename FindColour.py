from myro import *
from Constants import *

#given a colour, takes a picture and returns the location of that colour on the screen 
#and how many pixels of that colour were found
def findColour(colour):   
    pic = takePicture()
    r, g, b = colour    
    show(pic)
    
    pixels = []
                
    #scans all pixels between 1/3 height and 3/4 height
    for i in xrange(WIDTH):
        for j in xrange(HEIGHT/3, HEIGHT/4*3): 
            R, G, B = getRGB(getPixel(pic, i, j))
            deltaR = abs(R - r)
            deltaG = abs(G - g)
            deltaB = abs(B - b)
            #if the "distance" of the colour of the pixel is close enough 
            #to the colour we are looking for, it is added to the array
            if (deltaR + deltaG + deltaB < COLOUR_TOLERANCE): 
                pixels.append([i, j])                
                
    
    if len(pixels) > 0:
        pixel_count = len(pixels) 
        print 'pixel count: ', pixel_count
        #the average x-value of all the pixels in range is calculated
        average_x = sum(pixels[i][0] for i in xrange(pixel_count))/pixel_count 
    else:
        print 'pixel count: ', 0
        return False, 0
    
    #if not enough pixels are detected, it is probably an anomaly and ignored
    if pixel_count < MIN_PIXELS:
        return False, pixel_count
    #because the camera is off-center, the "left" and "right" of the robot is not symmetrical
    #through testing, left of 35% of the width is left
    elif average_x <= WIDTH*0.35:
        return "left", pixel_count
    #between 35% and 55% of the width is centered
    elif WIDTH*0.35 < average_x < WIDTH*0.55:
        return "centre", pixel_count
    #and greater than 55% is on the right
    else:
        return "right", pixel_count