# -*- coding:utf-8 -*-

#数据中心服务器必须和数据采集服务配合

from dataserver import mastersocket
from public.define import *
from public import timerctrl
from db import dbmgr
from net import psql
from public import txtlog
import dtsconf
from net import pping

def Init(sBindIP,iPort,iMaxCon,sLogPath,sRootPath):
	
	SetGlobalManager('logpath',sLogPath)
	SetGlobalManager('rootpath',sRootPath)
	
	oTimerMgr=timerctrl.CTimerManager()
	SetGlobalManager("timer",oTimerMgr)
	
	SetGlobalManager("txtlog",txtlog.CLog(sLogPath))
	
	oDataServer=mastersocket.CMasterSocket()
	oDataServer.SetSocket(sBindIP,iPort,iMaxCon)
	SetGlobalManager("dataserver",oDataServer)
	
	oDBManager=dbmgr.CDBManager(dtsconf.DB_HOST,dtsconf.DB_USER,dtsconf.DB_PSW,dtsconf.DB_Name)
	SetGlobalManager("dbmanager",oDBManager)
	
	#第二参数表示将处理好的数据传给谁
	oPSql=psql.CPSql(dtsconf.PSQL_CACHE_PARH,"dataserver")
	SetGlobalManager("psql",oPSql)
	
	oPPing=pping.CPPing('dataserver')
	SetGlobalManager("pping",oPPing)

def Start():
	oDataServer=GetGlobalManager('dataserver')
	oDataServer.Start()

