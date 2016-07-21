# -*- coding:utf-8 -*-
# 服务器信息基类 
# 尤泽顺
# 2016年1月12日
'''
所有的采集都必须继承该类  -- 基类不要规定的太细，只要其子类的核心结构能被看懂就行了
'''
import os

class CBaseCmd(object):
	#黄诚恩(2978) 2016-2-26 16:45:53
	#异步就有可能发生：FormatResult执行前，Exec可能未执行（不存在self.m_Result变量）
	#或者FormatResult连接执行了两次（执行一次后，它已经变成int了，第二次执行rstrip()会报错）
	m_ErrorDict={
		1:'意料之外的错误：shell的执行结果应该是字符串。可能是执行FormatResult前没执行Exec',
		2:'意料之外的错误：shell的执行结果应该是字符串。可能是执行了多次FormatResult',
	}
	
	def __init__(self):
		self.m_ResultDict	={} #存放结果
		self.m_ExecList		=[] #控制需要执行的命令项,这项是非必须的。这会让集成变得困难。
		self.m_ShellDict	={}
		self.m_Version		=''	#指定该使用方法支持的版本
		
		
	def SetExecItem(self,ExecItem):
		self.m_ExecList=ExecItem
	
	
	#shellcmd包中的命令不应该有过多的处理，它只是简单获得Linux中的数据并结构化
	def Start(self):
		self.Clear()			#清理掉上次的执行结果
		if not self.IsSupport():
			return {}
		self.Exec()
		self.FormatResult()
		return self.m_ResultDict
	
	
	def Clear(self):
		self.m_ResultDict={}
	
	
	#检查版本支持
	def IsSupport(self):
		return 1
	
	
	def Exec(self):
		if self.m_ExecList:
			ExecItemList=self.m_ExecList
		else:
			ExecItemList=list(self.m_ShellDict)
		
		for i in ExecItemList:
			#默认情况要求m_ShellDict是一个字典，如果需要用字符串请重写Exec方法（参考custom）
			sShellCmd=self.m_ShellDict[i]
			sResult=os.popen(sShellCmd).read()
			self.m_ResultDict[i]=sResult
	
	
	def FormatResult(self):
		pass
	
	