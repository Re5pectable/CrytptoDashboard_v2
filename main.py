from swapper import Swapper
from network import Network
import json
import time
import asyncio

wallets = json.load(open("static/wallets.json"))
bsc_config = json.load(open("static/BSC/config.json"))

# BSC_TESTNET = Network(
#     net_url=bsc_config['testnet']['net_url'],
#     tokens_mapping=None,
#     my_address=wallets[0]['address'],
#     my_key=wallets[0]['secret']
# )

PANCAKE_TESTNET = Swapper(
    # abi=json.load(open("static/BSC/pancake_abi.json")),
    abi={},
    router_contract=bsc_config['testnet']['pancake_router'],
    net_url=bsc_config['testnet']['net_url'],
    tokens_mapping=None,
    my_address=wallets[0]['address'],
    my_key=wallets[0]['secret']
)

BUSD = "0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7"
USDT = "0x7ef95a0FEE0Dd31b22626fA2e10Ee6A223F8a684"
WBNB = "0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd"

async def test():
    res = await PANCAKE_TESTNET.getAmountsOut(100000000000000, [BUSD, WBNB])
    print(res)

asyncio.run(test())
