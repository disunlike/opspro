# -*- coding:utf-8 -*-
'''
Created on Mar 4, 2016
author: youzeshun  (IM: 8766)
用途：启动数据采集服务
'''

import collectserver
import time
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
	collectserver.Init(sLogPath,sRootPath)
	
	#发送的时候需要将超时的回调处理一起给Send
	while True:
		collectserver.Send(
						{
							'action':'sql',
							'dbname':'gather',
							'tbname':'mem',
							'field':
									{
										'timestamp':1111111,
										'memfree':222,
									},
						})
		time.sleep(2)
	
