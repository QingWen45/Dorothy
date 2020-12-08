#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/8 20:03
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

from random import choice

from nonebot.typing import Bot, Event
from nonebot.plugin import on_command
from nonebot.log import logger

from src.utils.rules import is_banned
from .location_parser import location_parse
from .report_getter import location_get, report_get
from . import expression as e

weather = on_command("weather", aliases={"天气"}, rule=is_banned())


@weather.handle()
async def _(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        location = await location_parse(args)  # 如果用户发送了参数则直接赋值
        location_found = await location_get(location)
        if location_found:
            state["location"] = location_found
        else:
            await weather.finish("查找失败，请检查输入")


@weather.got("location", prompt=choice(e.WHERE))
async def _(bot: Bot, event: Event, state: dict):
    logger.info(state["location"][0])
    msg = await report_get(state["location"][1])
    if not msg:
        await weather.finish("连接出错，请重试")
    else:
        msg = state["location"][0] + ":\n" + msg
        await weather.finish(msg)


@weather.args_parser
async def _(bot: Bot, event: Event, state: dict):
    stripped_args = str(event.message).strip()
    if not stripped_args:
        return

    if state["_current_key"] == "location":
        location = await location_parse(stripped_args)
        location_found = await location_get(location)
        if location_found:
            state["location"] = location_found
        else:
            await weather.finish("查找失败，请检查输入")

