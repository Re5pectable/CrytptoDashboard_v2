from utils.db import DB, Token, LiquidityPool
from config import PANCAKE_FACTORY_MAINNET
import asyncio
import json
from config import APP_PATH


# ======= Liquidity ========

async def _get_one_lp(id: int):
    pool_contract = await PANCAKE_FACTORY_MAINNET.getContractOfPair(id)
    tokens = await asyncio.gather(*[PANCAKE_FACTORY_MAINNET.getInPairContractToken0(pool_contract),
                                    PANCAKE_FACTORY_MAINNET.getInPairContractToken1(pool_contract)])
    await DB.add_liquidity_pool(LiquidityPool(
        pool_contract=pool_contract,
        token0_contract=tokens[0],
        token1_contract=tokens[1]
    ))

async def get_liquidity_pools():
    await asyncio.gather(*[_get_one_lp(i) for i in range(4000, 5000)])


# ======= Tokens ========

async def _get_one_token(contract: str):
    info = await asyncio.gather(*[
        PANCAKE_FACTORY_MAINNET.getSymbol(contract),
        PANCAKE_FACTORY_MAINNET.getDecimals(contract),
    ])
    await DB.add_token(Token(
        contract=contract,
        symbol=info[0],
        decimals=info[1],
        veryfied=True
    ), ignore_dublicates=True)

async def get_tokens():
    tokens = json.load(open(APP_PATH + '/static/BSC/mainnet/tokens_cmc.json'))
    await asyncio.gather(*[
        _get_one_token(contract) for contract in list(tokens.values())
    ])

