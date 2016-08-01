# -*- coding:utf-8 -*-
# ��������Ϣ���� 
# ����˳
# 2016��1��12��
'''
���еĲɼ�������̳и���  -- ���಻Ҫ�涨��̫ϸ��ֻҪ������ĺ��Ľṹ�ܱ�����������
'''
import os

class CBaseCmd(object):
	#�Ƴ϶�(2978) 2016-2-26 16:45:53
	#�첽���п��ܷ�����FormatResultִ��ǰ��Exec����δִ�У�������self.m_Result������
	#����FormatResult����ִ�������Σ�ִ��һ�κ����Ѿ����int�ˣ��ڶ���ִ��rstrip()�ᱨ��
	m_ErrorDict={
		1:'����֮��Ĵ���shell��ִ�н��Ӧ�����ַ�����������ִ��FormatResultǰûִ��Exec',
		2:'����֮��Ĵ���shell��ִ�н��Ӧ�����ַ�����������ִ���˶��FormatResult',
	}
	
	def __init__(self):
		self.m_ResultDict	={} #��Ž��
		self.m_ExecList		=[] #������Ҫִ�е�������,�����ǷǱ���ġ�����ü��ɱ�����ѡ�
		self.m_ShellDict	={}
		self.m_Version		=''	#ָ����ʹ�÷���֧�ֵİ汾
		
		
	def SetExecItem(self,ExecItem):
		self.m_ExecList=ExecItem
	
	
	#shellcmd���е����Ӧ���й���Ĵ�����ֻ�Ǽ򵥻��Linux�е����ݲ��ṹ��
	def Start(self):
		self.Clear()			#������ϴε�ִ�н��
		if not self.IsSupport():
			return {}
		self.Exec()
		self.FormatResult()
		return self.m_ResultDict
	
	
	def Clear(self):
		self.m_ResultDict={}
	
	
	#���汾֧��
	def IsSupport(self):
		return 1
	
	
	def Exec(self):
		if self.m_ExecList:
			ExecItemList=self.m_ExecList
		else:
			ExecItemList=list(self.m_ShellDict)
		
		for i in ExecItemList:
			#Ĭ�����Ҫ��m_ShellDict��һ���ֵ䣬�����Ҫ���ַ�������дExec�������ο�custom��
			sShellCmd=self.m_ShellDict[i]
			sResult=os.popen(sShellCmd).read()
			self.m_ResultDict[i]=sResult
	
	
	def FormatResult(self):
		pass
	
	