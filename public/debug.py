# -*- coding:utf-8 -*-
'''
Created on 2016/4/22
author: youzeshun  (IM: 8766)
用途：
	不修改正式代码的情况下对als项目进行测试
	
原理：
	用户输入的第一个参数为g_GlobalManagerDict的键名
	用户输入的第二个参数为g_GlobalManagerDict键值的模块方法
	用于输入的第三个参数为方法的参数（可选）

Demo:
	#测试als项目的报警模块（alert）下的函数
	python opspro/debugals.py --mod=alert --func=Alert --argv=8766,AlertMsg

参数：
	--mod		:	模块名称
	--func		:	函数名
	--argv		:	参数，使用逗号隔开
	--startup	:	是否启动程序
'''

import sys
import getopt
import re
import traceback
from public.define import *
import time

g_LogPath='/tmp/tmplog'		#日志的位置
g_RootPath=''				#基本根目录的位置，用于找程序根据位置找资源
		
def GetOpt():
	OptList,Args = getopt.getopt(sys.argv[1:],'',['mod=','func=','argv=','startup=','runtime='])
	#参数的解析过程,长参数为--，短参数为-  
	sMod=sFunc=sSim=sRunTime=''
	lstArgv=[]
	for sOption, sValue in OptList:
		if sOption in ["--mod"]:
			sMod=sValue
		elif sOption in ["--func"]:
			sFunc=sValue
		elif sOption in ["--argv"]:
			sArgv=sValue
			lstArgv=re.split(r'[,]',sArgv)
		elif sOption in ["--startup"]:
			sSim=sValue
		elif sOption in ["--runtime"]:
			sRunTime=sValue
	return sMod,sFunc,lstArgv,sSim,sRunTime


#多数模块是这样初始化的
def InitMod(dLocal,sSim):
	if not 'Init' in dLocal:
		print '没有Init方法，无法初始化'
		EndTest()
	cbfunc=dLocal['Init']
	cbfunc(g_LogPath,g_RootPath)
	if sSim==1 and 'Start' in dLocal:
		cbfunc=dLocal['Start']						#有些测试仅仅初始化函数就好，不需要启动程序！
		cbfunc()
		
def ExecComeBack(cbfunc,*ArgvList):
	if ArgvList:
		Result= cbfunc(*ArgvList)
	else:
		Result= cbfunc()
	if Result:
		print Result

#对指定的模块进行测试
def TestMod(sMod,sFunc,*lstArgv):
	if not sMod in g_GlobalManagerDict:
		print '模块%s不存在'%(sMod)
		return
	oMod=g_GlobalManagerDict[sMod]
	cbfunc=getattr(oMod,sFunc,None)
	
	if not cbfunc:
		print '模块%s下的方法%s不存在'%(sMod,sFunc)
		return
	ExecComeBack(cbfunc,*lstArgv)

#线程自杀，如果日志文件不在tmplog中则需要清除
def EndTest():
	sShellCmd="ps -ef|grep %s|grep -v grep|awk '{print $2}'|xargs kill"%(sys.argv[0])
	ExecShell(sShellCmd)	#如果linux处于监视模式下，后台进程被kill杀死会打印出Terminated,set +m推出监视模式
	
def Debug(dLocal):
	sMod,sFunc,lstArgv,sSim,sRunTime=GetOpt()
	if not sFunc:
		print '必须有函数名'
		return
	InitMod(dLocal,sSim)						#初始化模块的环境
	try:
		if sMod:
			TestMod(sMod,sFunc,*lstArgv)	#测试模块的函数
		elif sFunc in dLocal:
			cbfunc=dLocal[sFunc]
			ExecComeBack(cbfunc,*lstArgv)
		else:
			print '没有找到方法%s'%(sFunc)
	except Exception as oErr:
		print oErr
		traceback.print_exc()
	finally:#杀死线程，结束程序
		if sRunTime:
			time.sleep(int(sRunTime))
		EndTest()
		
