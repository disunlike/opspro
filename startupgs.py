# -*- coding:utf-8 -*-
'''
Created on Feb 26, 2016
author: youzeshun  (IM: 8766)
用途：用于启动游戏服务器的监控
'''

import getopt
import sys
import gameserver

def GetOpt():
	lstOpt,lstArgs = getopt.getopt(sys.argv[1:],'',['logpath=','rootpath=',])
	#参数的解析过程,长参数为--，短参数为-  
	for sOption, sValue in lstOpt:  
		if  sOption in ["--logpath"]:
			sLogPath=sValue
		elif sOption in ["--rootpath"]:
			sRootPath=sValue
		
	if not locals().has_key('sLogPath'):
		raise UnboundLocalError("必须设置日志的路径")
	if not locals().has_key('sLogPath'):
		raise UnboundLocalError("必须设置程序的根路径(用于python调用shell脚本)")
		
	return sLogPath,sRootPath


#初始化游戏服务器的包，用来进行性能，数据监控
def InitGameServer(sLogPath,sRootPath):
	gameserver.Init(sLogPath,sRootPath)


def StartGameServer():
	gameserver.Start()

if __name__=='__main__':
	sLogPath,sRootPath=GetOpt()
	InitGameServer(sLogPath,sRootPath)
	StartGameServer()
	
