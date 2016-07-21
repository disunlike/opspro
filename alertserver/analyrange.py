# -*- coding:utf-8 -*-
'''
创建时间: Apr 11, 2016
作者: youzeshun  (IM: 8766)
用途:用于分析一次故障的影响范围

算法：

【假设故障点是线路】
1.按线路统计报警结果
2.受影响的线路是这经过这条线路的两个机房

【假设故障点是机房】
1.先按照机房统计监控节点，报警/被报警最多的机房视为故障点 

报警方是故障点：被他报警过的都说明已经被影响
被报警方是故障点：所有报过他的说明已经被影响

'''

import datamnt
from define import *
from public.define import *

class CAnalyRange():			#本来没必要写成类的，但为了能使用测试指令
	def __init__(self):
		self.m_SummaryDict={
				'netrange'			:[],
				'srrange'			:[],
				'influence percent'	:'',		
				}
	
	def SearchSR(self,sIP):
		for sSRName,IPList in datamnt.SERVER_ROOM_DICT.items():
			if sIP in IPList:
				return sSRName
			#sErr='ip:%s 没有找到对应的机房'%(sIP)
			#Log(PATH_LOG_CRIT,sErr)
			
	def LineRange(self,VectorList):
		if not VectorList:
			return []
		sDestination,sSource=VectorList
		
		RangeList=[]
		for sk,vList in datamnt.SERVER_ROOM_DICT.items():
			if sDestination in vList:
				RangeList+=vList
			
			elif sSource in vList:
				RangeList+=vList
			else:
				sText='LineRange:监控节点的ip 不在配置文件中，请查证'
		return RangeList
	
	def SRRange(self,sIP):
		if not sIP:
			return []
		RangeList=[]
		if sIP in datamnt.OPERATORS_IP_DICT['dx']:
			return datamnt.OPERATORS_IP_DICT['dx']
		
		elif sIP in datamnt.OPERATORS_IP_DICT['lt']:
			return datamnt.OPERATORS_IP_DICT['lt']
		
		elif sIP in datamnt.OPERATORS_IP_DICT['yd']:
			return datamnt.OPERATORS_IP_DICT['yd']
		
		elif sIP in datamnt.OPERATORS_IP_DICT['gbp']:
			return datamnt.OPERATORS_IP_DICT['dx']+datamnt.OPERATORS_IP_DICT['lt']+datamnt.OPERATORS_IP_DICT['yd']
		else:
			sText='监控节点的ip:%s不在配置文件中，请查证'%(sIP)
	
	def IpIntoSR(self,IPList):
		SRList=[]
		for sIP in IPList:
			sSRName=self.SearchSR(sIP)
			if not sSRName in SRList:
				SRList.append(sSRName)
		return SRList
	
	def Format(self,DataList):
		sSummary='\n'.join(DataList)
		return sSummary
	
	def IPFaultRange(self,sIP,VectorLsit):
		IPRangeList=[]
		for sThief,sPolice in VectorLsit:
			if sThief == sIP:
				if not sPolice in IPRangeList:
					IPRangeList.append(sPolice)
			if sPolice == sIP:
				if not sThief in IPRangeList:
					IPRangeList.append(sThief)
		return IPRangeList
	
	def SRFaultRange(self,IPRangeList):
		SRRangeList=[]
		for sIP in IPRangeList:
			sSRName=self.SearchSR(sIP)
			if sSRName in SRRangeList:
				continue
			SRRangeList.append(sSRName)
		return SRRangeList
	
	def ALLSR(self):#统计机房的总数
		iSum=0
		for sSRName,IPList in datamnt.SERVER_ROOM_DICT.items():
			iSum+=len(IPList)
		return iSum
	
	#和一个机房有监控关系的所有机房的数量.
	#如果故障点是一个私网ip，转为公网ip进行分析
	def SumMonitor(self,IPFault):
		if IPFault in datamnt.OPERATORS_IP_DICT['sw']:
			for MonitNodeDict in datamnt.MONITOR_NODE_LIST:
				if not MonitNodeDict['sw']==IPFault:
					continue
				
				if MonitNodeDict.has_key('bgp'):			#只可能是一个BGP结点
					return self.ALLSR()
				elif MonitNodeDict.has_key('dx') and MonitNodeDict.has_key('lt') and MonitNodeDict.has_key('yd'):
					return len(datamnt.OPERATORS_IP_DICT['dx'])+datamnt.OPERATORS_IP_DICT['lt']+datamnt.OPERATORS_IP_DICT['yd']-1
				elif MonitNodeDict.has_key('dx') and MonitNodeDict.has_key('lt'):	#双线监控
					return len(datamnt.OPERATORS_IP_DICT['dx'])+len(datamnt.OPERATORS_IP_DICT['lt'])-1
				elif MonitNodeDict.has_key('dx') and MonitNodeDict.has_key('yd'):	#双线监控
					return len(datamnt.OPERATORS_IP_DICT['dx'])+len(datamnt.OPERATORS_IP_DICT['yd'])-1
				elif MonitNodeDict.has_key('lt') and MonitNodeDict.has_key('yd'):
					return len(datamnt.OPERATORS_IP_DICT['lt'])+len(datamnt.OPERATORS_IP_DICT['yd'])-1
				elif MonitNodeDict.has_key('dx'):
					return len(datamnt.OPERATORS_IP_DICT['dx'])-1
				elif MonitNodeDict.has_key('lt'):
					return len(datamnt.OPERATORS_IP_DICT['lt'])-1
				elif MonitNodeDict.has_key('yd'):
					return len(datamnt.OPERATORS_IP_DICT['yd'])-1
					
		for sPerator,IPList in datamnt.OPERATORS_IP_DICT.items():
			if not IPFault in IPList:
				continue
			if sPerator=='bgp':
				iSumMonitor=self.ALLSR()									#所有IP
			else:
				iSumMonitor=len(IPList)+len(datamnt.OPERATORS_IP_DICT['sw'])		#同运营商+BGP
			return iSumMonitor
		sError='故障IP:%s没有分析出具有监控关系的机房数'%(IPFault)
		Log(PATH_LOG_CRIT,sError)
	
	def Clear(self):
		self.__init__()
		
	def Start(self,DataDict):
		
		self.Clear()
		if 'fault' in DataDict['line']:
			lstFaultLine=GetFault()		#受影响的机房范围
			sThiefIP=lstFaultLine[0]
			sPoliceIP=lstFaultLine[1]
			sThiefName=datamnt.IPToName(sThiefIP)
			sPoliceName=datamnt.IPToName(sPoliceIP)
			
			self.m_SummaryDict={
							'srrange'	:(sThiefName,sPoliceName),
							}
			return self.m_SummaryDict
		
		if 'fault' in DataDict['sr']:
			
			VectorList	=GetVector()
			IPFault		=GetFault()
			IPRangeList=self.IPFaultRange(IPFault,VectorList)		#报警矢量中和故障点有关的IP

			SRRangeList=self.SRFaultRange(IPRangeList)				#有关IP所在的机房视为受影响的机房
			
			iSumMnt=self.SumMonitor(IPFault)							#和故障IP具有监控关系的所有机房列表
			sPercent='%i/%i'%(len(SRRangeList),iSumMnt)
			#DataDict['accuracy']=round(len(SRRangeList)/1.0/iSumMnt,2)	#反应了报警的可靠程度
			self.m_SummaryDict={
							'netrange'			:IPRangeList,
							'srrange'			:SRRangeList,
							'influence percent'	:sPercent,
							}
			return self.m_SummaryDict
		
