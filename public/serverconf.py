# -*- coding:utf-8 -*-
'''
Created on Feb 1, 2016

@author: yzs

用于配置文件

注意：凡对系统做的更改，包括执行shell,更改文件都必须先记录
'''
import os 

import shellcmd
from public import path
from public.define import * 

class CBaseConf(object):
	#初始化：备份需要配置的文件
	def __init__(self):
		self.m_Name=''
		self.m_LogName='public/confserver'
		self.m_BackupDir=''#备份到那个目录下
		self.m_ModifyFile=''#需要被配置的文件名字
		self.m_NewConfig=''#新配置的内容
		self.m_RestartCmd=''#重启服务的命令，让配置生效
		#self.m_BackupFile=''#本次备份文件的路径，如果需要自行设置请重写BackupFile方法
		
	def Init(self):
		self.m_BackupDir=path.TranPath(self.m_BackupDir)#设置备份的路径，将路径中的～符号转换为家目录的形式
		self.m_BackupDir=path.GetStdDir(self.m_BackupDir)
		path.Create(self.m_BackupDir)#创建备份文件的路径
		
	#检查完权限，其他地方就能用理想情况来考虑了。
	def IsPermission(self):
		sError=''
		if not os.path.exists(self.m_BackupDir):
			sError='备份文件的路径(%s)创建失败，所以操作停止'%self.m_BackupDir
		elif os.path.isfile(self.m_ModifyFile):
			if not os.access(self.m_ModifyFile,os.R_OK):
				sError='无法备份文件，所以操作停止.因为对目标%s无读权限'%self.m_ModifyFile
			elif not os.access(self.m_ModifyFile,os.W_OK):
				sError='操作停止,因为对目标%s无写权限'%self.m_ModifyFile
		else:
			sDirPath=path.GetFilePath(self.m_ModifyFile)
			if not os.access(sDirPath,os.W_OK):
				sError='操作停止,因为目标%s不存在，且对该目录%s无写权限.无法创建'%(self.m_ModifyFile,sDirPath)
		if sError:
			print sError
			Log(self.m_LogName,sError)
			return 0
		return 1
	
	#检查版本是否一致
	def IsVerIden(self):
		return 0
	
	def IsConf(self):
		return 1
	
	def Start(self):
		#检查版本，版本合适才允许开始配置
		if not self.IsVerIden():
			sText='版本不合适,停止程序%s配置服务'%(self.m_Name)
			Log(self.m_LogName,sText)
			return
		
		#检查是否已经配置过了,已经配置过了（１）则不做任何更改
		if self.IsConf():
			sText='已经配置过:%s'%(self.m_Name)
			Log(self.m_LogName,sText)
			return
		
		#初始化是创建备份文件或备份文件的保存目录
		if not os.path.exists(self.m_BackupDir):
			self.Init()
		
		#检查权限和初始化是否成功
		if not self.IsPermission():
			print '初始化不成功：',self.m_Name
			Log(self.m_LogName,'初始化不成功，程序停止运行。文件没有被修改')
			return 
		
		#判断目标文件是否存在，存在就需要进行备份
		if os.path.isfile(self.m_ModifyFile):
			self.BackupFile()
		self.DeployFile()
		self.RestartServer()
			
	def BackupFile(self):
		sShellCmd=self.GetBackupCmd()
		Log(self.m_LogName,'执行命令:'+sShellCmd)
		shellcmd.Exec(sShellCmd)
	
	def GetBackupCmd(self):
		self.SetBackupPath()
		sShellCmd='cp %s %s'%(self.m_ModifyFile,self.m_BackupFile)
		return sShellCmd

	def SetBackupPath(self):
		sTime=GetTime("%Y-%m-%d_%H:%M:%S")
		sFileName=path.GetFileName(self.m_ModifyFile)
		self.m_BackupFile=self.m_BackupDir+sFileName+'_'+sTime#这步要求self.m_BackupDir的格式需要规范
		
	def DeployFile(self):
		Log(self.m_LogName,'文件'+self.m_ModifyFile+'被重写')
		oFile=open(self.m_ModifyFile,'w+')#消除文件内容，以读写方式打开。使用该方法前必须备份
		oFile.write(self.m_NewConfig)

	def RestartServer(self):
		if self.m_RestartCmd:
			Log(self.m_LogName,'执行命令:'+self.m_RestartCmd)
			shellcmd.Exec(self.m_RestartCmd)
