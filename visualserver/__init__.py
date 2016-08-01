#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-7-25 下午2:58
# @Author  : youzeshun
import cache
import query
import api
from public import timerctrl
from public import rwtext
from public.define import *


def Init(sLogPath, sRootPath):
    SetGlobalManager('rootpath', sRootPath)  # 脚本的根路径，用于寻找资源
    SetGlobalManager('log', rwtext.CRWText(sLogPath))
    SetGlobalManager("timer", timerctrl.CTimerManager())


def Start():
    cache.PeriodCache()
