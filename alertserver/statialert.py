# -*- coding:utf-8 -*-
'''
创建时间: Apr 11, 2016
作者: youzeshun  (IM: 8766)
用途:和分析故障的算法无关的通用统计（无论采取什么算法都必须统计的数据）

从数据库的最新记录中统计出满足下面条件的记录
1.统计私网IP的坏处：
	当公网出现问题的时候私网也会有问题。此时同时将私网纳入报警分析会出现部分报警是重复的。
	pub_a->pub_b	#结论：无
	pri_a->pri_b	#结论：线路a->b
	
2.记录的ip都是被ipsort文件注册过的

统计规则：
	波动统计算法：
		情况一：
			2:15 现在有一条报警a->b  统计结果　报警方　｛a:1｝ 	 被报警方　{b:1}		结论：无
			(间隔１分钟,继承上一分钟的数据)
			2:16 b->a     		统计结果　报警方　｛a:1，b:1｝ 	 被报警方　{a:1,b:1}		结论：无
			(间隔１分钟，继承上一分钟的数据)
			2:17 c->a		统计结果　报警方　｛a:1，b:1,c:1} 被报警方　{a:2,b:1}		结论：a节点有问题，报警
			2:18 a->c		统计结果　报警方　｛a:2，b:1,c:1} 被报警方　{a:2,b:1,c:1} 	结论：a节点有问题，报警
	
		情况二：
			2:15 现在有一条报警a->b  统计结果　报警方　｛a:1｝ 	 被报警方　{b:1}		结论：无
			(间隔１分钟,继承上一分钟的数据)
			2:16 b->a     		统计结果　报警方　｛a:1，b:1｝ 	 被报警方　{a:1,b:1}		结论：无
			(间隔１分钟，继承上一分钟的数据)
			2:17 c->a		统计结果　报警方　｛a:1，b:1,c:1} 被报警方　{a:2,b:1}		结论：a节点有问题，报警
			(间隔超过十分钟，不继承数据，重新分析)
			2:28 a->c		统计结果　报警方　｛a:1｝ 	 被报警方　{c:1}		结论：无
	
	故障统计算法：
		优先级高于波动算法（先进行故障匹配，再进行波动匹配）
		每次启动波动统计时检查过去一分钟内有没报警超过十条的现象。有则标识为故障，无则标识为波动。
		
		python opspro/debugals.py --func=CustomAnaly --argv='2016-06-02 19:32:00','2016-06-02 19:33:00'
		故障类型：机房
		故障点：沈阳(10.82.140.119)
		影响机房范围：6/7 腾讯北京1区,阿里北京B,阿里深圳B,济南,阿里上海B,中山
		起始统计时间：2016-06-02 19:32:32
		结束统计时间：2016-06-02 19:32:55
		（以上消息基于11条报警）
'''

from public.define import *
from alertserver import alsconf
from alertserver import datamnt
import re

