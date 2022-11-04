from config import PANCAKE_MAINNET, PANCAKE_FACTORY_MAINNET, BSC_MAINNET
import asyncio
import time
# from utils.fill_data import get_liquidity_pools, get_tokens
# from utils.db import DB
from services.sniper import sniper
from dex.swapper import SwapDetails
from utils.functions import get_abi

swapBUSDtoWBNB = SwapDetails(
    token_amountIn=0.06 * (10 ** 18),
    amountOutMin=0,
    path=["0xe9e7cea3dedca5984780bafc599bd69add087d56", '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'],
    deadline=int(time.time()) + 1000,
    gas=200000,
    gasPrice=5
)

swapWBNBtoBUSD = SwapDetails(
    token_amountIn=0.09 * (10 ** 18),
    amountOutMin=0,
    path=['0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c', "0xe9e7cea3dedca5984780bafc599bd69add087d56"],
    deadline=int(time.time()) + 1000,
    gas=200000,
    gasPrice=5
)

async def main():
    print("Begin")
    # nonce = await PANCAKE_MAINNET.getNonce(PANCAKE_MAINNET.my_address)
    s = time.time()
    # res = await PANCAKE_MAINNET.test_swapExactTokensForTokens(**swapBUSDtoWBNB.dict())
    # print(res)
    
    res = await get_abi("0xe9e7cea3dedca5984780bafc599bd69add087d56")
    print("END:", round(time.time() - s, 3))

asyncio.run(main())