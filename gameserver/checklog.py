# -*- coding:utf-8 -*-
'''
Created on Feb 4, 2016
author: youzeshun  (IM: 8766)
用途：检查新增的文本内容
'''

from public.define import *
import os
import gsconf
from public import path
from gameserver.define import *

class CCheckLog():
	
	def __init__(self):
		self.m_IsOpen=False
		self.m_IP=GetGlobalManager('ip')
	
	
	def CheckFile(self,LogDict):
		sStatusText=''
		for sLogPath in LogDict:
			if not os.path.isfile(sLogPath) or not os.access(sLogPath,os.R_OK):
				sText='不存在或无法读取:%s'%(sLogPath)
				Log('status/checkkernlog',sText)
				return 0
			sStatusText+='\n日志：%s已生成'%(sLogPath)
		Log('status/checkkernlog',sStatusText)
		return 1
	
	
	def GetIM(self,sFilePath):
		lstIM=gsconf.CHECKLOG_LOG_DICT[sFilePath]['imalert']
		return lstIM
	
	
	def Format(self,sIP,sFileName,sContent):
		sText='【日志检查】\nIP:%s\n日志名:%s\n%s'%(sIP,sFileName,sContent)
		return sText
	
	
	def DealNewLog(self,dNewLog):
		if not dNewLog:
			return
		for sFilePath,sContent in dNewLog.items():
			if not sContent:
				continue
			sFileName=path.GetFileName(sFilePath)
			sText=self.Format(self.m_IP,sFileName,sContent)
			lstIM=self.GetIM(sFilePath)
			Alert(sText,lstIM)
	
	
	#配置syslog，让kern.log错误级别在３以上的都独立在一个日志文件
	def Init(self):
		if self.CheckFile(gsconf.CHECKLOG_LOG_DICT):
			Log('status/checkkernlog','开始运行日志检查程序')
			self.m_IsOpen=True
			return 1
		Log('status/checkkernlog','日志检查程序初始化失败，无法检查日志更新')
		self.m_IsOpen=False
		return 0

	def EndProgress(self, sReason):
		sParameter = 'stop gs'
		sScriptName = 'promanager.sh'
		sScriptPath = GetGlobalManager('rootpath')
		sCommand = "%s/%s %s" % (sScriptPath, sScriptName, sParameter)
		Log('status/checkkernlog', sReason)
		ExecShell(sCommand)


	def Start(self):
		if not self.m_IsOpen:
			# 日志不存在停止整个程序
			self.EndProgress('日志不存在，无法检查日志，进程结束')
			return
		ExecManagerFunc('newlog','Start')
		dNewLog=GetNewLog()
		self.DealNewLog(dNewLog)
		Remove_Call_Out('checkkernlog')
		Call_Out(Functor(self.Start),gsconf.CHECKLOG_PERIOD,'checkkernlog')
