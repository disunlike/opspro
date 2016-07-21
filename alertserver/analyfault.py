# -*- coding:utf-8 -*-
'''
Created on Feb 24, 2016
author: youzeshun  (IM: 8766)

用途：进行数据的统计分析，最终将所有分析结果打包在一个字典里面。

要点：
	1.假设故障点只会有一个
	2.机房故障分为上行故障和下行故障，线路故障直接视为上下行同时故障。

链路故障算法：
	1.过滤掉同一个机房不同监控节点之间的报警
	2.将ip替换为所属的机房
	
	3.将s_a->s_b和s_b->s_a的报警视为同一条进行统计
	4.【判断故障点】统计结果中占比找过74%的视为故障点（每四条允许一条误报）
	5.【缓冲报警】结论不会被立刻发出，而是在得到结论一段时间后才发出。期间内收到的信息依然会修正结论
	6.【影响机房】线路两端
		【影响网段】线路两端

机房故障算法：
	要点：一个机房的上下行路由，带宽负载都可能是不同的。如下载业务
	1.过滤掉同一个机房不同监控节点之间的报警
	2.将ip替换为所属的机房
	
	3.将报警分为报警方和被报警方进行统计
	4.【判断故障点】统计机房的报警次数和被报警次数，其中一种统计中有超过50%视为故障点
	5.【缓冲报警】结论不会被立刻发出，而是在得到结论一段时间后才发出。期间内收到的信息依然会修正结论
	6.【可信度计算】指向该结果的报警机房占所有机房（包括没有报警的机房的百分百，因为没报警默认正常）
	7.【影响机房】
				a.故障机房中报警/被报警次数最多的IP所属于的运营商
				b.和故障机房使用相同运营商的机房
	  【影响网段】
				a.故障机房中报警/被报警次数最多的IP所属于的运营商
				b.和故障点相同运营商的ip

模糊判断：

可信度：
	举例：
		对于被报警方：报警的机房占所有监控机房的百分比
		对于报警方：？
		对于线路：？
'''

import datamnt
import alsconf
import copy
from public.define import *

class CBaseFeature(object):

	def __init__(self):
		self.m_VectorList=[]				#报警的源数据,被所有的对象共同维护。
		self.m_SummaryDict={
						}
	
	def Start(self,VectorList):
		self.Clear()						#进行新的分析前一定要清空历史数据，避免累加错误
		if not VectorList:
			return
		if len(VectorList)<2:				#有两条记录则开始分析故障点
			return
		self.m_VectorList=VectorList[:]		#传递可变对象传递的是对象的引用，这里必须使用浅拷贝！
		
		self.Stati()
		self.Analy()
		return self.m_SummaryDict			#这个return用于测试！
	
	def Analy(self):
		self.AnalyFault()
	
	#如何分析给子类重写
	def AnalyFault(self):
		pass
	
	#只删除引用，内存块的清除交给引用计数器处理。避免误操作
	def Clear(self):
		self.__init__()
		
	#对数据进行基础的统计
	#1.相同信息的报警出现的次数
	def Stati(self):
		pass
	
	def MaxIndex(self,DataDict):
		if not DataDict:
			return
		iMaxV=0
		sIndex=''
		for k,v in DataDict.items():
			if v>iMaxV:
				iMaxV=v
				sIndex=k
		return sIndex
	
	#玩过术士吗？里面有一个多边形反应大宗师和神之间的关系
	def Polygon(self,DataDict):
		if not DataDict:
			Log(PATH_LOG_CRIT,'Polygon:DataDict不应该为空')
			return 0.0,''
		#找出字典中的最大值，然后计算该值占报警次数的百分百
		iSumV=0
		iMaxV=0
		MaxK=None
		for k,v in DataDict.items():
			if v>iMaxV:
				iMaxV=v
				MaxK=k
			iSumV+=v
		 #注意，FPerce是个字符串
		if not iSumV==0:
			FPerce=round(iMaxV/float(iSumV),2)
			return FPerce,MaxK
		sError='ZeroDivisionError: float division by zero. 不合理的字典%s'%(str(DataDict))
		Log(PATH_LOG_CRIT,sError)
	
		#用于统计一个字典中所有值的
	def DictValueSum(self,DataDict):
		if not isinstance(DataDict,dict):
			return
		iSum=0
		for k,v in DataDict.items():
			iSum+=v
		return iSum
	
	def IsFault(self,FPerce,FRatio):
		if FPerce>FRatio:
			return 1
		return 0
	
	#有一个脚本中变量设置错了--运维-强尧(8838) 2016-4-5　（类似情况估计还会有很多，做一个过滤，只处理已经的监控节点）
	def Debug(self,FPerce,sMaxK,SRStaDict,sDirection):
		sText='没超过阀值的信息:\nFPerce:%s\nsMaxK:%s\nSRStaDict:%s\nSumm字典应该是空的：%s\n算法：%s\n'%(str(FPerce),str(sMaxK),str(SRStaDict),str(self.m_SummaryDict),sDirection)
		Log(PATH_LOG_DEBUG,sText)

