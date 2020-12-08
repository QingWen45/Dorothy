#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/8 16:47
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import httpx
from src.utils.yaml_loader import yml_loader
from pathlib import Path

YML = Path("D:/Dorothy/Dorothy/configs.yml")

search_url = "https://geoapi.qweather.com/v2/city/lookup?"
report_url = "https://devapi.qweather.com/v7/weather/now?"
air_url = "https://devapi.qweather.com/v7/air/now?"

key = "50bf6718eee8448f991f89f423e63afb"
form = {"key": key, "location": "朝阳", "adm1": "北京"}


resp = httpx.get(search_url, params=form)
js = resp.json()
print(js)
#city_id = js["location"][0]["id"]
#form2 = {"key": key, "location": city_id}
#resp = httpx.get(air_url, params=form2)
#print(resp.json())

#res = yml_loader(YML)
#print(res["hefeng"])

