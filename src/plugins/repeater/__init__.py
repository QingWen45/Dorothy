#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/7 20:11
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import asyncio
import ujson
from pathlib import Path
from random import randint
from typing import Dict
from dataclasses import dataclass

from nonebot.typing import Bot, Event
from nonebot.plugin import on_command, on_message
from nonebot.log import logger

from src.utils.rules import is_banned

RECORD = Path("./src/plugins/repeater/King_of_Repeaters.json")
if not RECORD.is_file():
    with open(RECORD, 'w') as f:
        data = {}
        ujson.dump(data, f)
else:
    with open(RECORD, 'r') as f:
        data = ujson.load(f)


# 保存单个记录
@dataclass
class Record:
    last_msg: str
    last_user_id: str
    repeat_count: int = 0


# 存储各个群的复读记录
records: Dict[str, Record] = {}

# 复读！学大家说话！
repeater = on_message(rule=is_banned(), priority=1)


@repeater.handle()
async def _(bot: Bot, event: Event, state: dict):
    msg = str(event.message)
    logger.info(msg)
    user_id = str(event.user_id)
    group = str(event.group_id)

    if group not in records:
        rec = Record(msg, user_id, 1)
        records[group] = rec
        return

    rec = records.get(group)
    if rec.last_msg != msg:
        rec.last_msg = msg
        rec.repeat_count = 1
        return

    rec.repeat_count += 1

    if rec.repeat_count == 2:
        if msg not in data:
            data[msg] = 1
        else:
            data[msg] += 1
        with open(RECORD, 'w') as file:
            ujson.dump(data, file)
        delay = randint(5, 20) / 10
        await asyncio.sleep(delay)
        await repeater.finish(msg)


repeater_rank = on_command("frank", aliases={"复读榜"})


@repeater_rank.handle()
async def _(bot: Bot, event: Event, state: dict):
    rank = sorted(data.items(), key=lambda kv: (kv[1], kv[0]))
    msg = "------+++复读榜+++------\n"
    size = 3 if len(rank) > 3 else len(rank)
    for i in range(size):
        msg += str(i) + ". " + rank[i][0] + " 被复读了足足 " + str(rank[i][1]) + " 次！\n"
    await repeater_rank.finish(msg)
