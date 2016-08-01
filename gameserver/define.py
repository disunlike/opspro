# -*- coding:utf-8 -*-
'''
Created on 2016-5-3
@author: admin
��;��
	���ýӿ�,�����߼������������ݣ���ÿɱ�����޸ĵ�
'''
from public.define import *


def GetInterval():
	iInterval=GetManagerAttr('analydos','m_iInterval')
	return iInterval


def GetIP():
	sIP=GetGlobalManager('ip')
	if not sIP:
		raise Exception('����Ĵ���û�н�ip����Ϊȫ�ֱ����ֵ�')
	return sIP


def GetSummaryDict():
	dSummary=GetManagerAttr('analydos','m_SummaryDict')
	return dSummary


def GetTitle():
	dSummary=GetSummaryDict()
	return dSummary['title']


def GetSpeed():
	dSummary=GetSummaryDict()
	return dSummary['detail']['speed']


def GetSlope():
	dSummary=GetSummaryDict()
	return dSummary['detail']['slope']


def GetStatus():
	dSummary=GetSummaryDict()
	return dSummary['detail']['status']


def GetCountStable():
	dSummary=GetSummaryDict()
	return dSummary['detail']['countstable']


def GetStartTime():
	dSummary=GetSummaryDict()
	return dSummary['dos']['starttime']


def GetEndTime():
	dSummary=GetSummaryDict()
	return dSummary['dos']['endtime']


def GetMaxTraff():
	dSummary=GetSummaryDict()
	return dSummary['dos']['maxtraff']


def GetDuration():
	dSummary=GetSummaryDict()
	return dSummary['dos']['duration']


def GetEvent():
	dEvent=GetManagerAttr('traff','m_EventDict')
	return dEvent


def GetNewLog():
	dNewLog=GetManagerAttr('newlog','m_NewContentDict')
	return dNewLog

def ExecDmesg():
	shellDict=GetGlobalManager('shelldict')
	oDmesg=shellDict['dmesg']
	dDmesg=oDmesg.Start()
	return dDmesg

