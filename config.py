import sys
from dex.swapper import Swapper, Factory
from dex.network import Network
import json
from cex.binance_client import BinanceClient


APP_PATH = sys.path[0] 
wallets = json.load(open(APP_PATH + "/static/wallets.json"))


# ----------- CEX -------------

BINANCE = BinanceClient(generate_tokens_mapping=True)


# ----------- DEX -------------

# ========= Testnet ===========

test_config = json.load(open(APP_PATH + "/static/BSC/testnet/config.json"))

BSC_TESTNET = Network(
    net_url=test_config['net_url'],
    tokens_mapping=None,
    my_address=wallets[0]['address'],
    my_key=wallets[0]['secret'])

PANCAKE_TESTNET = Swapper(
    router_contract=test_config['router_contract'],
    **BSC_TESTNET.__dict__)


# ========= Mainnet ============

main_config = json.load(open(APP_PATH + "/static/BSC/mainnet/config.json"))

BSC_MAINNET = Network(
    net_url=main_config['net_url'],
    tokens_mapping=None,
    my_address=wallets[0]['address'],
    my_key=wallets[0]['secret'])

PANCAKE_MAINNET = Swapper(
    router_contract=main_config['router_contract'],
    **BSC_MAINNET.__dict__)

PANCAKE_FACTORY_MAINNET = Factory(
    factory_contract=main_config['factory_contract'],
    **BSC_MAINNET.__dict__)
