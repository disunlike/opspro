# -*- coding:utf-8 -*-
'''
Created on Feb 15, 2016
author: youzeshun  (IM: 8766)
用途：获得开机时间的时间戳
'''

import basecmd
import os

class CCmd(basecmd.CBaseCmd):
	def __init__(self):
		super(CCmd,self).__init__()
		self.m_ShellDict={
						'uptime':'cat /proc/uptime|awk -F. \'{print $1}\''
						}
		
	def Start(self):
		self.Clear()
		self.Exec()
		self.FormatResult()
		return self.m_ResultDict['uptime']
	
	
	def Exec(self):
		self.m_ResultDict['uptime']=os.popen(self.m_ShellDict['uptime']).read()
	
	
	def FormatResult(self):
		#Exec可能还没运行
		if not self.m_ResultDict:
			raise Exception(self.m_ErrorDict[1])
		#已经转换过了，继续转会报警
		if isinstance(self.m_ResultDict['uptime'],int):
			raise Exception(self.m_ErrorDict[2])
		self.m_ResultDict['uptime']=self.m_ResultDict['uptime'].rstrip()
		self.m_ResultDict['uptime']=int(self.m_ResultDict['uptime'])

