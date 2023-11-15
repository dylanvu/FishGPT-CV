import cv2
import numpy as np

# creates the quadrants given the frame
def createQuadrants(frame):
    height, width, c = frame.shape
    
    midX = width // 2
    midY = height // 2
    
    topLeft = [(0, midX), (0, midY)]
    topRight = [(midX, width), (0, midY)]
    bottomLeft = [(0, midX), (midY, height)]
    bottomRight = [(midX, width), (midY, height)]
    
    # INDEX VALUES
    # TOPLEFT: 0, TOPRIGHT: 1, BOTTOMLEFT: 2, BOTTOMRIGHT: 3
    return [topLeft, topRight, bottomLeft, bottomRight]
    
# Input Coordinates, returns which quadrant it is in 
def checkCoordinate(X: int, Y: int, Quadrants: list):
    for quadX, quadY in Quadrants:
        if quadX[0] <= X <= quadX[1] and quadY[0] <= Y <= quadY[1]:
            return Quadrants.index([quadX, quadY])

# given, the box find the midpoint to get coordinate
def findMidpoint(X1: int, X2: int, Y1: int, Y2: int):
    return ( (X1 + X2) / 2, (Y1 + Y2) / 2)

# Function To Get Colors
def colorMask(frame):
    # converting BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    orange = np.uint8([[[32, 68, 146]]])
    
    # convert the color to HSV
    hsvOrange = cv2.cvtColor(orange, cv2.COLOR_BGR2HSV)
    print("HSVORANGE: ", hsvOrange)
    
    
    # Define the HSV range for orange
    # orange is 27, 99, 233 BGR
    lower_orange = np.array([-1, 99, 46])
    upper_orange = np.array([19, 209, 156])
    
    # # white
    # body = np.uint8([[[99, 144, 155]]])
    # hsvBody = cv2.cvtColor(body, cv2.COLOR_BGR2HSV)
    # print("HSVBODY: ", hsvBody)
    # # white HSV: 24, 92, 155
    # lower_body = np.array([14, -2, 55])
    # upper_body = np.array([34, 192, 255])
    # maskBody = cv2.inRange(hsv, lower_body, upper_body)
    
    # create the mask
    maskOrange = cv2.inRange(hsv, lower_orange, upper_orange)
    
    mask = maskOrange
    return mask
    