# -*- coding:utf-8 -*-
'''
Created on Mar 3, 2016
author: youzeshun  (IM: 8766)

用途：处理socket发来的json

封装socket，如果效率不够则需要改为封   装C版本的socket
一些处理不是必须的，但为了统一和公共代码的格式，方便检查。将一些处理保持一致
'''
from net.define import *
from net.netconf import *
from net import basesocket
from public.define import *
import socket

class CSocketManager(object):
	def __init__(self,sMode):
		self.m_HeartBeat=0
		self.m_iSeq=0
		self.m_SocketID=0
		self.m_Mode=sMode			#数据中心的运行模式，收到的数据被解析后将传递给相应模式的对象
		self.m_SocketDict={}		#保存所有的socket
		self.m_BadSocketList=[]		#认证成功后又连接异常中断的socket
		self.m_WaitConnectList=[]	#存放等待创建SocketObj的Socket信息
		self.m_CallbackDict={}		#回调字典，当回复超时调用回调函数进行处理
	
	def SetSocket(self,sBindIP,iPort,iMaxCon):
		self.m_TcpSockObj=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.m_TcpSockObj.bind((sBindIP,iPort))
		self.m_TcpSockObj.listen(iMaxCon)
	
	def Listening(self):
		while True:
			TcpSockObj, AddrList = self.m_TcpSockObj.accept()
			#这里封装socket后的socket好还是封装后的socket好？
			sIP=AddrList[0]
			iPort=AddrList[1]
			oJsonSocket=self.CreateJsonSocket(TcpSockObj,sIP,iPort)
			oJsonSocket.m_BoolConnect=True
			oJsonSocket.Start()
	
	#如果删除的Socket是正常的，那么对端会报错：Connection reset by peer
	def CleanBadSocket(self):
		for iSocketID in self.m_BadSocketList:
			#一对socket之间的多个数据包超时能使列表重复，所以在循环中一个iSocket对应SocketObj可能已经被删除
			if self.m_SocketDict.has_key(iSocketID):
				del self.m_SocketDict[iSocketID]
		del self.m_BadSocketList[:]
	
	#根据IP和端口创建一个不存在的Socket，无论创建是否成功，都会被记录在SocketDict中
	def CreateSocket(self,SocketInfoList):
		TmpList=[]
		for InfoList in SocketInfoList:
			sIP,iPort=InfoList
			TcpSockObj=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			oJsonSocket=self.CreateJsonSocket(TcpSockObj,sIP,iPort)
			try:
				oJsonSocket.m_TcpSockObj.connect((sIP,iPort))
			except socket.error as oSocketError:
				print '创建网络连接失败:IP:%s,Port:%i'%(sIP,iPort)
				oJsonSocket.m_BoolConnect=False
				TmpList.append(self.m_SocketID)
			else:
				print '创建网络连接成功:IP:%s,Port:%i'%(sIP,iPort)
				oJsonSocket.m_BoolConnect=True
				oJsonSocket.Start()
		self.m_WaitConnectList=TmpList
	
	#一个节点可能同时是数据中心和采集服务，比如监控节点服务要求多节点共享数据。
	#数据中心和采集服务对BadSocketList的处理方式是不同的，所以两者不能合并处理
	def ReConnectSocket(self,SocketIDList):
		print '开始尝试重连',SocketIDList
		if not SocketIDList:
			print '没有需要重连的'
			return
		TmpList=[]
		for iSocketID in SocketIDList:
			print '被重连的socket信息',self.m_SocketDict[iSocketID]
			oJsonSocket=self.m_SocketDict[iSocketID]['socketobj']
			#原来的socket文件描述符已经坏了
			TcpSockObj=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			oJsonSocket.m_TcpSockObj=TcpSockObj
			sIP=self.m_SocketDict[iSocketID]['ip']
			iPort=self.m_SocketDict[iSocketID]['port']
			try:
				oJsonSocket.m_TcpSockObj.connect((sIP,iPort))
			except Exception as sException:
				print '重连失败',sException
				oJsonSocket.m_BoolConnect=False
				TmpList.append(iSocketID)
			else:
				print '重连成功:IP:%s,Port:%i'.format(sIP,iPort)
				oJsonSocket.m_BoolConnect=True
				oJsonSocket.Start()
		SocketIDList=TmpList
		return SocketIDList
	
	#记录Socket放在创建这是为了防止遗漏调用或者多调用
	def CreateJsonSocket(self,TcpSockObj,sIP,iPort):
		self.NewSocketID()
		oJsonSocket=CJsonSocket(TcpSockObj,self.m_Mode,self.m_SocketID)
		self.RecordJsonSocket(oJsonSocket,sIP,iPort)
		return oJsonSocket
	
	def RecordJsonSocket(self,oJsonSocket,sIP,iPort):
		SockInfoDict={'socketobj':oJsonSocket,'ip':sIP,'port':iPort}
		self.m_SocketDict[oJsonSocket.m_SocketID]=SockInfoDict
		
	def NewSocketID(self):
		self.m_SocketID+=1
		
	#服务器做ping当连接断开的时候不进行重来，而等待客户端重连
	def HeartBeat(self):
		Remove_Call_Out('socket.heartbeat')
		Call_Out(self.HeartBeat,HEARTBEAT_INTERVAL,'socket.heartbeat')
		self.m_HeartBeat+=1
		#重连不由数据中心发起
		#if self.m_HeartBeat%3==0:
		#	self.ReConnectSocket()
		if self.m_HeartBeat%2==0:
			ExecManagerFunc('pping','Ping',self.m_SocketDict,self.m_BadSocketList)
		self.CheckTimeOut()
		
		#如果有等待连接的Socket信息则进行创建
		if self.m_WaitConnectList:
			self.CreateSocket(self.m_WaitConnectList)
		
		#self.CleanBadSocket()
	
	def ManagerSend(self,SocketObj,dData,iEncrypt=1,cbfunc=None,iTimeOut=DEFAULT_TIME_OUT):
		#该对象可能因为可能超时而被HearBeat函数删除，此时必须终止，避免AttributeError: 'NoneType' object has no attribute 'Send'
		if not SocketObj:
			return
		sAction=dData["action"]
		if sAction=='respond' and cbfunc:
			raise Exception('用法错误：回复包不应该回调')
		if cbfunc:
			self.NewSeq()
			dData['uuid']=self.m_iSeq
			iNewTime=GetSecond()
			iEndTime=iNewTime+iTimeOut
			self.m_CallbackDict[self.m_iSeq]=(cbfunc,iEndTime,SocketObj.m_SocketID)
			
		#记录日志
		sText='send,action:%s'%(sAction)
		Log('dataserver/mastersocket',sText) 
		SocketObj.Send(dData)
	
	def NewSeq(self):
		self.m_iSeq+=1
	
	def Callback(self,dData):
		iSeq=dData['uuid']
		if iSeq not in self.m_CallbackDict:
			#可能是延迟的包
			return
		func,iEndTime,iSocketID=self.m_CallbackDict[iSeq]
		del self.m_CallbackDict[iSeq]
		func(dData)
		
	def DisConnect(self,iSocketID):
		self.m_BadSocketList.append(iSocketID)
		
	def GetSocket(self,iSocketID):
		if iSocketID in self.m_SocketDict:
			return self.m_SocketDict[iSocketID]['socketobj']
	
	#当发出的数据包超时,对于有效的数据，当发送超时后要将其保存在本地
	def CheckTimeOut(self):
		if not self.m_CallbackDict:
			return
		iNowTime=GetSecond()
		TmpList=[]
		for iSeq,cbinfo in self.m_CallbackDict.items():
			cbfunc,iEndTime,iSocketID=cbinfo
			if iEndTime>iNowTime:
				continue
			TmpList.append(iSeq)
			#该协议用于模拟超时回复，以执行超时下的逻辑
			dData={
				"action":"respond",
				"recode":-1,#状态码，-1是超时
				}
			cbfunc(dData)
		
		for iSeq in TmpList:
			del self.m_CallbackDict[iSeq]
	
	#这种组织方式不行，换位nscentos那种
	def ManagerCommand(self,dData):
		#数据是对数据中心的回复，那么应该调用回调。否则应该使用协议包来解析
		sAction=dData['action']
		if sAction[:2]=='r_':
			self.Callback(dData)
		elif sAction=='ping':
			dData,iSocketID=ExecManagerFunc('pping','Respond',dData)
			SocketObj=self.GetSocket(iSocketID)
			self.ManagerSend(SocketObj,dData)
		else:
			self.CustomCommand(dData)
	
