# -*- coding:utf-8 -*-
'''
创建时间: Apr 15, 2016
作者: youzeshun  (IM: 8766)
用途:使用指令测试 gs项目的功能

真实的dos攻击流量数据：
2016-04-11 19:31:44 速度:607 kb/s 速度变化率: -2 kb/s^2 状态: ok 【Debug】StableCount: 0
2016-04-11 19:32:04 速度:587 kb/s 速度变化率: -1 kb/s^2 状态: ok 【Debug】StableCount: 0
2016-04-11 19:32:24 速度:589 kb/s 速度变化率: 0 kb/s^2 状态: ok 【Debug】StableCount: 0
2016-04-11 19:32:44 速度:74181 kb/s 速度变化率: 3679 kb/s^2 状态: warn 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:33:04 速度:123120 kb/s 速度变化率: 2446 kb/s^2 状态: warn 【Debug】StableCount: 1 动态阀值: 59344 kb/s
2016-04-11 19:33:25 速度:122559 kb/s 速度变化率: -29 kb/s^2 状态: warn 【Debug】StableCount: 2 动态阀值: 59344 kb/s
2016-04-11 19:33:45 速度:120664 kb/s 速度变化率: -95 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:34:05 速度:18980 kb/s 速度变化率: -5085 kb/s^2 状态: dos 【Debug】StableCount: 1 动态阀值: 59344 kb/s
2016-04-11 19:34:25 速度:36996 kb/s 速度变化率: 900 kb/s^2 状态: dos 【Debug】StableCount: 2 动态阀值: 59344 kb/s
2016-04-11 19:34:45 速度:120040 kb/s 速度变化率: 4152 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:35:05 速度:120043 kb/s 速度变化率: 0 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:35:25 速度:120024 kb/s 速度变化率: -1 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:36:05 速度:120003 kb/s 速度变化率: 0 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:36:25 速度:22531 kb/s 速度变化率: -4874 kb/s^2 状态: dos 【Debug】StableCount: 1 动态阀值: 59344 kb/s
2016-04-11 19:36:45 速度:3053 kb/s 速度变化率: -974 kb/s^2 状态: dos 【Debug】StableCount: 2 动态阀值: 59344 kb/s
2016-04-11 19:37:05 速度:99144 kb/s 速度变化率: 4804 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:37:25 速度:120030 kb/s 速度变化率: 1044 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:37:45 速度:120016 kb/s 速度变化率: -1 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:38:05 速度:120012 kb/s 速度变化率: -1 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:38:25 速度:120017 kb/s 速度变化率: 0 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:38:45 速度:120017 kb/s 速度变化率: 0 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:39:05 速度:120018 kb/s 速度变化率: 0 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:39:25 速度:120018 kb/s 速度变化率: 0 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:39:45 速度:120018 kb/s 速度变化率: 0 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:40:05 速度:120005 kb/s 速度变化率: -1 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:40:25 速度:126013 kb/s 速度变化率: 300 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:40:45 速度:120015 kb/s 速度变化率: -300 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
2016-04-11 19:41:05 速度:43953 kb/s 速度变化率: -3804 kb/s^2 状态: dos 【Debug】StableCount: 1 动态阀值: 59344 kb/s
2016-04-11 19:41:25 速度:4870 kb/s 速度变化率: -1955 kb/s^2 状态: dos 【Debug】StableCount: 2 动态阀值: 59344 kb/s
2016-04-11 19:41:45 速度:5997 kb/s 速度变化率: 56 kb/s^2 状态: ok 【Debug】StableCount: 0
2016-04-11 19:42:05 速度:5109 kb/s 速度变化率: -45 kb/s^2 状态: ok 【Debug】StableCount: 1
2016-04-11 19:42:25 速度:3550 kb/s 速度变化率: -78 kb/s^2 状态: ok 【Debug】StableCount: 0
2016-04-11 19:42:45 速度:3206 kb/s 速度变化率: -18 kb/s^2 状态: ok 【Debug】StableCount: 0
2016-04-11 19:43:05 速度:2332 kb/s 速度变化率: -44 kb/s^2 状态: ok 【Debug】StableCount: 0
2016-04-11 19:43:25 速度:1528 kb/s 速度变化率: -41 kb/s^2 状态: ok 【Debug】StableCount: 0
2016-04-11 19:43:45 速度:2201 kb/s 速度变化率: 33 kb/s^2 状态: warn 【Debug】StableCount: 0 动态阀值: 1760 kb/s
2016-04-11 19:44:05 速度:3303 kb/s 速度变化率: 55 kb/s^2 状态: warn 【Debug】StableCount: 1 动态阀值: 1760 kb/s
2016-04-11 19:44:25 速度:3301 kb/s 速度变化率: -1 kb/s^2 状态: warn 【Debug】StableCount: 2 动态阀值: 1760 kb/s
2016-04-11 19:44:45 速度:2894 kb/s 速度变化率: -21 kb/s^2 状态: warn 【Debug】StableCount: 0 动态阀值: 1760 kb/s
2016-04-11 19:45:05 速度:2694 kb/s 速度变化率: -10 kb/s^2 状态: ok 【Debug】StableCount: 0
2016-04-11 19:45:25 速度:2599 kb/s 速度变化率: -5 kb/s^2 状态: ok 【Debug】StableCount: 0
2016-04-11 19:45:45 速度:2681 kb/s 速度变化率: 4 kb/s^2 状态: ok 【Debug】StableCount: 0

测试指令：
	这是一段曾经被误报为dos的数据：（这里的单位是b）
	python opspro/debuggs.py --func=TestAanlyDos --argv=1432396986421,1432414792172,1432435820436,1432458231615,1432494929343,1432548198307,1432564332984,1432599473250,1432655966477,1432709524994,1432759501769,1432808219555,1432856046243,1432897716325,1432949388246,1432996938262,1433039138611,1433079379914,1433122774203,1433168981778,1433211183251,1433254309890,1433299122203

	曾经发生过的真实的dos攻击流量变化：（这里的单位是kb）
	python opspro/debuggs.py --func=TestAanlyDos --argv=607,587,589,74181,123120,122559,120664,18980,36996,120040,120043,120024,120003,22531,3053,99144,120030,120016,120012,120017,120017,120018,120018,120018,120005,126013,120015,43953,4870,5997,5109,3550,3206,2332,1528,2201,3303,3301,2894,2694,2599,2681

	测试环境下攻击软件打出来的一段流量：
	
'''
from gameserver.checktraff import *
from gameserver import *
from public.define import *
from public.debug import *
from gameserver.define import *

