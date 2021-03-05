def nested_get(dictionary:dict, keys:list):
    for key in keys:
        dictionary = dictionary.get(key)
    return dictionary

dictionary = {"ch":"market.xrpusdt.bbo","ts":1614879228646,"tick":{"seqId":106537609258,"ask":0.47543,"askSize":20290.53,"bid":0.47538,"bidSize":55.44,"quoteTime":1614879228646,"symbol":"xrpusdt"}}

print(nested_get(dictionary, ["tick",'bid']))