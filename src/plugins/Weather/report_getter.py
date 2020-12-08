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
    location = {"key": key}
    loc.reverse()
    for i, v in enumerate(loc):
        location["location"] = v
        if i < 3:
            location[f"adm{i}"] = v
        else:
            return []
    print(location)
    async with httpx.AsyncClient() as client:
        r = await client.get(api_config["SEARCH_API"], params=location).json()
    if r["code"] == "200":
        first_loc = r["location"][0]
        name = first_loc["adm1"] + first_loc["adm2"] + first_loc["name"]
        loc_id = first_loc["id"]
        print([name, loc_id])
        return [name, loc_id]
    else:
        return []




