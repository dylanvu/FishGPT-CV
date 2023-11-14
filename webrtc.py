import cv2
import asyncio
import socketio
from rtc_logic import offer, handle_connect, handle_incoming_sdp

import numpy as np
from webcoords import get_limits

async def main():

    # all the socket.io stuff
    sio = socketio.AsyncClient()

    @sio.event
    async def connect():
        await handle_connect(sio)


    @sio.event
    async def disconnect():
        print('disconnected from server')
        await sio.emit('pythonDisconnect')

    # define a function to answer an incoming SDP
    @sio.event
    async def incoming_sdp(data):
        await handle_incoming_sdp(data, sio)

    # actually connect now
    try:
        await sio.connect('http://localhost:5000')
        # send the SDP connection request to all connected JS clients
    except:
        print("Could not connect: {e}")

    try:
        # make offer
        await offer(sio)
    except Exception as e:
        print(f"Could not make offer: {type(e).__name__}: {e}")

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