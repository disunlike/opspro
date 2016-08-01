# -*- coding:utf-8 -*-
# 服务器信息基类 
# 尤泽顺
# 2016年1月12日
'''
所有的采集都必须继承该类
'''

import os

class CBaseDev(object):
	
	def __init__(self):
		self.m_Name=''#这个设备的名字
		self.m_ShellCmd=''#采集该设备的命令
		self.m_FormatDict=''#返回的数据格式
	
	
	def __call__(self):
		return self.Start()
		
		
	def SetShellCmd(self,ShellCmd):
		self.m_ShellCmd=ShellCmd
	
	
	def SetPeriod(self,iPeriod):
		self.m_period=iPeriod
	
	
	def Start(self,):
		sCmdResult=self.ExecShell()
		sResult=self.FormatResult(sCmdResult)
		return sResult
	
	
	def ExecShell(self,sShellCmd=''):
		if not sShellCmd:
			sShellCmd=self.m_ShellCmd
		sCmdResult=os.popen(sShellCmd).read()
		return sCmdResult
	
	
	def FormatResult(self,sResult):
		if not sResult:
			return
		sResult=sResult.rstrip()	#shell命令的执行结果将输出到终端，因此默认多一个换行来隔开'用户名@主机名'
		return sResult
	