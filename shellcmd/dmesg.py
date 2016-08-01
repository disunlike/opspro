# -*- coding:utf-8 -*-

'''
dmesg���ڼ���ں˻�����Ϣ��
�ں˻����ܼ�鵽�Ĵ�����
	1.�����Լ������Ϣ
	2.syn����
	... ...

������˵����
	debian6
			û�� --levelѡ���ü������ͨ�� -r��grep����
	debian7
'''

import basecmd

class CCmd(basecmd.CBaseCmd):
	def __init__(self):
		super(CCmd,self).__init__()
		self.m_ExecList=['alert','crit','error','time']
		self.m_ShellDict={
						'alert'			:'dmesg -r|grep \<1\>',
						'crit'			:'dmesg -r|grep \<2\>',
						'error'			:'dmesg -r|grep \<3\>',		#�൱�ڣ�dmesg --level=err,����һ��Ĵ���
						'warn'			:'dmesg -r|grep \<4\>',
						'time'			:"dmesg | tail -n1 | tail -n1|awk -F'[' '{print $2}'|awk -F']' '{print $1}'|tr -d ' '",
		}
		
		
	def FormatResult(self):
		if not self.m_ResultDict:
			raise Exception(self.m_ErrorDict[1])
		dNew={}
		for k,sV in self.m_ResultDict.items():
			if not isinstance(sV,str):
				raise Exception(self.m_ErrorDict[2])
			sV=sV.rstrip()
			lstValue=self.CutItem(sV)
			dNew[k]=lstValue
		self.m_ResultDict=dNew
	
	
	#Ĭ�������һ������Ķ�����¼������һ���һ���ַ���
	def CutItem(self,sV):
		if not sV:
			return []
		lstValue=sV.split('\n')
		return lstValue
	
