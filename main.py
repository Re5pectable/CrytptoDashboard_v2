from config import PANCAKE_MAINNET, PANCAKE_FACTORY_MAINNET, BSC_MAINNET
import asyncio
import time
from utils.fill_data import get_liquidity_pools, get_tokens
from utils.db import DB

async def main():
    print("Begin")
    s = time.time()
    # await get_liquidity_pools()
    # print(await DB.get_all_pools())
    print(1)

    print("END:", round(time.time() - s, 3))

asyncio.run(main())