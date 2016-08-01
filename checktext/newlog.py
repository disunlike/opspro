# -*- coding:utf-8 -*-
'''
Created on Feb 4, 2016
author: youzeshun  (IM: 8766)
path:ServerManager/checktext/checklog.py

���ڣ������ļ����������ӵ��н��л��Ƿ���
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
		#lstLine=sNewContent.split('\n')			#�����־����\n���Ż���ֽ�ȡ���󡣵���һ�㲻����
		self.m_NewContentDict[sFilePath]=sNewContent
		