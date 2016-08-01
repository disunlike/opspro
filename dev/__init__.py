# -*- coding:utf-8 -*-
'''
	初始化各项监控实例
	demo:
	>>import dev
	>>print dev.GetDevInfo('ip')#仅对linux有效
	>>10.32.12.32
'''
import netcark
import ip
from public.define import *

def Init():
	DevDict=InitData()
	return DevDict

def InitData():			#如果不是要用的设备非常多，不要用这种管理方式管理，因为不够直观
	DevDict				={}
	DevDict['netcark']	=netcark
	DevDict['ip']		=ip
	#批量实例化
	for k,v in DevDict.iteritems():
		DevDict[k]=v.CDev()
	return DevDict

#我看不到你的流程入口，这样很不好，摸不着头脑 --程序-基础研发-黄诚恩(2978) 2016-1-25
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

