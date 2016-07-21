# -*- coding: utf-8 -*-
'''
Created on Feb 1, 2016

@author: yzs

循环创建目录的代码

#Demo:
Create('/home/yzs/backup/a/a.txt')
Create('/home/yzs/backup/b/')
Create('/home/yzs/backup/c')
Create('~/backup/d/z.txt')
Create('~/backup/e/')
Create('~/backup/f')
'''
import os

#BoolCreateFile判断是否创建文件
def Create(sPath,BoolCreateFile=True):
	sPath=TranPath(sPath) #将~换为家目录
	if not IsAbsolutePath(sPath):
		raise Exception('请使用绝对路径,Linux中的绝对路径必须是以根开头的')

	if IsFilePath(sPath):
		sDirPath=GetFilePath(sPath)
		CreateDir(sDirPath)
		if BoolCreateFile:
			CreateFile(sPath)
	else:
		CreateDir(sPath)#循环建立目录


def GetFileName(sPath):
	pathList=CutPath(sPath)
	sFileName=pathList[-1]
	return sFileName


def GetFilePath(sPath):
	lstPath=os.path.split(sPath)
	sDirPath=lstPath[0]
	return sDirPath


def GroupPath(PathList):
	sPath='/'.join(PathList)
	return sPath


def CreateFile(sPath):
	open(sPath,'w')


#循环创建目录
#另一个好的方法:使用shell的mkdir -p,缺点是平台依赖
def CreateDir(sPath):
	lstFullDir=CutPath(sPath)
	lstExistDir=[]
	for sDir in lstFullDir:
		lstExistDir.append(sDir)
		sPath=GroupPath(lstExistDir)
		if not os.path.exists(sPath) and sPath:
			os.mkdir(sPath)


def CutPath(sPath):
	lstPath=sPath.split('/')
	return lstPath


#用于将～符号转为路径的形式
def TranPath(sPath):
	sPath=os.popen('echo %s'%sPath).read().rstrip()
	return sPath


def IsAbsolutePath(sPath):
	if not sPath:
		raise RuntimeError('错误：不能使用空路径作为传参')
	if sPath[0]=='/':
		return 1
	return 0


#单独使用时不判断是否是绝对路径
def IsFilePath(sPath):
	lstPath=os.path.split(sPath)
	sFileName=lstPath[1]
	if not sFileName:
		return 0
	return 1


def GetStdDir(sDirPath):
	if not sDirPath[-1]=='/':
		sDirPath+='/'
	return sDirPath


#获得项目的路径
def GetProPath():
	sScriptPath=os.path.realpath(__file__)
	#split and get path
	lstDirPath=os.path.split(os.path.realpath(__file__))
	#split and get path
	sDirPath=lstDirPath[0]
	lstPath=CutPath(sDirPath)
	lstProPath=lstPath[0:-1]
	if not lstProPath:
		raise RuntimeError('错误：项目不应该被直接放在根目录')
	sProPath=GroupPath(lstProPath)
	return sProPath

#完整测试,建议能使用单元测试的都必须写
if __name__=='__main__':
	def Test():
		Create('/home/yzs/backup/a/a.txt')
		Create('/home/yzs/backup/b/')
		Create('/home/yzs/backup/c')
		Create('~/backup/d/z.txt')
		Create('~/backup/e/')
		Create('~/backup/f')
		print GetProPath()
