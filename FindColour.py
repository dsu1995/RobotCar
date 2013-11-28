from myro import *
from Constants import *

def findColour(colour):   
    pic=takePicture()
    r,g,b=colour    
    show(pic)
    
    pixels=[]
                
    for i in xrange(WIDTH):
        for j in xrange(HEIGHT/3, HEIGHT/4*3):
            R,G,B = getRGB(getPixel(pic,i,j))
            deltaR=abs(R-r)
            deltaG=abs(G-g)
            deltaB=abs(B-b)
            if (deltaR+deltaG+deltaB<COLOUR_TOLERANCE):
                pixels.append([i,j])                
                
    if len(pixels)>0:
        pixel_count=len(pixels) 
        print 'pixel count: ',pixel_count
        average_x=sum(pixels[i][0] for i in xrange(pixel_count))/pixel_count 
    else:
        print 'pixel count: ', 0
        return False, 0
    
    if pixel_count<IS_OBJECT_THRESHOLD:
        return False, pixel_count
    elif average_x<=(WIDTH*0.35):
        return "left", pixel_count
    elif WIDTH*0.35<average_x<WIDTH*0.55:
        return "centre", pixel_count
    else:
        return "right", pixel_count