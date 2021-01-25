#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

from src.utils.yaml_loader import yml_loader
from src.utils.scheduler_job.epd_drawer import shutdown
from pathlib import Path

CONFIG_FILE = Path("./configs.yml")
configs = yml_loader(CONFIG_FILE)
bot_config = configs["bot"]

nonebot.init(debug=bot_config["DEBUG"],
             superusers=set(bot_config["SUPERUSERS"]),
             nickname=set(bot_config["NICKNAME"]),
             command_start=set(bot_config["COMMAND_START"]),
             command_sep=set(bot_config["COMMAND_SEP"]),
             host=bot_config["HOST"],
             port=bot_config["PORT"],
             apscheduler_autostart=False)
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
driver.on_shutdown(shutdown)

nonebot.load_builtin_plugins()
nonebot.load_plugin("nonebot_plugin_apscheduler")
nonebot.load_plugins("src/plugins")


if __name__ == "__main__":
    nonebot.run(app="bot:app")
