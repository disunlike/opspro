# -*- coding:utf-8 -*-
'''
Created on Feb 23, 2016
author: youzeshun  (IM: 8766)

1.维持和数据库之间的心跳
2.起到数据库层的作用，对象屏蔽数据库之间的差异
'''
from basemysql import CBaseMysql
from public.define import *

#先站一个坑，这个类的主用功能是确保数据一定能被正确存储。当一个数据库有问题时能切换到备用数据库（也许不再本地）进行存储
class CDBManager:
	def __init__(self,sHost,sUser,sPSW,sDBName):
		self.m_oDB=CBaseMysql(sHost,sUser,sPSW,sDBName)
		self.m_NewID=None
		self.LogPath='db/status'
		self.HeartBeat()
	
	#可以使用操作回调，和Send类似的操作
	def Insert(self,sSql):
		BoolTrue,sResult=self.m_oDB.Insert(sSql)
		if not BoolTrue:
			sText='数据库插入失败，原因:%s Sql语句:%s'%(str(sResult),str(sSql))
			Log(self.LogPath,sText)
			return 0
		return 1
	
	def Search(self,sSql):
		BoolTrue,ResultList=self.m_oDB.Search(sSql)
		if not BoolTrue:
			return None
		return ResultList

	def HeartBeat(self):
		Remove_Call_Out("DB_HeartBeat")
		Call_Out(Functor(self.HeartBeat),300,"DB_HeartBeat")
		try:
			self.m_oDB.m_Connect.ping()
		except:
			self.m_oDB.Connect()
	
	def SetNewID(self,sTableName):
		sSql='select id from %s order by id DESC limit 1'%(sTableName)
		ResultList=self.Search(sSql)
		#结果列表的第一个条记录的第一个字段
		if ResultList:
			self.m_NewID=ResultList[-1][0]
		else:
			self.m_NewID=0

	def GetNewData(self,sTableName):
		sSql='select * from {0} where id >{1};'.format(sTableName,self.m_NewID)
		#找出新增的数据
		DataList=self.Search(sSql)
		return DataList
	
	def UpdateNewID(self,DataList):
		self.m_NewID=DataList[-1][0]
	
	#检查一个表内容的更新，当表内容更新时则执行回调cdfunc
	def CheckUpdate(self,sTableName,cdfunc=None):
		if not self.m_NewID:
			self.SetNewID(sTableName)
			return
		DataList=self.GetNewData(sTableName)
		if DataList:					#如果有数据则更新最新的ID号
			self.UpdateNewID(DataList)
		if cdfunc:
			cdfunc(DataList)				#回调需要知道没有新数据增加，所以总是调用
		else:
			return DataList

if __name__=='__main__':
	DB_HOST='10.32.64.139'
	DB_USER='nagios'
	DB_PSW='duoyi'
	DB_Name='alarms'
	
	oDBManager=CDBManager('10.32.64.139','nagios','duoyi','alarms')
	sSql='select * from content where `timestamp` > "2016-4-25 16:58:00" and `timestamp` < "2016-4-25 17:00:00"'
	print oDBManager.Search(sSql)

