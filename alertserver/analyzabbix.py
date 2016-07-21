# -*- coding:utf-8 -*-
'''
Created on 2016-4-25
@author: admin
用途：
	分析zabbix数据库
	佛山10G-core 291.71
	佛山10G-联通 9.74
	香港 1.45
	沈阳网通-1 23.94
	中山双线-１ 185.37
	中山10G-core 193.72
	中山双线-3 14.95
	常州电信 77.82
	常州联通 4.15
	顺德电信-1 30.59
	惠州电信-1 46.0
	惠州电信-2 71.12
	南方基地 5.0
	济南网通-1 4.98
'''

from public.define import *
import time

class CBound():
	def GetHostID(self,sIP):
		sSql="select interface.hostid from interface where ip='%s'"%(sIP)
		ResultList=ExecManagerFunc('dbzabbix','Search',sSql)
		if ResultList:
			return ResultList[0][0]	#第一个记录的第一个字段
	
	#得到时时入口流量
	def GetItemID(self,HostID,sEther,IFHC):
		iHostID=self.GetHostID(HostID)
		sSql="select itemid from items where hostid=%i and key_='%s[%s]'" % (HostID,IFHC,sEther)
		ResultList=ExecManagerFunc('dbzabbix','Search',sSql)
		if ResultList:
			return ResultList[0][0]
	
	def GetValue(self,ItemID):
		sSql="select value from history_uint where itemid=%s order by clock DESC LIMIT 1" %(ItemID)
		ResultList=ExecManagerFunc('dbzabbix','Search',sSql)
		if ResultList:
			return ResultList[0][0]
	
	#218.213.229.66,GigabitEthernet1/0/24
	#''
	def GetTraffIn(self,HostID,sEther):
		ItemID=self.GetItemID(HostID,sEther,'ifHCInOctets')
		Value=self.GetValue(ItemID)
		return Value
	
	def GetTraffOut(self,HostID,sEther):
		ItemID=self.GetItemID(HostID,sEther,'ifHCOutOctets')
		Value=self.GetValue(ItemID)
		return Value
	
	#返回该IP的指定端口的时时上下行流量中最大的那个。
	#测试指令：python debugals.py --mod=bound --func=GetTraff --argv=121.201.102.1,TenGigabitEthernet1/1
	def GetTraff(self,sIP,sEther):
		LHostID=self.GetHostID(sIP)					#得到数据库的
		LTraffIn=self.GetTraffIn(LHostID,sEther)
		LTraffOut=self.GetTraffOut(LHostID,sEther)
		LTraff=max(LTraffIn,LTraffOut)
		return round(float(LTraff)/1024/1024,2)
	
	def GetPerce(self,sIP,sEther):
		pass
	
	#得到时时出口流量
	def IdcBoundLive(self):
		pass
	
	#测试数据库是否正常连接:python opspro/debugals.py --mod=bound --func=Test
	def Test(self):
		sSql='show tables'
		print ExecManagerFunc('dbzabbix','Search',sSql)
	
