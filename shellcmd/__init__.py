# -*- coding:utf-8 -*-
'''
	���shell�����ִ�н��
'''
import dmesg
import custom
from public.define import *

def Init():
	ShellCmdDict=InitData()
	return ShellCmdDict

#������������Щ������Ҫע���߳�����
def InitData():
	ShellCmdDict={}
	ShellCmdDict['dmesg']=dmesg
	ShellCmdDict['custom']=custom
	for k,v in ShellCmdDict.iteritems():
		ShellCmdDict[k]=v.CCmd()
	return ShellCmdDict

#��������Ǹ���֪ʹ�÷�ʽ�ģ���ʹ��public.define�е�ExecShell����import shellcmd
def Exec(sShellCmd):
	oManager=GetGlobalManager("shellcmd")
	if oManager:
		ShellCmdDict=oManager
	else:
		#�ⲻ���Ƽ����÷�����Ϊ�ظ��Ͷ���ȫ�ֱ������Ѿ��ֳ�ʼ�����ֵ���
		ShellCmdDict=InitData()
		
	if ShellCmdDict.has_key(sShellCmd):
		oShellCmd=ShellCmdDict[sShellCmd]
		Result=oShellCmd.Start()
		return Result
	else:
		oCustomCmd=ShellCmdDict['custom']
		oCustomCmd.SetShellCmd(sShellCmd)
		Result=oCustomCmd.Start()
		return Result
	