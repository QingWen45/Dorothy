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
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_command, on_regex
from nonebot import require

from src.utils.utils import counter
from src.utils.rules import is_banned, is_enabled

from .data_source import result_get, setu_linker, setu_loader

sauce_search = on_command("picsearch", aliases={"搜图"}, rule=is_banned(), block=True)


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
    await sauce_search.finish(msg)


_func_name = "gkd"
lsp_list = {}
lsp_stack = []
scheduler = require('nonebot_plugin_apscheduler').scheduler


def check_list(user: str) -> bool:
    return user in lsp_list


def en_lsp(user: str):
    global lsp_list
    if user not in lsp_list:
        lsp_list[user] = 1


def de_lsp(user: str):
    global lsp_list
    del lsp_list[user]


setu_get = on_regex(
    r"来[张份个幅][涩色瑟][图]|[涩色瑟][图]来|[涩色瑟][图][gkd|GKD|搞快点]|[gkd|GKD|搞快点]",
    rule=is_banned() & to_me(), priority=8, block=True)


@setu_get.handle()
async def _(bot: Bot, event: Event, state: dict):
    global lsp_stack
    user = str(event.user_id)
    group = str(event.group_id)

    if not is_enabled(_func_name, group):
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
                          args=(user,),
                          misfire_grace_time=60)

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
    await bot.send(event, "别急，涩图在搜索了")

    if state.get("keyword") == "local":
        setu = await setu_loader(user)
    else:
        key = state.get("keyword")
        setu = await setu_linker(user, key, mode=r18_switch)

    if not setu:
        msg = [
            {
                "type": "at",
                "data": {"qq": user}
            },
            {
                "type": "text",
                "data": {"text": "连接超时，涩图找丢了"}
            }
        ]

        await setu_get.finish(msg)

    lsp_stack.append(user)

    sender_info = dict(event.sender)
    if sender_info["card"]:
        user_name = sender_info["card"]
    else:
        user_name = sender_info["nickname"]
    # lsp榜单更新

    KSP = Path("./src/plugins/pic_search/King_of_LSP.json")
    if not KSP.is_file():
        sp_data = {}
    else:
        with open(KSP, 'r') as f:
            sp_data = ujson.load(f)
    if group not in sp_data:
        sp_data[group] = {}

    if user not in sp_data[group]:
        sp_data[group][user] = {"name": user_name, "times": 0}
    if sp_data[group][user]["name"] != user_name:
        sp_data[group][user]["name"] = user_name
    sp_data[group][user]["times"] += 1

    with open(KSP, 'w') as file:
        ujson.dump(sp_data, file)

    await setu_get.finish(setu)


lsp_rank = on_command("sprank", aliases={"lsp榜"})


@lsp_rank.handle()
async def _(bot: Bot, event: Event, state: dict):
    KSP = Path("./src/plugins/pic_search/King_of_LSP.json")
    if not KSP.is_file():
        data = {}
        with open(KSP, 'w') as f:
            ujson.dump(data, f)
    else:
        with open(KSP, 'r') as f:
            data = ujson.load(f)
    data = data.get(str(event.group_id), {})
    rank = sorted(data.items(), key=lambda kv: kv[1]["times"], reverse=True)
    msg = "   ------+++LSP榜+++------\n"
    size = 5 if len(rank) > 5 else len(rank)
    for i in range(size):
        if i != size - 1:
            msg += str(i) + ". " + rank[i][1]["name"] + " ... " + str(rank[i][1]["times"]) + " 次！\n"
        else:
            msg += str(i) + ". " + rank[i][1]["name"] + " ... " + str(rank[i][1]["times"]) + " 次！"
    await lsp_rank.finish(msg)
