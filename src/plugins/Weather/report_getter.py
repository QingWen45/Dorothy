#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : report_getter.py
# @Time : 2020/12/8 21:31
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import httpx
from src.utils.yaml_loader import yml_loader
from pathlib import Path

YML = Path("D:/Dorothy/Dorothy/configs.yml")
api_config = yml_loader(YML)["hefeng"]
key = api_config["KEY"]


async def location_get(loc: list):
    """
    由原始名称获取地点
    """
    if not loc:
        return False

    location = {"key": key, "number": "1"}
    loc.reverse()
    for i, v in enumerate(loc):
        if i == 0:
            location["location"] = v
        elif i < 3:
            location[f"adm{i}"] = v
        else:
            return False

    async with httpx.AsyncClient() as client:
        r = await client.get(api_config["SEARCH_API"], params=location)
    r = r.json()
    if r["code"] == "200":
        first_loc = r["location"][0]
        name = first_loc["adm1"] + first_loc["adm2"] + first_loc["name"]
        loc_id = first_loc["id"]
        return [name, loc_id]
    else:
        return False


async def report_get(loc_id: str):
    """
    获取天气报告
    """
    location = {"key": key, "location": loc_id}
    async with httpx.AsyncClient() as client:
        air_r = await client.get(api_config["AIR_NOW_API"], params=location)
        wea_r = await client.get(api_config["WEATHER_NOW_API"], params=location)
    air_r = air_r.json()
    wea_r = wea_r.json()
    if wea_r["code"] == "200":
        tmp = wea_r["now"]
        wea_msg = "气温: " + tmp["temp"] + "\n体感温度: " + tmp["feelsLike"] + "\n天气:" + tmp["text"]
        if air_r["code"] == "200":
            air_msg = "\n污染指数: " + air_r["now"]["aqi"] + " " + air_r["now"]["category"]
            return wea_msg + air_msg
        else:
            return wea_msg

    else:
        return False



