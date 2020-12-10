#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/9 10:05
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import re
import ujson
from pathlib import Path
from datetime import datetime, timedelta
from apscheduler.triggers.date import DateTrigger

from nonebot.rule import to_me
from nonebot.log import logger
from nonebot.sched import scheduler
from nonebot.typing import Bot, Event
from nonebot.plugin import on_command, on_regex

from src.utils.utils import counter
from src.utils.rules import is_banned, is_enabled

from .data_source import result_get, setu_linker, setu_loader

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
    try:
        msg = await result_get(state["user"], img[0])
    except Exception:
        msg = ["超时嘞"]
    logger.info(msg)
    if len(msg) > 1:
        await bot.send(event, msg[1])
    await sauce_search.finish(msg[0])


_func_name = "gkd"
search_type = 0  # 0 is from url, while 1 is from local
lsp_list = {}
lsp_stack = []


def check_list(user: str) -> bool:
    if user in lsp_list:
        return True
    return False


def en_lsp(user: str):
    global lsp_list
    lsp_list[user] += 1


def de_lsp(user: str):
    global lsp_list
    del lsp_list[user]


setu_get = on_regex(
    r"来[点丶张份副个幅][涩色瑟][图圖]|[涩色瑟][图圖]来|[涩色瑟][图圖][gkd|GKD|搞快点]|[gkd|GKD|搞快点]",
    rule=is_banned() & to_me(), block=True)


@setu_get.handle()
async def _(bot: Bot, event: Event, state: dict):
    global lsp_stack, search_type
    user = str(event.user_id)
    group = str(event.group_id)

    if not is_enabled(_func_name, True, group):
        await setu_get.finish("该功能不可用")
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

    r18_switch = 0
    ON_FILE = Path("./src/plugins/pic_search/on_list.json")
    if ON_FILE.is_file():
        with open(ON_FILE, 'r') as file:
            data = ujson.load(file)
        if group in data:
            r18_switch = 1 if data[group] == "on" else 0

    args = str(event.message).strip().split()
    if len(args) > 1:
        state["keyword"] = args[1]
        if state["keyword"] == "local":
            search_type = 1
    await bot.send(event, "别急，涩图在搜索了")

    if search_type == 0:
        key = state["keyword"] if "keyword" in state else None

        setu = await setu_linker(user, key, mode=r18_switch)

    else:
        setu = await setu_loader(user)
        logger.info(setu)

    if not setu:
        await setu_get.finish(f"[CQ:at,qq={user}]连接超时，涩图找丢了")
    lsp_stack.append(user)

    # lsp榜单更新
    if event.sender["card"] != "":
        user_name = event.sender["card"]
    else:
        user_name = event.sender["nickname"]
    KSP = Path("./src/plugins/pic_search/King_of_LSP.json")
    if not KSP.is_file():
        sp_data = {}
    else:
        with open(KSP, 'r') as f:
            sp_data = ujson.load(f)
    if group not in sp_data:
        sp_data[group] = {}

    if user_name not in sp_data[group]:
        sp_data[group][user_name] = 0
    sp_data[group][user_name] += 1
    logger.info(sp_data)
    with open(KSP, 'w') as file:
        ujson.dump(sp_data, file)

    await setu_get.finish(setu)


lsp_rank = on_command("sprank", aliases={"lsp榜"})


@lsp_rank.handle()
async def _(bot: Bot, event: Event, state: dict):
    KSP = Path("./src/plugins/pic_search/King_of_LSP.json")
    if not KSP.is_file():
        data = {}
    else:
        with open(KSP, 'r') as f:
            data = ujson.load(f)
    data = data.get(str(event.group_id), {})
    rank = sorted(data.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    msg = "------+++LSP榜+++------\n"
    size = 5 if len(rank) > 5 else len(rank)
    for i in range(size):
        if i != size - 1:
            msg += str(i) + ". " + rank[i][0] + " ... " + str(rank[i][1]) + " 次！\n"
        else:
            msg += str(i) + ". " + rank[i][0] + " ... " + str(rank[i][1]) + " 次！"
    await lsp_rank.finish(msg)
