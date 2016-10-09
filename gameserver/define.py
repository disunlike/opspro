# -*- coding:utf-8 -*-
'''
Created on 2016-5-3
@author: youzeshun
用途：
	调用接口,不让逻辑代码碰到数据，免得可变对象被修改到
'''
from public.define import *


def GetInterval():
	iInterval=GetManagerAttr('analydos','m_iInterval')
	return iInterval


def GetIP():
	sIP=GetGlobalManager('ip')
	if not sIP:
		raise Exception('意外的错误：没有将ip加入为全局变量字典')
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


