# -*- coding:utf-8 -*-
'''
创建时间: Mar 18, 2016
作者: youzeshun  (IM: 8766)
用途:游戏服专用报警
'''
from public.define import *
import gsconf
import subprocess

class CGSAlert():
	
	def __init__(self):
		self.m_AlertScriptPath=gsconf.PATH_SCRIPT_ALERT
		self.m_AlertLog=GetGlobalManager('logpath')+"/debug.txt"
	
	
	def Alert(self,sAlertMsg,IMNumber):
		sShellCmd='sh %s %s "%s" &'%(self.m_AlertScriptPath,IMNumber,sAlertMsg)
		Log(PATH_LOG_DEBUG,sShellCmd)
		oPopen=subprocess.Popen(sShellCmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		#不使用下述方法，stdout产生的内容太多，会超过系统的buffer。导致程序被卡住！下面的方法不会导致程序阻塞
		oPopen.communicate()
		
		
#解决重复报警的问题
class CAlertManager(object):
	
	def __init__(self):
		self.m_AlertRecord={}
		self.m_oGSAler=CGSAlert()
	
	
	def Register(self,sAlertMsg):
		iTime=GetSecond('us')						#这个单位一定要非常小，小到即使连续执行报警，也不会发生键名重复
		self.m_AlertRecord[iTime]=sAlertMsg
	
	
	def IsReAlert(self,sNameRegister):
		for k,v in self.m_AlertRecord.items():
			if sNameRegister==v:
				sDebug='发现重复的报警，注册名：%s'%(sNameRegister)
				Log(PATH_LOG_DEBUG,sDebug)
				return 1
		return 0
	
	
	def UpdateRecord(self):
		iNowTime=GetSecond('us')
		dTmp={}
		for k,v in self.m_AlertRecord.items():
			if iNowTime-k<TIME_REALERT*1000*1000:	#必须换算到纳秒进行比较
				dTmp[k]=v
		self.m_AlertRecord=dTmp
	
	
	def CustomMsg(self,AlertMsg):
		if isinstance(AlertMsg,str):
			sTitle=sBody=AlertMsg
		elif isinstance(AlertMsg,dict):
			sTitle=AlertMsg['title']				#报警的结论
			sBody=AlertMsg['body']					#报警的相关数据
		else:
			sErr='不可使用的类型，AlertMsg:%s'%(AlertMsg)
			Log(PATH_LOG_ERR, sErr)
			return '',''
		if not isinstance(sTitle,str):
			sTitle=str(sTitle)
		if not isinstance(sBody,str):
			sBody=str(sBody)
		return sTitle,sBody
	
	
	def Alert(self,AlertMsg,IMNumber,iReAlertNum=COUNT_ALERT_RETRY,sLogName=PATH_LOG_ALERT_HISTORY):
		self.UpdateRecord()							#删除10分钟以前尝试的报警记录
		title,sAlertMsg=self.CustomMsg(AlertMsg)
		sNameRegister=str(IMNumber)+str(title)		#相同的报警是发给相同火星号的相同消息
		if self.IsReAlert(sNameRegister):
			return
		self.Register(sNameRegister)
		Log(sLogName,sAlertMsg)
		self.m_oGSAler.Alert(sAlertMsg,IMNumber)
		
