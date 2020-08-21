import sys

import asyncio

import asyncio


class Server:
    async def _start(self):
        server = await asyncio.start_server(
            self.main, *self.interface)
        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')
        async with server:
            await server.serve_forever()

    def start(self):
        asyncio.run(self._start())

    def __init__(self, interface):
        self.interface = interface 

    async def main(self, reader, writer):
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')

        print(f"Received {message!r} from {addr!r}")

        print(f"Send: {message!r}")
        writer.write(data)
        await writer.drain()

        print("Close the connection")
        writer.close()



if __name__ == '__main__':
    server = Server(('127.0.0.1', 8888))
    server.start()
