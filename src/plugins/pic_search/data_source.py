#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : data_source.py
# @Time : 2020/12/9 10:37
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import httpx
from pathlib import Path
from src.utils.yaml_loader import yml_loader
from src.utils.img_utils import compress_img, download_img

CONFIG_PATH = Path("./configs.yml")
configs = yml_loader(CONFIG_PATH)

sauce_api = configs["saucenao"]["API"]
sauce_key = configs["saucenao"]["KEY"]


async def result_get(user: str, img_url: str):
    data = {"api_key": sauce_key, "output_type": 2, "testmode": 0, "db": 5, "numres": 1, "url": img_url}
    async with httpx.AsyncClient() as client:
        response = await client.get(sauce_api, params=data)
    response = response.json()["results"]
    if not response:
        return False
    else:
        response = response[0]

    if float(response["header"]["similarity"]) < 60:
        return f"[CQ:at,qq={user}]\n找不到",
    thumbnail = f"""[CQ:image,file={response["header"].get("thumbnail")}]"""
    msg = f"""[CQ:at,qq={user}]
SauceNAO Info:
相似度: {response["header"].get("similarity", 0)}
标题: {response["data"].get("title")}
Pixiv ID: {response["data"].get("pixiv_id")}
画师: {response["data"].get("member_name")}
画师ID: {response["data"].get("member_id")}"""
    return [msg, thumbnail]


setu_api = configs["setu"]["API"]
setu_key = configs["setu"]["KEY"]


async def setu_linker(keyword=None, mode=0):
    data = {"apikey": setu_key,
            "r18": mode,
            "num": 1,
            "size1200": "true"}
    if keyword:
        data["keyword"] = keyword
    try:
        print(data)
        async with httpx.AsyncClient() as client:
            response = await client.get(setu_api, params=data, timeout=60.0)
        response = response.json()
        print(response)
        if response["code"] != 0:
            return ""
        if response["quota"] < 20:
            return "冲得太多，额度已经用光了"
        img_data = response["data"][0]
        img_loc = await download_img(img_data["pid"], img_data["url"])
        img_loc = await compress_img(img_loc)
        msg = f"""SETU Info:
标题: {img_data["title"]}
Pid: {img_data["pid"]}
[CQ:image,file=file:///{img_loc}]"""
        return msg
    except Exception:
        return ""
