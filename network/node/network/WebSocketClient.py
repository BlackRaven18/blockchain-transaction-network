import websockets

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
        try:
            self.websocket = await websockets.connect(self.server_url)
            print(f"Connected to {self.server_url}")
        except Exception as e:
            print(f"Error connecting to {self.server_url}: {e}")

    async def send_and_receive(self, message: str):
        """
        Wysyłanie wiadomości do serwera WebSocket i oczekiwanie na odpowiedz
        """
        if self.websocket:
            await self.websocket.send(message)
            response = await self.websocket.recv()
            # print(f"Sent: {message}")
            return response
        
    async def send(self, message: str):
        """
        Wysyłanie wiadomości do serwera WebSocket.
        """
        if self.websocket:
            await self.websocket.send(message)
            # print(f"Sent: {message}")

    async def disconnect(self):
        """
        Rozłączanie z serwerem WebSocket.
        """
        self.keep_running = False
        if self.websocket:
            self.task.cancel()
            await self.websocket.close()

            print("Disconnected from WebSocket server.")