#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2021/1/17 19:42
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

def counter(l: list, elm) -> int:
    elm_sum = 0
    for i in l:
        if i == elm:
            elm_sum += 1
    return elm_sum
