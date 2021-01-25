#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/10 16:38
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import ujson
import httpx
import platform
from pathlib import Path
from random import choice, randint
from datetime import date

from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_command, on_notice, on_keyword

from src.utils.utils import counter
from src.utils.rules import is_banned
from src.utils.yaml_loader import yml_loader

CONFIG_PATH = Path("./configs.yml")
config = yml_loader(CONFIG_PATH)

notice_handler = on_notice(rule=is_banned(), block=True)


@notice_handler.handle()
async def _(bot: Bot, event: Event, state: dict):
    if platform.system() == "Windows":
        event_type = event.detail_type
    else:
        event_type = event.notice_type
    if event_type == "group_increase":
        if str(event.user_id) == str(event.self_id):
            await notice_handler.finish("大家好啊")
        else:
            await notice_handler.finish("欢迎新人")

    elif event_type == "group_decrease":
        if str(event.user_id) != str(event.self_id):
            await notice_handler.finish(f"{event.user_id} 退群了..")

    elif event_type == "notify":
        if event.sub_type == "poke":
            if str(event.target_id) == str(event.self_id):
                user = str(event.user_id)
                LV = Path("./src/plugins/ShaDiao/love_value.json")
                if not LV.is_file():
                    data = {}
                else:
                    with open(LV, 'r') as f:
                        data = ujson.load(f)

                if user not in data:
                    data[user] = [randint(1, 100), str(date.today())]
                    msg = [
                        {
                            "type": "text",
                            "data": {"text": "Dorothy对 "}
                        },
                        {
                            "type": "at",
                            "data": {"qq": user}
                        },
                        {
                            "type": "text",
                            "data": {"text": f"的初始好感为{data[user][0]}点"}
                        }
                    ]

                else:
                    if str(date.today()) != data[user][1]:
                        data[user][1] = str(date.today())
                        increment = randint(1, 3)
                        data[user][0] += increment
                        if data[user][0] >= 100:
                            data[user][0] = 100
                            msg = [
                                {
                                    "type": "at",
                                    "data": {"qq": user}
                                },
                                {
                                    "type": "text",
                                    "data": {"text": "好感满分！100点"}
                                }
                            ]
                        else:
                            msg = [
                                {
                                    "type": "text",
                                    "data": {"text": "对"
                                             }
                                },
                                {
                                    "type": "at",
                                    "data": {"qq": user}
                                },
                                {
                                    "type": "text",
                                    "data": {"text": f"的好感上升了{increment}点，变成{data[user][0]}点了"}
                                }
                            ]
                    else:
                        msg = "好感无法上升了"

                with open(LV, 'w') as file:
                    ujson.dump(data, file)
                await notice_handler.finish(msg)

        elif event.sub_type == "talkative":
            img_path = Path("./images/long_wang.jpg").resolve()
            msg = {
                "type": "image",
                "data": {"file": f"file:///{str(img_path)}"}
            }
            await notice_handler.finish(msg)


nmsl = on_command("嘴臭", aliases={"口臭", "开骂"}, rule=to_me(), block=True)
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


pyq = on_keyword({"朋友圈"}, rule=to_me(), block=True)


@pyq.handle()
async def _(bot: Bot, event: Event, state: dict):
    api = config["shadiao"]["peng_you_quan"]

    async with httpx.AsyncClient() as client:
        response = await client.get(api)
    await pyq.finish(response.text)


chp = on_keyword({"夸"}, rule=to_me(), block=True)


@chp.handle()
async def _(bot: Bot, event: Event, state: dict):
    api = config["shadiao"]["rainbow_fart"]

    async with httpx.AsyncClient() as client:
        response = await client.get(api)
    await chp.finish(response.text)


djt = on_keyword({"毒鸡汤"}, rule=to_me(), block=True)


@djt.handle()
async def _(bot: Bot, event: Event, state: dict):
    api = config["shadiao"]["du_ji_tang"]

    async with httpx.AsyncClient() as client:
        response = await client.get(api)
    await djt.finish(response.text)


trans = on_command("nbnhhsh", rule=to_me(), block=True,
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
    msg = msg.strip("，")
    await trans.finish(msg)
