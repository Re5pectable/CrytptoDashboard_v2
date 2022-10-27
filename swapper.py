from web3 import Web3
import time
from services import toChecksumAddress, to_64_symbols, createRawTransaction
from network import Network

class Swapper(Network):
    def __init__(self,
                abi: dict,
                router_contract: str,
                **kwargs):
        
        self.abi = abi
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
             to_64_symbols(hex(amountOutMin)),
             to_64_symbols("80"),
             to_64_symbols(self.my_address),
             to_64_symbols(hex(deadline)),
             to_64_symbols(str(len(path)))
        ] + [to_64_symbols(address) for address in path]
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
        print(f"==== swapExactETHForTokens READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self.eth_sendRawTransaction(signed_trx)
        print(f"==== swapExactETHForTokens FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
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
             to_64_symbols(hex(token_amountIn)),
             to_64_symbols(hex(amountOutMin)),
             to_64_symbols("a0"),
             to_64_symbols(self.my_address),
             to_64_symbols(hex(deadline)),
             to_64_symbols(str(len(path)))
        ] + [to_64_symbols(address) for address in path]
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
        print(f"==== swapExactTokensForETH READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self.eth_sendRawTransaction(signed_trx)
        print(f"==== swapExactTokensForETH FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
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
             to_64_symbols(hex(token_amountIn)),
             to_64_symbols(hex(amountOutMin)),
             to_64_symbols("a0"),
             to_64_symbols(self.my_address),
             to_64_symbols(hex(deadline)),
             to_64_symbols(str(len(path)))
        ] + [to_64_symbols(address) for address in path]
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
        print(f"==== swapExactTokensForETH READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self.eth_sendRawTransaction(signed_trx)
        print(f"==== swapExactTokensForETH FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
        return res


    async def approve(self, token_address: str, amount, gas: int, gasPrice: int, nonce: int):
        s = time.time()
        data = [
            "0x095ea7b3",
            to_64_symbols(self.router_contract),
            "f"*64 if amount == 'all' else to_64_symbols(hex(amount))
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
        print(f"==== approve READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self.eth_sendRawTransaction(signed_trx)
        print(f"==== approve FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
        return res

    async def getAmountsOut(self, amountsIn: int, path: list):
        s = time.time()
        data = [
             "0xd06ca61f",
             to_64_symbols(hex(amountsIn)),
             to_64_symbols("40"),
             to_64_symbols(str(len(path)))
        ] + [to_64_symbols(address) for address in path]
        params = [
            {
                "from": "0x0000000000000000000000000000000000000000",
                "to": self.router_contract,
                "data": "".join(data)
            },
            "latest"
        ]
        print(f"==== getAmountsOut READY TO SEND     {round(time.time() - s, 3)} s.")
        res = await self.eth_call(params)
        print(f"==== getAmountsOut FINISHED IN TOTAL {round(time.time() - s, 3)} s.")
        return int(res['result'][-64:], 16)
        

