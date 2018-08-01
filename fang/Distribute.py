#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Author wangdechang
Time 2018/7/26
"""

import threading
import time


class Distribute(object):
    def __init__(self, NumThread, func):
        self.NumThread = NumThread
        self.func = func

    def execute(self):
        threads = []
        for i in range(self.NumThread):
            t = threading.Thread(target=self.func)
            threads.append(t)

        start = time.time()
        for i in range(self.NumThread):
            threads[i].start()
        for i in range(self.NumThread):
            threads[i].join()

        end = time.time()
        return end - start
