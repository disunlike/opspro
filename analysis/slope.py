# -*- coding:utf-8 -*-
'''
Created on 2016-1-13

@author: admin

提供对数据基础特征的分析方法：
1.速率
2.变化率
'''
from public.define import *

class CAnaly(object):
	
	def __init__(self):
		self.m_iDataNext	=0				#下一个时刻的数据量
		self.m_iDataPre		=0				#上一个时刻的数据量
		self.m_iSpeedNext	=0				#下一个时刻的速度
		self.m_iSpeedPre	=0				#上一个时刻的速度
		self.m_iInterval	=0				#分析的间隔
		self.m_iSlope		=0				#速度的变化率
		self.m_iUnstable	=2				#抛弃计数最开始的两个值
	
	
	def SetInterval(self,iInterval):
		self.m_iInterval=iInterval
	
	
	def IsInit(self,iData):
		if not isinstance(iData, int):
			print '运维监控：%s传入的数据应该是整型,而非'%(__file__,type(iData))
			return 0
		elif self.m_iInterval<=0:
			print '运维监控：:%s时间间隔Interval必须大于0'%(__file__)
			return 0
		return 1
	
	
	def Start(self,iData):
		if not self.IsInit(iData):
			return

		self.UpdateData(iData)
		self.GetSpeed()					#获得当前速度
		self.GetSlope()					#获得当前速度变化率

		if self.m_iUnstable>0:			#舍弃前两个值，由于刚刚启动，用到了默认值0
			self.m_iUnstable-=1
			return
		
		self.OnCommand()				#其他处理
	
	
	def UpdateData(self,iData):
		self.m_iDataPre=self.m_iDataNext
		self.m_iDataNext=iData
		
		
	def GetSpeed(self):	#计算当前的速率
		self.m_iSpeedPre=self.m_iSpeedNext
		self.m_iSpeedNext=(self.m_iDataNext-self.m_iDataPre)/self.m_iInterval
	
	
	def GetSlope(self):	#计算当前的变化率
		self.m_iSlope=(self.m_iSpeedNext-self.m_iSpeedPre)/self.m_iInterval
	
	
	def OnCommand(self):
		pass
	
if __name__=='__main__':
	oSlope=CAnaly()
	oSlope.SetInterval(10)
	
	def Start(TraffList):
		for i in TraffList:
			oSlope.Start(i)
	Start([2000,2500,3000,5000,8000,10000,14000])
