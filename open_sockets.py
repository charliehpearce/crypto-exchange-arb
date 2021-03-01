from dotenv import load_dotenv
from exchange_data import XRPUSDT
import redis
import websockets
import logging
import asyncio
import json

"""
Notes: .env is chmod 400
"""
class Socket:
    def __init__(self, exchange_information:dict):
        self.exchange_id = exchange_information['exchange_id']
        self.socket_url = exchange_information['endpoint']
        self.server_request = json.dumps(exchange_information['params'])

    async def consume(self, connectionurl, sub_request):
        async with websockets.connect(self.socket_url) as websocket:
            await websocket.send(self.server_request)
            await self.consumer_handler(websocket=websocket)

    async def consumer_handler(self, websocket):
        async for message in websocket:
            try:
                response = json.loads(message)
            except:
                logger.error("Error in parsing result")

if __name__ == '__main__':
    # Init logging, Redis and Environment vars (API KEYS etc)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    r = redis.Redis()
    load_dotenv()

    asyncio.get_event_loop().run_until_complete(consume())

