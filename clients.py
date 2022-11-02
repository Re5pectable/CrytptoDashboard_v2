from dex.swapper import Swapper, Factory
from dex.network import Network
import json
from cex.binance_client import BinanceClient

BINANCE = BinanceClient(generate_tokens_mapping=True)


wallets = json.load(open("static/wallets.json"))


# ========= Testnet ============

BSC_TESTNET = Network(
    net_url=json.load(open("static/BSC/testnet/config.json"))['net_url'],
    tokens_mapping=None,
    my_address=wallets[0]['address'],
    my_key=wallets[0]['secret'])

PANCAKE_TESTNET = Swapper(
    router_contract=json.load(open("static/BSC/testnet/config.json"))['router_contract'],
    **BSC_TESTNET.__dict__)


# ========= Mainnet ============

BSC_MAINNET = Network(
    net_url=json.load(open("static/BSC/mainnet/config.json"))['net_url'],
    tokens_mapping=None,
    my_address=wallets[0]['address'],
    my_key=wallets[0]['secret'])

PANCAKE_MAINNET = Swapper(
    router_contract=json.load(open("static/BSC/mainnet/config.json"))['router_contract'],
    **BSC_MAINNET.__dict__)

PANCAKE_FACTORY_MAINNET = Factory(
    factory_contract="0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73",
    **BSC_MAINNET.__dict__
)
