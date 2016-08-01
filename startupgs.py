# -*- coding:utf-8 -*-
'''
Created on Feb 26, 2016
author: youzeshun  (IM: 8766)
��;������������Ϸ�������ļ��
'''

import getopt
import sys
import gameserver

def GetOpt():
	lstOpt,lstArgs = getopt.getopt(sys.argv[1:],'',['logpath=','rootpath=',])
	#�����Ľ�������,������Ϊ--���̲���Ϊ-  
	for sOption, sValue in lstOpt:  
		if  sOption in ["--logpath"]:
			sLogPath=sValue
		elif sOption in ["--rootpath"]:
			sRootPath=sValue
		
	if not locals().has_key('sLogPath'):
		raise UnboundLocalError("����������־��·��")
	if not locals().has_key('sLogPath'):
		raise UnboundLocalError("�������ó���ĸ�·��(����python����shell�ű�)")
		
	return sLogPath,sRootPath


#��ʼ����Ϸ�������İ��������������ܣ����ݼ��
def InitGameServer(sLogPath,sRootPath):
	gameserver.Init(sLogPath,sRootPath)


def StartGameServer():
	gameserver.Start()

if __name__=='__main__':
	sLogPath,sRootPath=GetOpt()
	InitGameServer(sLogPath,sRootPath)
	StartGameServer()
	
