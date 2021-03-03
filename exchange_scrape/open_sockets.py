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
class ExchangeSocket:
    def __init__(self, exchange_information:dict):
        # Init details about exchange
        self.exchange_id = exchange_information['exchange_id']
        self.socket_url = exchange_information['endpoint']
        self.server_request = json.dumps(exchange_information['sub_request'])
        self.response_map = exchange_information['reponse_map']

    # Create websocket consumer
    async def consume(self) -> None:
        async with websockets.connect(self.socket_url) as websocket:
            await websocket.send(self.server_request)
            await self.consumer_handler(websocket=websocket)
    
    # Handle reponses, need to hook this up to reddis
    async def consumer_handler(self, websocket) -> None:
        async for message in websocket:
            try:
                response = json.loads(message)
                best_bid = response[self.response_map['best_bid']]
                best_ask = response[self.response_map['best_ask']]
                print(f'BINANCE best bid" {best_bid}, best ask: {best_ask}')

            except:
                print("Error in parsing result")

# Takes in list of ExchangeSocket objects and returns a coroutine object
async def open_multiple_sockets(exchangeSockets: list):
    pass
    

if __name__ == '__main__':
    # Init logging, Redis and Environment vars (API KEYS etc)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    #r = redis.Redis()
    load_dotenv()
    binanceXRP = ExchangeSocket(XRPUSDT.binance_XRPUSDT)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(binanceXRP.consume())


