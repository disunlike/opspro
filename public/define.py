# -*- coding: utf-8 -*-

'''
	����Ŀ���õķ���
'''

import time
from pubconf import *

if not globals().has_key("g_GlobalManagerDict"):
	g_GlobalManagerDict={}
	
def SetGlobalManager(sFlag,oManager):
	global g_GlobalManagerDict
	g_GlobalManagerDict[sFlag]=oManager


def GetGlobalManager(sFlag):
	global g_GlobalManagerDict
	if sFlag in g_GlobalManagerDict:
		return g_GlobalManagerDict[sFlag]
	return None
	
	
def GetManagerAttr(sMode,sAttr):
	oManager=GetGlobalManager(sMode)
	if oManager:
		sAttr=getattr(oManager,sAttr,None)
		return sAttr
	
	
#��Ϊʹ���������һ����ҪGetGlobalManager������Ҫ��import��public.define��ز�������������д����
def Log(LogPath,Content):
	if not LogPath or not Content:
		return
	oManager=GetGlobalManager("txtlog")
	if not oManager:
		raise Exception('���벻���Ĵ���txtlogû�б���ʼ��')
	#������ת���б�Ĳ���������
	if isinstance(Content,list) or isinstance(Content,dict) or isinstance(Content,int):
		oManager.Write(LogPath,str(Content))
	elif isinstance(Content,str):
		oManager.Write(LogPath,Content)


#�����ڲ�ͬ�������ȷ���ñ���ģ��
def Alert(Content,IMNumberList,iReAlertNum=0,sLogName=PATH_LOG_ALERT_HISTORY):
	if not Content or not IMNumberList:
		Log(PATH_LOG_INFO,'û�д��������Ķ��������')
		return
	oManager=GetGlobalManager("alert")
	if not oManager:
		Log(PATH_LOG_ERR,'���棺alertû�б���ʼ��')
		return
	#���Ǻ�ֻ�����б�
	if not isinstance(IMNumberList,list):
		IMNumberList=[IMNumberList]
	#Contentֻ�����ֵ�����б�
	if not isinstance(Content,dict) and not isinstance(Content,list):
		Content=[Content]
	
	if isinstance(Content,list):
		TmpList=[]
		for IMNumber in IMNumberList:
			if IMNumber in TmpList:		#�б��п������ظ��Ļ��Ǻţ�����Ҫ�ظ�����
				continue
			TmpList.append(IMNumber)
			for sContent in Content:
				oManager.Alert(sContent,IMNumber,iReAlertNum,sLogName)
	elif isinstance(Content,dict):
		for IMNumber in IMNumberList:
			oManager.Alert(Content,IMNumber,iReAlertNum,sLogName)


def ExecShell(sShellCmd):
	if not sShellCmd:
		return
	ShellCmdDict=GetGlobalManager('shelldict')
	if not ShellCmdDict:
		raise Exception('���벻���Ĵ���shelldictû�б���ʼ��')
	if ShellCmdDict.has_key(sShellCmd):
		oShellCmd=ShellCmdDict[sShellCmd]
		Result=oShellCmd.Start()
		return Result
	else:
		oCustomCmd=ShellCmdDict['custom']
		oCustomCmd.SetShellCmd(sShellCmd)
		Result=oCustomCmd.Start()
		return Result
	
	
#��õ�ǰʱ���ָ����ʽ����%s,��õ�ǰʱ����ַ���ʱ���,%S��õ�ǰ������
def GetTime(sFormat="%Y-%m-%d %H:%M:%S"):
	t=time.localtime()
	sTime=time.strftime(sFormat,t)
	return sTime


#������ε�ʱ���
def GetSecond(sUnit='s'):
	FTime=time.time()
	if sUnit=='s':
		return int(FTime)
	elif sUnit=='ms':
		return int(FTime*1000)
	elif sUnit=='us':
		return int(FTime*1000*1000)


#��ʽ��ָ����ʱ���
def FormatTime(iTime,sFormat="%Y-%m-%d %H:%M:%S"):
	if not isinstance(iTime, int):
		iTime=int(iTime)
	oTime=time.localtime(iTime)
	sTime=time.strftime(sFormat,oTime)
	return sTime


def Call_Out(cbfunc,iDelay,sFlag,iPeriod=False): #������һ���ص��������ӳ٣���־
	oManager=GetGlobalManager("timer")
	if not oManager:
		return
	oManager.Register(cbfunc,iDelay,sFlag,iPeriod)


def Remove_Call_Out(sFlag):
	oManager=GetGlobalManager("timer") #���ȫ�ֱ����е�timer��ʱ����Ķ�������һ�������ʱ
	if not oManager:
		return  
	oManager.UnRegister(sFlag)


def ExecManagerFunc(sMode,sFunc,*args):
	oManager=GetGlobalManager(sMode)
	if oManager:
		func=getattr(oManager,sFunc)
		return func(*args)
	#sMode�����ǲ������ٵģ����������̡�ֻ�п�����ִ�еĳ�����Ϊ����ֵ�������ʼ���쳣������
	sError='����û�ж�Ӧģʽ%s��ȫ�ֱ�������'%(sMode)
	raise Exception(sError)

class Functor:
	"""
	�������������Callback�����ࡣ
	@ivar _fn:          Callback����
	@type _fn:          function
	@ivar _args:        ����
	@type _args:        tuple
	"""

	def __init__(self,fn,*args):
		"""
		���캯����
		@param fn:          Callback����
		@type fn:           function
		@param args:        ����
		@type args:         tuple
		"""
		self._fn=fn
		self._args=args
		self.m_Type=""

	def __call__(self,*args):
		"""
 		����Callback����fn��
		@param args:        ����
		@type args:         tuple
		@return:            Callback�����ķ���ֵ
		"""
		return self._fn(*(self._args+args))

	def Type(self):
		return self.m_Type

	def SetType(self,a):
		self.m_Type=a
		