'''
原始统计方式：
		1.#[('机房','机房'),('机房','机房').......]
		2.#{'('机房','机房')':1,'('机房','机房')':2......}
缺点：
		信息量丢失
改进：
		1.[(ip,ip),(ip,ip)]
		2.{(ip,ip):xx}
'''
#链路故障，问题发生在链路上
class CLineFault(CBaseFeature):
	#做统计之前一定要先罗列出可能有的问题，否则就不知道数据的特征
	
	def __init__(self):
		super(CLineFault,self).__init__()
	
	def Clear(self):
		self.__init__()
	
	def StatiSRVector(self,lstVector):
		dStatiVector={}
		for lstIPVector in lstVector:
			if not dStatiVector.has_key(lstIPVector):
				dStatiVector[lstIPVector]=0
			dStatiVector[lstIPVector]+=1
		return dStatiVector
	
	#对a->b,b->a的报警统计进行合并
	def MergeLine(self,dStatiVector):
		TmpDict={}
		if not dStatiVector:
			return
		for kList,v in dStatiVector.items():
			if kList[::-1] in dStatiVector:
				if kList[::-1] in TmpDict:						#正方向计算过，反方向不再计算（从反方向看，正方向是::-1）
					continue
				TmpDict[kList]=v+dStatiVector[kList[::-1]]			#正方向的报警数量+反方向的报警数量
			else:
				TmpDict[kList]=v								#没有反方向的报警
		return TmpDict
	
	
	def StatiBySR(self,dStati):
		if not dStati:
			return
		dStatiSR={}
		for VectorList,v in dStati.items():
			sDSTIP=VectorList[0]
			sDSTSR=datamnt.SearchSR(sDSTIP)
			
			sSRCIP=VectorList[1]
			sSRCSR=datamnt.SearchSR(sSRCIP)
			if (sDSTSR,sSRCSR) in dStatiSR:
				dStatiSR[(sDSTSR,sSRCSR)]+=v
			else:
				dStatiSR[(sDSTSR,sSRCSR)]=v
		return dStatiSR
	
	
	def Stati(self):
		#self.SetSRVectorList()
		dStatiVector						=self.StatiSRVector(self.m_VectorList)	#
		self.m_SummaryDict['stati by ip']	=self.MergeLine(dStatiVector)			#ip1->ip2与ip2->ip1的报警次数合并在一起
		self.m_SummaryDict['stati by sr']	=self.StatiBySR(self.m_SummaryDict['stati by ip'])

	def CalFault(self):
		FPerce,MaxList=self.Polygon(self.m_SummaryDict['stati by ip'])
		return MaxList
		
	def AnalyFault(self):
		if not 'stati by sr' in self.m_SummaryDict:
			return
		if not self.m_SummaryDict['stati by sr']:
			return
		FPerce,MaxList=self.Polygon(self.m_SummaryDict['stati by sr'])
		if not self.IsFault(FPerce,alsconf.THR_LINE):
			self.Debug(FPerce,str(MaxList),self.m_SummaryDict['stati by sr'],self.m_SummaryDict)
			return
		self.m_SummaryDict['title']		=MaxList		#结论标题，相同的title在一段时间内只会出现一次
		self.m_SummaryDict['percent']	=FPerce			#指出是这个故障点的报警占重报警的比例，用于结论的可靠性参考
		self.m_SummaryDict['fault']		=self.CalFault()		#丢包最严重的ip矢量

		
