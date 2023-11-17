import cv2
import asyncio
import socketio
import base64
import numpy as np

from webcoords import colorMask, createQuadrants, checkCoordinate, findMidpoint
from PIL import Image
import random
import time

# Function to return emoji depending on quadrant
EmojiDic = {"<(O w O)>": 0, "<(.-.)>": 1, "<(T^T)>": 2, "<(O _ O)>": 3}
EmojiArr = ["<(O w O)>", "<(.-.)>", "<(T^T)>", "<(O _ O)>"]
def shuffleEmojis(oldepoch):
    if time.time() - oldepoch >= 30:
        # just shuffled, return true
        random.shuffle(EmojiArr)
        return True
    else:
        # not time yet
        return False
    
    
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

# Function to draw a thought bubble
def draw_thought_bubble(frame, x, y, text="Thoughts"):
    cv2.ellipse(frame, (x, y), (50, 30), 0, 0, 360, (255, 255, 255), -1)  # Draw bubble
    cv2.putText(frame, text, (x-40, y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)  # Add text
    
async def main():
    # create socket.io connection
    sio = socketio.Client()
    @sio.event
    def connect():
        print("CONNECTED")

        cap = cv2.VideoCapture(0)
        
        # Shapes video for fisheye fix adjustment
        codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        cap.set(6, codec)
        cap.set(5, 30)
        cap.set(3, 1920)
        cap.set(4, 1080)
        
        # Camera, fixing fisheye
        cameraMatrix = np.genfromtxt("./camera_matrix.txt")
        dist = np.genfromtxt("./distortion.txt")
        
        ret, frame = cap.read()
        h, w = frame.shape[:2]
        
        newCameraMatrix, roi = cv2. getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 1, (w, h))
        
        justShuffled = True
        
        while True:
            
            ret, frame = cap.read()

            # undistorts the fisheye frame
            frame = cv2.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)
            x, y, w, h = roi
            frame = frame[y:y+h, x:x+w]
            
            # Resize the frame
            new_width = 640  # New width
            new_height = 480  # New height
            frame = cv2.resize(frame, (new_width, new_height))

            # do masking
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
            # shuffle the emojis once in a while
            if justShuffled:
                # we just shuffled so save the time
                oldtime = time.time()
            else:
                # is it time to shuffle?
                justShuffled = shuffleEmojis(oldtime)
                
            if largest_contour is not None:
                # Get the bounding box of the largest contour
                x, y, w, h = cv2.boundingRect(largest_contour)

                # Draw a rectangle around the largest contour
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
                    # Calculates coordinates, by calculating the center of the box that highlights the fish
                coord = findMidpoint(x, x + w, y, y + h)
                quad = checkCoordinate(coord[0], coord[1], quadrants)
                
                # Create a thought bubble
                # get the emotion based on the quadrant
                emotion = EmojiArr[quad]
                draw_thought_bubble(frame, x, y - 50, emotion)
                
                # # DEBUG PRINTS
                # print("COORD: ", coord)
                # print("QUADRANT IT IS IN: ", quad)
                
                # send the coordinates
                if (coord is not None):
                    # sio.emit("coordsSend", {"data": {"x": coord[0], "y": coord[1], "quadrant": quad}})
                    # this gives the frontend a consistent "quadrant" associated with each emotion, despite the emoji array shuffling around
                    emotionIndex = EmojiDic[emotion]
                    sio.emit("coordsSend", {"data": {"quadrant": emotionIndex}})
                    
            
            cv2.imshow('frame', frame)
            
            # Encode the frame with a specified JPEG compression quality (e.g., 50)
            jpeg_quality = 50  # Adjust this value as needed
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
            retval, buffer = cv2.imencode('.jpg', frame, encode_param)
            
            jpg_as_text = base64.b64encode(buffer)
            sio.emit("imageSend", {"data": jpg_as_text.decode('utf-8')})
               
            # 30 ms delay
            key = cv2.waitKey(30) & 0xFF
            # press q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    # actually connect now
    try:
        print("connecting to socket.io server")
        # sio.connect('https://3540-76-78-137-148.ngrok-free.app')
        sio.connect('https://ea1b-76-78-137-157.ngrok-free.app/', wait_timeout=10)
    except Exception as e:
        print(e)
    
    while (True):
        pass

if __name__ == "__main__":
    asyncio.run(main())