class CJsonSocket(basesocket.CBaseSocket):
	def __init__(self,TcpSockObj,sMode,iSocketID):
		self.m_RecvCache=''
		self.m_SocketID=iSocketID	#用于注册判断连接的心跳
		self.m_Mode=sMode			#用于标记管理类是谁，因为需要把数据传递给管理类
		self.m_BoolAuth=False		#是否认证过
		self.m_LossPacket=0
		super(CJsonSocket,self).__init__(TcpSockObj)
	
	#执行Recv的时候self.m_RecvCache将被基类函数动态更改，改变不会引起错误。但继承时必须注意
	def Recv(self,Data):
		self.m_RecvCache+=Data
		while True:
			iLen=len(self.m_RecvCache)#self.m_RecvCache来自基类
			if iLen<4:
				#包大小没收齐
				break
			sSize=self.m_RecvCache[:4]
			iSize=ConverByteToInt(sSize)
			if iSize>iLen:
				#包没有接收完
				print '包没有收完'
				break
			
			packstr=self.m_RecvCache[4:iSize]#一个数据
			self.m_RecvCache=self.m_RecvCache[iSize:]#其他的数据
			
			#数据内容的第一个字节表示数据是否加密
			sEncrypt=packstr[0]
			sCmdData=packstr[1:-1]
			#数据内容的最后个字节作为内容结束的标示符，用于组合大包
			sEndChar=packstr[-1]
			
			iEncrypt=ConverByteToInt(sEncrypt)
			iEndChar=ConverByteToInt(sEndChar)
			
			#正常结束并且数据是没加密的
			if iEndChar==0 and not iEncrypt:
				#这里需要补充一个数据的解码
				dData=ConverStrToDict(sCmdData)
				dData=self.AddSign(dData)
				self.OnCommand(dData)
			else:
				print '这是测试阶段不考虑的情况'
	
	def AddSign(self,dData):
		if not isinstance(dData,dict):
			print '类型错误:数据的解析或者数据本身有错误，不是一个字典',dData
			return
		dData['socketid']=self.m_SocketID
		return dData
	
	def DelSign(self,dData):
		if 'socketid' in dData:
			del dData['socketid']
		return dData
	
	#按照协议的类型进行分发
	def OnCommand(self,dData):
		#print '接收数据',dData
		#缩小工程量，先走私网，暂不验证
		if self.AuthCommand(dData):
			print '验证不通过'
			return
		ExecManagerFunc(self.m_Mode,'ManagerCommand',dData)
		
	def AuthCommand(self,dData):
		sAction=dData["action"]
		if sAction=='getauth':
			self.GetAuth({})
			return True
		if sAction=='setstep':
			self.SetStep(dData)
			return True
		return False
	
	def GetAuth(self,dData):
		pass
	
	def SetStep(self,dData):
		pass
	
	#数据的结构：长度位(4)-是否加密(1)-字符串形式的字典数据内容(变长)-结束符(1)
	def Send(self,dData,iEncrypt=0):
		if not self.m_BoolConnect:
			return
		#print 'JsonSend',dData
		#删除标记Socket标记，标记用于给Socket管理类从Socket字典中找到对应的Socket
		dData=self.DelSign(dData)
		
		sData=ConverDictToStr(dData)
		if iEncrypt:
			pass
		sIsEncrypt=ConvertIntToByte(iEncrypt,1)#用一位1来表示数据是否经过加密
		sEndChar=ConvertIntToByte(0,1)#用一位0来表示结束
		sData=sIsEncrypt+sData+sEndChar
		#计算数据总长
		iSize=len(sData)+4	#4位表示数据长度
		sSize=ConvertIntToByte(iSize)
		sData=sSize+sData
		super(CJsonSocket,self).BaseSend(sData)
	
	def ConnectSuccess(self):
		#这里也许要改用ip,对端ip
		#getpeername()
		self.Log("%i ConnectSuccess"%(self.m_SocketID))
		self.m_BoolConnect=True
		ExecManagerFunc(self.m_Mode,"OnConnect",self)
	
	def DisConnect(self):
		self.m_BoolConnect=False
		#重置掉包
		self.m_LossPacket=0
		#告诉管理类自己断开了，让其将自己加入BadSocketList
		ExecManagerFunc(self.m_Mode,"DisConnect",self.m_SocketID)
		
