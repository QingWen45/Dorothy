#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : epd_drawer.py
# @Time : 2021/1/20 16:29
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import platform
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import psutil

font_light = Path("./fonts/msyhl.ttc")
font_bold = Path("./fonts/msyhbd.ttc")
font_regular = Path("./fonts/msyh.ttc")

font_36 = ImageFont.truetype(str(font_light), 36)
font_30 = ImageFont.truetype(str(font_regular), 30)
font_18 = ImageFont.truetype(str(font_regular), 18)
font_50 = ImageFont.truetype(str(font_regular), 50)


async def epd_start_screen(epd):
    now = datetime.now()
    img = Image.new("1", (200, 200), 0xFF)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 199, 199), outline=0x00)

    draw.text((139, 0), now.strftime("%b %d"), fill=0x00, font=font_18)
    draw.text((0, 0), "Dorothy", fill=0x00, font=font_36)
    draw.line((135, 0, 135, 158), fill=0x00, width=2)
    draw.line((135, 26, 200, 26), fill=0x00, width=1)
    draw.line((0, 50, 200, 50), fill=0x00, width=2)

    draw.text((3, 52), f"CPU:\nMEM:", fill=0x00, font=font_18)
    draw.text((138, 55), "\n  mpm", fill=0x00, font=font_18, spacing=-2)
    draw.line((135, 50, 135, 158), fill=0x00, width=2)
    draw.line((0, 105, 200, 105), fill=0x00, width=2)

    bytes_sent = '# kb/s'
    bytes_rcvd = '# kb/s'
    net_status = "↑%s\n↓%s" % (bytes_rcvd, bytes_sent)

    draw.text((3, 108), net_status, fill=0x00, font=font_18)
    draw.text((140, 108), "(≧∇≦)ﾉ", fill=0x00, font=font_18)
    draw.text((140, 134), "cqhttp", fill=0x00, font=font_18)
    draw.line((135, 134, 200, 134), fill=0x00, width=2)
    draw.line((0, 158, 200, 158), fill=0x00, width=2)

    draw.text((5, 165), "bot online {:>10s}".format("0:00:00"), fill=0x00, font=font_18)
    epd.display(epd.getbuffer(img))


async def epd_updater(thruput: int, epd, boot_time: datetime):
    img = await image_loader(thruput, boot_time)
    epd.display(epd.getbuffer(img))


async def image_loader(thruput: int, boot_time: datetime):
    now = datetime.now()
    img = Image.new("1", (200, 200), 0xFF)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 199, 199), outline=0x00)

    draw.text((139, 0), now.strftime("%b %d"), fill=0x00, font=font_18)
    form = "%H: %M" if now.second % 2 == 0 else "%H  %M"
    draw.text((138, 25), now.strftime(form), fill=0x00, font=font_18)
    draw.text((0, 0), "Dorothy", fill=0x00, font=font_36)
    draw.line((135, 0, 135, 158), fill=0x00, width=2)
    draw.line((135, 26, 200, 26), fill=0x00, width=1)
    draw.line((0, 50, 200, 50), fill=0x00, width=2)

    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    draw.text((3, 52), f"CPU: {cpu}%\nMEM: {memory}%", fill=0x00, font=font_18)
    draw.text((138, 55), "%d\n  mpm" % thruput, fill=0x00, font=font_18, spacing=-2)
    draw.line((135, 50, 135, 158), fill=0x00, width=2)
    draw.line((0, 105, 200, 105), fill=0x00, width=2)

    net = psutil.net_io_counters()
    bytes_sent = '{0:.2f} kb/s'.format(net.bytes_recv / 1024 / 1024)
    bytes_rcvd = '{0:.2f} kb/s'.format(net.bytes_sent / 1024 / 1024)
    net_status = "↑%s\n↓%s" % (bytes_rcvd, bytes_sent)

    draw.text((3, 108), net_status, fill=0x00, font=font_18)
    draw.text((140, 108), "(≧∇≦)ﾉ", fill=0x00, font=font_18)
    draw.text((140, 134), "cqhttp", fill=0x00, font=font_18)
    draw.line((135, 134, 200, 134), fill=0x00, width=2)
    draw.line((0, 158, 200, 158), fill=0x00, width=2)

    deltatime = now - boot_time
    days = deltatime.days
    h, m = divmod(deltatime.seconds, 3600)
    m = m // 60
    deltatime = f"{days}:{h}:{m}"
    draw.text((5, 165), "bot online {:>10s}".format(deltatime), fill=0x00, font=font_18)

    return img


async def shutdown():
    from nonebot import require
    scheduler = require('nonebot_plugin_apscheduler').scheduler
    if scheduler.running:
        scheduler.shutdown()
    if platform.system() == "Linux":
        from waveshare_epd import epd1in54
        epd = epd1in54.EPD()
        epd.init(epd.lut_full_update)
        epd.Clear(0xFF)

        img = Image.new("1", (200, 200), 0xFF)
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, 199, 199), outline=0x00)

        draw.text((33, 33), "Good\nNight", fill=0x00, font=font_50)
        epd.display(epd.getbuffer(img))
