#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/10 9:49
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import ujson
from pathlib import Path

from nonebot.typing import Bot, Event
from nonebot.log import logger
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER, GROUP_ADMIN, GROUP_OWNER

from src.utils.func_switch import func_switcher

switch = on_command("switch", permission=(SUPERUSER | GROUP_OWNER | GROUP_ADMIN))


@switch.handle()
async def _(bot: Bot, event: Event, state: dict):
    group = str(event.group_id)
    args = str(event.message).strip()
    if not args:
        msg = """--+Welcome Contro1-C+--
Type in
switch {func_name} on/off
to switch func for group
switch {func-name} all-on/off
to swtich func for all"""
        await switch.finish(msg)

    args = args.split()
    if len(args) != 2:
        await switch.finish("Wrong syntax!")
    if args[1] == "on":
        await switch.finish(func_switcher(args[0], True, group))
    if args[1] == "off":
        await switch.finish(func_switcher(args[0], False, group))

    if args[1] == "all-on":
        await switch.finish(func_switcher(args[0], True))
    if args[1] == "all-off":
        await switch.finish(func_switcher(args[0], False))

    else:
        await switch.finish("Worng 嘞")


switch_ex = on_command("e18on", permission=SUPERUSER)


@switch_ex.handle()
async def _(bot: Bot, event: Event, state: dict):
    group = str(event.group_id)
    args = str(event.message).strip()
    if args == "on" or args == "off":
        ON_FILE = Path("./src/plugins/pic_search/on_list.json")
        if not ON_FILE.is_file():
            data = {}
        else:
            with open(ON_FILE, 'r') as file:
                data = ujson.load(file)

        if data.get(group) == args:
            await switch_ex.finish("已设置")

        data[group] = args
        with open(ON_FILE, 'w') as file:
            ujson.dump(data, file)
        msg = "已开启" if args == "on" else "已关闭"
        await switch_ex.finish(msg)
    else:
        await switch_ex.finish("参数错误")
