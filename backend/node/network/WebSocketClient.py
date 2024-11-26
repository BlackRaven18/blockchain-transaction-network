import websockets
import asyncio

class WebSocketClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.websocket = None
        self.task = None
        self.keep_running = True

    async def connect(self):
        """
        Nawiązanie połączenia z serwerem WebSocket.
        """
        self.websocket = await websockets.connect(self.server_url)
        #self.task = asyncio.create_task(self.receive())
        print("Connected to WebSocket server.")

    async def send(self, message: str):
        """
        Wysyłanie wiadomości do serwera WebSocket.
        """
        if self.websocket:
            await self.websocket.send(message)
            response = await self.websocket.recv()
            print(f"Sent: {message}")
            return response

    # async def receive(self):
    #     """
    #     Odbieranie wiadomości z serwera WebSocket.
    #     """
    #     # while self.keep_running:
    #     try:
    #         if self.websocket:
    #             response = await self.websocket.recv()
    #             print(f"Received: {response}")
    #     except websockets.ConnectionClosed:
    #         print("Connection closed.")
    #         self.keep_running = False
    #         #break

    async def disconnect(self):
        """
        Rozłączanie z serwerem WebSocket.
        """
        self.keep_running = False
        if self.websocket:
            self.task.cancel()
            await self.websocket.close()

            print("Disconnected from WebSocket server.")