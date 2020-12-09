#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/9 10:05
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import re
from random import randint
from datetime import datetime, timedelta
from apscheduler.triggers.date import DateTrigger

from nonebot.rule import to_me
from nonebot.log import logger
from nonebot.sched import scheduler
from nonebot.typing import Bot, Event
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command, on_message, on_regex

from src.utils.utils import counter
from src.utils.rules import is_banned

from .data_source import result_get

sauce_search = on_command("picsearch", aliases={"搜图"}, rule=is_banned())


@sauce_search.handle()
async def _(bot: Bot, event: Event, state: dict):
    user = str(event.user_id)
    group = str(event.group_id)
    state["user"] = user
    state["group"] = group
    img = str(event.message).strip()

    if img:
        state["img"] = img


@sauce_search.got("img", prompt="请发一张图哦")
async def _(bot: Bot, event: Event, state: dict):
    img = state["img"]
    img = re.findall(r"(http://.*?)]", img)

    if not img:
        await sauce_search.reject("图呢？")

    await bot.send(event, "开始搜索嘞...")
    msg = await result_get(state["user"], img[0])
    logger.info(msg)
    if len(msg) > 1:
        await bot.send(event, msg[1])
    await sauce_search.finish(msg[0])

