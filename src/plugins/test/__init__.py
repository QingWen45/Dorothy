#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/8 16:47
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

from nonebot.typing import Bot, Event
from nonebot.plugin import on_command

test = on_command("test")


@test.handle()
async def _(bot: Bot, event: Event, state: dict):
    msg = "[CQ:image,file=file:///D:/Pixel/Cup/Haze.png]"
    await test.finish(msg)