class CStatiAlert():
	def __init__(self):
		self.m_StableCount 	 = 0  # 通过稳定计数器来判断当前的状态是波动还是真的发生了问题
		self.m_VectorList 	 = [] # 过滤以后的矢量信息，即(被报警方，报警方)
		self.m_lstValid 	 = [] # 过滤以后的完整信息，既数据库的记录
		self.m_iFault 	     = None
		self.m_Level		 = ''  # 表示等级：波动-故障
		self.m_SummaryDict 	 = {
					'vector':[],
					'sum'	:0,
					'start'	:'',
					'end'	:'',
					}
	
	
	def IsUpDate(self, lstData):
		if lstData:
			return 1
		return 0
	
	def Start(self, lstData):
		if self.IsReset(lstData):
			self.Reset()
		elif self.IsUpDate(lstData):  # 没有新数据，不重新进行分析
			self.Update(lstData)
		return self.m_SummaryDict  # 这个return用于测试而不用于传值，对象的流水线方式组织会让代码难以调试！
	
	def Reset(self):
		self.m_VectorList 	 = []  # 尽量不适用del管理列表
		self.m_SummaryDict	 = {  # 将变量m_SummaryDict指向另一个内存快，让原内存块的引用计数-1
						'vector':[],
						'sum'	:0,
						'start'	:'',
						'end'	:'',
					}
		self.m_Level		 = ''  # 表示等级：波动-故障
		self.m_lstValid		 = []
		self.m_iFault 	     = None
	
	
	def ResetFault(self):
		self.m_iFault=None
	
	
	def IsReset(self, Data):
		if Data:
			self.m_StableCount = alsconf.STABLE_COUNT
		else:
			self.m_StableCount -= 1
			
		if self.m_StableCount < 0:
			return 1
		return 0
	
	
	def MatchIP(self, sAddr):
		oResult = re.search(r'\d+\.\d+\.\d+\.\d+', sAddr)  # 匹配所有ＩＰ
		if oResult:
			return oResult.group(0)
	
	
	# IP必须是已经被注册的
	def IsRegIP(self, sIP):
		if not sIP:
			return 0
		if sIP in datamnt.OPERATORS_IP_DICT['dx']:
			return 1
		elif sIP in datamnt.OPERATORS_IP_DICT['lt']:
			return 1
		elif sIP in datamnt.OPERATORS_IP_DICT['yd']:
			return 1
		elif sIP in datamnt.OPERATORS_IP_DICT['bgp']:
			return 1
		elif sIP in datamnt.OPERATORS_IP_DICT['sw']:
			return 1
		else:
			sErr = '监控节点的ip:%s不在配置文件中，请查证' % (sIP)
			Alert(alsconf.IM_GROUP_MATINTAIN, sErr)
			Log(PATH_LOG_ERR, sErr)
			return 0
	
	
	def SearchSR(self, sIP):
		for sSRName, IPList in datamnt.SERVER_ROOM_DICT.items():
			if sIP in IPList:
				return sSRName
	
	
	# 过滤掉同机房之间的监控节点报警
	def IsSameSR(self, sThief, sPolice):
		if self.SearchSR(sThief) == self.SearchSR(sPolice):
			return 1
		return 0
	
	
	def UpdataValidList(self, lstValidData):
		if not lstValidData:
			return
		for lstData in lstValidData:
			self.m_lstValid.append(lstData)
	
	
	def SetFaultList(self):
		if not self.m_lstValid:
			return
		self.ResetFault()
		iSum = len(self.m_lstValid)
		oEndTime = self.m_lstValid[-1][1]
		if iSum<10:
			return 0
		#range前闭后开
		for i in range(0,iSum-9):
			oStartTime = self.m_lstValid[i][1]
			iDuration = (oEndTime - oStartTime).seconds
			#公式：报警的时间历程/报警的条数>6 秒/条    ,密度6s一条视为故障
			#print (iSum-i) * 6,iDuration
			#print self.m_lstValid[i][1],iSum-i,iDuration
			if (iSum-i) * alsconf.THR_Fault_FREQUENCY >= iDuration:
				self.m_iFault=i
				return 1
		return 0
	
	
	def GetLevel(self):
		if not self.m_iFault == None:
			return 1
		return 2
	
	
	def UpdataSummary(self, lstValidData):
		if not lstValidData:
			return
		iLevel=self.GetLevel()
		self.m_SummaryDict['level']		 = iLevel
		oDataEndTime = lstValidData[-1][1]
		self.m_SummaryDict['end'] 		 = oDataEndTime.strftime("%Y-%m-%d %H:%M:%S")
		
		#self.iFault表示大密度报警开始的序列号
		if iLevel == 1:
			self.m_SummaryDict['vector'] 	 = self.m_VectorList[self.m_iFault:]
			self.m_SummaryDict['sum'] 		 = len(self.m_VectorList[self.m_iFault:])
			if not self.m_SummaryDict['start']:  # 开始时间不能被覆盖
				oDataStartTime = lstValidData[self.m_iFault][1]
				self.m_SummaryDict['start'] = oDataStartTime.strftime("%Y-%m-%d %H:%M:%S")
		elif iLevel == 2:
			self.m_SummaryDict['vector'] 	 = self.m_VectorList[:]
			self.m_SummaryDict['sum'] 		 = len(self.m_VectorList)
			if not self.m_SummaryDict['start']:  # 开始时间不能被覆盖
				oDataStartTime = lstValidData[0][1]
				self.m_SummaryDict['start'] = oDataStartTime.strftime("%Y-%m-%d %H:%M:%S")


	# 当被报警方是私网ip的时候，报警方的出口应该也是私网ip。如果不是则进行转换
	def CorrectErr(self, sThief, sPolice):
		if not self.IsPri(sThief):
			return sThief, sPolice
		for MNTDict in datamnt.MONITOR_NODE_LIST:
			for k, v in MNTDict.items():
				if not v == sPolice:
					continue
				return sThief, MNTDict['sw']
	
	
	def UpdataVector(self, lstData):
		lstValid = []
		for i in lstData:
			iId, sTime, sLevel, sThief, sType, Status, sPolice = i  # 解包数据库数据，这种写法不好，数据库变了就需要重写有需要请联系强尧
			
			sThief = self.MatchIP(sThief)
			sPolice = self.MatchIP(sPolice)
			if self.IsIgnore(sThief, sPolice):  # 按照规则决定是否忽略掉这条记录
				continue
			lstValid.append(i)
			sThief, sPolice = self.CorrectErr(sThief, sPolice)
			self.m_VectorList.append((sThief, sPolice))
		return lstValid
	
	
	def Update(self, lstData):
		lstValid = self.UpdataVector(lstData)
		self.UpdataValidList(lstValid)
		self.SetFaultList()
		self.UpdataSummary(lstValid)
	
	
	def IsPri(self, sIP):
		IPSplitList = sIP.split('.')
		sIPHead = IPSplitList[0]
		if sIPHead == '10' or sIPHead == '172' or sIPHead == '192':
			return 1
			
			
	# 过滤掉部分数据
	def IsIgnore(self, sThief, sPolice):
		if not sThief or not sPolice:
			return 1
		if not alsconf.IS_ANALYSIS_PRI_NET:  # 不分析私网则检查到私网就返回1
			if self.IsPri(sThief):
				return 1
			elif self.IsPri(sPolice):
				return 1
		
		if not self.IsRegIP(sThief):
			sWarning = 'IP:%s没有被注册所属的运营商.' % (sThief)
			Alert(sWarning, alsconf.IM_GROUP_DEVELOPER)
			Log(PATH_LOG_WARNNING, sWarning)
			return 1
		elif not self.IsRegIP(sPolice):
			sWarning = 'IP:%s没有被注册所属的运营商.' % (sPolice)
			Alert(sWarning, alsconf.IM_GROUP_DEVELOPER)
			Log(PATH_LOG_WARNNING, sWarning)
			return 1
		
		elif self.IsSameSR(sThief, sPolice):  # 同一个机房的监控是没有意义的
			return 1
		return 0

if __name__ == '__main__':
	
	oStatiAlert = CStatiAlert()
	def Test_IsIgnore():
		pass
	
