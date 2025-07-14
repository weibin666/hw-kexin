# -*- coding: utf-8 -*-
import re
import time
from loguru import logger
import requests
import json


def verify(url=None):

    global num, s
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    }
    # 禁用代理
    proxies = {
        "http": None,
        "https": None
    }

    response = requests.get(url, headers=headers, proxies=proxies)
    res = (
        response.text.replace("\n", "")
        .replace("\r", "")
        .replace("\t", "")
        .replace(" ", "")
    )

    script = re.findall("<script>window._config_=(.*?);</script>", res)[0]
    config = json.loads(script)

    json_data = {
        "url": url,
        "config": config,
    }

    t1 = time.time()
    response = requests.post("http://127.0.0.1:9002", json=json_data, headers=headers, proxies=proxies)
    # print(response.text)
    logger.info(f"响应耗时 => {float(time.time() - t1)} s")
    if response.status_code == 200:
        logger.info(f"服务器接口响应 => {response.json()}")
        action = config["action"]
        logger.info(f"滑块类型: {action}")
        headers["bx_et"] = response.json()["data"]["bx_et"]
        headers["bx-pp"] = response.json()["data"]["bx-pp"]
        headers["referer"] = response.json()["data"]["referer"]
        url = response.json()["data"]["url"]
        time.sleep(0.5)
        response = requests.get(url, headers=headers, proxies=proxies)
        x5sec = response.cookies.get("x5sec")
        logger.info(f"滑块响应 => {response.json()}")
        if x5sec:
            logger.info(f"x5sec => {x5sec}")
        s += 1
        if x5sec:
            num += 1
        logger.info(f"目前成功率 {num / s * 100} %, {num}/{s}")
        return response.cookies.get("x5sec")


num = 0
s = 0
while True:

    # 滑动
    url = "https://ditu.amap.com/detail/get/detail?id=B00155L3DH"


    x5sec = verify(url)
