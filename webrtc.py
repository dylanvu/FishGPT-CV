import cv2
import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
import socketio

class VideoStream(VideoStreamTrack):
    def __init__(self):
        super().__init__()

    async def recv(self):
        pass
        # Implement video capture logic here (using Raspberry Pi camera)
        # Return video frames as bytes
        # Example: return await capture_video_frames()

async def offer(sio):
    connection = RTCPeerConnection()
    connection_id = "your_unique_connection_id"

    # Add your video stream to the connection
    video_stream = VideoStream()
    connection.addTrack(video_stream)

    # Create an SDP offer
    offer = await connection.createOffer()
    await connection.setLocalDescription(offer)

    # send the offer to Node.js server (implement this part)
    offer_dict = {
        "type": offer.type,
        "sdp": offer.sdp,
    }
    sio.emit("openCVoffer", {"data": offer_dict})

async def main():

    # openCV stuff
    cap = cv2.VideoCapture(0)

    sio = socketio.Client()

    @sio.event
    def connect():
        print('connection established')


    @sio.event
    def disconnect():
        print('disconnected from server')

    # actually connect now
    sio.connect('http://localhost:5000')
    
    # send the SDP connection request to all connected JS clients
    await offer(sio)

    # now do all the openCV stuff
    while(True):
        ret, frame = cap.read()  # return a single frame in variable `frame`
        # frame = cv2.resize(frame, (1920, 1080))
        cv2.imshow('Capturing Video', frame)  # display the captured image
        key = cv2.waitKey(1) & 0xFF
        if key == ord('y'):  # exit on pressing 'y'
            cv2.destroyAllWindows()
            break

    cap.release()

if __name__ == "__main__":
    asyncio.run(main())