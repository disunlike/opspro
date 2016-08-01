# -*- coding:utf-8 -*-
'''
Created on Feb 16, 2016
author: youzeshun  (IM: 8766)
用途：开机自检

原理：
'''

from public.define import *
from define import *
import gsconf
import re

g_FNowTime=None

def OnCommand(dDmesg):
	iBoolUpdateTime=False
	for k,VList in dDmesg.items():
		if not VList:
			continue
		#key为'time'的项记录了最后一条数据的时间信息，如果下次执行获得的数据时间大于该值则说明是新的
		if k == 'time':
			continue
		iBoolUpdateTime=True
		#由于dmesg里的信息不会被清空，所以必须筛选新产生的数据
		lstNowData=FilterNowData(VList)
		if not lstNowData:
			continue
		lstNowData=VList
		lstIMNumber=gsconf.KERN_BUFF_DEAL_DICT[k]['imalert']
		IMAlert(lstIMNumber,lstNowData,k)
	if iBoolUpdateTime:
		UpdateNowTime(dDmesg)


def UpdateNowTime(dDmesg):
	global g_FNowTime
	sNowTime=dDmesg['time'][0]
	sNowTime=sNowTime.strip()
	g_FNowTime=float(sNowTime)


def FilterNowData(VList):
	if not g_FNowTime:
		#第一次检查，所有数据都没检查过
		return VList
	if not VList:
		return []
	NowVList=[]
	for sV in VList:
		if not sV:
			#意料中的情况是没有的，以防万一
			continue
		DataList=re.split(r'[\[\]]',sV)
		sTime=DataList[1]
		#避免这种情况：[  199.406864]
		sTime=sTime.rstrip()
		FTime=float(sTime)
		if g_FNowTime > FTime:
			#这是旧数据
			continue
		NowVList.append(sV)
	return NowVList

#根据白名单进行过滤
def IsFilter(sErr):
	for sWhiteList,sMatchRule in gsconf.KERN_BUFF_WHITE_LIST.items():
		sShellCmd="echo '%s'|%s"%(sErr,sMatchRule)
		sResult=ExecShell(sShellCmd)
		if sResult==sWhiteList:
			return 1
	return 0

def IMAlert(lstIMNumber,lstValue,sLevel):
	if not lstIMNumber or not lstValue:
		return
	for i in lstValue:
		if not i:
			continue
		if IsFilter(i):
			continue
		sAlertContent=AlertContent(i,sLevel)
		#Alert(IMNumber,sAlertContent)#分层调用报警时为了能对报警的信息进行定制
		Alert(sAlertContent,lstIMNumber)
		
		
def AlertContent(sBody,sLevel):
		sAlertHead='【dmesg】%s[level]%s %s'%(g_IP,sLevel,sBody)
		return sAlertHead


def Init():
	InitPara()
	Log('status/post','‘内核缓存’结果检查脚本已初始化')


def InitPara():
	global g_IP
	g_IP=GetGlobalManager('ip')


def Start():
	dDmesg=ExecDmesg()
	OnCommand(dDmesg)
	Remove_Call_Out('dmesg')
	Call_Out(Functor(Start),gsconf.KERN_BUFF_PERIOD,'dmesg') #为了不重名，使用文件名作为注册名

