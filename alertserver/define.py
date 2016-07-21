# -*- coding:utf-8 -*-
'''
Created on 2016-4-30
@author: admin
用途：
	对象的调用接口。为了避开对象的流水线方式调用（每个对象轮番对一个结果集进行处理），
'''

from public.define import *

def GetStartTime():
	dSummary=GetManagerAttr('stati','m_SummaryDict')
	return dSummary['start']

def GetEndTime():
	dSummary=GetManagerAttr('stati','m_SummaryDict')
	return dSummary['end']

def GetSum():
	dSummary=GetManagerAttr('stati','m_SummaryDict')
	return dSummary['sum']

def GetLevel():
	dSummary=GetManagerAttr('stati','m_SummaryDict')
	return dSummary['level']

def GetSRRange():
	dSummary=GetManagerAttr('range','m_SummaryDict')
	return dSummary['srrange']

def GetInfluencePercent():
	dSummary=GetManagerAttr('range','m_SummaryDict')
	return dSummary['influence percent']

def GetVector():
	dSummary=GetManagerAttr('stati','m_SummaryDict')
	return dSummary['vector']

def GetSRStati():
	dSummary=GetManagerAttr('analyfault','m_SummaryDict')
	return dSummary['sr']['stati']

def GetLineStati():
	dSummary=GetManagerAttr('analyfault','m_SummaryDict')
	return dSummary['line']['stati by ip']

def GetFault():
	dSummary=GetManagerAttr('analyfault','m_SummaryDict')
	if 'fault' in dSummary['line']:							#线路故障的范围小，所以优先级高
		return dSummary['line']['fault']
	if 'fault' in dSummary['sr']:
		return dSummary['sr']['fault']
