import cv2
import asyncio
import socketio
import base64
import numpy as np
from webcoords import colorMask, createQuadrants, checkCoordinate, findMidpoint
from PIL import Image

async def main():
    # create socket.io connection
    sio = socketio.Client()

    @sio.event
    def connect():

        cap = cv2.VideoCapture(0)
        fCount = 0
        coord = None
        
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
            cv2.imshow('frame', frame)

            if (fCount % 10000 == 0):
                # convert to base64 to emit as data
                retval, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer)
                print("image sent")
                sio.emit("imageSend", {"data": jpg_as_text.decode('utf-8')})
                # also send the coordinates
                if (coord is not None):
                    sio.emit("coordsSend", {"data": {"x": coord[0], "y": coord[1], "quadrant": quad}})
                fCount = 0
            else:
                fCount += 1

    # actually connect now
    try:
        print("connecting to socket.io server")
        # sio.connect('https://3540-76-78-137-148.ngrok-free.app')
        sio.connect('https://fishgpt-backend.dylanvu9.repl.co/')
    except Exception as e:
        print(e)
    
    while (True):
        pass

if __name__ == "__main__":
    asyncio.run(main())