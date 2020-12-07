#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : bot.py
# @Time : 2020/12/7 13:08
# @Author : QingWen
# @E-mail : hurrsea@outlook.com


from src.utils.yaml_loader import yml_loader
from pathlib import Path

import nonebot

CONFIG_FILE = Path("./configs.yml")
config = yml_loader(CONFIG_FILE)
bot_config = config["bot"]
nonebot.init(debug=bot_config["DEBUG"],
             superusers=set(bot_config["SUPERUSERS"]),
             nickname=set(bot_config["NICKNAME"]),
             command_start=set(bot_config["COMMAND_START"]),
             command_sep=set(bot_config["COMMAND_SEP"]),
             host=bot_config["HOST"],
             port=bot_config["PORT"])
app = nonebot.get_asgi()

nonebot.load_builtin_plugins()
nonebot.load_plugins("src/plugins")

nonebot.load_plugin("nonebot_plugin_docs")
nonebot.load_plugin("nonebot_plugin_test")
nonebot.load_plugin("nonebot_plugin_status")

if __name__ == "__main__":
    nonebot.run(app="bot:app")
