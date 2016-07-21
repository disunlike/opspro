# -*- coding:utf-8 -*-
'''
创建时间: Mar 18, 2016
作者: youzeshun  (IM: 8766)
用途:游戏服专用报警
'''
import os
from public.define import *
import gsconf
import subprocess

URL_QUOTE_SAFE="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
URL_QUOTE_MAP={}

#标准ASCII只有128个字符，后来IBM扩展为256个字符
#Byte数据类型（字节型）用一个字节（Byte）储存，可区别256个数字。每个数字都有唯一ASCII对应
for i in xrange(256):
	k=v=chr(i)
	#如果ascii不在安全字符中，或者已经到了扩展部分。则将其转为16进制 
	if i>=128 or not v in URL_QUOTE_SAFE:
		v="%%%02X"%i			#%02X表示转为16进制，%%表示输出%符号
	URL_QUOTE_MAP[k]=v			#转换后的值由网站转回

def UrlQuote(s):
	return "".join(map(URL_QUOTE_MAP.__getitem__,s))


class CGSAlert():
	
	def __init__(self):
		self.m_AlertScriptPath=gsconf.PATH_SCRIPT_ALERT
		self.m_AlertLog=GetGlobalManager('logpath')+"/debug.txt"
	
	
	def Alert(self,AlertMsg,IMNumber):
		sEncodingContent=UrlQuote(AlertMsg)
		sShellCmd='sh %s %s "%s" &'%(self.m_AlertScriptPath,IMNumber,sEncodingContent)
		Log(PATH_LOG_DEBUG,sShellCmd)
		#该方法有奇怪的机制，当同事调用多次该方法的时候，该方法会失效！
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
		
