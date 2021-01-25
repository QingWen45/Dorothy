#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/7 22:20
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import asyncio
from random import randint

from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_command

from src.utils.rules import is_banned

safe_left = 0
current_bullet_num = 0
players = {}

spin = on_command("rr", rule=is_banned(), block=True)


@spin.handle()
async def _(bot: Bot, event: Event, state: dict):
    if event.sub_type == "private":
        await spin.finish("此功能仅对群聊开放。")

    group_id = event.group_id
    user_id = event.user_id
    bot_id = int(event.self_id)
    bot_info = await bot.get_group_member_info(group_id=group_id, user_id=bot_id)
    player_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    bot_role = bot_info["role"]
    player_role = player_info["role"]

    if bot_role == "member":
        await spin.finish("平民无法禁言呀喂，群主来个绿牌")
    elif bot_role == "admin" and player_role == "admin":
        await spin.finish("然而管理员之间无法互相伤害")
    elif player_role == "owner":
        await spin.finish("群主我可打不过呢")

    else:
        global current_bullet_num, safe_left
        sender_info = dict(event.sender)
        if sender_info["card"]:
            user_name = sender_info["card"]
        else:
            user_name = sender_info["nickname"]
        state["user_name"] = user_name

        group_id = str(group_id)
        if group_id not in players:
            players[group_id] = {}

        cur_players = players[group_id]

        if user_name not in cur_players:
            cur_players[user_name] = {}
            cur_players[user_name]["point"] = 0
            cur_players[user_name]["death"] = 0
        args = str(event.message).strip()

        if current_bullet_num == 0:
            if args:
                state["bullet"] = args
        else:
            state["bullet"] = current_bullet_num


@spin.got("bullet", prompt="紧张刺激的禁言转盘活动，请输入要填入的子弹数目(最多5颗)")
async def _bullet(bot: Bot, event: Event, state: dict):
    global current_bullet_num, safe_left

    if not current_bullet_num:
        if len(state["bullet"]) < 2 and '0' < state["bullet"] < '6':
            current_bullet_num = int(state["bullet"])
            safe_left = safe_couter(current_bullet_num)
            await spin.finish("装填完成")
        else:
            await spin.finish("请输入可行的数目")

    else:
        user_name = state["user_name"]
        group_id = str(event.group_id)
        cur_players = players[group_id]

        if safe_left == 0:
            await bot.send(event, "“砰”")
            await bot.set_group_ban(group_id=event.group_id,
                                    user_id=event.user_id,
                                    duration=60)
            cur_players[user_name]["point"] /= 2
            cur_players[user_name]["death"] += 1
            current_bullet_num -= 1
            if current_bullet_num == 0:
                await bot.send(event, "感谢各位的参与，以下是游戏结算:")
                await asyncio.sleep(1)
                rank = sorted(cur_players.items(), key=lambda x: (x[1]["point"], x[0]))

                msg = ''
                for i, data in enumerate(rank):
                    if i != len(cur_players) - 1:
                        msg += ("%s:\nP: %s分 D: %s\n" % (data[0], data[1]["point"], data[1]["death"]))
                    else:
                        msg += ("%s:\nP: %s分 D: %s" % (data[0], data[1]["point"], data[1]["death"]))
                del players[group_id]
                await spin.finish(msg)

            else:
                msg = "有请下一位，还有 %d 发" % current_bullet_num
                safe_left = safe_couter(current_bullet_num)
                await spin.finish(msg)
        else:
            safe_left -= 1
            msg = "无事发生，还有 %d 发" % current_bullet_num
            cur_players[user_name]["point"] += 300 * current_bullet_num ** 2 / 30 + 20
            await spin.finish(msg)


def safe_couter(cur_num: int) -> int:
    """
    计算距离下一枪还有几次
    """
    n = 6 - randint(1, 6)
    if n <= cur_num:
        return 0
    else:
        return 6 - n + 1
