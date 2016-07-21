# -*- coding:utf-8 -*-
'''
1.只主动建立连接 -- 采集服务 -- 用继承的方式写
2.只被动建立连接 -- 数据中心 -- 用继承的方式写
3.既主动建立连接也被动建立 -- 去中心的监控网络
'''

import clientsocket
from public.define import *
from public import timerctrl
from net import psql
import clsconf
from public import txtlog
from public import txtcache
from net import pping

#socket保存在全局变量中以便不会被销毁

def Init(sLogPath,sRootPath):
	global oCollector
	
	SetGlobalManager('logpath',sLogPath)
	SetGlobalManager('rootpath',sRootPath)
	
	oTimerMgr=timerctrl.CTimerManager()
	SetGlobalManager("timer",oTimerMgr)
	
	SetGlobalManager("txtlog",txtlog.CLog(sLogPath))
	
	oCollector=clientsocket.CMasterSocket()
	SetGlobalManager('collectserver',oCollector)
	
	oTxtCache=txtcache.CCache()
	SetGlobalManager('txtcache',oTxtCache)
	
	oPSql=psql.CPSql(clsconf.PSQL_CACHE_PARH,'collectserver')
	SetGlobalManager("psql",oPSql)
	
	oPPing=pping.CPPing('collectserver')
	SetGlobalManager("pping",oPPing)
	
	oCollector.Start()
	
def Send(sData):
	oCollector=GetGlobalManager('collectserver')
	oCollector.Send(sData)
	
