import json
import asyncio
from time import sleep
from enum import Enum

from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Request
from utils.websocket_manager import ConnectionManager



ROUTE_PREFIX = '/ws'

router = APIRouter(
    prefix = ROUTE_PREFIX
)


manager = ConnectionManager()

@router.websocket("/example")
async def websocket_endpoint(websocket: WebSocket):

    try:
        print("\nwebsocket connection request\n")
        await websocket.accept()
        data = await websocket.receive_text()
        print("This is data: {}".format(data))
        data = json.loads(data)
        client_id = data["client_id"]
        await manager.connect(websocket, client_id)
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client # left the chat")

@router.get("/example")
async def example(request: Request):
    return {"status": True}


async def start_console(manager= manager):
    interval = 5
    count = 0
    while True:
        print("Printing from test console example in modules/console_example/\n \
            To stop this test console, set enable_test_console in flags.py to False")
        print("loop: {}".format(count))
        try:
            count += 1
            await manager.broadcast(str(count))
        except Exception as e:
            pass
        sleep(interval)


def start_example_console():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(start_console())
    loop.close()


class routes(Enum):
    example_websocket_console: dict = {
        "url": ROUTE_PREFIX + "/example",
        "method": "ws"
    }
