# -*- coding:utf-8 -*-
'''
Created on Mar 8, 2016
author: youzeshun  (IM: 8766)
用途：ping协议
'''
from net.netconf import *
from public.define import *
import baseprotocol

class CPPing(baseprotocol.CBaseProtocol):
	def __init__(self,sMode):
		self.m_Mode=sMode
	
	#向所有正常的Socket发送探测链路是否正常的ping包协议
	def Ping(self,SocketDict,BadSocketList):
		for iSocketID,SocketInfoDict in SocketDict.items():
			if iSocketID in BadSocketList:
				continue
			dSourceData=self.GetSourceData()
			cbfunc=Functor(self.Callback,iSocketID,SocketDict)#PingCallback用于处理接受到的Ping协议包。第三个参数是接受到的数据
			#这里的self.Send会从继承树的底层找起，必须避免这个方法被覆盖
			ExecManagerFunc(self.m_Mode,'ManagerSend',SocketInfoDict['socketobj'],dSourceData,0,cbfunc)
			
	def GetSourceData(self):
		dData={
			"action"	:"ping",
			"time"		:GetSecond('us'),
		}
		return dData
	
	def Respond(self,dData):
		iSocketID=dData['socketid']
		dRespondData={
			'action':'r_ping',
			'time':dData['time'],
			'uuid':dData['uuid'],
			'recode':RECODE_NORMAL
			}
		return dRespondData,iSocketID

	#两种情况调用
	def Callback(self,iSocketID,SocketDict,dRespondData):
		#根据ping的结果处理socket
		GetGlobalManager('')
		#socket可能已经被删除
		if iSocketID not in SocketDict:
			return
		recode=dRespondData["recode"]
		if recode==-1:
			#ping协议也许能整体搬到C引擎中
			self.TimeOut(iSocketID,SocketDict)
			return
		if recode==1:
			self.Normal(iSocketID,SocketDict)
			iStartTime=dRespondData['time']
			iEndTime=GetSecond('us')
			iLostTime=iEndTime-iStartTime
	
		#socket的断开有两种机制判断：1.pingself.m_Mode超时 2.发送数据的父类发生了错误
	def TimeOut(self,iSocketID,SocketDict):
		if iSocketID not in SocketDict:
			return
		oJsonSocket=SocketDict[iSocketID]['socketobj']
		oJsonSocket.m_LossPacket+=1
		print '丢包次数',oJsonSocket.m_LossPacket
		if oJsonSocket.m_LossPacket>3:
			print '超时'
			ExecManagerFunc(self.m_Mode,'DisConnect',iSocketID)
	
	def Normal(self,iSocketID,SocketDict):
		if iSocketID not in SocketDict:
			print '意料之外的状况：一个正常收到ping包的socket居然不存在。'
			return
		oJsonSocket=SocketDict[iSocketID]['socketobj']
		oJsonSocket.m_LossPacket=0
		
