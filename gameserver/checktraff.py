# -*- coding:utf-8 -*-
# ����˳
# 2016��1��12��

from public.define import *
from define import *
import gsconf


def Normal():
	dEvent=GetSummaryDict()
	return dEvent


def DosStart():
	sTitle		='��%s��%s'					%(GetTitle(),GetIP())
	sSpeed		='[��ǰ�ٶ�]%.2f m/s'			%(float(GetSpeed()/1000.0))
	sSlope		='[��ǰ�ٶȱ仯��]%i kb/s^2'	%(GetSlope())
	sBody		=sTitle+sSpeed+sSlope
	dAlertMsg={
				'title'	:sTitle,
				'body'	:sBody
				}
	return dAlertMsg


def DosEnd():
	sTitle		='��%s��%s'					%(GetTitle(),GetIP())
	sSpeed		='[��ǰ�ٶ�]%.2f m/s'			%(float(GetSpeed()/1000.0))
	sSlope		='[��ǰ�ٶȱ仯��]%i kb/s^2'	%(GetSlope())
	sStartTime	='\n��ʼʱ�䣺%s'				%(GetStartTime())
	sEndTime	='\n����ʱ�䣺%s'				%(GetEndTime())
	sDuration	='\n����ʱ�䣺%.1f ����'		%(GetDuration())
	sMaxtraff	='\n������ֵ��%.1f M/s'		%(GetMaxTraff())
	sBody=sTitle+sSpeed+sSlope+sStartTime+sEndTime+sDuration+sMaxtraff
	dAlertMsg={
				'title'	:sTitle,
				'body'	:sBody
				}
	return dAlertMsg


def CheckPath():
	iTraff=ExecManagerFunc('netcark','Traff')
	if iTraff==None:	#����ֵ����0�������
		raise Exception('���ܻ������������')
	Log(gsconf.PATH_LOG_STATUS_TRAFF,'dos��鹦�ܿ���')


class CCheckTraff():
	#���ڵĳ��̽���analydos����
	def __init__(self):
		self.m_EventDict	=	{}		#����ÿ�μ���������ص�����״������������������գ�dos��������������
		
		
	def FormatEvent(self):
		sTitle=GetTitle()
		if sTitle=='':
			dEvent=Normal()
		elif sTitle=='����Dos����':
			dEvent=DosStart()
		elif sTitle=='�쳣��������':
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
		iTraff=ExecManagerFunc('netcark','Traff')	#���豸�����л�ø��豸���ֵ�����
		ExecManagerFunc('analydos','Start',iTraff)	#���������ݽ��з���
		self.m_EventDict=self.FormatEvent()			#��ʽ���õ������Ķ�����Ϣ
		self.Record(self.m_EventDict)				#��¼��Ϣ
		self.Alert(self.m_EventDict)				#����Ҫ��������Ϣ���д���
		Remove_Call_Out("checktraff")
		Call_Out(Functor(self.Start),GetInterval(),"checktraff") #Ϊ�˲�������ʹ���ļ�����Ϊע����
	
	
	def Init(self):
		CheckPath()
		Log(gsconf.PATH_LOG_STATUS_TRAFF,'��ʼ�������')
	
