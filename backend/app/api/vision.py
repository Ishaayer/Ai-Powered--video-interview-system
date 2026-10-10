import asyncio

import cv2
import numpy as np

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from app.services.vision_service import VisionService


router = APIRouter(
    prefix="/vision",
    tags=["Computer Vision"]
)


# Temporary/simple version.
# Later we can move this to app.state.
vision_service = VisionService()


@router.websocket(
    "/{interview_id}"
)
async def vision_stream(
    websocket: WebSocket,
    interview_id: int,
):

    await websocket.accept()

    print(
        f"CV connected for interview "
        f"{interview_id}"
    )

    try:

        while True:

            # Receive JPEG bytes
            data = await websocket.receive_bytes()

            # Decode JPEG
            array = np.frombuffer(
                data,
                dtype=np.uint8
            )

            frame = cv2.imdecode(
                array,
                cv2.IMREAD_COLOR
            )

            if frame is None:

                await websocket.send_json({
                    "success": False,
                    "error": "Invalid image frame",
                })

                continue

            # CV is CPU-bound, so don't block
            # FastAPI's async event loop.
            result = await asyncio.to_thread(
                vision_service.process_frame,
                frame,
            )

            result["success"] = True
            result["interview_id"] = interview_id

            await websocket.send_json(
                result
            )

    except WebSocketDisconnect:

        print(
            f"CV disconnected for interview "
            f"{interview_id}"
        )

    except Exception as exc:

        print(
            f"Vision error: {exc}"
        )

        try:

            await websocket.close(
                code=1011
            )

        except Exception:
            pass