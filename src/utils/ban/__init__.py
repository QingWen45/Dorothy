#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/7 14:31
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import ujson
from pathlib import Path

BAN_LIST_FILE = Path("./src/utils/ban/ban_list.json")
# 如果文件不存在，则创建一个空文件
if not BAN_LIST_FILE.is_file():
    with open(BAN_LIST_FILE, 'w') as f:
        ujson.dump({}, f)

with open(BAN_LIST_FILE, 'r') as f:
    data = ujson.load(f)


def ban(user: str):
    """
    封禁某个用户
    :param user: str
    :return: none
    """
    data[user] = user
    with open(BAN_LIST_FILE, 'w') as file:
        ujson.dump(data, file)


def unban(user: str):
    """
    解除某个用户的封禁状态
    :param user: str
    :return: none
    """
    del data[user]
    with open(BAN_LIST_FILE, 'w') as file:
        ujson.dump(data, file)
