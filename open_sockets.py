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
async def consume(connectionurl, sub_request, redis):
    async with websockets.connect(connectionurl) as websocket:
        await websocket.send(sub_request)
        await consumer_handler(websocket=websocket)

async def consumer_handler(websocket):
    async for message in websocket:
        try:
            response = json.loads(message)
            best_ask = response['b']
            best_bid = response['a']
            global r
            r.mset(({}))
        except:
            logger.error("Error in parsing result")

if __name__ == '__main__':
    # Init logging, Redis and Environment vars (API KEYS etc)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    r = redis.Redis()
    load_dotenv()

    asyncio.get_event_loop().run_until_complete(consume())
