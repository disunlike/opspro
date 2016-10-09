# -*- coding:utf-8 -*-
#　尤泽顺　(IM:8766)
'''
用途：
	dos.py
		检查是否发生dos攻击

模块说明：
	analysis：提供数据分析。目前分析数据的变化特征是否符合dos的特性
	dev:提供设备的管理，比如获得ＩＯ使用，系统负载。目前用于获得网卡流量
	log:只是一个文件夹，用于保管其他程序生成的日志
	public:通用代码。比如写日志，火星报警，路径解析
	shellcmd:封装shell命令
	
	各模块的运行状况写：txtlog.Write('status/脚本名称','开始检查流量')
	各模块产生的日志写：txtlog.Write('包名称/脚本名称','开始检查流量')
	各模块的产生的数据写：txtlog.Write('data/脚本名称','开始检查流量')

注意：
	游戏服上部署代码的坏处：
		1.【重点】给游戏服带来额外的负载
		2周五更新代码
		3.要拿日志分析得找人

	部署在zabbix结点的坏处
	1.【难点】交换机和主机的对应关系不好确认
	2.监控结点和游戏服负载提高
'''
import os
import analysis
import gsalert
import analydos
import checktraff
import gsconf
from public.define import *
from public import timerctrl
from public import txtlog
from dev import netcark
from dev import ip

def GetIP():
	sIP=os.popen(gsconf.PATH_SCRIPT_GET_IP).read()	#优先使用游戏服的方式获得ip
	if not sIP:
		oIP=ip.CDev()
		sIP=oIP.Start()
	return sIP


def Init(sLogPath,sRootPath):
	if not sLogPath:
		raise Exception('没有找到日志路径，请检查promanager.sh')
	SetGlobalManager('logpath',sLogPath)
	SetGlobalManager('rootpath',sRootPath)		#脚本的根路径，用于寻找资源
	SetGlobalManager("timer",timerctrl.CTimerManager())
	SetGlobalManager('ip',GetIP())
	'''
		用途：根据网卡流量检查dos
	'''
	oAnalyDos=analydos.CAnalyDos()
	oAnalyDos.SetInterval(gsconf.PERIOD_NORMAL)
	SetGlobalManager("analydos",oAnalyDos)					#为了能够使用测试代码对这个类进行测试，将其打包到这里
	SetGlobalManager("traff",checktraff.CCheckTraff())
	'''
		用途：获得网卡接收到的数据
		测试指令：python opspro/debuggs.py --mod=netcark --func=Traff
	'''
	SetGlobalManager("netcark",netcark.CDev()) 			#dev.DevDict这种方式会让全局变量和全局变量管理字典同时保存相同的内容。
	SetGlobalManager("txtlog",txtlog.CLog(sLogPath))
	#SetGlobalManager("imalert",alert.CIMAlert())
	SetGlobalManager("alert",gsalert.CAlertManager())
	
	
def Start():
	ExecManagerFunc("traff",'Init')
	ExecManagerFunc("traff",'Start')
	
