import cv2
import asyncio
import socketio
from rtc_logic import offer, handle_incoming_sdp

import numpy as np

# GamePlan
# Read From WebCam
# Apply Coordinates to the Video Received
    # Apply Question Coordinates
    # Can Be Scalable to how many questions/answers
# Mask Out all the colors, Recognize Goldfish Color
# Get Coordinates From Color
# Check which Coordinate Matches From Color, Return Answer

# Input Coordinates, Returns if it is in the Quadrant Parameter 
def CheckCoordinate(X: int, Y: int, Quadrants: list):
    return False

# Apply Question & Emoji To Quadrant
def QuestionQuadrants(Questions: list, Emojis: list, Quadrants: list):
    return False

# Function To Get Colors
def get_limits(color):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value

    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit

async def main():


    sio = socketio.Client()

    @sio.event
    def connect():
        print('connection established')


    @sio.event
    def disconnect():
        print('disconnected from server')

    # define a function to answer an incoming SDP
    @sio.event
    def incoming_sdp(data):
        handle_incoming_sdp(data)

    # actually connect now
    try:
        sio.connect('http://localhost:5000')
        # send the SDP connection request to all connected JS clients
        await offer(sio)
    except:
        print("Could not connect and make offer")

    

    # now do all the openCV stuff
    # Turning Camera On -------------------------------------

    # VideoCapture(0), 0 is the default value of webcam
    cam = cv2.VideoCapture(0)
    Orange = [0, 165, 255]

    # while the camera is on, reads each frame by frame
    while(True):
        check, frame = cam.read()
        cv2.imshow('frame', frame)
        
        # handling color detection
        # convert BGR color space to RGB
        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lowerLimit, upperLimit = get_limits(color=Orange)
        
        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
        cv2.imshow('frame', mask)
        # press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    asyncio.run(main())