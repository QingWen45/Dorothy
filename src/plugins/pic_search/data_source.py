#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : data_source.py
# @Time : 2020/12/9 10:37
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import httpx
from pathlib import Path
from src.utils.yaml_loader import yml_loader

CONFIG_PATH = Path("./configs.yml")
configs = yml_loader(CONFIG_PATH)

sauce_api = configs["saucenao"]["API"]
sauce_key = configs["saucenao"]["KEY"]

data = {"api_key": sauce_key,
        "output_type": 2,
        "testmode": 0,
        "db": 5,
        "numres": 1}


async def result_get(user: str, img_url: str):
    data["url"] = img_url
    async with httpx.AsyncClient() as client:
        response = await client.get(sauce_api, params=data)
    response = response.json()["results"]
    if not response:
        return False
    else:
        response = response[0]
    print(response)

    if float(response["header"]["similarity"]) < 50:
        return "找不到",
    thumbnail = f"""[CQ:image,file={response["header"].get("thumbnail")}]"""
    msg = f"""[CQ:at,qq={user}]
SauceNAO Info:
相似度: {response["header"].get("similarity", 0)}
标题: {response["data"].get("title")}
Pixiv ID: {response["data"].get("pixiv_id")}
画师: {response["data"].get("member_name")}
画师ID: {response["data"].get("member_id")}"""
    return [msg, thumbnail]