#机房故障类
class CSRVRMFault(CBaseFeature):
	
	def __init__(self):
		super(CSRVRMFault,self).__init__()
		self.m_DSTDict		={}
		self.m_SRCDict		={}
		
		self.m_SRDSTDict	={}
		self.m_SRSRCDict	={}
		
		self.m_MergeStaDict	={}		#合并按照上下行的统计结果，这种算法的优先级是最低的
		
	def Clear(self):
		self.__init__()
	
	def SortStati(self):
		for sDST,sSRC in self.m_VectorList:
			if not self.m_SRCDict.has_key(sSRC):
				self.m_SRCDict[sSRC]=0
			if not self.m_DSTDict.has_key(sDST):
				self.m_DSTDict[sDST]=0
			self.m_SRCDict[sSRC]+=1
			self.m_DSTDict[sDST]+=1
	
	def SortByType(self,DataDict,TypeDict):
		if not DataDict or not TypeDict:
			return
		
		TmpDict={}
		#如果DataDict的键存在于OPERATORS的三个项目中
		for sType,IPList in TypeDict.items():
			Tmp2Dict={}
			for sIP in DataDict:
				if not sIP in IPList:
					continue
				if not TmpDict.has_key(sType):
					TmpDict[sType]=[]
				Tmp2Dict[sIP]=DataDict[sIP]
			if Tmp2Dict:
				TmpDict[sType]=Tmp2Dict
		return TmpDict
		
	#统计一个机房一共报了几次警告，同一个机房的不同ip报警信息都算在这个机房身上。 
	def StatiSRSum(self,DataDict):
		if DataDict:
			DataDict=DataDict.copy()
		for k,vDict in DataDict.items():
			DataDict[k]=self.DictValueSum(vDict)
		return DataDict
	

	#对于一些服务如下载，上下行的压力是不等的。下载服务更容易发出报警！因此上下行都需要进行分析
	#不同的监控结点相对于故障点的线路状况是不同的，因此报警的数量可能会有所集中，这将会影响分析
	def AnalyStatiData(self,SRStatiDict,SRDict,sDirection,FPerce,sMaxK):
		if not SRStatiDict or not SRDict:
			return
		dIP={}
		if self.IsFault(FPerce,alsconf.THR_SR):
			dIP=SRDict[sMaxK]
			sMaxIP=self.MaxIndex(dIP)						#问题机房中报警/被报警次数最多的IP
			self.m_SummaryDict['title']		=sMaxK				#结论标题，相同的title在一段时间内只会出现一次
			self.m_SummaryDict['percent']	=FPerce				#指出是这个故障点的报警占重报警的比例，用于结论的可靠性参考
			self.m_SummaryDict['fault']		=sMaxIP				##发生事故的ip
			self.m_SummaryDict['arith']		=sDirection
			return
		
		#得到被判断为故障机房的所有报警和被报警过的IP
		FMergePerce,sMergeMaxK=self.Polygon(self.m_MergeStaDict)	#合并上下行统计得到的占比和机房名称
		if sMergeMaxK in self.m_DSTSRDict and sMergeMaxK in self.m_SRCSRDict:
			dIP=self.Merge(self.m_DSTSRDict[sMergeMaxK],self.m_SRCSRDict[sMergeMaxK])
		elif sMergeMaxK in self.m_DSTSRDict:
			dIP=self.m_DSTSRDict[sMergeMaxK]
		elif sMergeMaxK in self.m_SRCSRDict:
			dIP=self.m_SRCSRDict[sMergeMaxK]
		sMaxIP=self.MaxIndex(dIP)							#问题机房中报警/被报警次数最多的IP
		if self.IsFault(FMergePerce,alsconf.THR_SR_MERGE) and dIP[sMaxIP]>alsconf.THR_SR_MERGE_OPEN:	#第二个条件是条数太少的情况下发生误报
			self.m_SummaryDict['title']		=sMaxK				#结论标题，相同的title在一段时间内只会出现一次
			self.m_SummaryDict['percent']	=FPerce				#指出是这个故障点的报警占重报警的比例，用于结论的可靠性参考
			self.m_SummaryDict['fault']		=sMaxIP				##发生事故的ip
			self.m_SummaryDict['arith']		='merge'
			return
		
		
	def Merge(self,dUpData,dDownData):
		lstKey=dUpData.keys()+dDownData.keys()
		dNewDict={}
		for sKey in lstKey:
			if sKey in dNewDict:	#键有重复的
				continue
			if sKey in dUpData and sKey in dDownData:
				dNewDict[sKey]=dUpData[sKey]+dDownData[sKey]
			elif sKey in dUpData:
				dNewDict[sKey]=dUpData[sKey]
			elif sKey in dDownData:
				dNewDict[sKey]=dDownData[sKey]
		return dNewDict
		
		
	def Stati(self):
		self.SortStati()
		
		self.m_SRCSRDict	=self.SortByType(self.m_SRCDict,datamnt.SERVER_ROOM_DICT)	#被报警的ip按照机房统计，格式{'机房名':{'ip1':被报警次数，'ip2':被报警次数}}
		self.m_SRCSRStaDict	=self.StatiSRSum(self.m_SRCSRDict)							##该机房中的所有报警算在该机房中，进行统计。格式 {'机房名'：总报警次数，'机房名'：总报警次数}
		
		self.m_DSTSRDict	=self.SortByType(self.m_DSTDict,datamnt.SERVER_ROOM_DICT)	#被报警的ip按照机房统计，格式{'机房名':{'ip1':被报警次数，'ip2':被报警次数}}
		self.m_DSTSRStaDict	=self.StatiSRSum(self.m_DSTSRDict)							##该机房中的所有报警算在该机房中，进行统计。格式 {'机房名'：总报警次数，'机房名'：总报警次数}
		
		self.m_MergeStaDict	=self.Merge(self.m_DSTSRStaDict,self.m_SRCSRStaDict)
		
		self.m_SummaryDict['stati']		={
								'down'	:self.m_SRCSRStaDict,
								'up'	:self.m_DSTSRStaDict,
								'merge'	:self.m_MergeStaDict,
								}
		
		
	#单独分析上行和下行，认为故障点只有一处
	def AnalyFault(self):
		FSRCPerce,sSRCMaxK=self.Polygon(self.m_SRCSRStaDict)
		FDSTPerce,sDSTMaxK=self.Polygon(self.m_DSTSRStaDict)
		
		if FSRCPerce>FDSTPerce:
			self.AnalyStatiData(self.m_SRCSRStaDict,self.m_SRCSRDict,'down',FSRCPerce,sSRCMaxK)			#down表示下行
		else:
			self.AnalyStatiData(self.m_DSTSRStaDict,self.m_DSTSRDict,'up',FDSTPerce,sDSTMaxK)
		
		
