# -*- coding:utf-8 -*-
'''
Created on Feb 1, 2016

@author: yzs

ִ���û��Զ����shell cmd
'''
import basecmd
import os

class CCmd(basecmd.CBaseCmd):
	
	def Start(self):
		self.Clear()
		self.Exec()
		self.FormatResult()
		return self.m_ResultDict['custom']
	
	def Exec(self):
		self.m_ResultDict['custom']=os.popen(self.m_ShellDict['custom']).read()
	
	def SetShellCmd(self,sShellCmd):
		self.m_ShellDict['custom']=sShellCmd
	
	def FormatResult(self):
		if not self.m_ResultDict.has_key('custom'):
			raise RuntimeError('û�������ṩ��FormatResult��ʽ��')
		self.m_ResultDict['custom']=self.m_ResultDict['custom'].rstrip()

