from web3 import Web3
import time
from utils.functions import toChecksumAddress, to64Symbols, createRawTransaction
from dex.network import Network

class Swapper(Network):
    def __init__(self,
                router_contract: str,
                **kwargs):
        self.router_contract = toChecksumAddress(router_contract)
        super().__init__(**kwargs)

    
    async def swapExactETHForTokens(
        self,
        ETH_amount: float = 0,
        amountOutMin: int = 0,
        path: list = None,
        deadline: int = None,
        gas: int = None,
        gasPrice: int = None,
        nonce: int = None,
        ):
        s = time.time()
        data = [
             "0x7ff36ab5",
             to64Symbols(hex(amountOutMin)),
             to64Symbols("80"),
             to64Symbols(self.my_address),
             to64Symbols(hex(deadline)),
             to64Symbols(str(len(path)))
        ] + [to64Symbols(address) for address in path]
        txn = {
            "to": self.router_contract,
            "from": self.my_address,
            "value": Web3.toWei(ETH_amount, 'ether'),
            "gas": gas,
            "gasPrice": Web3.toWei(gasPrice, 'gwei'),
            "nonce": nonce,
            "data": "".join(data),
        }
        signed_trx = createRawTransaction(txn, self.my_key)
        # print(f"==== swapExactETHForTokens READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self._eth_sendRawTransaction(signed_trx)
        # print(f"==== swapExactETHForTokens FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
        return res

    
    async def swapExactTokensForETH(
        self,
        token_amountIn: int,
        amountOutMin: int,
        path: list,
        deadline: int,
        gas: int,
        gasPrice: int,
        nonce: int):
        s = time.time()
        data = [
             "0x18cbafe5",
             to64Symbols(hex(token_amountIn)),
             to64Symbols(hex(amountOutMin)),
             to64Symbols("a0"),
             to64Symbols(self.my_address),
             to64Symbols(hex(deadline)),
             to64Symbols(str(len(path)))
        ] + [to64Symbols(address) for address in path]
        txn = {
            "to": self.router_contract,
            "from": self.my_address,
            "value": 0,
            "gas": gas,
            "gasPrice": Web3.toWei(gasPrice, 'gwei'),
            "nonce": nonce,
            "data": "".join(data),
        }
        signed_trx = createRawTransaction(txn, self.my_key)
        # print(f"==== swapExactTokensForETH READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self._eth_sendRawTransaction(signed_trx)
        # print(f"==== swapExactTokensForETH FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
        return res


    async def swapExactTokensForTokens(
        self,
        token_amountIn: int,
        amountOutMin: int,
        path: list,
        deadline: int,
        gas: int,
        gasPrice: int,
        nonce: int):
        s = time.time()
        data = [
             "0x38ed1739",
             to64Symbols(hex(token_amountIn)),
             to64Symbols(hex(amountOutMin)),
             to64Symbols("a0"),
             to64Symbols(self.my_address),
             to64Symbols(hex(deadline)),
             to64Symbols(str(len(path)))
        ] + [to64Symbols(address) for address in path]
        txn = {
            "to": self.router_contract,
            "from": self.my_address,
            "value": 0,
            "gas": gas,
            "gasPrice": Web3.toWei(gasPrice, 'gwei'),
            "nonce": nonce,
            "data": "".join(data),
        }
        signed_trx = createRawTransaction(txn, self.my_key)
        # print(f"==== swapExactTokensForETH READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self._eth_sendRawTransaction(signed_trx)
        # print(f"==== swapExactTokensForETH FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
        return res


    async def approve(self, token_address: str, amount, gas: int, gasPrice: int, nonce: int):
        s = time.time()
        data = [
            "0x095ea7b3",
            to64Symbols(self.router_contract),
            "f"*64 if amount == 'all' else to64Symbols(hex(amount))
        ]
        txn = {
            "to": token_address,
            "from": self.my_address,
            "value": 0,
            "gas": gas,
            "gasPrice": Web3.toWei(gasPrice, 'gwei'),
            "nonce": nonce,
            "data": "".join(data)
        }
        signed_trx = createRawTransaction(txn, self.my_key)
        # print(f"==== approve READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self._eth_sendRawTransaction(signed_trx)
        # print(f"==== approve FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
        return res


    async def getRawAmountsOut(self, amountsIn: int, path: list):
        s = time.time()
        data = [
             "0xd06ca61f",
             to64Symbols(hex(amountsIn)),
             to64Symbols("40"),
             to64Symbols(str(len(path)))
        ] + [to64Symbols(address) for address in path]
        params = [
            {
                "from": "0x0000000000000000000000000000000000000000",
                "to": self.router_contract,
                "data": "".join(data)
            },
            "latest"
        ]
        # print(f"==== getAmountsOut READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self._eth_call(params)
        # print(f"==== getAmountsOut FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
        return int(res['result'][-64:], 16)


    async def getRawAmountsIn(self, amountsOut: int, path: list):
        s = time.time()
        data = [
             "0x1f00ca74",
             to64Symbols(hex(amountsOut)),
             to64Symbols("40"),
             to64Symbols(str(len(path)))
        ] + [to64Symbols(address) for address in path]
        params = [
            {
                "from": "0x0000000000000000000000000000000000000000",
                "to": self.router_contract,
                "data": "".join(data)
            },
            "latest"
        ]
        # print(f"==== getRawAmountsIn READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self._eth_call(params)
        # print(f"==== getRawAmountsIn FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
        return int(res['result'][-64:], 16)
        

class Factory(Network):
    def __init__(self,
                factory_contract: str,
                **kwargs):
        self.factory_contract = factory_contract
        super().__init__(**kwargs)

    async def getAllPairsLength(self):
        s = time.time()
        data = "0x574f2ba3"
        params = [{
            "from": "0x0000000000000000000000000000000000000000",
            "to": self.factory_contract,
            "data": data
        }, "latest"]
        # print(f"==== getAllPairsLength READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self._eth_call(params)
        # print(f"==== getAllPairsLength FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
        return int(res['result'], 0)

    async def getContractOfPair(self, id: int) -> str:
        s = time.time()
        data = "0x1e3dd18b" + to64Symbols(hex(id))
        params = [{
            "from": "0x0000000000000000000000000000000000000000",
            "to": self.factory_contract,
            "data": data
        }, "latest"]
        # print(f"==== allPairs READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self._eth_call(params)
        # print(f"==== allPairs FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
        return "0x" + res['result'][-40:]

    async def getInPairContractToken0(self, pair_contract) -> str:
        s = time.time()
        data = "0x0dfe1681"
        params = [{
            "from": "0x0000000000000000000000000000000000000000",
            "to": pair_contract,
            "data": data
        }, "latest"]
        # print(f"==== token0 READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self._eth_call(params)
        # print(f"==== token0 FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
        return "0x" + res['result'][-40:]


    async def getInPairContractToken1(self, pair_contract) -> str:
        s = time.time()
        data = "0xd21220a7"
        params = [{
            "from": "0x0000000000000000000000000000000000000000",
            "to": pair_contract,
            "data": data
        }, "latest"]
        # print(f"==== token1 READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self._eth_call(params)
        # print(f"==== token1 FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
        return "0x" + res['result'][-40:]

    async def getReserves(self, pair_contract):
        s = time.time()
        data = "0x0902f1ac"
        params = [{
            "from": "0x0000000000000000000000000000000000000000",
            "to": pair_contract,
            "data": data
        }, "latest"]
        # print(f"==== getReserves READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self._eth_call(params)
        # print(f"==== getReserves FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
        return int(res['result'][2:][:64], 16), int(res['result'][2:][64:128], 16)
