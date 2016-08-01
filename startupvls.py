#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-7-27 下午2:21
# @Author  : youzeshun
# 用途：定时生成json缓存文件，供可视化程序启动

import getopt
import sys
import visualserver


def GetOpt():
    optList, args = getopt.getopt(sys.argv[1:], '', ['logpath=', 'rootpath=', ])

    # 参数的解析过程,长参数为--，短参数为-
    for sOption, sValue in optList:
        if sOption in ["--logpath"]:
            sLogPath = sValue
        elif sOption in ["--rootpath"]:
            sRootPath = sValue

    if not locals().has_key('sLogPath'):
        raise UnboundLocalError("必须设置日志的路径")
    if not locals().has_key('sLogPath'):
        raise UnboundLocalError("必须设置程序的根路径(用于python调用shell脚本)")

    return sLogPath, sRootPath


def StartUp():
    sLogPath, sRootPath = GetOpt()
    visualserver.Init(sLogPath, sRootPath)
    visualserver.Start()


if __name__ == '__main__':
    StartUp()
