# -*- coding:utf-8 -*-
'''
Created on Mar 3, 2016
author: youzeshun  (IM: 8766)

底层socket，保证底层网络的可靠，该类以后必须使用C实现

1.负责底层数据的收发，收到数据自动调用子类对象的Recv
2.负责网络状况的判定，当网络断开的时候自动调用子类对象
'''

import socket
import threading

#基础Socket方法
class CBaseSocket(object):
	def __init__(self,TcpSockObj):
		self.m_TcpSockObj=TcpSockObj
		self.m_BoolConnect=False
		
	def Start(self):
		threading.Thread(target=self.BaseRecv).start()
	
	#这里可能要使用try expect避免网络问题
	def BaseSend(self,sData):
		if not sData:
			return
		if not self.m_BoolConnect:
			return
		try:
			self.m_TcpSockObj.send(sData)
		except Exception as sException:
			#这里需要记录原因
			self.BaseDisconnect()
		else:
			pass
		
	def BaseRecv(self):
		while True:
			if not self.m_BoolConnect:
				print '网络中断，停止接收数据'
				return
			try:
				RecvCache=self.m_TcpSockObj.recv(1024)
			except Exception as sException:
				print sException
				self.BaseDisconnect()
			else:
				self.Recv(RecvCache)
	
	def BaseCloseSocket(self):
		self.m_TcpSockObj.close()
	
	def BaseDisconnect(self):
		self.DisConnect()
		#关闭socket,否则重连时可能报错：Transport endpoint is already connected
		self.BaseCloseSocket()
		
	def BaseConnect(self):
		self.m_BoolConnect=True
		
	#当删除这个对象的时候需要先将Socket关闭，来释放端口。超时释放会在对象销毁以后继续占用一段时间。这可能引发意想不到的错误
	def __del_(self):
		self.BaseCloseSocket()
	
