# -*- coding:utf-8 -*-
'''
Created on Feb 19, 2016
author: youzeshun  (IM: 8766)

#用途：从保存有nagios报警记录的数据库中读取信息，分析报警然后发送结论

流程：
1.dbMgr循环检查数据库
2.StatiAlert过滤（私网等）统计（有效信息：源和目的地）
3.analyfault分析统计结果
4.CAlert处理分析结果
'''

from public.define import *
from define import *
import alsconf
import copy
import analyrange
from alertserver import datamnt

g_IsSend = True

def GetNewAlert():
	DataList = ExecManagerFunc('dbnagios', 'CheckUpdate', alsconf.DB_NAGIOS_TABLE)  # Content表如果更新了，则把更新的内容交给g_oStati.Start
	return DataList

def StatiAlert(NewDataList):
	ExecManagerFunc('stati', 'Start', NewDataList)

def AnalyFault():
	dSummary = GetManagerAttr('stati', 'm_SummaryDict')
	dStati = copy.deepcopy(dSummary)
	ExecManagerFunc("analyfault", 'Start', dStati)

def SendSummary(dSummary):
	global g_IsSend
	if not dSummary:
		return
	if not 'body' in dSummary:
		return
	if GetLevel() == 1:  # 最少需要xx条报警发送到群中.一次判断故障后不会再对此次故障的累计结果进行报警
		if g_IsSend:
			g_IsSend = False
			Alert(dSummary, alsconf.OPS_MNT)
	else:
		g_IsSend = True
		if GetSum() >= alsconf.THR_MIN_USER_SEND:  # 最少需要xx条报警才发送给使用者
			ExecManagerFunc('delayalert', 'Alert', dSummary, alsconf.IM_USER, 1, alsconf.PATH_LOG_ALERT)
		
def TranSRRange(SRList):
	TmpList = []
	for sSRAbbr in SRList:
		sSRName = datamnt.AbbrToName(sSRAbbr)
		if sSRName:
			TmpList.append(sSRName)
		else:
			sDebug = '简称转全称过程失败,简称为%s：' % (sSRAbbr)
			Log(PATH_LOG_ERR, sDebug)
	return TmpList

def FormatSRInfo():
	FaultDict = GetManagerAttr('analyfault', 'm_SummaryDict')
	if GetLevel() == 1:
		sFaultType	 = '级别：故障'
	else:
		sFaultType	 = '级别：波动'
	sSRAbbr		 = FaultDict['sr']['title']
	sSRName		 = datamnt.AbbrToName(sSRAbbr)
	sTitle		 = '位置：%s(%s)' % (sSRName, FaultDict['sr']['fault'])
	
	SRAbbrList	 = GetSRRange()
	SRNameList	 = TranSRRange(SRAbbrList)
	sSRRange	 = '影响机房范围：%s %s'		 % (GetInfluencePercent(), ','.join(SRNameList))
	# sNetRange	='影响网络范围：%s'%(str(SummaryDict['netrange']))		#运维-小桂子(2693) 2016-4-20 这个我认为先不要加了，意义不大
	sStartTime	 = '起始统计时间：%s'			 % (GetStartTime())
	sEndTime	 = '结束统计时间：%s'			 % (GetEndTime())
	sSum		 = '（以上消息基于%i条报警）'	 % (GetSum())
	# sPerce=str(SummaryDict['perce'])
	SummaryDict = {
			'title'	:sTitle,
			'body'	:sFaultType + '\n' + sTitle + '\n' + sSRRange + '\n' + sStartTime + '\n' + sEndTime + '\n' + sSum,
			}
	return SummaryDict

def FormatLineInfo():
	sThiefName, sPoliceName = GetSRRange()
	sThiefIPe, sPoliceIP = GetFault()
	sOperator = datamnt.IPToOperator(sPoliceIP)
	if GetLevel() == 1:
		sFaultType	 = '级别：故障'
	else:
		sFaultType	 = '级别：波动'
	sTitle		 = '位置：%s>>>%s>>>%s'		 % (sThiefName, sOperator, sPoliceName)
	sSRRange	 = '影响机房范围：%s,%s'		 % (sThiefName, sPoliceName)
	# sNetRange	='影响网络范围：%s'%(str(SummaryDict['netrange']))		#运维-小桂子(2693) 2016-4-20 这个我认为先不要加了，意义不大
	sStartTime	 = '起始统计时间：%s'			 % (GetStartTime())
	sEndTime	 = '结束统计时间：%s'			 % (GetEndTime())
	sSum		 = '（以上消息基于%i条报警）'	 % (GetSum())
	# sPerce=str(SummaryDict['perce'])
	SummaryDict = {
			'title'	:sTitle,
			'body'	:sFaultType + '\n' + sTitle + '\n' + sSRRange + '\n' + sStartTime + '\n' + sEndTime + '\n' + sSum,
			}
	return SummaryDict

