# -*- coding:utf-8 -*-
'''
Created on Feb 4, 2016
author: youzeshun  (IM: 8766)
path:ServerManager/checktext/checklog.py

用于：监视文件，将新增加的行进行火星发送
'''
import basecheck

class CCheck(basecheck.CCheckLine):
	
	def __init__(self,FileDict):
		super(CCheck,self).__init__(FileDict)
		self.m_NewContentDict={}
	
	
	def ClearOldContent(self,sFilePath):
		if sFilePath in self.m_NewContentDict:
			self.m_NewContentDict[sFilePath]=''
	
	
	def OnCommand(self,sNewContent,sFilePath):
		self.ClearOldContent(sFilePath)
		if not sNewContent:
			return
		#lstLine=sNewContent.split('\n')			#如果日志中有\n符号会出现截取错误。但是一般不会有
		self.m_NewContentDict[sFilePath]=sNewContent
		