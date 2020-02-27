from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import requests
import urllib3.request
import time


def get_it(url):
    r = requests.get(url)
    print("request")
    return


urls = ["http://localhost:3000/?loc_name=Vaslui",
        "http://localhost:3000/?loc_name=Iasi",
        "http://localhost:3000/?loc_name=Botosani",
        "http://localhost:3000/?loc_name=Suceava",
        "http://localhost:3000/?loc_name=Cluj"] * 10

with PoolExecutor(max_workers=50) as executor:
    for _ in executor.map(get_it, urls):
        pass


