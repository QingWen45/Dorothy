#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : __init__.py.py
# @Time : 2020/12/10 9:17
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

import ujson
from pathlib import Path
from typing import Optional


def func_switcher(func_name: str, enabled: bool, group: Optional[str] = None) -> str:
    SWITCH_FILE = Path("./src/utils/func_switch/switch_list.json")
    if not SWITCH_FILE.is_file():
        data = {}
    else:
        with open(SWITCH_FILE, 'r') as file:
            data = ujson.load(file)

    if group:
        if func_name not in data:
            data[func_name] = {}
        data[func_name][group] = str(enabled)

        with open(SWITCH_FILE, 'w') as file:
            ujson.dump(data, file)
        if enabled:
            return f"{func_name} is enabled for this group"
        else:
            return f"{func_name} is disabled for this group"

    if func_name not in data:
        data[func_name] = {}
    data[func_name]["all_enabled"] = str(enabled)

    with open(SWITCH_FILE, 'w') as file:
        ujson.dump(data, file)
    if enabled:
        return f"{func_name} is globally enabled"
    else:
        return f"{func_name} is globally disabled"
