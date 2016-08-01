# -*- coding:utf-8 -*-
'''
Created on Feb 3, 2016
author: youzeshun  (IM: 8766)

用于说明：
监视文件的函数变化，并且获得新增加的行。具体处理方式需要集成OnCommand后自行写
'''
import os
from public.define import *

class CCheckLine(object):
	def __init__(self,dFile):
		self.m_FileDict		=dFile	#等待被检查的文件字典,传入的是列表也可以
		self.m_FileLineDict	={}	 	#记录新的对应文件的长度
		

	def Start(self):
		if not self.m_FileLineDict:
			self.Init()
		self.CheckLine()
	
	#初始化m_LineDict中的数据，这里还做了检查路径是否正确，可以分开
	def Init(self):
		self.SetLineDict()
	
	
	#记录当前目标文件有多少行
	def SetLineDict(self):
		for sFilePath in self.m_FileDict:
			if not os.path.isfile(sFilePath):#用户输入的值有可能是错的
				sError='checkline:路径错误,给出的路径不存在：'+sFilePath
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
	
	
	#检查行数变动
	def CheckLine(self):
		for sFilePath,iOldLine in self.m_FileLineDict.items():#由于m_FileList由于用户输入，可能出错，所以不遍历他
			iNewLine=self.GetNewLine(sFilePath)
			self.m_FileLineDict[sFilePath]=iNewLine
			if self.IsUpdate(iNewLine, iOldLine):
				iStartLine=self.GetStartLine(iOldLine)
				sNewContent=self.GetFileContent(iStartLine,iNewLine,sFilePath)
				self.OnCommand(sNewContent,sFilePath)
			else:
				self.OnCommand('',sFilePath)
	
	
	#获得文件的行数
	def GetNewLine(self,sFilePath):
		sShellCmd='wc -l '+sFilePath+'|awk \'{print $1}\''
		sNewLine=ExecShell(sShellCmd)
		iNewLine=int(sNewLine)
		return iNewLine
	
	
	#按照始末行得到文件的内容
	def GetFileContent(self,iStartLine,iEndLine,sFilePath):
		sShellCmd='sed -n \'%d,%dp\' %s'%(iStartLine,iEndLine,sFilePath)
		sNewContent=ExecShell(sShellCmd)
		return sNewContent
	
	
	#得到一个文件和该文件新增加的内容
	#建议使用者重写该方法以适应需求
	def OnCommand(self,sNewContent,sFilePath):
		sText='文件:%s 新增加内容:%s'%(sFilePath,sNewContent)
		Log('checktext/default', sNewContent)

#import time
#a={'/tmp/a.txt':'8766','/tmp/b.txt':'8766'}
#c=CCheckLine(a)
#c.Start()
#time.sleep(20)
#c.Start()