# -*- coding:utf-8 -*-

'''
dmesg用于检查内核缓存信息：
内核缓存能检查到的错误有
	1.开机自检错误信息
	2.syn队列
	... ...

兼容性说明：
	debian6
			没有 --level选项，获得级别仅能通过 -r加grep过滤
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
						'error'			:'dmesg -r|grep \<3\>',		#相当于：dmesg --level=err,这是一般的错误
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
	
	
	#默认情况下一个级别的多条记录是连在一起的一个字符串
	def CutItem(self,sV):
		if not sV:
			return []
		lstValue=sV.split('\n')
		return lstValue
	