class CAnalyManager():
	def __init__(self):
		self.m_oLineFault	=CLineFault()
		self.m_oSRVRMFault	=CSRVRMFault()
		self.m_SummaryDict	={
						'line'	:{},
						'sr'	:{},
						}
	
	def Clear(self):
		self.m_SummaryDict	={
						'line'	:{},
						'sr'	:{},
						}
	
	def AnalyLineFault(self,VectorList):
		LineSummaryDict=self.m_oLineFault.Start(VectorList)
		if LineSummaryDict:
			sDebug='命中线路算法：LineSummaryDict %s'%(str(LineSummaryDict))
			Log(PATH_LOG_DEBUG,sDebug)
			return LineSummaryDict
	
	def AnalySRFault(self,VectorList):
		SRSummaryDict=self.m_oSRVRMFault.Start(VectorList)
		if SRSummaryDict:
			sDebug='命中机房单线算法：SRSummaryDict %s'%(SRSummaryDict)
			Log(PATH_LOG_DEBUG,sDebug)
			return SRSummaryDict
	
	#对统计的矢量进行分析，把结论合并到原来的字典中
	def Start(self,Dict):
		self.Clear()
		VectorList=Dict['vector']
		if not VectorList:
			return {}
		if len(VectorList)<alsconf.THR_MIN_ANALY:
			return {}
		#假设故障点只有一个，如果是线路故障则认为机房没有故障
		self.m_SummaryDict={
						'line'	:self.AnalyLineFault(VectorList),
						'sr'	:self.AnalySRFault(VectorList),
					}
		return self.m_SummaryDict	#这个returan仅仅用于测试的时候获得输出
		
if __name__=='__main__':
	g_oLineFault=CLineFault()
	def Test_MergeLine():
		DataDict={('cz', 'sy'): 2, ('sy', 'cz'): 1}
		print g_oLineFault.MergeLine(DataDict)		#{('cz', 'sy'): 3}

	Test_MergeLine()
	
