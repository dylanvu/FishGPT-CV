from VideoStream import VideoStream
from aiortc import RTCPeerConnection, RTCSessionDescription

def createPeerConnection():
    connection = RTCPeerConnection()

    # Add your video stream to the connection
    video_stream = VideoStream()
    connection.addTrack(video_stream)
    return connection

async def offer(sio):
    connection = createPeerConnection()
    # Create an SDP offer
    offer = await connection.createOffer()
    await connection.setLocalDescription(offer)

    # send the offer to Node.js server (implement this part)
    offer_dict = {
        "type": offer.type,
        "sdp": offer.sdp,
    }
    print("sending offer dict")
    # print(offer_dict)
    await sio.emit("pythonOffer", {"data": offer_dict})

async def handle_connect(sio):
    print('connection established')
    # send message with the socket io
    await sio.emit('pythonConnect')

async def handle_incoming_sdp(data, sio):
    print("incoming sdp")
    # now, we create an offer and send it back
    await answer(data["sdp"], sio)

async def answer(sdp, sio):
    connection = createPeerConnection()

    # Create an SDP offer
    await connection.setRemoteDescription(RTCSessionDescription(sdp, type="offer"))
    rtcAnswer = await connection.createAnswer()
    answer_dict = {
        "type": rtcAnswer.type,
        "sdp": rtcAnswer.sdp,
        "socketId": sio.id
    }
    print(answer_dict)
    sio.emit('pythonAnswer', answer_dict)