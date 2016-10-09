# -*- coding:utf-8 -*-
# 尤泽顺
# 2016年1月12日

from public.define import *
from define import *
import gsconf


def Normal():
	dEvent=GetSummaryDict()
	return dEvent


def DosStart():
	sTitle		='【%s】%s'					%(GetTitle(),GetIP())
	sSpeed		='[当前速度]%.2f m/s'			%(float(GetSpeed()/1000.0))
	sSlope		='[当前速度变化率]%i kb/s^2'	%(GetSlope())
	sBody		=sTitle+sSpeed+sSlope
	dAlertMsg={
				'title'	:sTitle,
				'body'	:sBody
				}
	return dAlertMsg


def DosEnd():
	sTitle		='【%s】%s'					%(GetTitle(),GetIP())
	sSpeed		='[当前速度]%.2f m/s'			%(float(GetSpeed()/1000.0))
	sSlope		='[当前速度变化率]%i kb/s^2'	%(GetSlope())
	sStartTime	='\n开始时间：%s'				%(GetStartTime())
	sEndTime	='\n结束时间：%s'				%(GetEndTime())
	sDuration	='\n持续时间：%.1f 分钟'		%(GetDuration())
	sMaxtraff	='\n流量峰值：%.1f M/s'		%(GetMaxTraff())
	sBody=sTitle+sSpeed+sSlope+sStartTime+sEndTime+sDuration+sMaxtraff
	dAlertMsg={
				'title'	:sTitle,
				'body'	:sBody
				}
	return dAlertMsg


def CheckPath():
	iTraff=ExecManagerFunc('netcark','Traff')
	if iTraff==None:	#流量值等于0是允许的
		raise Exception('不能获得网卡流量！')
	Log(gsconf.PATH_LOG_STATUS_TRAFF,'dos检查功能可用')


class CCheckTraff():
	#周期的长短交由analydos控制
	def __init__(self):
		self.m_EventDict	=	{}		#包含每次检查流量返回的网络状况，共有三种情况：空，dos攻击，攻击结束
		
		
	def FormatEvent(self):
		sTitle=GetTitle()
		if sTitle=='':
			dEvent=Normal()
		elif sTitle=='疑似Dos攻击':
			dEvent=DosStart()
		elif sTitle=='异常流量结束':
			dEvent=DosEnd()
		return dEvent
	
	
	def Record(self,dEvent):
		if 'body' in dEvent:
			Log(gsconf.PATH_LOG_TRAFF,dEvent['body'])
		else:
			Log(gsconf.PATH_LOG_TRAFF,dEvent)
	
	
	def Alert(self,dEvent):
		if 'body' in dEvent:
			Alert(dEvent,gsconf.IM_DOS)
	
	
	def Start(self):
		iTraff=ExecManagerFunc('netcark','Traff')	#从设备对象中获得该设备的字典数据
		ExecManagerFunc('analydos','Start',iTraff)	#将流量数据进行分析
		self.m_EventDict=self.FormatEvent()			#格式化得到容易阅读的信息
		self.Record(self.m_EventDict)				#记录信息
		self.Alert(self.m_EventDict)				#对需要报警的信息进行处理
		Remove_Call_Out("checktraff")
		Call_Out(Functor(self.Start),GetInterval(),"checktraff") #为了不重名，使用文件名作为注册名
	
	
	def Init(self):
		CheckPath()
		Log(gsconf.PATH_LOG_STATUS_TRAFF,'开始检查流量')
	
