import cv2
import asyncio
import socketio
from rtc_logic import offer, handle_connect, handle_incoming_sdp

import numpy as np
from webcoords import colorMask, createQuadrants, checkCoordinate, findMidpoint
from PIL import Image

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


if __name__ == "__main__":
    asyncio.run(main())