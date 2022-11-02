from bs4 import BeautifulSoup
import requests
import json
import time

def get_token_url(slug: str):
    return f"https://coinmarketcap.com/currencies/{slug}/"

res = requests.get("https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=2000&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,self_reported_circulating_supply,self_reported_market_cap,total_supply,volume_7d,volume_30d&tagSlugs=bnb-chain")
data = res.json()['data']['cryptoCurrencyList']

contracts = {}

for token in data:
    s = time.time()
    content = requests.get(get_token_url(token['slug']))
    soup = BeautifulSoup(content.content, "html.parser").find("body")
    a_s = soup.find_all("a", {"class": 'cmc-link'})
    for a in a_s:
        try:
            if a["href"].startswith("https://bscscan.com/token/"):
                contracts[token['symbol']] = a['href'][26:]
                break
        except:
            pass
    print(time.time() - s)

with open("bsc_contracts_cmc.json", "w") as f:
    json.dump(contracts, f)