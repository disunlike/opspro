# -*- coding: utf-8 -*-
'''
用于im火星报警

测试指令：
	 python opspro/debugals.py --mod=alert --func=Alert --argv=8766,ff
'''
from define import *
import os

g_SpecialSymbol={
				#'%':'%25',这个符号必须单独进行替换
				'+'		:	'%2B',
				' '		:	'%20',
				'/'		:	'%2F',
				'?'		:	'%3F',
				'#'		:	'%23',
				'&'		:	'%26',
				'\n'	:	'%0a',
				'='		:	'%3D',
				}

#一些在url出现的字符必须被过滤掉，比如空格等
def ContentFilter(sContent):
	if not isinstance(sContent,str):
		return sContent #只有字符串才需要进行编码的检查
	sContent=sContent.replace('%','%25')#单独替换百分号，然后再遍历替换其他特殊符号。否则其他符号会被百分号替换掉
	for sSpecialSymbol,sUrlEncoding in g_SpecialSymbol.items():
		sContent=sContent.replace(sSpecialSymbol,sUrlEncoding)
	return sContent


def GetAlertUrl(sContent,sIMNumber):
	sIMNumber=str(sIMNumber)
	sContent=str(sContent)
	sUrl="http://im.2980.com:8088/sendmsg?key=public_server_waring&accounts=%s&content=%s"%(sIMNumber,sContent)
	return sUrl


#基于wget命令的报警，需在linux中使用。
#wget对一些特殊符号会出现报警不正常的情况
def AlertLinux(sContent,sIMNumber):
	sEncodingContent=ContentFilter(sContent)
	sUrl=GetAlertUrl(sEncodingContent,sIMNumber)
	#--quiet 安静模式，--spider 不下载  --tries表示报警次数  & 后台进行，当网络不可访问的时候不会引起阻塞
	#可能是wget命令的bug。当使用--tries部分报价会失败
	sShellCmd="wget --quiet -O /dev/null '%s' &"%(sUrl)
	ExecShell(sShellCmd)

'''
	说明：
		通用报警，能在windows下使用
		基类提供报警，并且保证报警可靠。报警一定能成功（错误重报功能）
	语法：
		oCommonAler.Alert(IMNumber,sAlertMsg,iReAlertNum=0,sLogName=PATH_LOG_ALERT_HISTORY)
	注意：
		网络质量差的情况下，该报警会发生阻塞直到超时。因而不推荐使用此类
'''
import urllib2
import random
class CCommonAlert(object):
	m_RegisterCode=0
	#这个方法也使用默认值是为了能不使用AlertManager的时候单独使用这个函数能有默认值
	def Alert(self,Content,IMNumber,iReAlertNum=0,sLogName=PATH_LOG_ALERT_HISTORY):
		sEncodingContent=ContentFilter(Content)
		sUrl=GetAlertUrl(IMNumber,sEncodingContent)
		try:
			ResponseObj=urllib2.urlopen(sUrl)
		except urllib2.URLError as oError:
			self.FailAlert(str(oError.reason),IMNumber,Content,iReAlertNum,sLogName)
		else: 
			self.CheckResponse(ResponseObj,sLogName,Content)
	
	
	#处理失败的报警
	def FailAlert(self,sReason,IMNumber,Content,iReAlertNum,sLogName):
		if iReAlertNum<0:
			sText='【IM报警失败】%s【内容】%s'%(sReason,Content)
			Log(PATH_LOG_ERR,sText)
			return
		iReAlertNum=self.ReAlertNum(iReAlertNum)
		#只对已经确定了是网络问题导致的报警失败进行重报
		if sReason=='[Errno -3] Temporary failure in name resolution':
			Log(sLogName,'域名无法解析【延迟报警】%s'%(Content))
			self.DealReAlert(IMNumber,Content,iReAlertNum,sLogName)
			return
		sText='【IM报警失败】%s【内容】%s'%(sReason,Content)
		Log(PATH_LOG_ERR,sText)
	
	
	def ReAlertNum(self,iReAlertNum):
		iReAlertNum-=1
		return iReAlertNum
	
	
	def GetRegisterCode(self):
		if self.m_RegisterCode>8000:
			self.m_RegisterCode=0
		self.m_RegisterCode+=1
		sRegisterCode='realert%i'%(self.m_RegisterCode)
		return sRegisterCode
	
	
	def DealReAlert(self,IMNumber,Content,iReAlertNum,sLogName):
		sTime=GetTime()
		iDelayTime=random.randint(120,300)
		sRegisterCode=self.GetRegisterCode()
		Call_Out(Functor(self.ReAlert,IMNumber,Content,sTime,iReAlertNum,sLogName),iDelayTime,sRegisterCode)


	#对网络原因引起的报警失败进行定时重报
	#这里没有限制重报的次数是一个安全隐患
	def ReAlert(self,IMNumber,Content,sTime,iReAlertNum,sLogName):
			sNowContent="【重报】%s %s"%(sTime,Content)
			sEncodingContent=self.ContentFilter(sNowContent)
			sUrl=self.GetAlertUrl(IMNumber,sEncodingContent)
			try:
				ResponseObj=urllib2.urlopen(sUrl)
			except urllib2.URLError as oError:
				sText='【IM报警失败】%s【失败的链接】%s'%(oError.reason,sUrl)
				Log(sLogName,sText)
				self.FailAlert(oError.reason,IMNumber,Content,iReAlertNum,sLogName)
			else:
				self.CheckResponse(ResponseObj,sLogName,Content)
	
	
	#该方法依赖IM的返回值，会有维护问题
	def CheckResponse(self,ResponseObj,sLogName,Content):
		if not isinstance(sLogName,str):
			sText='警告：日志的路径必须是字符串。错误的日志路径：%s'%(sLogName)
			Log(PATH_LOG_WARNNING,sText)
			return
		sResult=ResponseObj.read()
		sContent=str(Content)
		if sResult=='0|OK':
			sText='【IM报警成功】%s'%(sContent)
			
		else:
			sText='【IM报警失败】%s'%(sContent)
			Log(PATH_LOG_WARNNING, sText)


#解决重复报警的问题
class CAlertManager(object):
	def __init__(self):
		self.m_AlertRecord={}
		self.m_oCommonAler=CCommonAlert()
	
	
	def Register(self,sAlertMsg):
		iTime=GetSecond('us')				#这个单位一定要非常小，小到即使连续执行报警，也不会发生键名重复
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
			sBody=AlertMsg['body']				#报警的相关数据
		else:
			sErr='不可使用的类型:%s，AlertMsg:%s'%(type(AlertMsg),AlertMsg)
			Log(PATH_LOG_ERR, sErr)
			return '',''
		if not isinstance(sTitle,str):
			sTitle=str(sTitle)
		if not isinstance(sBody,str):
			sBody=str(sBody)
		return sTitle,sBody
	
	
	def Alert(self,AlertMsg,IMNumber,iReAlertNum=COUNT_ALERT_RETRY,sLogName=PATH_LOG_ALERT_HISTORY):
		self.UpdateRecord()						#删除10分钟以前尝试的报警记录
		Title,sAlertMsg=self.CustomMsg(AlertMsg)
		sNameRegister=str(IMNumber)+str(Title)	#相同的报警是发给相同火星号的相同消息
		if self.IsReAlert(sNameRegister):
			return
		self.Register(sNameRegister)
		Log(sLogName,sAlertMsg)
		#self.m_oCommonAler.Alert(IMNumber,sAlertMsg,iReAlertNum,sLogName)
		AlertLinux(sAlertMsg,IMNumber)

