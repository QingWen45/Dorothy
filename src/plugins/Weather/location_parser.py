#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : location_parser.py
# @Time : 2020/12/8 20:57
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import jieba_fast
from typing import List, Union


async def location_parse(word: Union[str, List[str]]) -> list:
    """
    构建用于api的地点字符串列表
    """
    if not word:
        return []
    if isinstance(word, str):
        loc = jieba_fast.lcut(word)
    else:
        loc = word

    location = []
    for i in loc:
        location.append(i.strip('省市区县'))
    return location


