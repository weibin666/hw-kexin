import requests
import json
import socks
import socket
#! /usr/bin/python
# coding=utf-8
import requests
import time

def get_proxy():
    res = requests.get("https://service.ipzan.com/core-extract?num=1&no=20240512326767842864&minute=1&format=json&pool=quality&mode=auth&secret=4tes3co25ogs3o")
    json_data = json.loads(res.text)
    if json_data["code"] == 0:
        ip = json_data["data"]["list"][0]["ip"]
        port = json_data["data"]["list"][0]["port"]
        account = json_data["data"]["list"][0]["account"]
        password = json_data["data"]["list"][0]["password"]
        return ip, int(port), account, password
    else:
        return None, None, None, None


if __name__ == '__main__':
    ip, port, account, password=get_proxy()
    print(ip, port, account, password)
    proxyMeta = f"http://{account}:{password}@{ip}:{port}"
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta
    }
    resp = requests.get("https://www.baidu.com", proxies=proxies, timeout=10, verify=False)
    print(resp.status_code)

