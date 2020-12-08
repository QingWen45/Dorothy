#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/8 20:03
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

from nonebot.typing import Bot, Event
from nonebot.plugin import on_command

from src.utils.rules import is_banned
from src.plugins.Weather.location_parser import location_parse
from src.plugins.Weather.report_getter import location_get
from . import expression as e

weather = on_command("weather", aliases={"天气"}, rule=is_banned())


@weather.got("location", prompt=e.WHERE)
async def _(bot: Bot, event: Event, state: dict):
    await weather.finish(state["city"] + "is got")


@weather.args_parser
async def _(bot: Bot, event: Event, state: dict):
    stripped_args = str(event.message).strip()
    if not stripped_args:
        return

    if state["_current_key"] == "location":
        location = await location_parse(stripped_args)
        location_found = await location_get(location)
        state["location"] = location_found[1]
        await weather.finish(state["location"])

