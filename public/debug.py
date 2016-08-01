# -*- coding:utf-8 -*-
'''
Created on 2016/4/22
author: youzeshun  (IM: 8766)
��;��
	���޸���ʽ���������¶�als��Ŀ���в���
	
ԭ��
	�û�����ĵ�һ������Ϊg_GlobalManagerDict�ļ���
	�û�����ĵڶ�������Ϊg_GlobalManagerDict��ֵ��ģ�鷽��
	��������ĵ���������Ϊ�����Ĳ�������ѡ��

Demo:
	#����als��Ŀ�ı���ģ�飨alert���µĺ���
	python opspro/debugals.py --mod=alert --func=Alert --argv=8766,AlertMsg

������
	--mod		:	ģ������
	--func		:	������
	--argv		:	������ʹ�ö��Ÿ���
	--startup	:	�Ƿ���������
'''

import sys
import getopt
import re
import traceback
from public.define import *
import time

g_LogPath='/tmp/tmplog'		#��־��λ��
g_RootPath=''				#������Ŀ¼��λ�ã������ҳ������λ������Դ
		
def GetOpt():
	OptList,Args = getopt.getopt(sys.argv[1:],'',['mod=','func=','argv=','startup=','runtime='])
	#�����Ľ�������,������Ϊ--���̲���Ϊ-  
	sMod=sFunc=sSim=sRunTime=''
	lstArgv=[]
	for sOption, sValue in OptList:
		if sOption in ["--mod"]:
			sMod=sValue
		elif sOption in ["--func"]:
			sFunc=sValue
		elif sOption in ["--argv"]:
			sArgv=sValue
			lstArgv=re.split(r'[,]',sArgv)
		elif sOption in ["--startup"]:
			sSim=sValue
		elif sOption in ["--runtime"]:
			sRunTime=sValue
	return sMod,sFunc,lstArgv,sSim,sRunTime


#����ģ����������ʼ����
def InitMod(dLocal,sSim):
	if not 'Init' in dLocal:
		print 'û��Init�������޷���ʼ��'
		EndTest()
	cbfunc=dLocal['Init']
	cbfunc(g_LogPath,g_RootPath)
	if sSim==1 and 'Start' in dLocal:
		cbfunc=dLocal['Start']						#��Щ���Խ�����ʼ�������ͺã�����Ҫ��������
		cbfunc()
		
def ExecComeBack(cbfunc,*ArgvList):
	if ArgvList:
		Result= cbfunc(*ArgvList)
	else:
		Result= cbfunc()
	if Result:
		print Result

#��ָ����ģ����в���
def TestMod(sMod,sFunc,*lstArgv):
	if not sMod in g_GlobalManagerDict:
		print 'ģ��%s������'%(sMod)
		return
	oMod=g_GlobalManagerDict[sMod]
	cbfunc=getattr(oMod,sFunc,None)
	
	if not cbfunc:
		print 'ģ��%s�µķ���%s������'%(sMod,sFunc)
		return
	ExecComeBack(cbfunc,*lstArgv)

#�߳���ɱ�������־�ļ�����tmplog������Ҫ���
def EndTest():
	sShellCmd="ps -ef|grep %s|grep -v grep|awk '{print $2}'|xargs kill"%(sys.argv[0])
	ExecShell(sShellCmd)	#���linux���ڼ���ģʽ�£���̨���̱�killɱ�����ӡ��Terminated,set +m�Ƴ�����ģʽ
	
def Debug(dLocal):
	sMod,sFunc,lstArgv,sSim,sRunTime=GetOpt()
	if not sFunc:
		print '�����к�����'
		return
	InitMod(dLocal,sSim)						#��ʼ��ģ��Ļ���
	try:
		if sMod:
			TestMod(sMod,sFunc,*lstArgv)	#����ģ��ĺ���
		elif sFunc in dLocal:
			cbfunc=dLocal[sFunc]
			ExecComeBack(cbfunc,*lstArgv)
		else:
			print 'û���ҵ�����%s'%(sFunc)
	except Exception as oErr:
		print oErr
		traceback.print_exc()
	finally:#ɱ���̣߳���������
		if sRunTime:
			time.sleep(int(sRunTime))
		EndTest()
		
