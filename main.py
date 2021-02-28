from dotenv import load_dotenv
from exchange_infomation import binance
import redis
import websockets
import logging
import asyncio
import json
import os



"""
Notes: .env is chmod 400
"""
async def consume(connectionurl, sub_request):
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

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    r = redis.Redis()

    # Load private varibles (api keys, etc) into env vars
    load_dotenv()
    binance_api_key = os.getenv('BINANCE_API_KEY')
    binance_secret_key = os.getenv('BINANCE_SECRET_KEY')

    binance_base_endpoint = 'wss://stream.binance.com:9443/ws/xrpusdt@bookTicker'
    binance_sub_request = json.dumps({
        "method": "SUBSCRIBE",
        "params": [
            "xrpusdt@bookTicker"
        ],
        "id":1
    })
    
    print(binance_sub_request)
    asyncio.get_event_loop().run_until_complete(consume(binance['xrpusdt']['endpoint'],binance['xrpusdt']['sub_request']))
