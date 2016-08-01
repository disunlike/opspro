# -*- coding:utf-8 -*-
'''
����ʱ��: Mar 18, 2016
����: youzeshun  (IM: 8766)
��;:��Ϸ��ר�ñ���
'''
import os
from public.define import *
import gsconf
import subprocess

URL_QUOTE_SAFE="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
URL_QUOTE_MAP={}

#��׼ASCIIֻ��128���ַ�������IBM��չΪ256���ַ�
#Byte�������ͣ��ֽ��ͣ���һ���ֽڣ�Byte�����棬������256�����֡�ÿ�����ֶ���ΨһASCII��Ӧ
for i in xrange(256):
	k=v=chr(i)
	#���ascii���ڰ�ȫ�ַ��У������Ѿ�������չ���֡�����תΪ16���� 
	if i>=128 or not v in URL_QUOTE_SAFE:
		v="%%%02X"%i			#%02X��ʾתΪ16���ƣ�%%��ʾ���%����
	URL_QUOTE_MAP[k]=v			#ת�����ֵ����վת��

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
		#�÷�������ֵĻ��ƣ���ͬ�µ��ö�θ÷�����ʱ�򣬸÷�����ʧЧ��
		oPopen=subprocess.Popen(sShellCmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		#��ʹ������������stdout����������̫�࣬�ᳬ��ϵͳ��buffer�����³��򱻿�ס������ķ������ᵼ�³�������
		oPopen.communicate()
		
		
#����ظ�����������
class CAlertManager(object):
	
	def __init__(self):
		self.m_AlertRecord={}
		self.m_oGSAler=CGSAlert()
	
	
	def Register(self,sAlertMsg):
		iTime=GetSecond('us')						#�����λһ��Ҫ�ǳ�С��С����ʹ����ִ�б�����Ҳ���ᷢ�������ظ�
		self.m_AlertRecord[iTime]=sAlertMsg
	
	
	def IsReAlert(self,sNameRegister):
		for k,v in self.m_AlertRecord.items():
			if sNameRegister==v:
				sDebug='�����ظ��ı�����ע������%s'%(sNameRegister)
				Log(PATH_LOG_DEBUG,sDebug)
				return 1
		return 0
	
	
	def UpdateRecord(self):
		iNowTime=GetSecond('us')
		dTmp={}
		for k,v in self.m_AlertRecord.items():
			if iNowTime-k<TIME_REALERT*1000*1000:	#���뻻�㵽������бȽ�
				dTmp[k]=v
		self.m_AlertRecord=dTmp
	
	
	def CustomMsg(self,AlertMsg):
		if isinstance(AlertMsg,str):
			sTitle=sBody=AlertMsg
		elif isinstance(AlertMsg,dict):
			sTitle=AlertMsg['title']				#�����Ľ���
			sBody=AlertMsg['body']					#�������������
		else:
			sErr='����ʹ�õ����ͣ�AlertMsg:%s'%(AlertMsg)
			Log(PATH_LOG_ERR, sErr)
			return '',''
		if not isinstance(sTitle,str):
			sTitle=str(sTitle)
		if not isinstance(sBody,str):
			sBody=str(sBody)
		return sTitle,sBody
	
	
	def Alert(self,AlertMsg,IMNumber,iReAlertNum=COUNT_ALERT_RETRY,sLogName=PATH_LOG_ALERT_HISTORY):
		self.UpdateRecord()							#ɾ��10������ǰ���Եı�����¼
		title,sAlertMsg=self.CustomMsg(AlertMsg)
		sNameRegister=str(IMNumber)+str(title)		#��ͬ�ı����Ƿ�����ͬ���Ǻŵ���ͬ��Ϣ
		if self.IsReAlert(sNameRegister):
			return
		self.Register(sNameRegister)
		Log(sLogName,sAlertMsg)
		self.m_oGSAler.Alert(sAlertMsg,IMNumber)
		
