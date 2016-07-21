# -*- coding:utf-8 -*-
'''
Created on Feb 23, 2016
author: youzeshun  (IM: 8766)
用途：基础mysql存储功能
'''

#这个包依赖需要改为手动安装
import MySQLdb

class CBaseMysql:
	def __init__(self,sHost,sUser,sPSW,sDBName):
		self.m_Host = sHost
		#self.m_Port = 3306, #使用默认端口
		self.m_User = sUser
		self.m_Passwd = sPSW
		self.m_DBName = sDBName
		self.m_Connect = None

	def Connect(self):
		self.m_Connect= MySQLdb.connect(
			host = self.m_Host,
			user = self.m_User,
			passwd = self.m_Passwd,
			db = self.m_DBName,
		)
	
	def IsConnect(self):
		try:
			self.m_Connect.ping()
		except:
			#self.Connect()
			return 0
		else:
			return 1
	
	#游标表示操作进行到的步骤，主要功能是数据会回滚
	def GetCursor(self):
		oCursor=self.m_Connect.cursor()
		return oCursor

	def Insert(self,sSql):
		if not self.IsConnect():
			return False,'和数据库失去连接'
		oCursor=self.GetCursor()
		try:
			oCursor.execute(sSql)
			self.m_Connect.commit()
		except Exception,(iErrorNumber,sErrorReason):
			sText='编号：%i 原因：%s'%(iErrorNumber,sErrorReason)
			return False,sText
		else:
			return True,''
		
	def Search(self,sSql):
		if not self.IsConnect():
			return False,'数据库没有连接！'
		oCursor=self.GetCursor()
		try:
			oCursor.execute(sSql)
			self.m_Connect.commit()			#如果不提交游标，将无法捕获数据库的更新
		except Exception,sErrorReason:
			return False,sErrorReason
		else:
			ResultList=oCursor.fetchall()
			return True,ResultList
	
	def Close(self):
		self.m_Connect.close()

if __name__=='__main__':	
	oBaseMysql=CBaseMysql('172.168.128.1','root','youzeshun','gather')
	oBaseMysql.Connect()
	print oBaseMysql.Search('select * from mem')

