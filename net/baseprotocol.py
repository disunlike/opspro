# -*- coding:utf-8 -*-
'''
创建时间: Mar 25, 2016
作者: youzeshun  (IM: 8766)
用途:父类协议
'''

from public.define import *

class CBaseProtocol(object):
	
	def __init__(self,sMode):
		self.m_Mode=sMode
	
	def GetSourceData(self):
		pass
	
	def Respond(self):
		pass

	#两种情况调用
	def Callback(self):
		pass
	
	def TimeOut(self,dData,iSocketID):
		pass
	
	def LocalSave(self):
		pass
	
	#正常则检查本地缓存数据开始重发
	def Normal(self):
		pass
	
	def ReSend(self):
		pass
		
		