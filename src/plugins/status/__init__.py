#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/8 17:52
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import psutil
import platform

if platform.system() == "Linux":
    from waveshare_epd import epd1in54

    epd = epd1in54.EPD()
from datetime import datetime

from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_command, on_metaevent
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from nonebot import require
from nonebot.message import run_preprocessor

from src.utils.scheduler_job.throughput_counter import ThroughPut
from src.utils.scheduler_job.epd_drawer import epd_updater, epd_start_screen

counter = 0
boot_time = datetime(1970, 1, 1)

status = on_command("status", permission=SUPERUSER, block=True)


@status.handle()
async def _(bot: Bot, event: Event, state: dict):
    try:
        py_info = platform.python_version()
        pla = platform.platform()
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        memory = round(memory, 2)
    except Exception:  # ignore
        await status.finish("获取状态失败！")
        return

    msg = r"""  __                  _   _        
 |   \ ___ _ _ ___| |_| |_ _    _ 
 | |) / _ \ '_/ _  \ __|  ' \ | | |
 |_ /\__/_| \___/\__|_||_\_, |
                                     |__/ 
"""

    if cpu > 80 or memory > 80:
        ex_msg = "感觉要炸了..."
    else:
        ex_msg = "状态正常"

    msg += "Dorothy status:\n"
    msg += f"OS: {pla}"
    msg += f"Running on Python {py_info}\n"
    msg += f"CPU {cpu}%\n"
    msg += f"MEM {memory}%\n"
    msg += ex_msg
    await status.finish(msg)


def check_first_connect(bot: Bot, event: Event, state: dict) -> bool:
    return event.sub_type == 'connect'


startup_metaevent = on_metaevent(rule=check_first_connect, block=True)


@startup_metaevent.handle()
async def _(bot: Bot, event: Event, state: dict):
    global boot_time
    boot_time = datetime.now()
    if platform.system() == "Linux":
        epd.init(epd.lut_full_update)
        epd.Clear(0xFF)
        await epd_start_screen(epd)
        epd.init(epd.lut_partial_update)
        epd.Clear(0xFF)
    if not scheduler.running:
        scheduler.start()


@run_preprocessor
async def _(match, bot: Bot, event: Event, state: dict):
    if event.sub_type == 'connect':
        return
    global counter
    counter += 1
    logger.info(str(counter))


scheduler = require('nonebot_plugin_apscheduler').scheduler
through_put = ThroughPut()


@scheduler.scheduled_job('interval', seconds=1, id="001")
async def run_per_second():
    global counter
    through_put.push(counter)
    counter = 0
    throuput_per_minute = through_put.count()
    if platform.system() == "Linux":
        await epd_updater(throuput_per_minute, epd, boot_time)
