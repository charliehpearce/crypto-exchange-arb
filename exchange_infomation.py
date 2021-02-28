binance = {
    'xrpusdt': {
        'endpoint': 'wss://stream.binance.com:9443/ws/xrpusdt@bookTicker',
        'sub_request': {
            "method": "SUBSCRIBE",
            "params": [
                "xrpusdt@bookTicker"
            ],
            "id":1
        }
    }
}
