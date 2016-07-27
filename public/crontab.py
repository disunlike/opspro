# -*- coding:utf-8 -*-
'''
Created on Feb 15, 2016
author: youzeshun  (IM: 8766)
path:ServerManager/public/crontab.py

用途：每过一个小时检查期间是否重启过,重启过则执行传入的回调函数
原理:如果没有重启过，那么开机时间的差应该等于系统时间的差
'''
#执行dmesg命令，然后根据不同的信息级别进行处理（m_DealType）
import shellcmd
from xmlstore import basetree
from define import *

class CRestart():
	
	def __init__(self,sXmlName,cFunc,Args=None):
		#上次系统的运行时间
		self.m_LastRunTime=0
		#上次的系统时间
		self.m_LastSysTime=0
		#现在的运行时间
		self.m_NowRunTime=0
		#现在的系统运行时间
		self.m_NowSysTime=0
		#xml树
		self.m_XmlTree=None
		#xml文件的名字，也作为timerctrl的注册
		self.m_XmlName=sXmlName
		#回调函数，当满足条件时将调用他
		self.m_Func=cFunc
		#给予回调的参数
		self.m_FuncArgs=Args
		#生成ｘｍｌ树
		self.m_XmlTree=basetree.CBaseTree(self.m_XmlName)
		
	def Init(self):
		self.InitTag()
		self.InitAttr()
	
	def InitTag(self):
		self.m_XmlTree.InsertNode(self.m_XmlTree.m_NodeRoot,'LastTime')
		
	def InitAttr(self):
		self.UpdateNowTime()
		self.SaveLastTime()
			
	def UpdateNowTime(self):
		#不申明全局，将生成局部变量
		self.m_NowRunTime=shellcmd.Exec('uptime')
		self.m_NowSysTime=int(GetTime("%s"))
		
	#将LastTime保存在xml中
	def SaveLastTime(self):
		oNode=self.m_XmlTree.GetCustomNode('LastTime')
		oNode.set('LastRunTime',str(self.m_NowRunTime))
		oNode.set('LastSysTime',str(self.m_NowSysTime))
		self.m_XmlTree.SaveTree()
	
	#从xml中读取LastTime
	def ReadLastTime(self):
		LastSysTime=self.m_XmlTree.SearchNodeValue('LastTime','LastSysTime')
		LastRunTime=self.m_XmlTree.SearchNodeValue('LastTime','LastRunTime')
		self.m_LastRunTime=int(LastRunTime)
		self.m_LastSysTime=int(LastSysTime)
		
	def GetAbs(self):
		iDiffSysTime=self.m_NowSysTime-self.m_LastSysTime
		iDiffRunTime=self.m_NowRunTime-self.m_LastRunTime
		iDiffTime=iDiffSysTime-iDiffRunTime
		iAbsTime=abs(iDiffTime)
		return iAbsTime
	
	def Start(self):
		#这里使用if　not的方式不可行？原因未知
		if self.m_XmlTree.GetCustomNode('LastTime')==None:
			self.Init()
			return
			
		self.UpdateNowTime()
		self.ReadLastTime()
		#上次没运行过，则运行
		iAbsTime=self.GetAbs()
		#允许2s的误差,误差值不能大于一次重启的时间
		if iAbsTime<2:
			return
		#重启过
		if self.m_FuncArgs:
			self.m_Func(self.m_FuncArgs)
		else:
			self.m_Func()
			#记录最后一次运行
		self.SaveLastTime()
		#Remove_Call_Out(self.m_XmlName)
		#Call_Out(Functor(self.Start),self.m_Period,self.m_XmlName) #为了不重名，使用文件名作为注册名
