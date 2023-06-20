import asyncio
import datetime
import logging
import pprint

import names
from aiofile import async_open
from aiopath import AsyncPath
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
import websockets

from chat_commands import bank

logging.basicConfig(level=logging.INFO)
log_file = AsyncPath("chat/chat_log.txt")


async def log_command(command: str):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with await async_open(log_file, "a") as f:
        await f.write(f"{current_time}: Command executed: {command}\n")


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.startswith("exchange"):
                await self.send_to_clients("Wait pls we are dealing with your question")
                await log_command(message)
                response = await bank.main(message)
                formatted_response = pprint.pformat(response, indent=4)
                await self.send_to_clients(f"PrivatBank:\n{formatted_response}")
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, "localhost", 8080):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
