# -*- coding: utf-8 -*-

'''
	各项目常用的方法
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


#获得当前时间的指定格式，如%s,获得当前时间的字符串时间戳,%S获得当前的秒针
def GetTime(sFormat="%Y-%m-%d %H:%M:%S"):
	sTime=time.strftime(sFormat,time.localtime())
	return sTime


#获得整形的时间戳
def GetSecond(sUnit='s'):
	FTime=time.time()
	if sUnit=='s':
		return int(FTime)
	elif sUnit=='ms':
		return int(FTime*1000)
	elif sUnit=='us':
		return int(FTime*1000*1000)


#格式化指定的时间戳
def FormatTime(iTime,sFormat="%Y-%m-%d %H:%M:%S"):
	if not isinstance(iTime, int):
		iTime=int(iTime)
	oTime=time.localtime(iTime)
	sTime=time.strftime(sFormat,oTime)
	return sTime


def Call_Out(cbfunc,iDelay,sFlag,iPeriod=False): #参数：一个回调函数，延迟，标志
	oManager=GetGlobalManager("timer")
	if not oManager:
		return
	oManager.Register(cbfunc,iDelay,sFlag,iPeriod)


def Remove_Call_Out(sFlag):
	oManager=GetGlobalManager("timer") #获得全局变量中的timer，时间类的对象，他是一个负责计时
	if not oManager:
		return
	oManager.UnRegister(sFlag)


def ExecManagerFunc(sMode,sFunc,*args):
	oManager=GetGlobalManager(sMode)
	if oManager:
		func=getattr(oManager,sFunc)
		return func(*args)
	#sMode对象是不会销毁的，它是主进程。只有可能在执行的初期因为变量值不当或初始化异常而报错
	sError='错误：没有对应模式%s的全局变量对象'%(sMode)
	raise Exception(sError)

class Functor:
	"""
	构造任意参数的Callback函数类。
	@ivar _fn:          Callback函数
	@type _fn:          function
	@ivar _args:        参数
	@type _args:        tuple
	"""

	def __init__(self,fn,*args):
		"""
		构造函数。
		@param fn:          Callback函数
		@type fn:           function
		@param args:        参数
		@type args:         tuple
		"""
		self._fn=fn
		self._args=args
		self.m_Type=""

	def __call__(self,*args):
		"""
 		调用Callback函数fn。
		@param args:        参数
		@type args:         tuple
		@return:            Callback函数的返回值
		"""
		return self._fn(*(self._args+args))

	def Type(self):
		return self.m_Type

	def SetType(self,a):
		self.m_Type=a
