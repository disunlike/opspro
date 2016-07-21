# -*- coding:utf-8 -*-
'''
Created on Mar 4, 2016
author: youzeshun  (IM: 8766)

对于坏的socket如何处理？由主线程负责删除（只能用主线程删，不允许子现场修改MasterSocket的SocketDict）
'''

from net import jsonsocket
from public.define import *
from dtsconf import *

class CMasterSocket(jsonsocket.CSocketManager):
	def __init__(self):
		self.m_Mode='dataserver'	#数据中心的运行模式，收到的数据被解析后将传递给相应模式的对象
		super(CMasterSocket,self).__init__(self.m_Mode)
		
	def Start(self):
		self.HeartBeat()
		self.Listening()
		
	#管理类的发送需要知道数据由哪个socket发出
	#JsonSocket类的Send需要保证发生符合业务的格式
	#BaseSoceket的发送需要保证发生不发生错误
	def Send(self,dData):
		if not 'socketid' in dData:
			print dData
			#这个报错只是在代码启动初期会触发，可以改为只运行一次的方式
			raise Exception('意想不到的错误：数据中心发送的数据包里没有包含表示数据发给谁的socketid键！')
		iSocketID=dData['socketid' ]
		if not iSocketID in self.m_SocketDict:
			return
		SocketObj=self.m_SocketDict[iSocketID]['socketobj']
		#数据中心通常的回复是为了告诉采集方数据已经被采集，所以不需要使用回调函数
		super(CMasterSocket,self).ManagerSend(SocketObj,dData)
	
	def HeartBeat(self):
		Remove_Call_Out('socket.heartbeat')
		Call_Out(self.HeartBeat,HEARTBEAT_INTERVAL,'socket.heartbeat')
		#最优先清除坏的socket，否则Ping的时候依然会向坏的Socket发送数据，这个数据会存回调的。效率会浪费
		self.CleanBadSocket()
		
		self.m_HeartBeat+=1
		#重连不由数据中心发起
		if self.m_HeartBeat%2==0:
			ExecManagerFunc('pping','Ping',self.m_SocketDict,self.m_BadSocketList)
		self.CheckTimeOut()
		#如果有等待连接的Socket信息则进行创建
		print '心跳',self.m_HeartBeat,'SocketDict',self.m_SocketDict
	
	#这种组织方式不行，换位nscentos那种
	def CustomCommand(self,dData):
		#数据是对数据中心的回复，那么应该调用回调。否则应该使用协议包来解析
		sAction=dData['action']
		if sAction[:2]=='r_':
			raise Exception('意想不到的错误：数据中心的管理类不应该接受到回复类型的协议')
		sProtocolName='p%s'%(sAction)
		ExecManagerFunc(sProtocolName,'Respond',dData,self.m_SocketDict)
		
