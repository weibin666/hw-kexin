# --*-- coding: utf-8 --*--
# @Software: PyCharm
# =======================
import json
import random
import re
import time
from urllib import parse
import execjs
import requests
from loguru import logger
import random
import hashlib

from flask import Flask, request, jsonify

app = Flask(__name__)


import urllib.parse

def encode(data):
    return "&".join(f"{urllib.parse.quote_plus(str(k))}={urllib.parse.quote_plus(str(v))}" for k, v in data.items())




def generate_number(length: int):
    number = "0"
    for _ in range(length - 1):
        digit = random.randint(0, 9)
        number += str(digit)
    return number


def get_bx_pp(params):
    assert params['l'] == 0, '暂不支持的类型'
    i = 0
    j = 0
    random_string = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", k=16))
    md5_string = '|'.join([str(params['l']), str(params['i']), params['q'], params['t'], params['f'], params['k'], '1', '1', '', random_string, '0'])
    md5_data = hashlib.md5(md5_string.encode()).hexdigest()
    return ':'.join(['xa', md5_data, md5_string, random_string, str(i), params['enc'], str(j)]).encode().hex()




with open("x82y.js", "r", encoding="utf-8") as f:
    fireyejs = execjs.compile(f.read())



class Ali231:
    def __init__(self):
        self.session = requests.Session()


        # 提取代理API接口，获取1个代理IP

        self.session.trust_env = False
        self.headers = {
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        }

    def get_etag(self):
        # return '12345678'
        try:
            response = self.session.get('https://ynuf.aliapp.org/w/wu.json', timeout=5)
            Etag = response.headers.get('ETag')
            if Etag is None or str(Etag) == "":
                raise Exception("获取Etag失败")
            else:
                return Etag
        except:
            return ''

    def get_x5secdata(self):
        url = "https://ditu.amap.com/detail/get/detail?id=B00155L3DH"
        response = self.session.get(url, headers=self.headers).text
        x5referer = re.findall('"url":"(.*?)"', response)[0]
        return x5referer

    def punish_info(self, config):
        # logger.info(x5referer_url)
        # response = self.session.get(x5referer_url, headers=self.headers).text
        # print(response)
        nc_app_key = config['NCAPPKEY']
        nc_token_str = config['NCTOKENSTR']
        sec_data = config['SECDATA']
        pp_info = config['pp']
        return nc_app_key, nc_token_str, sec_data, pp_info

    def initialize(self, nc_app_key, nc_token_str):
        url = "https://cf.aliyun.com/nocaptcha/initialize.jsonp"
        params = {
            "a": nc_app_key,
            "t": nc_token_str,
            "scene": "register",
            "lang": "cn",
            "v": "v1.3.21",
            "href": "https://ditu.amap.com/detail/get/detail",
            "comm": "\\{\\}",
            "callback": f"initializeJsonp_{generate_number(18)}"
        }
        response = self.session.get(url, headers=self.headers, params=params)
        logger.info(response.text)

    def info_report(self, x5secdata, nc_token_str):
        url = "https://ditu.amap.com/detail/get/detail/_____tmd_____/report"
        params = {
            "x5secdata": x5secdata,
            "type": "loadPageSuccess",
            "msg": "PunishPage load success",
            "uuid": nc_token_str,
            "v": str(random.random()).replace(".", "")
        }
        self.session.get(url, headers=self.headers, params=params)

    def verify(self, nc_app_key, nc_token_str, sec_data, ret):
        url = "https://ditu.amap.com/detail/get/detail/_____tmd_____/slide"
        p_str = json.dumps({
            "ncbtn": "701.6666870117188|532|41.333335876464844|29.33333396911621|532|561.3333339691162|701.6666870117188|743.0000228881836",
            "umidToken": self.umidToken,
            "ncSessionID": "5e701efcf769",
            "et": "1"
        }, separators=(",", ":"))
        params = {
            "slidedata": json.dumps({
                "a": nc_app_key,
                "t": nc_token_str,
                "n": ret,
                "p": p_str,
                "scene": "register",
                "asyn": 0,
                "lang": "cn",
                "v": 1
            }),
            "x5secdata": sec_data,
            "ppt": "0",
            "landscape": 1,
            "ts": str(int(time.time() * 1000)),
            "v": str(random.random()).replace(".", "")
        }
        params_string = parse.urlencode(params).replace("+", "").replace("%21", "!")
        # print(ret)
        self.headers.update({
            "Bx_et": "nosgn"
        })
 
        response = self.session.get(url, headers=self.headers, params=params)
        print(response.text)
        resp_data = response.json()
        if resp_data.get("code") == 300:
            logger.error(resp_data)
            return resp_data
        elif resp_data.get("code") != 0:
            logger.debug(resp_data)
            return resp_data
        else:
            logger.success(resp_data)
            logger.success(response.headers.get("bx-x5sec"))
            logger.success(response.cookies.get_dict()['x5sec'])
            return response.cookies.get_dict()

    def crawl(self, url, config, umidToken):
        self.umidToken = umidToken if umidToken else self.get_etag()

        self.headers["Referer"] = url
        nc_app_key, nc_token_str, sec_data, pp_info = self.punish_info(config)

        bx_pp = get_bx_pp(config['pp'])
        
        validateUrl = "https://" + config['HOST'].replace(':443', '') + config['PATH'] + '/_____tmd_____/slide'


        n = fireyejs.call("get_231_5")
        logger.debug(n)
        
        
        slidedata = {
            "a": nc_app_key,"t": nc_token_str, "n": n,
            "p": f'{{"ncbtn":"808|593|42|30|593|623|808|850","umidToken":"{self.umidToken}","ncSessionID":"5e701f1956fb","et":"1"}}',
            "scene": "register", "asyn": 0, "lang": "cn", "v": 1,
        }


        slidedata = json.dumps(slidedata).replace(' ', '')
        params = {
            'slidedata': slidedata, 'x5secdata': sec_data,
            'ppt': '1', 'landscape': '1', 'ts': str(int(time.time() * 1000)), 'v': random.randint(10000000000, 99999999999),
        }
        validateUrl = validateUrl + "?" + encode(params)

     
  
        return {'code': 200, 'data': {'bx_et': "nosgn", 'bx-pp': bx_pp, 'url': validateUrl, "referer": url.replace(':443', '')} , 'msg': 'success'}





# 定义一个简单的路由，只接受 POST 请求
@app.route('/', methods=['POST'])
def hello():
    # 获取 POST 请求中的 JSON 数据
    data = request.get_json()
    
    # 获取 config 参数，默认为空字典
    url = data.get('url')
    config = data.get('config')
    cookie = data.get('cookie')
    umidToken = data.get('umidToken')
    config = json.loads(config) if type(config) == str else config
    
    logger.info(url)
    
    # 实例化 Ali231 类并调用 crawl 方法
    ali = Ali231()
    res = ali.crawl(url, config, umidToken)
    
    # 返回结果
    return jsonify(res)

if __name__ == '__main__':
    app.run(threaded=True, host="0.0.0.0", port="9002")