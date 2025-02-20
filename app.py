import cv2
import numpy as np
import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from av import VideoFrame

pcs = set()

async def offer(request):
    params = await request.json()
    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("track")
    def on_track(track):
        if track.kind == "video":
            async def recv():
                async for frame in track:
                    img = frame.to_ndarray(format="bgr24")
                    cv2.imshow("WebRTC Video", img)
                    cv2.waitKey(1)

            asyncio.ensure_future(recv())

    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})

app = web.Application()
app.router.add_post("/offer", offer)

web.run_app(app, host="0.0.0.0", port=8080)
