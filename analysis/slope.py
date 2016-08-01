# -*- coding:utf-8 -*-
'''
Created on 2016-1-13

@author: admin

�ṩ�����ݻ��������ķ���������
1.����
2.�仯��
'''
from public.define import *

class CAnaly(object):
	
	def __init__(self):
		self.m_iDataNext	=0				#��һ��ʱ�̵�������
		self.m_iDataPre		=0				#��һ��ʱ�̵�������
		self.m_iSpeedNext	=0				#��һ��ʱ�̵��ٶ�
		self.m_iSpeedPre	=0				#��һ��ʱ�̵��ٶ�
		self.m_iInterval	=0				#�����ļ��
		self.m_iSlope		=0				#�ٶȵı仯��
		self.m_iUnstable	=2				#���������ʼ������ֵ
	
	
	def SetInterval(self,iInterval):
		self.m_iInterval=iInterval
	
	
	def IsInit(self,iData):
		if not isinstance(iData, int):
			print '��ά��أ�%s���������Ӧ��������,����'%(__file__,type(iData))
			return 0
		elif self.m_iInterval<=0:
			print '��ά��أ�:%sʱ����Interval�������0'%(__file__)
			return 0
		return 1
	
	
	def Start(self,iData):
		if not self.IsInit(iData):
			return

		self.UpdateData(iData)
		self.GetSpeed()					#��õ�ǰ�ٶ�
		self.GetSlope()					#��õ�ǰ�ٶȱ仯��

		if self.m_iUnstable>0:			#����ǰ����ֵ�����ڸո��������õ���Ĭ��ֵ0
			self.m_iUnstable-=1
			return
		
		self.OnCommand()				#��������
	
	
	def UpdateData(self,iData):
		self.m_iDataPre=self.m_iDataNext
		self.m_iDataNext=iData
		
		
	def GetSpeed(self):	#���㵱ǰ������
		self.m_iSpeedPre=self.m_iSpeedNext
		self.m_iSpeedNext=(self.m_iDataNext-self.m_iDataPre)/self.m_iInterval
	
	
	def GetSlope(self):	#���㵱ǰ�ı仯��
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
