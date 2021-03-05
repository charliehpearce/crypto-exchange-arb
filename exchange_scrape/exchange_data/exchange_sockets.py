XRPUSDT = [
{
    'exchange_id': 1,
    'exchange_name':'Binance',
    'endpoint': 'wss://stream.binance.com:9443/ws/xrpusdt@bookTicker',
    'sub_request': {
        "method": "SUBSCRIBE",
        "params": [
            "xrpusdt@bookTicker"
        ],
        "id":1
    },
    'reponse_map': {'best_bid':["b"], 'best_ask':["a"], "id":["u"]},
    'gzip': False
},
{
    'exchange_id': 2,
    'exchange_name':'Huobi',
    'endpoint': 'wss://api.huobi.pro/ws',
    'sub_request': {
        "sub": "market.xrpusdt.bbo",
        "id" : "id1"
    },
    'reponse_map': {'best_bid':["tick","bid"], 'best_ask':["tick","ask"], "id":["tick","seqId"]},
    'gzip': True
},

]

TEST = [
{
    'exchange_id': 3,
    'exchange_name':'Kraken',
    'endpoint': 'wss://ws.kraken.com/',
    'sub_request': {
        "event": "subscribe",
        "pair": ["XRP/USDT"],
        "subscription": {"name": "ticker"}
    },
    'reponse_map': {'best_bid':[1,"b",0], 'best_ask':[1,"a",0], "id":[3]},
    'gzip': False
}
]




"""
TEMPLATE:
{
    'exchange_id': ,
    'exchange_name':'',
    'endpoint': '',
    'sub_request': {

    },
    'reponse_map': {'best_bid':[], 'best_ask':[], "id":[]},
    'gzip': True/False
}
"""
