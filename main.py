from clients import BINANCE, PANCAKE_MAINNET, PANCAKE_FACTORY_MAINNET, BSC_MAINNET
import asyncio
import time

async def main():
    res = await PANCAKE_FACTORY_MAINNET.getAllPairsLength()
    print(res)

asyncio.run(main())