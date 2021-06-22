from fastapi import WebSocket



class ConnectionManager:

    def __init__(self):

        self.active_connections = {}


    async def connect(self, websocket: WebSocket, client_id:str):

        if client_id not in self.active_connections:
            self.active_connections[client_id] = websocket


    def disconnect(self, websocket: WebSocket):

        for key, val in self.active_connections.items():
            if val==websocket:
                del self.active_connections[key]


    async def send_personal_message(self, message: str, websocket: WebSocket):

        await websocket.send_text(message)


    async def broadcast(self, message: str):

        for client, connection in self.active_connections.items():
            print("client: {}".format(client))
            await connection.send_text(message)
