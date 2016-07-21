# -*- coding:utf-8 -*-
'''
Created on Mar 4, 2016
author: youzeshun  (IM: 8766)

#用于启动数据中心服务
'''

import dataserver
import getopt
import sys

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

if __name__=='__main__':
	sLogPath,sRootPath=GetOpt()
	dataserver.Init('0.0.0.0',65534,7000,sLogPath,sRootPath)
	dataserver.Start()

