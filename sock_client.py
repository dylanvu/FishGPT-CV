import cv2
import asyncio
import socketio
import base64
import numpy as np
from webcoords import get_limits

async def main():
    # create socket.io connection
    sio = socketio.Client()

    @sio.event
    def connect():
        sio.emit("test")

        cam = cv2.VideoCapture(0)
        Orange = [0, 165, 255]
        fCount = 0

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
            if (fCount % 1000 == 0):
                # convert to base64 to emit as data
                retval, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer)
                print("image sent")
                sio.emit("imageSend", {"data": jpg_as_text})
                fCount = 0
            else:
                fCount += 1
            # press q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("manually closing camera")
                cam.release()
                cv2.destroyAllWindows()
                break

    # actually connect now
    try:
        print("connecting to socket.io server")
        sio.connect('http://localhost:5000')
    except Exception as e:
        print(e)
    
    while (True):
        pass

if __name__ == "__main__":
    asyncio.run(main())