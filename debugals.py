# -*- coding:utf-8 -*-
'''
Created on 2016/4/22
author: youzeshun  (IM: 8766)
用途 ：
	不修改正式代码的情况下对als项目进行测试
Demo :
	#测试als项目的报警模块（alert）下的函数
	python opspro/debugals.py --mod=alert --func=Alert --argv=8766,AlertMsg
	
	#使用自定义的函数进行测试
	python opspro/debugals.py --func=QuickAnaly
	
	#
	python opspro/debugals.py --mod=stati --func=IsIgnore --argv=10.79.34.237,183.61.86.28
	
	python opspro/debugals.py --mod=stati --func=CorrectErr --argv=10.79.33.130,121.201.116.28



代码测试例子：
	测试指令：
			python opspro/debugals.py --func=CustomAnaly --argv='2016-5-1 21:53:00','2016-5-1 21:54:47'
			【测试版信息】
			故障类型：线路
			故障点：常州>>>中山
			影响机房范围：常州,中山
			起始统计时间：2016-05-01 21:53:46
			结束统计时间：2016-05-01 21:53:47
			（以上消息基于2条报警）
			
			python opspro/debugals.py --func=CustomAnaly --argv='2016-4-27 23:15:11','2016-4-27 23:22:33'
			【测试版信息】
			故障类型：机房
			故障点：常州(112.73.64.4)
			影响机房范围：7/28 阿里杭州D,腾讯北京1区,腾讯广州1区,阿里杭州B,顺德,中山,阿里北京B
			起始统计时间：2016-04-27 23:15:21
			结束统计时间：2016-04-27 23:20:21
			（以上消息基于20条报警）
			
			python opspro/debugals.py --func=CustomAnaly --argv='2016-06-02 19:32:00','2016-06-02 19:33:00'
			系统消息 2016-6-3 16:21:56
			级别：故障
			位置：沈阳(10.82.140.119)
			影响机房范围：6/7 腾讯北京1区,阿里北京B,阿里深圳B,济南,阿里上海B,中山
			起始统计时间：2016-06-02 19:32:32
			结束统计时间：2016-06-02 19:32:55
			（以上消息基于11条报警）
			
			python opspro/debugals.py --func=CustomAnaly --argv='2016-06-12 14:52:00','2016-06-12 15:07:00'

			python opspro/debugals.py --func=CustomAnaly --argv='2016-6-12 16:38:00','2016-6-12 16:41:00'
'''

from alertserver import *
from public.debug import *
from db import dbmgr
import time

DB_HOST='172.168.128.8'
DB_USER='root'
DB_PSW='youzeshun'
DB_Name='alarms'
#
g_AlertDict={
	#故障点是常州 
	'sql2':'select * from content where `timestamp` > "2016-4-27 23:15:11" and `timestamp` < "2016-4-27 23:22:33"',
	}
#故障点：中山机房，python opspro/debugals.py --func=CustomAnaly --argv='2016-5-1 11:23:00','2016-5-1 11:25:00'
def QuickAnaly(iKey):
		from public.define import ExecManagerFunc
		from alertserver.nagiosping import AutoAnaly
		if not g_AlertDict.has_key(iKey):
			print '不存在的键名'
			return
		sSql=g_AlertDict[iKey]
		NewAlertList=ExecManagerFunc('dbnagios','Search',sSql)
		AutoAnaly(NewAlertList)

def PrintList(NewAlertList):
	print '被分析的数据为：'
	for i in NewAlertList:
		print '    ',i

# python opspro/debugals.py --func=CustomAnaly --argv='2016-4-29 04:27:00','2016-4-29 04:28:00'
def CustomAnaly(sStartTime,sEndTime):
		from public.define import ExecManagerFunc
		sSql='select * from content where `timestamp` > "%s" and `timestamp` < "%s"'%(sStartTime,sEndTime)
		NewAlertList=ExecManagerFunc('dbnagios','Search',sSql)
		PrintList(NewAlertList)
		if NewAlertList:
			nagiosping.StatiAlert(NewAlertList)		#统计报警信息
			nagiosping.AnalyFault()		#定位故障点
			print GetManagerAttr("analyfault",'m_SummaryDict')
			nagiosping.AnalyRange()
			SummaryDict=nagiosping.Format()				#格式化报警数据
			nagiosping.SendSummary(SummaryDict)					#发送结论
			nagiosping.Debug(SummaryDict)
		
def GetSql(sContent):
	sSql='INSERT INTO `alarms`.`content` (`id`, `timestamp`, `nlevel`, `hostname`, `descs`, `status`, `shost`) VALUES (%s);'%(sContent)
	return sSql

