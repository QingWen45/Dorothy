#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/10 16:38
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import ujson
import httpx
from pathlib import Path
from random import choice, randint
from datetime import date

from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.typing import Bot, Event
from nonebot.plugin import on_command, on_notice, on_keyword

from src.utils.utils import counter
from src.utils.rules import is_banned
from src.utils.yaml_loader import yml_loader

CONFIG_PATH = Path("./configs.yml")
config = yml_loader(CONFIG_PATH)

notice_handler = on_notice(rule=is_banned(), block=True)


@notice_handler.handle()
async def _(bot: Bot, event: Event, state: dict):
    if event.raw_event["notice_type"] == "group_increase":
        if event.user_id == event.self_id:
            await notice_handler.finish("大家好啊")
        else:
            await notice_handler.finish("欢迎新人")

    elif event.raw_event["notice_type"] == "group_decrease":
        if event.user_id != event.self_id:
            await notice_handler.finish(f"{event.user_id} 退群了..")

    elif event.raw_event["notice_type"] == "notify":
        if event.raw_event["sub_type"] == "poke":
            user = str(event.user_id)
            LV = Path("./src/plugins/ShaDiao/love_value.json")
            if not LV.is_file():
                data = {}
                with open(LV, 'w') as f:
                    ujson.dump(data, f)
            else:
                with open(LV, 'r') as f:
                    data = ujson.load(f)

            if user not in data:
                data[user] = [randint(1, 100), str(date.today())]
                msg = f"Dorothy对 [CQ:at,qq={user}] 的初始好感为{data[user][0]}点"

            else:
                increment = 0
                if str(date.today()) != data[user][1]:
                    increment = randint(1, 3)
                    data[user][0] += increment
                else:
                    await notice_handler.finish("好感无法上升了")

                msg = f"对 [CQ:at,qq={user}] 的好感上升了{increment}点，变成{data[user][0]}点了"

            logger.info(data)
            with open(LV, 'w') as file:
                ujson.dump(data, file)
            await notice_handler.finish(msg)

        elif event.raw_event["sub_type"] == "talkative":
            img_path = Path("./images/long_wang.jpg").resolve()
            msg = f"[CQ:image,file=file:///{str(img_path)}]"
            await notice_handler.finish(msg)


nmsl = on_command("嘴臭", aliases={"口臭", "开骂"}, rule=to_me())
count_list_n = []


@nmsl.handle()
async def _(bot: Bot, event: Event, state: dict):
    user = str(event.user_id)
    count = counter(count_list_n, user)
    if 6 > count > 3:
        await bot.send(event, "还，还要吗？!")

    api = config["shadiao"]["zui_chou"]
    if count < 7:
        count_list_n.append(user)
    async with httpx.AsyncClient() as client:
        response = await client.get(api)
    await nmsl.finish(response.text)


pyq = on_keyword({"朋友圈"}, rule=to_me())


@pyq.handle()
async def _(bot: Bot, event: Event, state: dict):
    api = config["shadiao"]["peng_you_quan"]

    async with httpx.AsyncClient() as client:
        response = await client.get(api)
    await pyq.finish(response.text)


chp = on_keyword({"夸"}, rule=to_me())


@chp.handle()
async def _(bot: Bot, event: Event, state: dict):
    api = config["shadiao"]["rainbow_fart"]

    async with httpx.AsyncClient() as client:
        response = await client.get(api)
    await chp.finish(response.text)


djt = on_keyword({"毒鸡汤"}, rule=to_me())


@djt.handle()
async def _(bot: Bot, event: Event, state: dict):
    api = config["shadiao"]["du_ji_tang"]

    async with httpx.AsyncClient() as client:
        response = await client.get(api)
    await djt.finish(response.text)


trans = on_command("nbnhhsh", rule=to_me(),
                   aliases={"屌话翻译器", "能不能好好说话", "屌话翻译机", "翻译机", "翻译器"})


@trans.handle()
async def _(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip()
    if args:
        state["text"] = args


@trans.got("text", prompt="请发送要翻译的密文")
async def _(bot: Bot, event: Event, state: dict):
    api = config["shadiao"]["nbnhhsh"]
    data = {"text": state["text"]}
    async with httpx.AsyncClient() as client:
        response = await client.post(api, data=data)
    response = response.json()
    if not response:
        await trans.finish("没有对应的翻译")
    msg = "得到的翻译如下：\n"
    for i in response[0]["trans"]:
        msg += i + "，"
    msg.strip("，")
    await trans.finish(msg)


hitokoto = on_command("一言", rule=to_me())


@hitokoto.handle()
async def _(bot: Bot, event: Event, state: dict):
    api = config["ad_api"]["hitokoto"]

    async with httpx.AsyncClient() as client:
        response = await client.get(api)
    await hitokoto.finish(response.text)
"""
music = on_command("点歌", rule=to_me())


@music.handle()
async def _(bot: Bot, event: Event, state: dict):
    music_id = choice(["1349937484", "1349927611", "1349932444", "1349929719"])
"""
