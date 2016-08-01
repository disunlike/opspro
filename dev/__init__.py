# -*- coding:utf-8 -*-
'''
	��ʼ��������ʵ��
	demo:
	>>import dev
	>>print dev.GetDevInfo('ip')#����linux��Ч
	>>10.32.12.32
'''
import netcark
import ip
from public.define import *

def Init():
	DevDict=InitData()
	return DevDict

def InitData():			#�������Ҫ�õ��豸�ǳ��࣬��Ҫ�����ֹ���ʽ������Ϊ����ֱ��
	DevDict				={}
	DevDict['netcark']	=netcark
	DevDict['ip']		=ip
	#����ʵ����
	for k,v in DevDict.iteritems():
		DevDict[k]=v.CDev()
	return DevDict

#�ҿ��������������ڣ������ܲ��ã�������ͷ�� --����-�����з�-�Ƴ϶�(2978) 2016-1-25
def GetDevInfo(sDevName):
	oManager=GetGlobalManager("devdict")
	if oManager:
		DevDict=oManager
	else:
		DevDict=Init()
	
	if not sDevName in DevDict:
		return None
	DevInfoDict=DevDict[sDevName].Start()
	return DevInfoDict

