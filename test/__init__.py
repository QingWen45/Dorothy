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


