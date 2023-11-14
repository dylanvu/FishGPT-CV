import cv2
import asyncio
import socketio
from rtc_logic import offer, handle_connect, handle_incoming_sdp

import numpy as np
from webcoords import colorMask, createQuadrants, checkCoordinate, findMidpoint
from PIL import Image

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

    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()

        mask = colorMask(frame)
        
        # split frame into quadrants
        quadrants = createQuadrants(frame)
        
        # DEBUGGING PRINTS
        # Display the quadrants
        # print("QUADRANTS")
        # print("TOPLEFT: ", quadrants[0])
        # print("TOPRIGHT: ", quadrants[1])
        # print("BOTTOMLEFT: ", quadrants[2])
        # print("BOTTOMRIGHT: ", quadrants[3])

        # actualQuad = checkCoordinate(coords[0], coords[1], quadrants)
        # print("QUADRANT IT IS IN: ", actualQuad)
        # creating box to highlight fish
        mask_ = Image.fromarray(mask)
        
        bbox = mask_.getbbox()
        
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            
            # DEBUG PRINTS
            # print("x1: ", x1)
            # print("x2: ", x2)
            # print("y1: ", y1)
            # print("y2: ", y2)
            
            # Calculates coordinates, by calculating the center of the box that highlights the fish
            coord = findMidpoint(x1, x2, y1, y2)
            quad = checkCoordinate(coord[0], coord[1], quadrants)
            
            # DEBUG PRINTS
            print("COORD: ", coord)
            print("QUADRANT IT IS IN: ", quad)
            
            # Creates the frame around the goldfish
            frameBox = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

        
        # displays fish w/o box
        cv2.imshow('frame', frame)
        # displays fish with box
        # cv2.imshow('frame', frameBox)
        
        # press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    asyncio.run(main())