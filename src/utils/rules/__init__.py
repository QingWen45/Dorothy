#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/7 15:07
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import ujson
from pathlib import Path

from nonebot.rule import Rule
from nonebot.typing import Bot, Event


def is_banned() -> Rule:
    """
    检查当前用户是否属于违禁用户。
    :return: Rule
    """
    async def _is_banned(bot: Bot, event: Event, state: dict) -> bool:
        user = str(event.user_id)
        BAN_LIST_FILE = Path("./src/utils/ban/ban_list.json")
        # 如果文件不存在，则创建一个空文件
        if not BAN_LIST_FILE.is_file():
            with open(BAN_LIST_FILE, 'w') as f:
                ujson.dump({}, f)
        # 检查该用户是否在已封禁用户内
        with open(BAN_LIST_FILE, 'r') as f:
            data = ujson.load(f)
        return user not in data
    return Rule(_is_banned)
