#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/7 22:20
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import asyncio
from random import randint

from nonebot.typing import Bot, Event
from nonebot.plugin import on_command

from src.utils.rules import is_banned

safe_left = 0
current_bullet_num = 0
players = {}

spin = on_command("rr", rule=is_banned())


@spin.handle()
async def _(bot: Bot, event: Event, state: dict):
    if event.sub_type == "private":
        await spin.finish("此功能仅对群聊开放。")
    else:
        global current_bullet_num, safe_left
        if event.sender["card"] != "":
            user_name = event.sender["card"]
        else:
            user_name = event.sender["nickname"]

        if user_name not in players:
            players[user_name] = {}
            players[user_name]["point"] = 0
            players[user_name]["death"] = 0
        args = str(event.message).strip()
        if current_bullet_num == 0:
            if args:
                if len(args) < 2 and '0' < args < '6':
                    current_bullet_num = int(args)
                    state["bullet"] = current_bullet_num
                    safe_left = safe_couter(current_bullet_num)
                    await bot.send(event, "装填完成")
                else:
                    await spin.finish("请输入可行的数目")
        else:
            if safe_left == 0:
                await bot.send(event, "“砰”")
                await bot.call_api("set_group_ban",
                                   group_id=event.group_id,
                                   user_id=event.user_id,
                                   duration=60)
                players[user_name]["point"] /= 2
                players[user_name]["death"] += 1
                current_bullet_num -= 1
                if current_bullet_num == 0:

                    await bot.send(event, "感谢各位的参与，以下是游戏结算:")
                    await asyncio.sleep(1)
                    rank = sorted(players.items(), key=lambda x: (x[1]["point"], x[0]))

                    msg = ''
                    for i, data in enumerate(rank):
                        if i != len(players) - 1:
                            msg += ("%s:\nP: %s分 D: %s\n" % (data[0], data[1]["point"], data[1]["death"]))
                        else:
                            msg += ("%s:\nP: %s分 D: %s" % (data[0], data[1]["point"], data[1]["death"]))
                    players.clear()
                    await spin.finish(msg)

                else:
                    msg = "有请下一位，还有 %d 发" % current_bullet_num
                    safe_left = safe_couter(current_bullet_num)
                    await spin.finish(msg)
            else:
                safe_left -= 1
                msg = "无事发生，还有 %d 发" % current_bullet_num
                players[user_name]["point"] += 300 * current_bullet_num**2 / 30 + 20
                await spin.finish(msg)


@spin.got("bullet", prompt="紧张刺激的禁言转盘活动，请输入要填入的子弹数目(最多5颗)")
async def _bullet(bot: Bot, event: Event, state: dict):
    global current_bullet_num, safe_left
    if not current_bullet_num:
        if (len(state["bullet"]) < 2) & ('0' < state["bullet"] < '6'):
            current_bullet_num = int(state["bullet"])
            state["bullet"] = current_bullet_num
            safe_left = safe_couter(current_bullet_num)
            await bot.send(event, "装填完成")
        else:
            await spin.finish("请输入可行的数目")


def safe_couter(cur_num: int) -> int:
    """
    计算距离下一枪还有几次
    """
    n = 6 - randint(1, 6)
    if n <= cur_num:
        return 0
    else:
        return 6-n+1
