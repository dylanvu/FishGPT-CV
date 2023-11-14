from VideoStream import VideoStream
from aiortc import RTCPeerConnection, RTCSessionDescription

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
    print("sending offer dict:")
    print(offer_dict)
    sio.emit("pythonOffer", {"data": offer_dict})

def handle_connect(sio):
    print('connection established')
    # send message with the socket io
    sio.emit('pythonConnect')

def handle_incoming_sdp(data):
    print("incoming sdp")
    print(data)