import os, json
import requests

with open("test_res.json", "r", encoding="utf-8") as fr:
    lines = fr.readlines()
    for line in lines:
        line = json.loads(line)
        print(line)
        res=requests.post(line["url"],data=line["post_data"],headers=line["headers"])
        print(res.status_code)
        print(res.text)
        # break
        # p=Pool()

