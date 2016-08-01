# -*- coding: utf-8 -*-
'''
����ο���Ϸ��־����ͬ��Ŀ����־�ֱ����д�����ͬ��Ŀ¼����

ʹ��˵����
'Write('c/d','post')'
'''
from public.define import *
import path
import os

class CLog():
	def __init__(self,sRootDir='log',sPostfix='.txt'):
		self.m_RootDir=sRootDir #�ռ��ļ��ĸ�Ŀ¼
		self.m_Postfix=sPostfix
	
	
	def Write(self,sFilePath,sText):
		if not sFilePath or not sText:
			return
		self.CheckPathFormat(sFilePath)
		sLogName=path.GetFileName(sFilePath)
		sFolder=path.GetFilePath(sFilePath)
		self.CheckNameFormat(sLogName)
		sDirPath=self.m_RootDir+'/'+sFolder
		self.CreateFolder(sDirPath)
		sText=self.GetText(sText)
		sLogName=self.GetPath(sDirPath,sLogName)
		self.WriteFile(sLogName,sText)
	
	
	def GetPath(self,sDirPath,sLogName):
		sLogName=sDirPath+'/'+sLogName+self.m_Postfix
		return sLogName
	
	
	def GetText(self,sText):
		sTime=GetTime()
		if not isinstance(sText,str):
			sText=str(sText)
		sText=sTime+' '+sText+'\n'
		return sText
	
	
	def WriteFile(self,sPath,sText):
		fLocal=open(sPath,'a+')
		fLocal.write(sText)
	
	
	def CheckNameFormat(self,sName):
		if not sName.find(self.m_Postfix):
			raise RuntimeError('����Ҫʹ��Ĭ�Ϻ�׺')
	
	
	def CheckPathFormat(self,sFilePath):
		ResultList=sFilePath.split('/')
		if len(ResultList)<2:
			raise RuntimeError('��־�Ĵ洢����������Ŀ¼')
	
	
	def CreateFolder(self,sDirPath):
		path.CreateDir(sDirPath)

#����GlobalManager����Ϊ�˱���import���ģ�� --����-�����з�-�Ƴ϶�(2978) 2016-3-15 09:44:45
#def Write(sFilePath,sText):
#	if not sText:
#		return
#	oManager=GetGlobalManager("txtlog")
#	if oManager:
#		oManager.Write(sFilePath, sText)

