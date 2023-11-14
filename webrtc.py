import cv2
import asyncio
import socketio
from rtc_logic import offer, handle_connect, handle_incoming_sdp

import numpy as np
from webcoords import get_limits

async def main():

    # all the socket.io stuff
    sio = socketio.Client()

    @sio.event
    def connect():
        handle_connect(sio)


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

    # end socket.io stuff

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