def LineFault():
	SqlList=[
		'NULL, "2016-02-24 01:02:27", "[CRITICAL]", "CZ_222.132.63.4", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "SY-124.95.140.119"',
		'NULL, "2016-02-24 01:02:37", "[CRITICAL]", "CZ_222.132.63.4", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "SY-124.95.140.119"',
		'NULL, "2016-02-24 01:02:47", "[CRITICAL]", "SY-124.95.140.119", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "CZ_222.132.63.4"',
	]
	Insert(SqlList)

def SRFault():
	SqlList=[
		'NULL, "2016-02-24 01:02:57", "[CRITICAL]", "CZ_222.132.63.4", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "SY-124.95.140.119"',
		'NULL, "2016-02-24 01:03:37", "[CRITICAL]", "ALI-SH-B_139.196.252.251", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "SY-124.95.140.119"',
	]
	Insert(SqlList)

def PriLineFault():
	SqlList=[
		'NULL, "2016-02-24 01:02:27", "[CRITICAL]", "QQ-BJ-1_10.79.22.36", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "ALI-SZ-B-120.25.199.237"',
		'NULL, "2016-02-24 01:02:37", "[CRITICAL]", "QQ-BJ-1_10.79.22.36", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "ALI-SZ-B-120.25.199.237"',
		'NULL, "2016-02-24 01:02:47", "[CRITICAL]", "ALI-SZ-B-120.25.199.237", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "QQ-BJ-1_10.79.22.36"',
	]
	Insert(SqlList)

def PriSRFault():
	SqlList=[
		'NULL, "2016-02-24 01:02:27", "[CRITICAL]", "QQ-BJ-1_10.79.22.36", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "ALI-SZ-B-120.25.199.237"',
		'NULL, "2016-02-24 01:02:37", "[CRITICAL]", "QQ-BJ-1_10.79.22.36", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "ZS-3_10.82.102.19"',
		'NULL, "2016-02-24 01:02:47", "[CRITICAL]", "QQ-BJ-1_10.79.22.36", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "QQ-BJ-1_10.79.22.36"',
	]
	Insert(SqlList)

#测试分布插入
def Step():
	time.sleep(10)
	SqlList=[
		'NULL, "2016-02-24 01:02:27", "[CRITICAL]", "CZ_10.82.64.4", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "ZS-183.61.80.191"',
		'NULL, "2016-02-24 01:02:37", "[CRITICAL]", "ZS-2_120.31.145.12", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "QQ-SH-1-115.159.190.168"',
		'NULL, "2016-02-24 01:02:47", "[CRITICAL]", "ALI-SH-B_10.79.34.251", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "ZS-121.201.102.19"',
		'NULL, "2016-02-24 01:02:47", "[CRITICAL]", "ZS-2_10.82.80.191", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "222.211.64.201"',
		'NULL, "2016-02-24 01:02:47", "[CRITICAL]", "ZS-2_10.82.80.191", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "JN-123.129.209.12"',
		'NULL, "2016-02-24 01:02:47", "[CRITICAL]", "ZS-2_10.82.80.191", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "ALI-HZ-D-120.26.0.237"',
		'NULL, "2016-02-24 01:02:47", "[CRITICAL]", "ZS-2_120.31.145.12", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "JN-119.188.15.147"',
		'NULL, "2016-02-24 01:02:47", "[CRITICAL]", "ZS-1_10.82.86.28", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "JN-119.188.15.147"',
	]
	Insert(SqlList)
	time.sleep(10)
	SqlList=[
		'NULL, "2016-02-24 01:02:27", "[CRITICAL]", "JN-1_10.82.209.12", "ping state", "CRITICAL - 222.132.63.4 rta 46.833ms, lost 60%", "FS-219.132.195.81"',
	]
	Insert(SqlList)
	time.sleep(10)

def Insert(SqlList):
	oDBManager=dbmgr.CDBManager(DB_HOST,DB_USER,DB_PSW,'alarms')
	for sSql in SqlList:
		sSql=GetSql(sSql)
		oDBManager.Insert(sSql)

def Search():
	sSql='select * from content where `timestamp` > "2016-4-25 16:58:00" and `timestamp` < "2016-4-25 17:00:00"'
	print ExecManagerFunc('dbnagios','Search',sSql)

def TestDelayAlert():
	SummaryDict={
				'title':'title',
				'body':'这是测试多人报警的情况，部分人会接收重复报警',
				}
	Alert(alsconf.IM_USER, SummaryDict)
	print '分割线'
	Alert(alsconf.IM_USER, SummaryDict)

#如何用指令启动子定义的测试函数，这是为了减少对测试代码的修改
if __name__=='__main__':
	Debug(locals())
	