#测试模式下才会有输出，正式环境没有
#输入的是流量的速度，单位kb/s,相比于输入接收到的数据包对于测试者比较直观些，但不如输入数据包的总量那么准确
def TestAanlyDos(*SpeedList):
	oAnalyDos=GetGlobalManager('analydos')
	for sSpeed in SpeedList:
		oAnalyDos.ResetCountSummary()
		iSpeed=int(sSpeed)
		oAnalyDos.m_iSpeedPre=oAnalyDos.m_iSpeedNext
		oAnalyDos.m_iSpeedNext=iSpeed
		oAnalyDos.GetSlope()
		
		if oAnalyDos.m_iUnstable>0:
			oAnalyDos.m_iUnstable-=1
			continue
		oAnalyDos.OnCommand()
		oAnalyDos.Summary()
		SummaryDict=GetSummaryDict()

def TestCheckTraff(*TraffList):
	for sTraff in TraffList:
		ExecManagerFunc('analydos','Start',int(sTraff))	#将流量数据进行分析
		ResultDict=ExecManagerFunc('traff','FormatEvent')	#获得对流量的分析结果
		if 'body' in ResultDict:
			print ResultDict['body']
		else:
			print ResultDict
		
#上次报警出现了发现攻击，但是报警失败的情况
def TestAlert(sMsg='',IM=8766):
	if not sMsg:
		sMsg='【测试报警模块】\n\
【异常流量结束】172.168.128.9[当前速度]0.00 m/s[当前速度变化率]0 kb/s^2\n\
开始时间：2016-05-04 14:31\n\
结束时间：2016-05-04 14:32\n\
持续时间：0.2 分钟\n\
流量峰值：4.6 M/s'
	ExecManagerFunc('alert','Alert',sMsg,IM)

if __name__=='__main__':
	Debug(locals())
	#测试报警是否可用
	'python opspro/debuggs.py --func=TestAlert --argv=测试报警模块能否正常调用,8766'
	#测试dos的计算
	'python opspro/debuggs.py --func=TestCheckTraff --argv=0,0,0,0,84000000,116000000,31100000011,40000002211,5000000,60000000,7000000,8000000'
	
