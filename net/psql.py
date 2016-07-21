# -*- coding:utf-8 -*-
'''
Created on Mar 10, 2016
author: youzeshun  (IM: 8766)

处理数据库协议：action:sql
'''
from public.define import *
import os
import baseprotocol

class CPSql(baseprotocol.CBaseProtocol):
	def __init__(self,sCachePath,sMode=''):
		self.m_Mode=sMode				#标记处理好的数据传给的对象
		self.m_CacheFilePath=''
		self.InitCachePath(sCachePath)		#当收到recode=-1时，回调函数要将数据保存的位置
	
	def InitCachePath(self,sCachePath):
		sLogPath=GetGlobalManager('logpath')
		self.m_CacheFilePath=sLogPath+'/'+sCachePath
		
	def Respond(self,dSourceData,SocketDict):
		#socketid是自己加的，一定存在
		iSocketID=dSourceData['socketid']
		#如果网络突然闪断，m_SocketDict的iSocket是会被清掉的
		if not iSocketID in SocketDict:
			return
		if not isinstance(dSourceData['field'],dict):
			return
		dSourceData['field']['ip']=SocketDict[iSocketID]['ip']
		
		sSql=self.GetSql(dSourceData)
		Bool=self.ExecInsertSql(sSql)
		dRespondData=self.GetRespondData(Bool,dSourceData)
		#调用全局变量字典中，键为Mode的对象的 ，dRespondData作为参数
		ExecManagerFunc(self.m_Mode,'Send',dRespondData)
	
	#1：执行成功
	#0：执行失败
	#-1:又发送方给出，超时没得到回复
	def GetRespondData(self,Bool,dSourceData):
		if Bool==1:
			recode=1
		elif Bool==0:
			recode=0
		dRespondData={
			'action':'r_sql',
			'recode':recode,					#标记数据包的状态
			'uuid':dSourceData['uuid'],			#给发送方删除其回调
			'socketid':dSourceData['socketid'],	#告诉管理类该把包发给谁
			}
		#print '回应的数据：',dRespondData
		return dRespondData
		
			
	#第一个参数：发送的数据dSourceData
	#第二个参数：回应的数据dRespondData
	#回应的数据包中recode=-1则说明没有对方没有接受到数据，那么dSourceData应该被保存并且延迟重发
	def Callback(self,iSocketID,dSourceData,dRespondData):
		#print '开启回调',dSourceData,dRespondData
		recode=dRespondData["recode"]
		if recode==-1:
			#ping协议也许能整体搬到C引擎中
			self.TimeOut(dSourceData,iSocketID)
			return
		elif recode==1:
			self.Normal(iSocketID)
	
	#正常则检查本地缓存数据开始重发
	def Normal(self,iSocketID):
		self.ReSend(iSocketID)
	
	def ReSend(self,iSocketID):
		if not  self.IsCache():
			return
		
		DataList=ExecManagerFunc('txtcache','Read',self.m_CacheFilePath)
		if not DataList:
			return
		for sData in DataList:
			dData,iSocketID=eval(sData)
			ExecManagerFunc(self.m_Mode,'ReSend',dData,iSocketID)
	
	#检查是否有缓存数据需要续传
	def IsCache(self):
		if os.stat(self.m_CacheFilePath).st_size:
			return 1
		return 0
		
	def TimeOut(self,dData,iSocketID):
		self.LocalSave(dData,iSocketID)
	
	def LocalSave(self,dData,iSocketID):
		sData=str((dData,iSocketID))
		#print '开始保存数据'
		ExecManagerFunc('txtcache','Save',sData,self.m_CacheFilePath)
	
	def GetSql(self,dData):
		FieldDict=dData['field']
		sDBName=dData['dbname']
		sTBName=dData['tbname']
	
		sField,sValue='',''
		for k,v in FieldDict.items():
			sField+=k+','
			sValue+='\''+str(v)+'\''+','
		sSql='insert into %s (%s) values (%s);'%(sTBName,sField[:-1],sValue[:-1])
		return sSql
	
	def ExecInsertSql(self,sSql):
		oDBManager=GetGlobalManager('dbmanager')
		Bool=oDBManager.Insert(sSql)
		return Bool
		
	#oDBManager=CDBManager('192.168.63.139','root','youzeshun','gather')
	#print oDBManager.Search('select * from mem')

