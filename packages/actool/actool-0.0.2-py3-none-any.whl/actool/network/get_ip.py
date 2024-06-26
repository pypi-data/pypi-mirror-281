import requests


def get_ip():
    url = "https://httpbin.org/ip"
    resp = requests.get(url=url)
    print(resp.json()["origin"])
