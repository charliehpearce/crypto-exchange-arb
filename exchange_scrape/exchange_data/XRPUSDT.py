binance_XRPUSDT = {
    'exchange_id': 1,
    'endpoint': 'wss://stream.binance.com:9443/ws/xrpusdt@bookTicker',
    'sub_request': {
        "method": "SUBSCRIBE",
        "params": [
            "xrpusdt@bookTicker"
        ],
        "id":1
    },
    'reponse_map': {'best_bid':"b", 'best_ask':"a"}
}
