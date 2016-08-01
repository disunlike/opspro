# -*- coding:utf-8 -*-
'''
Created on Feb 4, 2016
author: youzeshun  (IM: 8766)
��;������������ı�����
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
				sText='�����ڻ��޷���ȡ:%s'%(sLogPath)
				Log('status/checkkernlog',sText)
				return 0
			sStatusText+='\n��־��%s������'%(sLogPath)
		Log('status/checkkernlog',sStatusText)
		return 1
	
	
	def GetIM(self,sFilePath):
		lstIM=gsconf.CHECKLOG_LOG_DICT[sFilePath]['imalert']
		return lstIM
	
	
	def Format(self,sIP,sFileName,sContent):
		sText='����־��顿\nIP:%s\n��־��:%s\n%s'%(sIP,sFileName,sContent)
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
	
	
	#����syslog����kern.log���󼶱��ڣ����ϵĶ�������һ����־�ļ�
	def Init(self):
		if self.CheckFile(gsconf.CHECKLOG_LOG_DICT):
			Log('status/checkkernlog','��ʼ������־������')
			self.m_IsOpen=True
			return 1
		Log('status/checkkernlog','��־�������ʼ��ʧ�ܣ��޷������־����')
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
			# ��־������ֹͣ��������
			self.EndProgress('��־�����ڣ��޷������־�����̽���')
			return
		ExecManagerFunc('newlog','Start')
		dNewLog=GetNewLog()
		self.DealNewLog(dNewLog)
		Remove_Call_Out('checkkernlog')
		Call_Out(Functor(self.Start),gsconf.CHECKLOG_PERIOD,'checkkernlog')
