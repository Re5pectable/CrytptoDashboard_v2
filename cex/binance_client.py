import httpx
from utils.functions import web2_client as asyncClient 
import pandas as pd

num_cols = ["highest_bid", "lowest_ask"]
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class BinanceClient:

    def __init__(self, generate_tokens_mapping=False):
        if generate_tokens_mapping:
            self.mapping_pairs = {}
            for pair in httpx.get('https://api.binance.com/api/v3/exchangeInfo').json()["symbols"]:
                self.mapping_pairs[pair["symbol"]] = {"topAsset": pair["baseAsset"],
                                            "lowAsset": pair["quoteAsset"]}


    async def get_tickers(self, endToken=None, split_pair_names=False):
        res = (await asyncClient.get("https://www.binance.com/api/v3/ticker/bookTicker")).json()

        if split_pair_names: 
            for d in res:
                try:
                    d["topAsset"] = self.mapping_pairs[d["symbol"]]["topAsset"]
                    d["lowAsset"] = self.mapping_pairs[d["symbol"]]["lowAsset"]
                except KeyError:
                    pass
            data = pd.DataFrame(res)[["symbol", "bidPrice", "askPrice", "topAsset", "lowAsset"]]
            data.columns = ["pair", "highest_bid", "lowest_ask", "topAsset", "lowAsset"]
        else:
            data = pd.DataFrame(res)[["symbol", "bidPrice", "askPrice"]]
            data.columns = ["pair", "highest_bid", "lowest_ask"]
        data[num_cols] = data[num_cols].apply(pd.to_numeric, axis=1)
        
        if endToken: return data.loc[data.pair.str.endswith(endToken)]
        else: return data
     

    async def get_token_networks(self, token, withdraw):
        res = (await asyncClient.get(f"https://www.binance.com/bapi/capital/v2/public/capital/config/getOne?coin={token.upper()}&lang=en")).json()["data"]
        networks = {"deposit": [], "withdraw": []}
        for r in res:
            if r["depositEnable"] == True:
                networks["deposit"].append(r["network"])
            if r["withdrawEnable"] == True:
                networks["withdraw"].append(r["network"]) 
        if withdraw:
            return networks["withdraw"]
        else:
            return networks["deposit"]
    

    async def get_order_book(self, ticker):
        return (await asyncClient.get("https://api.binance.com/api/v3/depth", params={"symbol": ticker})).json()