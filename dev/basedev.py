# -*- coding:utf-8 -*-
# ��������Ϣ���� 
# ����˳
# 2016��1��12��
'''
���еĲɼ�������̳и���
'''

import os

class CBaseDev(object):
	
	def __init__(self):
		self.m_Name=''#����豸������
		self.m_ShellCmd=''#�ɼ����豸������
		self.m_FormatDict=''#���ص����ݸ�ʽ
	
	
	def __call__(self):
		return self.Start()
		
		
	def SetShellCmd(self,ShellCmd):
		self.m_ShellCmd=ShellCmd
	
	
	def SetPeriod(self,iPeriod):
		self.m_period=iPeriod
	
	
	def Start(self,):
		sCmdResult=self.ExecShell()
		sResult=self.FormatResult(sCmdResult)
		return sResult
	
	
	def ExecShell(self,sShellCmd=''):
		if not sShellCmd:
			sShellCmd=self.m_ShellCmd
		sCmdResult=os.popen(sShellCmd).read()
		return sCmdResult
	
	
	def FormatResult(self,sResult):
		if not sResult:
			return
		sResult=sResult.rstrip()	#shell�����ִ�н����������նˣ����Ĭ�϶�һ������������'�û���@������'
		return sResult
	