# -*- coding:utf-8 -*-
'''
Created on Feb 16, 2016
author: youzeshun  (IM: 8766)
��;�������Լ�

ԭ��
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
		#keyΪ'time'�����¼�����һ�����ݵ�ʱ����Ϣ������´�ִ�л�õ�����ʱ����ڸ�ֵ��˵�����µ�
		if k == 'time':
			continue
		iBoolUpdateTime=True
		#����dmesg�����Ϣ���ᱻ��գ����Ա���ɸѡ�²���������
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
		#��һ�μ�飬�������ݶ�û����
		return VList
	if not VList:
		return []
	NowVList=[]
	for sV in VList:
		if not sV:
			#�����е������û�еģ��Է���һ
			continue
		DataList=re.split(r'[\[\]]',sV)
		sTime=DataList[1]
		#�������������[  199.406864]
		sTime=sTime.rstrip()
		FTime=float(sTime)
		if g_FNowTime > FTime:
			#���Ǿ�����
			continue
		NowVList.append(sV)
	return NowVList

#���ݰ��������й���
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
		#Alert(IMNumber,sAlertContent)#�ֲ���ñ���ʱΪ���ܶԱ�������Ϣ���ж���
		Alert(sAlertContent,lstIMNumber)
		
		
def AlertContent(sBody,sLevel):
		sAlertHead='��dmesg��%s[level]%s %s'%(g_IP,sLevel,sBody)
		return sAlertHead


def Init():
	InitPara()
	Log('status/post','���ں˻��桯������ű��ѳ�ʼ��')


def InitPara():
	global g_IP
	g_IP=GetGlobalManager('ip')


def Start():
	dDmesg=ExecDmesg()
	OnCommand(dDmesg)
	Remove_Call_Out('dmesg')
	Call_Out(Functor(Start),gsconf.KERN_BUFF_PERIOD,'dmesg') #Ϊ�˲�������ʹ���ļ�����Ϊע����

