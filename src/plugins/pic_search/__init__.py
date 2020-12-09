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

from .data_source import result_get, setu_linker

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


search_type = 0  # 0 is from url, while 1 is from local, 2 is closed
lsp_list = {}
lsp_stack = []


def check_list(user) -> bool:
    if user in lsp_list:
        return True
    return False


def en_lsp(user):
    global lsp_list
    lsp_list["user"] += 1


def de_lsp(user):
    global lsp_list
    del lsp_list["user"]


setu_get = on_regex(
    r"来[点丶张份副个幅][涩色瑟][图圖]|[涩色瑟][图圖]来|[涩色瑟][图圖][gkd|GKD|搞快点]|[gkd|GKD|搞快点]",
    rule=is_banned() & to_me())


@setu_get.handle()
async def _(bot: Bot, event: Event, state: dict):
    global lsp_stack
    user = event.user_id

    if check_list(user):
        await setu_get.finish("冲的太多了，休息一下吧")

    if counter(lsp_stack, user) == 5:
        en_lsp(user)
        lsp_stack = list(set(lsp_stack))
        delta = timedelta(minutes=10)
        trigger = DateTrigger(run_date=datetime.now() + delta)
        scheduler.add_job(func=de_lsp,
                          trigger=trigger,
                          args=(user, ),
                          misfire_grace_time=60)
        return

    if search_type == 0:
        setu = await setu_linker()
        if not setu:
            await setu_get.finish("超时嘞")
        lsp_stack.append(user)
        logger.info(setu)
        await setu_get.finish(setu)