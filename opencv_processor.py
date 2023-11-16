import cv2
import asyncio
import socketio
import base64
import numpy as np
from webcoords import colorMask, createQuadrants, checkCoordinate, findMidpoint
from PIL import Image

# this file handles the CV and coordinate system

# Function to find the largest contour in the mask
def find_largest_contour(mask, min_contour_area):
    # Convert the image to grayscale (single-channel)
    grayscale_result = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # Threshold the image to create a binary mask
    _, binary_mask = cv2.threshold(grayscale_result, 1, 255, cv2.THRESH_BINARY)

    # Find contours in the binary mask
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        # do not show anything below min contour area specified
        if cv2.contourArea(largest_contour) > min_contour_area:
            return largest_contour
    else:
        return None

def main():
    # create socket.io connection
    sio = socketio.Client()

    @sio.event
    def connect():
        print("we are connected!")

    @sio.event
    def imageReceive(data):
        print("image received")
        # decode the base64-encoded string to bytes
        decoded_image = base64.b64decode(data["data"])

        # convert the bytes to a NumPy array
        nparr = np.frombuffer(decoded_image, np.uint8)

        # decode the NumPy array to an OpenCV image
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        mask = colorMask(frame)
        kernel = np.ones((5,5),np.uint8)
        # removes small noise
        erosion = cv2.erode(mask,kernel,iterations = 1)
        # fills gaps, connects nearby regions
        img_dilation = cv2.dilate(erosion, kernel, iterations=1)
        
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= img_dilation)

        # Find the largest contour in the mask
        largest_contour = find_largest_contour(res, 2)
        
        # split frame into quadrants
        quadrants = createQuadrants(frame)
        
        if largest_contour is not None:
            # Get the bounding box of the largest contour
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Draw a rectangle around the largest contour
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
                # Calculates coordinates, by calculating the center of the box that highlights the fish
            coord = findMidpoint(x, x + w, y, y + h)
            quad = checkCoordinate(coord[0], coord[1], quadrants)
            
            # DEBUG PRINTS
            print("COORD: ", coord)
            print("QUADRANT IT IS IN: ", quad)
            # send the coordinates
            if (coord is not None):
                sio.emit("coordsSend", {"data": {"x": coord[0], "y": coord[1], "quadrant": quad}})
        
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
    main()