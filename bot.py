#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : bot.py
# @Time : 2020/12/7 13:08
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import nonebot

# You can pass some keyword args config to init function
nonebot.init(_env_file=".env.dev")
app = nonebot.get_asgi()

nonebot.load_builtin_plugins()
nonebot.load_plugins("src/plugins")
nonebot.load_plugin("nonebot_plugin_docs")
nonebot.load_plugin("nonebot_plugin_test")
nonebot.load_plugin("nonebot_plugin_status")

if __name__ == "__main__":
    nonebot.run(app="bot:app")