# -*- coding: utf-8 -*-
'''
Created on Feb 1, 2016

@author: yzs

ѭ������Ŀ¼�Ĵ���

#Demo:
Create('/home/yzs/backup/a/a.txt')
Create('/home/yzs/backup/b/')
Create('/home/yzs/backup/c')
Create('~/backup/d/z.txt')
Create('~/backup/e/')
Create('~/backup/f')
'''
import os
import re
import shellcmd

#BoolCreateFile�ж��Ƿ񴴽��ļ�
def Create(sPath,BoolCreateFile=True):
	sPath=TranPath(sPath) #��~��Ϊ��Ŀ¼
	if not IsAbsolutePath(sPath):
		raise Exception('��ʹ�þ���·��,Linux�еľ���·���������Ը���ͷ��')
	
	if IsFilePath(sPath):
		sDirPath=GetFilePath(sPath)
		CreateDir(sDirPath)
		if BoolCreateFile:
			CreateFile(sPath)
	else:
		CreateDir(sPath)#ѭ������Ŀ¼


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


#ѭ������Ŀ¼
#��һ���õķ���:ʹ��shell��mkdir -p,ȱ����ƽ̨����
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


#���ڽ�������תΪ·������ʽ
def TranPath(sPath):
	sPath=shellcmd.Exec('echo %s'%sPath)
	return sPath


def IsAbsolutePath(sPath):
	if not sPath:
		raise RuntimeError('���󣺲���ʹ�ÿ�·����Ϊ����')
	if sPath[0]=='/':
		return 1
	return 0


#����ʹ��ʱ���ж��Ƿ��Ǿ���·��
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


#�����Ŀ��·��
def GetProPath():
	sScriptPath=os.path.realpath(__file__)
	#split and get path 
	lstDirPath=os.path.split(os.path.realpath(__file__))
	#split and get path 
	sDirPath=lstDirPath[0]
	lstPath=CutPath(sDirPath)
	lstProPath=lstPath[0:-1]
	if not lstProPath:
		raise RuntimeError('������Ŀ��Ӧ�ñ�ֱ�ӷ��ڸ�Ŀ¼')
	sProPath=GroupPath(lstProPath)
	return sProPath

#��������,������ʹ�õ�Ԫ���ԵĶ�����д
if __name__=='__main__':
	def Test():
		Create('/home/yzs/backup/a/a.txt')
		Create('/home/yzs/backup/b/')
		Create('/home/yzs/backup/c')
		Create('~/backup/d/z.txt')
		Create('~/backup/e/')
		Create('~/backup/f')
		print GetProPath()
		
