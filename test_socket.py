from websocket import create_connection
ws = create_connection('wss://stream.binance.com:9443/ws/xrpusdt@bookTicker')
"""
binance_sub_request = json.dumps({
        "method": "SUBSCRIBE",
        "params": [
            "xrpusdt@bookTicker"
        ],
        "id":1
    })
"""
result = ws.recv()
ws.close()