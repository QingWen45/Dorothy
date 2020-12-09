#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/9 19:21
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import os
from pathlib import Path
import httpx
from random import sample
import string
from PIL import Image


async def download_img(url: str) -> str:
    img_path = Path("./local_data").resolve()
    if not img_path.exists():
        img_path.mkdir()
    name = ''.join(sample(string.ascii_letters + string.digits, 16))
    img_loc = Path(str(img_path) + f"/{name}.png")
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=60.0)
    with open(img_loc, "wb") as f:
        f.write(response.content)
    return img_loc


async def compress_img(img_loc: str, kb=500, quality=80, k=0.9) -> str:
    img_size = os.path.getsize(img_loc) // 1024
    if img_size <= kb:
        return img_loc
    out_loc = ""
    while img_size > kb:
        img = Image.open(img_loc)
        x, y = img.size
        out = img.resize((int(x*k), int(y*k)), Image.ANTIALIAS)
        print(img_loc)
        out_loc = img_loc.replace(".png", "_c.png")
        out.save(out_loc, quality=quality)
        img_size = os.path.getsize(out_loc) // 1024
    return out_loc
