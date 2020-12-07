#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/7 20:06
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

def counter(l: list, elm) -> int:
    """
    检查元素出现次数
    """
    elm_sum = 0
    for i in l:
        if i == elm:
            elm_sum += 1
    return elm_sum
