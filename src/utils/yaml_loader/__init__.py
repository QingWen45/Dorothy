#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/7 19:32
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import yaml
from pathlib import Path


def yml_loader(file: Path) -> dict:
    """
    读取一个yml文件
    :return: dict
    """
    with open(file, 'r', encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data
