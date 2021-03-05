import websocket
import os
from exchange_data import exchange_sockets
import redis
import json
import gzip
import asyncio

class RedisClient:
    def __init__(self, redis_host:str, redis_port):
        self.client = redis.Redis(host=redis_host, port=redis_port)

    def add_to_sorted_list(self, exchange_id:str, currency_pair, best_bid, best_ask):
        self.client.zadd(name=currency_pair+'-best_bid', mapping={exchange_id:best_bid})
        self.client.zadd(name=currency_pair+'-best_ask', mapping={exchange_id:best_ask})

class Utils:
    @staticmethod
    def nested_get(dictionary:dict, keys:list):
        for key in keys:
            dictionary = dictionary.get(key)
        return dictionary

class ExchangeSocket:
    def __init__(self, exchange_information:dict, currency_pair:str):
        self.endpoint = exchange_information['endpoint']
        self.exchange_id = exchange_information['exchange_id']
        self.exchange_name = exchange_information['exchange_name']
        self.response_map = exchange_information['reponse_map']
        self.currency_pair = currency_pair
        self.server_request = exchange_information['sub_request']
        self.gzip = exchange_information['gzip']
        self.consume()
    
    async def open_socket(self, ws):
        await ws.send(json.dumps(self.server_request))
    
    @staticmethod
    def on_ping(ws, message):
        print(f'Ping recieved from server {json.dumps(message)}')
    
    @staticmethod
    def on_pong(ws, message):
        print(f'Pong recieved from server {json.dumps(message)}, no need to respond')
    
    # Handles the responses from the server
    async def on_message(self, ws, message):
        
        # Decompress and deserialize 
        if self.gzip:
            result = json.loads(gzip.decompress(message))
        else:
            result = json.loads(message)
        
        # Send back pong to server, (as the ping was gzipped)
        if result.get('ping') != None:
            val = {'pong':result.get('ping')}
            ws.send(json.dumps(val))

        else:
            try:
                # Get values
                best_bid = float(Utils.nested_get(result, self.response_map['best_bid']))
                best_ask = float(Utils.nested_get(result, self.response_map['best_ask']))
                print(f'{self.exchange_name} {best_bid,best_ask}')

                try:
                    redis_client.add_to_sorted_list(exchange_id=self.exchange_id, \
                    currency_pair=self.currency_pair, best_bid=best_bid, best_ask=best_ask)
                except Exception as e: 
                    print(e)

            except:
                print(result)

    def consume(self):
        socket_app = websocket.WebSocketApp(self.endpoint, on_message=self.on_message, \
            on_ping=self.on_ping, on_pong= self.on_pong, on_open=self.open_socket)
        socket_app.run_forever()

if __name__ == '__main__':
    # Load environment varibles 
    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('REDIS_PORT')

    # Create redis client
    redis_client = RedisClient(redis_host=redis_host, redis_port=redis_port)

    # Start each exchange socket on a different daemon thread
    thread_list = []
    for _, socket in enumerate(exchange_sockets.XRPUSDT):
        thread = threading.Thread(target=ExchangeSocket, args=(socket, 'XRPUSDT'))
        thread_list.append(thread)
        thread.daemon = True
        thread.start()

    for index, thread in enumerate(thread_list):
        thread.join()