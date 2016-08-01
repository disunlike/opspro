# -*- coding:utf-8 -*-
#������˳��(IM:8766)
'''
��;��
	dos.py
		����Ƿ���dos����
	checkkernlog.py
		���ϵͳ��־�м���3���ϵĴ���
	kernelbuffer.py
		����ں˻������3�������ϵĴ���

ģ��˵����
	analysis���ṩ���ݷ�����Ŀǰ�������ݵı仯�����Ƿ����dos������
	dev:�ṩ�豸�Ĺ��������ãɣ�ʹ�ã�ϵͳ���ء�Ŀǰ���ڻ����������
	log:ֻ��һ���ļ��У����ڱ��������������ɵ���־
	public:ͨ�ô��롣����д��־�����Ǳ�����·������
	shellcmd:��װshell����
	
	��ģ�������״��д��txtlog.Write('status/�ű�����','��ʼ�������')
	��ģ���������־д��txtlog.Write('������/�ű�����','��ʼ�������')
	��ģ��Ĳ���������д��txtlog.Write('data/�ű�����','��ʼ�������')

ע�⣺
	��Ϸ���ϲ������Ļ�����
		1.���ص㡿����Ϸ����������ĸ���
		2������´���
		3.Ҫ����־����������

	������zabbix���Ļ���
	1.���ѵ㡿�������������Ķ�Ӧ��ϵ����ȷ��
	2.��ؽ�����Ϸ���������
'''

import analysis
import gsalert
import analydos
import checktraff
import gsconf
import checklog
from checktext import newlog
from public.define import *
from public import timerctrl
from public import txtlog
from dev import netcark
from dev import ip
import shellcmd

def GetIP():
	sIP=ExecShell(gsconf.PATH_SCRIPT_GET_IP)	#����ʹ����Ϸ���ķ�ʽ���ip
	if not sIP:
		oIP=ip.CDev()
		sIP=oIP.Start()
	return sIP


def Init(sLogPath,sRootPath):
	if not sLogPath:
		raise Exception('û���ҵ���־·��������promanager.sh')
	SetGlobalManager('logpath',sLogPath)
	SetGlobalManager('rootpath',sRootPath)		#�ű��ĸ�·��������Ѱ����Դ
	SetGlobalManager("timer",timerctrl.CTimerManager())
	SetGlobalManager("shelldict",shellcmd.Init())
	SetGlobalManager('ip',GetIP())
	'''
		��;�����������������dos
	'''
	oAnalyDos=analydos.CAnalyDos()
	oAnalyDos.SetInterval(gsconf.PERIOD_NORMAL)
	SetGlobalManager("analydos",oAnalyDos)					#Ϊ���ܹ�ʹ�ò��Դ�����������в��ԣ�������������
	SetGlobalManager("traff",checktraff.CCheckTraff())
	'''
		��;������������յ�������
		����ָ�python opspro/debuggs.py --mod=netcark --func=Traff
	'''
	SetGlobalManager("netcark",netcark.CDev()) 			#dev.DevDict���ַ�ʽ����ȫ�ֱ�����ȫ�ֱ��������ֵ�ͬʱ������ͬ�����ݡ�
	SetGlobalManager("txtlog",txtlog.CLog(sLogPath))
	#SetGlobalManager("imalert",alert.CIMAlert())
	SetGlobalManager("alert",gsalert.CAlertManager())
	SetGlobalManager('newlog',newlog.CCheck(gsconf.CHECKLOG_LOG_DICT))
	SetGlobalManager("checklog",checklog.CCheckLog())
	
	
def Start():
	ExecManagerFunc("traff",'Init')
	ExecManagerFunc("traff",'Start')
	
	#�����Լ���Ϣ���
	import kernbuff
	kernbuff.Init()
	kernbuff.Start()
	
	#�����־�м�¼�����ش��󣬻��Ƿ���
	ExecManagerFunc("checklog",'Init')
	ExecManagerFunc("checklog",'Start')
	
