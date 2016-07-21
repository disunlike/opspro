# -*- coding:utf-8 -*-
'''
Created on Mar 4, 2016
author: youzeshun  (IM: 8766)

对于坏的socket如何处理？由主线程负责删除（只能用主线程删，不允许子现场修改MasterSocket的SocketDict）
'''

from net import jsonsocket
import clsconf
from public.define import *

class CMasterSocket(jsonsocket.CSocketManager):
	def __init__(self):
		self.m_Mode='collectserver'
		super(CMasterSocket,self).__init__(self.m_Mode)
	
	#self.ManagerSend(SocketInfoD     ict['socketobj'],dData,0,cbfunc)
	def Send(self,dData):
			
		sAction=dData['action']
		cbfunc=self.GetCallback(sAction)
		
			#这里可能会消耗额外内存，可以用字符串来代替这个回调
		for iSocketID,SocketInfo in self.m_SocketDict.items():
			SocketObj=SocketInfo['socketobj']
			cbfunc=Functor(cbfunc,iSocketID,dData)
			super(CMasterSocket,self).ManagerSend(SocketObj,dData,0,cbfunc)
	
	#重发一定知道需要发给谁
	def ReSend(self,dData,iSocketID):
		print '向{0} 重发数据{1}'.format(iSocketID,dData)
		sAction=dData['action']
		cbfunc=self.GetCallback(sAction)
		if iSocketID and iSocketID in self.m_SocketDict:
			SocketObj=self.m_SocketDict[iSocketID]['socketobj']
			cbfunc=Functor(cbfunc,iSocketID,dData)
			super(CMasterSocket,self).ManagerSend(SocketObj,dData,0,cbfunc)
	
	def GetCallback(self,sAction):
		if sAction[:2] == 'r_':			#回复的数据不需要使用回调
			return None
		sManagerName='p%s'%(sAction)	#p_开头的表示协议
		oManager=GetGlobalManager(sManagerName)
		if not oManager:
			raise Exception('初始化错误：没有初始化psql')
		return oManager.Callback
	
	#模式Collect Server
	def Start(self):
		self.HeartBeat()
		self.CreateSocket(clsconf.DATACENTER_SOCKET_INFO)
	
	def HeartBeat(self):
		Remove_Call_Out('socket.heartbeat')
		Call_Out(self.HeartBeat,clsconf.HEARTBEAT_INTERVAL,'socket.heartbeat')
		self.m_HeartBeat+=1
		#重连不由数据中心发起
		if self.m_HeartBeat%3==0 and ( self.m_WaitConnectList or self.m_BadSocketList ):
			self.ReConnectSocket()
		if self.m_HeartBeat%2==0:
			ExecManagerFunc('pping','Ping',self.m_SocketDict,self.m_BadSocketList)
		self.CheckTimeOut()
		
		#如果有等待连接的Socket信息则进行创建
		print '心跳',self.m_HeartBeat
	
	def ReConnectSocket(self):
		NewList=self.m_WaitConnectList+self.m_BadSocketList
		#这里需要去除重复
		NewList = set(NewList)
		NewList = [i for i in NewList]
		del self.m_BadSocketList[:]
		self.m_WaitConnectList=super(CMasterSocket,self).ReConnectSocket(NewList)
		
