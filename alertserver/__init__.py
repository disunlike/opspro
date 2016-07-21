# -*- coding:utf-8 -*-
'''
Created on Feb 25, 2016
author: youzeshun  (IM: 8766)

#用途：报警自动化服务器，用于分析信息，将故障定位后发送到群里

业务特点：
1.报警是不均匀的，当一个故障点出现，不同的监控节点报警的次数不均匀。故而分析报警源比较不可靠
2.报警的频率能够在遇到故障点时自动增加

运维-小桂子(2693) 2016-4-11 14:59:51
这个分析的目标就是：当出现异常时，我们需要知道
1、是哪个机房/线路异常了；
2、异常的范围是哪些，影响到这个机房和哪些机房的互联；

修改目标：

系统消息 2016-5-4 10:39:06
故障类型：线路
故障点：
		常州>>>中山
		（即：网段>>>网段）
		（即：出口>>出口）
影响机房范围：
		常州（xx网段）（xx/xx条）
		中山（xx网段）（xx/xx条）
起始统计时间：2016-05-04 10:32:54
结束统计时间：2016-05-04 10:38:04
（以上消息基于2条报警）
一周之内该点xx次被判断为故障点，排列x/x
'''

import analysis
import shellcmd
import dev
import nagiosping
import alsconf
import delayalert
import statialert
import analyzabbix
import analyrange
from public.define import *
from public import timerctrl
from public import txtlog
from public import alert
from db import dbmgr
from alertserver import analyfault

def Init(sLogPath,sRootPath):
	
	SetGlobalManager('logpath',sLogPath)
	SetGlobalManager('rootpath',sRootPath)
	
	#设置数据库
	oDBNagios=dbmgr.CDBManager(alsconf.DB_NAGIOS_HOST,
								alsconf.DB_NAGIOS_USER,
								alsconf.DB_NAGIOS_PSW,
								alsconf.DB_NAGIOS_NAME
								)
	SetGlobalManager("dbnagios",oDBNagios)
	
	oDBZabbix=dbmgr.CDBManager(alsconf.DB_ZABBIX_HOST,
								alsconf.DB_ZABBIX_USER,
								alsconf.DB_ZABBIX_PSW,
								alsconf.DB_ZABBIX_NAME
								)
	SetGlobalManager("dbzabbix",oDBZabbix)
	
	oAnalyManager=analyfault.CAnalyManager()
	SetGlobalManager("analyfault",oAnalyManager)
	
	oBound=analyzabbix.CBound()
	SetGlobalManager("bound",oBound)
	
	oCStatiAlert=statialert.CStatiAlert()
	SetGlobalManager("stati",oCStatiAlert)
	
	oAnalyRange=analyrange.CAnalyRange()
	SetGlobalManager("range",oAnalyRange)
	
	oTimerMgr=timerctrl.CTimerManager()
	SetGlobalManager("timer",oTimerMgr)
	SetGlobalManager("devdict",dev.Init()) #dev.DevDict这种方式会让全局变量和全局变量管理字典同时保存相同的内容。
	SetGlobalManager("alert",alert.CAlertManager())
	SetGlobalManager("txtlog",txtlog.CLog(sLogPath))
	SetGlobalManager('shelldict',shellcmd.Init())
	SetGlobalManager('delayalert',delayalert.CDelayAlert())
	#开始加载功能模块
	#检查日志中记录的严重错误，火星发送
	Log('status/alertserver','开始加载nagiosping')

def Start():
	nagiosping.Start()

