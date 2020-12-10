#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/8 17:52
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import psutil
import platform
from nonebot.typing import Bot, Event
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER

status = on_command("status", permission=SUPERUSER)


@status.handle()
async def _(bot: Bot, event: Event, state: dict):
    try:
        py_info = platform.python_version()
        cpu = psutil.cpu_percent()
        memory = 100 - psutil.virtual_memory().percent
        memory = round(memory, 2)
    except Exception:  # ignore
        await status.finish("获取状态失败！")

    msg = r"""  __                  _   _        
 |   \ ___ _ _ ___| |_| |_ _    _ 
 | |) / _ \ '_/ _  \ __|  ' \ | | |
 |_ /\__/_| \___/\__|_||_\_, |
                                     |__/ """
    await bot.send(event, msg)

    if cpu > 80 or memory > 80:
        ex_msg = "感觉要炸了..."
    else:
        ex_msg = "ALL is WELL"

    msg2 = "Dorothy status:\n"
    msg2 = f"Running on Python {py_info}\n"
    msg2 += f"CPU {cpu}%\n"
    msg2 += f"MEM {memory}%\n"
    msg2 += ex_msg
    await status.finish(msg2)
