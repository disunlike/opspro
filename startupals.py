# -*- coding:utf-8 -*-
'''
Created on Feb 26, 2016
author: youzeshun  (IM: 8766)
用途：启动报警服务
'''

import getopt
import sys
from alertserver import *

def GetOpt():
	optList,args = getopt.getopt(sys.argv[1:],'',['logpath=','rootpath=',])

	#参数的解析过程,长参数为--，短参数为-  
	for sOption, sValue in optList:  
		if  sOption in ["--logpath"]:
			sLogPath=sValue
		elif sOption in ["--rootpath"]:
			sRootPath=sValue
		
	if not locals().has_key('sLogPath'):
		raise UnboundLocalError("必须设置日志的路径")
	if not locals().has_key('sLogPath'):
		raise UnboundLocalError("必须设置程序的根路径(用于python调用shell脚本)")
		
	return sLogPath,sRootPath

def StartUpALS():
	sLogPath,sRootPath=GetOpt()
	Init(sLogPath,sRootPath)
	Start()

if __name__=='__main__':
	StartUpALS()
	
