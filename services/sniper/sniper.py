from config import PANCAKE_MAINNET, PANCAKE_FACTORY_MAINNET
import asyncio
import time

async def gather_info(id: int):
    s = time.time()
    pool_contract = await PANCAKE_FACTORY_MAINNET.getContractOfPair(id)
    reserves, token0, token1 = await asyncio.gather(*[
        PANCAKE_FACTORY_MAINNET.getReserves(pool_contract),
        PANCAKE_FACTORY_MAINNET.getInPairContractToken0(pool_contract),
        PANCAKE_FACTORY_MAINNET.getInPairContractToken1(pool_contract)
    ])
    token0_symbol, token0_decimals, token1_symbol, token1_decimals = await asyncio.gather(*[
        PANCAKE_FACTORY_MAINNET.getSymbol(token0),
        PANCAKE_FACTORY_MAINNET.getDecimals(token0),
        PANCAKE_FACTORY_MAINNET.getSymbol(token1),
        PANCAKE_FACTORY_MAINNET.getDecimals(token1),
    ])
    print(
        f'''

        New LP. {token0_symbol}/{token1_symbol}
        Pool: {reserves}
        ------------
        Token0: {token0_symbol}, decimals: {token0_decimals}, contract: {token0}
        Token1: {token1_symbol}, decimals: {token1_decimals}, contract: {token1}
        ------------
        Done in {round(time.time() - s, 3)} sec

         '''
    )


async def main():
    old_n_pools = await PANCAKE_FACTORY_MAINNET.getAllPairsLength()
    while True:
        n_pools = await PANCAKE_FACTORY_MAINNET.getAllPairsLength()
        if n_pools > old_n_pools:
            await asyncio.gather(*[gather_info(id) for id in range(old_n_pools, n_pools)])
        old_n_pools = n_pools
        # print(n_pools)
        await asyncio.sleep(60)