#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/8 16:47
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import httpx
from pathlib import Path
from src.utils.yaml_loader import yml_loader

YML = Path("D:/Dorothy/Dorothy/configs.yml")
config = yml_loader(YML)

data = {"apikey": config["setu"]["KEY"],
        "r18": 1,
        "num": 1,
        "size1200": True}

response = httpx.get(config["setu"]["API"], params=data)
print(response.json())
#path = Path("D:/IDE/1.jpg")
#img = httpx.get("https://i.pixiv.cat/img-original/img/2020/06/20/00/58/02/82433685_p0.jpg")
#with open(path, "wb") as f:
    #f.write(img.content)
