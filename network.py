import json
from services import eth_headers, to_64_symbols, toChecksumAddress, web2_client

class Network:
    def __init__(
                self,
                net_url: str,
                tokens_mapping: dict,
                my_address: str,
                my_key: str):

        self.net_url = net_url
        self.tokens_mapping = tokens_mapping
        self.my_address = toChecksumAddress(my_address)
        self.my_key = my_key


    async def eth_sendRawTransaction(self, data: str, _id: int = 1):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_sendRawTransaction",
            "params": [data],
            "id": _id
        }
        res = await web2_client.post(self.net_url, headers=eth_headers, data=json.dumps(payload))
        return json.loads(res.content.decode())


    async def eth_call(self, params: list, _id=1):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_call",
            "params": params,
            "id": _id
        }
        res = await web2_client.post(self.net_url, headers=eth_headers, data=json.dumps(payload))
        return  json.loads(res.content.decode())


    async def getNonce(self, address: str, _id=1):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getTransactionCount",
            "params": [address, "latest"],
            "id": _id
        }
        res = await web2_client.post(self.net_url, headers=eth_headers, data=json.dumps(payload))
        return int(res['result'], 0)


    async def getBalance(self, address: str, _id=1):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBalance",
            "params": [address, "latest"],
            "id": _id
        }
        res = await web2_client.post(self.net_url, headers=eth_headers, data=json.dumps(payload))
        return int(res['result'], 0) / (10 ** 18)


    async def getRawTokenBalance(self, token_contract: str, address: str):
        params = [{
            "to": token_contract,
            "from": "0x0000000000000000000000000000000000000000",
            "data": "0x70a08231" + to_64_symbols(address), # balanceOf
        }, 'latest']
        res = await self.eth_call(params)
        return int(res['result'], 0)