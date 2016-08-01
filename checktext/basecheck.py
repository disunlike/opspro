# -*- coding:utf-8 -*-
'''
Created on Feb 3, 2016
author: youzeshun  (IM: 8766)

����˵����
�����ļ��ĺ����仯�����һ�������ӵ��С����崦��ʽ��Ҫ����OnCommand������д
'''
import os
from public.define import *

class CCheckLine(object):
	def __init__(self,dFile):
		self.m_FileDict		=dFile	#�ȴ��������ļ��ֵ�,��������б�Ҳ����
		self.m_FileLineDict	={}	 	#��¼�µĶ�Ӧ�ļ��ĳ���
		

	def Start(self):
		if not self.m_FileLineDict:
			self.Init()
		self.CheckLine()
	
	#��ʼ��m_LineDict�е����ݣ����ﻹ���˼��·���Ƿ���ȷ�����Էֿ�
	def Init(self):
		self.SetLineDict()
	
	
	#��¼��ǰĿ���ļ��ж�����
	def SetLineDict(self):
		for sFilePath in self.m_FileDict:
			if not os.path.isfile(sFilePath):#�û������ֵ�п����Ǵ��
				sError='checkline:·������,������·�������ڣ�'+sFilePath
				raise Exception(sError)
				continue
			self.m_FileLineDict[sFilePath]=self.GetNewLine(sFilePath)
	
	
	def IsUpdate(self,iNewLine,iOldLine):
		if iNewLine>iOldLine:
			return 1
		return 0
	
	
	def GetStartLine(self,iOldLine):
		iStartLine=iOldLine+1
		return iStartLine
	
	
	#��������䶯
	def CheckLine(self):
		for sFilePath,iOldLine in self.m_FileLineDict.items():#����m_FileList�����û����룬���ܳ������Բ�������
			iNewLine=self.GetNewLine(sFilePath)
			self.m_FileLineDict[sFilePath]=iNewLine
			if self.IsUpdate(iNewLine, iOldLine):
				iStartLine=self.GetStartLine(iOldLine)
				sNewContent=self.GetFileContent(iStartLine,iNewLine,sFilePath)
				self.OnCommand(sNewContent,sFilePath)
			else:
				self.OnCommand('',sFilePath)
	
	
	#����ļ�������
	def GetNewLine(self,sFilePath):
		sShellCmd='wc -l '+sFilePath+'|awk \'{print $1}\''
		sNewLine=ExecShell(sShellCmd)
		iNewLine=int(sNewLine)
		return iNewLine
	
	
	#����ʼĩ�еõ��ļ�������
	def GetFileContent(self,iStartLine,iEndLine,sFilePath):
		sShellCmd='sed -n \'%d,%dp\' %s'%(iStartLine,iEndLine,sFilePath)
		sNewContent=ExecShell(sShellCmd)
		return sNewContent
	
	
	#�õ�һ���ļ��͸��ļ������ӵ�����
	#����ʹ������д�÷�������Ӧ����
	def OnCommand(self,sNewContent,sFilePath):
		sText='�ļ�:%s ����������:%s'%(sFilePath,sNewContent)
		Log('checktext/default', sNewContent)

#import time
#a={'/tmp/a.txt':'8766','/tmp/b.txt':'8766'}
#c=CCheckLine(a)
#c.Start()
#time.sleep(20)
#c.Start()