# {'title': ('cz', 'sy'), 'netrange': ['112.73.64.4', '222.132.63.4', '124.95.140.119'], 'fault': ('cz', 'sy'), 'perce': 1.0, 'type': 'line', 'srrange': ('cz', 'sy')}
# 需要额外增加一种没有匹配到任何规则，但是需要让人知道现在的故障分布的情况
def Format():
	FaultDict = GetManagerAttr('analyfault', 'm_SummaryDict')
	if 'title' in FaultDict['line']:
		SummaryDict = FormatLineInfo()
	elif'title' in FaultDict['sr']:
		SummaryDict = FormatSRInfo()
	else:
		return {}
	return SummaryDict

def IsGtTHR(SummaryDict):
	if SummaryDict['type'] == 'server room':
		if SummaryDict['percent'] >= alsconf.THR_SR:  # 用于衡量报警的可信度
			return 1
		sText = '可信度不足的结论' + str(SummaryDict)
		Log(PATH_LOG_DEBUG, sText)
		return 0
	elif SummaryDict['type'] == 'line':
		if SummaryDict['percent'] >= alsconf.THR_LINE:
			return 1
		sText = '可信度不足的结论' + str(SummaryDict)
		Log(PATH_LOG_DEBUG, sText)
		return 0

def Debug(SummaryDict):
	if SummaryDict:
		SRStatiDict = GetSRStati()
		LineStatiDict = GetLineStati()
		dDebug = {
				'title'	:'Debug:' + str(SummaryDict['title']),
				'body'	:'【nagios自动分析】开发者Debug消息\n【正文】：\n' + SummaryDict['body'] + '\n【Debug】\n报警准确否：' + str(SRStatiDict) + str(LineStatiDict) + '\ntitle重复否:' + str(SummaryDict['title']),
			}
		# if alsconf.IM_USER==alsconf.IM_GROUP_DEVELOPER:		#说明是调试状态
		# 	dDebug['body']='【测试版信息】\n'+SummaryDict['body']
		Alert(dDebug, alsconf.IM_GROUP_DEVELOPER)
		return
	StatiList = GetVector()
	dDebug = {
				'title'	:'Debug:没有匹配中',
				'body'	:'【nagios自动分析】开发者Debug消息\n矢量信息%s' % (str(StatiList)),
			}
	if not 'body' in SummaryDict:
		return
	if alsconf.IM_USER == alsconf.IM_GROUP_DEVELOPER:  # 说明是调试状态
		dDebug['body'] = '【测试版信息】\n' + SummaryDict['body']
	Alert(dDebug, alsconf.IM_GROUP_DEVELOPER)
	
def AnalyRange():
	SummaryDict = GetManagerAttr("analyfault", 'm_SummaryDict')
	if SummaryDict:
		ExecManagerFunc('range', 'Start', copy.deepcopy(SummaryDict))

def AutoAnaly(NewDataList):
	StatiAlert(NewDataList)  # 统计报警信息
	AnalyFault()  # 定位故障点
	AnalyRange()
	SummaryDict = Format()  # 格式化报警数据
	SendSummary(SummaryDict)  # 发送结论
	Debug(SummaryDict)
	
# #检查最近一条记录的产生时间，如果有更新的则激活算法，并一次性读取所有更新的内容
def Start():
	Remove_Call_Out('nagiosping')
	Call_Out(Functor(Start), alsconf.PERIOD_CHECK_DB, 'nagiosping')  # 为了不重名，使用文件名作为注册名
	# 将各个功能拆开，方便进行测试
	NewAlertList = GetNewAlert()  # 获得最新的报警信息
	AutoAnaly(NewAlertList)
	
