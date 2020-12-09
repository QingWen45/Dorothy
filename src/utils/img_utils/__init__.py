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

img_path = Path("./local_data/img").resolve()
compressed_path = Path("./local_data/compressed").resolve()


async def download_img(url: str) -> Path:
    if not img_path.exists():
        img_path.mkdir()
    name = ''.join(sample(string.ascii_letters + string.digits, 16))
    img_loc = Path(str(img_path) + f"/{name}.png")
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=60.0)
    with open(img_loc, "wb") as f:
        f.write(response.content)
    return img_loc


async def compress_img(img_loc: Path, kb=500, quality=80, k=0.9) -> str:
    if not compressed_path.exists():
        compressed_path.mkdir()
    img_size = os.path.getsize(img_loc) // 1024
    if img_size <= kb:
        return str(img_loc)
    img = Image.open(img_loc)
    name = img_loc.name
    out_loc = str(compressed_path) + f"{name}.png"

    while img_size > kb:
        x, y = img.size
        out = img.resize((int(x*k), int(y*k)), Image.ANTIALIAS)
        out.save(out_loc, quality=quality)
        img = Image.open(out_loc)
        img_size = os.path.getsize(out_loc) // 1024
    return out_loc
