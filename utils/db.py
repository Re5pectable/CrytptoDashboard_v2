import aiosqlite
from pydantic import BaseModel
from sqlite3 import IntegrityError
from config import APP_PATH

CREATE_TABLE_LIQUIDITY_POOLS =  '''
    create table if not exists liquidity_pools (
    id integer primary key autoincrement,
    pool_contract varchar(64) unique,
    token0_contract varchar(64),
    token1_contract varchar(64));
'''

DROP_TABLE_LIQUIDITY_POOLS = '''
    drop table if exists liquidity_pools;
'''

CREATE_TABLE_TOKENS = '''
    create table if not exists tokens (
    id integer primary key autoincrement,
    contract varchar(64) unique,
    symbol varchar(32),
    decimals integer,
    veryfied tinyint(1));
'''

DROP_TABLE_TOKENS = '''
    drop table if exists tokens;
'''

create_cmd = [CREATE_TABLE_TOKENS, CREATE_TABLE_LIQUIDITY_POOLS]
drop_cmd = [DROP_TABLE_TOKENS, DROP_TABLE_LIQUIDITY_POOLS]


class Token(BaseModel):
    contract: str
    symbol: str
    decimals: int
    veryfied: bool = None

    def to_db_add(self):
        return f"'{self.contract}', '{self.symbol}', {self.decimals}, {self.veryfied}"


class LiquidityPool(BaseModel):
    pool_contract: str
    token0_contract: str
    token1_contract: str

    def to_db_add(self):
        return f"'{self.pool_contract}', '{self.token0_contract}', '{self.token1_contract}'"


class DB:
    db_name = APP_PATH + '/database.sqlite'

    @staticmethod
    async def initialize(recreate=False):
        async with aiosqlite.connect(DB.db_name) as db:
            if recreate:
                for cmd in drop_cmd:
                    await db.execute(cmd)
            
            for cmd in create_cmd:
                await db.execute(cmd)

            await db.commit()


    @staticmethod
    async def add_token(token: Token, ignore_dublicates: bool = True):
        async with aiosqlite.connect(DB.db_name) as db:
            if ignore_dublicates:
                try:
                    await db.execute(f'insert into tokens (contract, symbol, decimals, veryfied) values ({token.to_db_add()})')
                except IntegrityError:
                    pass
            else:
                await db.execute(f'insert into tokens (contract, symbol, decimals, veryfied) values ({token.to_db_add()})')

            await db.commit()

    @staticmethod
    async def add_liquidity_pool(lp: LiquidityPool, ignore_dublicates: bool = True):
        async with aiosqlite.connect(DB.db_name) as db:
            if ignore_dublicates:
                try:
                    await db.execute(f'insert into liquidity_pools (pool_contract, token0_contract, token1_contract) values ({lp.to_db_add()})')
                except IntegrityError:
                    pass
            else:
                await db.execute(f'insert into liquidity_pools (pool_contract, token0_contract, token1_contract) values ({lp.to_db_add()})')
            await db.commit()

    @staticmethod
    async def get_all_pools():
        async with aiosqlite.connect(DB.db_name) as db:
            res = await db.execute_fetchall(
                '''
                select * from liquidity_pools
                join tokens on liquidity_pools.token0_contract=tokens.contract
                join tokens on liquidity_pools.token1_contract=tokens.contract
                '''
            )
            return res

    
        


