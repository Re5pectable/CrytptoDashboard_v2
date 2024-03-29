from web3 import Web3
import json
import httpx

eth_headers = {"Content-Type": "application/json"}

web2_client = httpx.AsyncClient()
web3 = Web3()


_createRawTransaction = web3.eth.account.sign_transaction
def createRawTransaction(txn_data, secret):
    return _createRawTransaction(txn_data, private_key=secret).rawTransaction.hex()


_toChecksumAddress = web3.toChecksumAddress
def toChecksumAddress(address: str):
    return _toChecksumAddress(address)


def to64Symbols(value: str, n=64):
        if value.startswith('0x'):
            value = value[2:]
        return '0' * (n-len(value)) + value


def decodeResponse(httpResponse):
    return json.loads(httpResponse.content.decode())


async def get_abi(contract: str):
    link = f"https://api.bscscan.com/api?module=contract&action=getabi&address={contract}"
    res = await web2_client.get(link)
    try:
        return json.loads(res.json()['result'])
    except json.decoder.JSONDecodeError:
        return None
