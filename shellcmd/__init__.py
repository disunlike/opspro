# -*- coding:utf-8 -*-
'''
	获得shell命令的执行结果
'''
import dmesg
import custom
from public.define import *

def Init():
	ShellCmdDict=InitData()
	return ShellCmdDict

#其他程序共用这些对象，需要注意线程问题
def InitData():
	ShellCmdDict={}
	ShellCmdDict['dmesg']=dmesg
	ShellCmdDict['custom']=custom
	for k,v in ShellCmdDict.iteritems():
		ShellCmdDict[k]=v.CCmd()
	return ShellCmdDict

#这个方法是给告知使用方式的，请使用public.define中的ExecShell避免import shellcmd
def Exec(sShellCmd):
	oManager=GetGlobalManager("shellcmd")
	if oManager:
		ShellCmdDict=oManager
	else:
		#这不是推荐的用法，因为重复劳动，全局变量中已经又初始化的字典了
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
	