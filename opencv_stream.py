import cv2
import asyncio
import socketio
import base64
import numpy as np

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

            
            cv2.imshow('frame', frame)


            # Encode the frame with a specified JPEG compression quality (e.g., 50)
            jpeg_quality = 50  # Adjust this value as needed
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
            retval, buffer = cv2.imencode('.jpg', frame, encode_param)
            
            jpg_as_text = base64.b64encode(buffer)
            sio.emit("imageSend", {"data": jpg_as_text.decode('utf-8')})

            cv2.imshow('frame', frame)

            # 30 ms delay
            key = cv2.waitKey(30) & 0xFF
            # press q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    # actually connect now
    try:
        print("connecting to socket.io server")
        # sio.connect('https://3540-76-78-137-148.ngrok-free.app')
        sio.connect('https://marshy-glaze-brazil.glitch.me/', wait_timeout=10)
    except Exception as e:
        print(e)
    
    while (True):
        pass

if __name__ == "__main__":
    asyncio.run(main())