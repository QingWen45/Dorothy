#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @File : throughput_counter.py
# @Time : 2021/1/20 10:56
# @Author : QingWen
# @E-mail : hurrsea@outlook.com

class ThroughPut:
    def __init__(self):
        self.queue = [0 for i in range(60)]

    def push(self, data_num: int):
        self.queue.append(data_num)
        if len(self.queue) > 60:
            self.pop()

    def pop(self):
        self.queue.pop(0)

    def count(self):
        return sum(self.queue)
