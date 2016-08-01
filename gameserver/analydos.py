# -*- coding:utf-8 -*-
# 服务器信息基类 
# 尤泽顺
# 2016年1月12日
'''
分析数据的变化是否符合dos攻击下的变化规律

简单的说：根据流量变化趋势来判断是否异常(误报产生的主要原因是突发流量)

新旧版本对比：
	#	旧版本：			改进：									说明：
	1	没有启动阀值		当流量大于3.2M激活dos分析					不追求分析的精准，追求业务上的状态。在3.2M下即使有异常流量也不会明显影响，故而不分析
	2	没有瞬时流量的判断	启动计数器，当判断为warn->dos，或者判断为dos->正常状态都需要进行稳定周期的计数，不立刻进入
	4	没有具体的状态显示	报警的信息带有当前流量 /变化率信息，辅助判断状态
	5	没有报警的次数限制	相同的警告在一定周期之内不会重复，降低骚扰和刷屏
	6	使用shell		使用python
	7	没大波动报警												2016-4-29 17:00 13s内流量激增到700M然后急速回落
算法：
	变化率超过阀值进入warn状态（该状态不报警），记录当前流量的0.8倍作为动态阀值
	warn状态下流量超过阀值(SpeedThreshold)进入dos状态,持续在接下来的判断中超过阀值则判断为非波动可以报警
	dos下速率低于动态阀值或者静态阀值判断为normal状态
	

算法：
	normal				
						程序失去激活(前几个周期都低于激活阀值)
	normal	-->	warn 	
						程序激活（高于激活阀值则激活若干周期）期间速度变化率高于阀值
	warn	-->	dos		
						1速度变化率多次超过阀值（期间会记录一个动态阀值）
						2.warn期间记录的最大速度远远大于阀值（如比阀值大50M）
						
						，如果是瞬时超高流量攻击，(13s内达到800M流量)。那么m_CountWarn计数器依然只会技术一次！
	warn	-->	ok		
						1.程序失去激活(前几个周期都低于激活阀值)
						2.速度变化率在激活warn状态期间不高于阀值(允许缓慢进入高流量状态)
	dos		-->	ok		
						1.程序失去激活(连续低于激活阀值)
						2.流量低于动态阀值
	dos		-->	报警		
						dos状态下，流量连续维持几个周期(处于高流量状态)
	
	程序激活：
			1.程序激活后会维持若干周期，期间流量超过阀值会刷新激活周期。周期用完自动进入normal状态
			2.正常情况下，流量少有那么高的（3.2M）.没激活状态只会是normal,因此极大降低了误报。
	warn状态：
			1.warn状态被激活后会维持若干周期。周期内能进入dos或者回到ok
			2.说明此时的速度变化率是高的。
			1
			1     --
			1    |
			1   |
			1  |
			1 |
			--------------------------
	dos状态：
			1.warn状态激活后若干次高速度变化率会进入dos
			2.判定dos后不会立刻报警。而是启动计数器，如果dos状态下流量居高不下则会报警
	高流量状态：
			实用的功能，高流量就报警，简单粗暴。（这个状态下报警不一定能成功，消息可能无法发出。）
	动态阀值：
			一些服务的流量可能确实比较高，为了能够适应这种情况，使用动态阀值，在第一次进入warn后记录当前流量。
			如果是dos攻击，那么流量还会继续上升，后续的流量会比动态阀值大。
				当判断为dos时，不需要流量回落到固定阀值以后，只需要稳定小于动态阀值就算normal
				如果没有判断为dos，warn会回到normal状态，动态阀值将被释放
'''
from analysis import slope
from public.define import *
import gsconf


class CAnalyDos(slope.CAnaly):
	
	def __init__(self):
		super(CAnalyDos,self).__init__()
		self.m_iCountStable	=0					#稳定计数器，判断状态是否稳定。每进入新的状态都将清空这个计数器
		self.m_iReleaseSpeed=None				#记录流量上升前的速度，作为异常流量结束的判断阀值
		self.m_iCountWarn	=0
		self.m_iCountDos	=0					#表示发生dos的周期数
		self.m_iCountOpen	=0					#流量大于阀值则给计数器赋值，在若干周期内进行分析
		self.m_iCountSummary=0					#标识这次调用Start方法有没修改过SummaryDict
		self.m_sStatus		='normal'
		#Dos的相关信息统计
		self.m_InfoDosDict	={
							'starttime'	:0,			#起始时间
							'endtime'	:0,			#结束时间
							'maxtraff'	:0,			#峰值
							'duration'	:0,			#持续时间
						}
		
		self.m_SummaryDict	={
							'title'	:'',			#时间的概述
							'detail':{},			#详细信息
							'stati'	:{},			#统计信息
						}


	def Start(self,iData):
		if not self.IsInit(iData):
			return
		self.ClearSummary()
		self.ResetCountSummary()
		iData=self.ConvertUnit(iData)
		self.UpdateData(iData)
		self.GetSpeed()
		self.GetSlope()

		if self.m_iUnstable>0:
			self.m_iUnstable-=1
			return
		
		self.OnCommand()
		self.Summary()
		
		
	def ConvertUnit(self,iData):
		iData=iData/1000
		return iData 
	
	
	#静态阀值的判断方式是复杂的，请参考文档
	def OnCommand(self):
		if not self.IsOpen():						#程序是否激活
			self.IntoNormal()						#不激活则说明状态正常
			return
		if self.m_sStatus	==	'normal':
			self.StatusNormal()
		elif self.m_sStatus	==	'warn':
			self.StatusWarn()
		elif self.m_sStatus	==	'dos':
			self.StatusDos()
		else:
			raise RuntimeError("未知的状态: %s"%(self.m_sStatus))
	
	
	def StatusNormal(self):
		if self.IsWarn():							#速度变化率高
			self.IntoWarn()
		else:
			self.IntoNormal()						#清空所有计数器
	
	
	'''
		warn	-->	dos
				速度变化率多次超过阀值（期间会记录一个动态阀值）
		warn	-->	ok
				1.程序失去激活(前几个周期都低于激活阀值)
				2.速度变化率在激活warn状态期间不高于阀值(允许缓慢进入高流量状态)
	'''
	def StatusWarn(self):
		if not self.m_iCountWarn>0:						#激活warn状态后如果warn在激活周期内没有进入dos状态则会回到normal状态
			self.IntoNormal()
			return
		self.m_iCountWarn-=1
		if self.IsDos():
			self.IntoDos()
	
	
	'''
		dos		-->	ok
			1.[被动]程序失去激活(连续低于激活阀值)
			2.[主动]流量低于动态阀值
		dos		-->	报警		
			dos状态下，流量连续维持几个周期(处于高流量状态)
	'''
	def StatusDos(self):
		if self.IsNormal():							#不能太容易回到normal状态，如果是流量波动，那么会出现高流量的normal状态。不合理
			self.IntoNormal()
		if self.IsDos():
			self.IntoDos()
		
		
	'''
		程序激活：
			1.程序激活后会维持若干周期(gsconf.COUNT_OPEN)，期间流量超过阀值会刷新激活周期。周期用完进入normal状态
			2.正常情况下，流量少有那么高的（3.2M）.没激活状态只会是normal,因此极大降低了误报。
	'''
	def IsOpen(self):					
		if self.m_iCountOpen>0:
			self.m_iCountOpen-=1
			return 1
		if self.m_iSpeedNext>gsconf.THR_OPEN:		#每当流量大于THR_OPEN时重新激活检查程序若干个周期
			self.m_iCountOpen=gsconf.COUNT_OPEN
			self.m_iCountOpen-=1
			return 1
		return 0
	
	
	#用于判断一个新的状态是稳定的还是流量的瞬时变化
	def IsStable(self,iCountStable):
		if self.m_iCountStable<iCountStable:
			self.AddCountStable()				#稳定计数器增加1，当超过阀值的时判断为稳定的
			return 0
		return 1
	
	
	'''
		warn	-->	ok		
			1.【被动】程序失去激活(前几个周期都低于激活阀值)
			2.【被动】速度变化率在激活warn状态期间不高于阀值(允许缓慢进入高流量状态)
		dos		-->	ok		
			1.【被动】程序失去激活(连续低于激活阀值)
			2.【主动】流量稳定低于动态阀值或阀值
	'''
	def IsNormal(self):
		#流量攀升前的速度，或阀值，低于其一则判断恢复正常（该阀值为了防止攀升时的流量过低）
		if self.m_iSpeedNext<self.m_iReleaseSpeed or self.m_iSpeedNext<gsconf.THR_OPEN:
			if self.IsStable(gsconf.COUNT_STABLE_INTO_NORMAL):#是否是normal状态，并且稳定（连续两次normal判断为稳定），期间IntoDos计数器重置
				return 1
			else:
				return 0
	
	
	def IsWarn(self):#流量上升过快
		if self.m_iSlope>gsconf.THR_SLOPE:
			return 1
		return 0
	
	
	'''
		warn	-->	dos		
			1速度变化率多次超过阀值（期间会记录一个动态阀值）
			2.warn期间记录的最大速度远远大于阀值（如比阀值大50M）
	'''
	def IsDos(self):
		if self.m_iSpeedNext>gsconf.THR_DOS_TRAFF:
			return 1
		if self.m_iSlope>gsconf.THR_SLOPE:		#Warn状态下，如果持续高流量变化率则说明是dos
			if self.IsStable(gsconf.COUNT_STABLE_INTO_DOS):
				return 1
			else:
				return 0
	
	
	def IntoNormal(self):
		self.SetStatus('normal')
		if self.m_iCountDos:#(这个计数器没有清零，说明一定报警过)
			self.DosEndTime()
			self.DosDuration()
			self.GetStatiInfo()
			self.Summary('异常流量结束')
		self.ResetCountWarn()
		self.ResetCountDos()
		self.ResetCountStable()
		self.ResetReleaseSpeed()
		self.ClearInfoDos()
		self.SetInterval(gsconf.PERIOD_NORMAL)
	
	
	def IntoWarn(self):
		if self.m_sStatus=='normal':
			self.m_iReleaseSpeed=round(self.m_iSpeedNext*0.8)	#不使用round小数可能保留非常多位
		self.m_iCountWarn=gsconf.COUNT_WARN
		self.SetStatus('warn')
		self.ResetCountStable()
		self.SetInterval(gsconf.PERIOD_WARN)
	
	
	def IntoDos(self):
		if not self.m_sStatus=='dos':
			self.Summary('疑似Dos攻击')
		self.SetStatus('dos')
		self.DosStati()
		self.ResetCountStable()
	
	def SetStatus(self,sStatus):
		self.m_sStatus=sStatus
	
	
	#统计这次dos的持续时间，最大流量等等信息
	def DosStati(self):
		self.m_iCountDos+=1
		self.DosStartTime()
		self.DosMaxTraff()
	
	
	#记录Dos的持续时间
	def DosStartTime(self):
		if self.m_sStatus=='dos' and not self.m_InfoDosDict['starttime']:
			iTime=int(GetTime('%s'))
			self.m_InfoDosDict['starttime']=iTime
	
	
	def DosEndTime(self):
		if self.m_sStatus=='normal' and self.m_InfoDosDict and not self.m_InfoDosDict['endtime']:
			iTime=int(GetTime('%s'))
			self.m_InfoDosDict['endtime']=iTime
	
	
	def DosMaxTraff(self):
		if self.m_iSpeedNext>self.m_InfoDosDict['maxtraff']:
			self.m_InfoDosDict['maxtraff']=self.m_iSpeedNext
	
	
	def DosDuration(self):
		iDuration=self.m_InfoDosDict['endtime']-self.m_InfoDosDict['starttime']
		self.m_InfoDosDict['duration']=iDuration
	
	
	def GetStatiInfo(self):
		sStartTime=FormatTime(self.m_InfoDosDict['starttime'],"%Y-%m-%d %H:%M:%S")
		sEndTime=FormatTime(self.m_InfoDosDict['endtime'],"%Y-%m-%d %H:%M:%S")
		fMaxTraff=self.m_InfoDosDict['maxtraff']/1000.0 	#kb换为M
		fDuration=self.m_InfoDosDict['duration']/60.0
		self.m_InfoDosDict={
						'starttime'	:sStartTime,
						'endtime'	:sEndTime,
						'maxtraff'	:fMaxTraff,
						'duration'	:fDuration,
						}
	
	
	def ResetReleaseSpeed(self):
		self.m_iReleaseSpeed=None
	
	
	def ResetCountStable(self):
		self.m_iCountStable	=0
		
		
	def ResetCountDos(self):
		self.m_iCountDos	=0
	
	
	def ResetCountWarn(self):
		self.m_iCountWarn	=0
	
	
	def ResetCountSummary(self):
		self.m_iCountSummary=0
	
	
	def ClearInfoDos(self):
		self.m_InfoDosDict	={
						'starttime':0,
						'endtime':0,
						'maxtraff':0,
						'duration':0,
						}
		
		
	def ClearSummary(self):
		self.m_SummaryDict	={
						'title'	:'',
						'detail':{},
						'stati'	:{},
						}
	
	
	def AddCountStable(self):
		self.m_iCountStable+=1
	
	
	def Summary(self,sTitle=''):	#状态的总结
		if self.m_iCountSummary>0:
			return
		self.m_iCountSummary+=1
		self.m_SummaryDict={
							'title'	:sTitle,				#事件的概述
							'detail':self.Detail(),			#事件的细节，使用可变对象！
							'dos'	:self.m_InfoDosDict,
						}
	
	
	def Detail(self):						#状态信息统计
		dDetail={
				'speed'			:self.m_iSpeedNext,
				'slope'			:self.m_iSlope,
				'status'		:self.m_sStatus,
				'releasespeed'	:self.m_iReleaseSpeed,
				'interval'		:self.m_iInterval,
				'countstable'	:self.m_iCountStable,
				'traff'			:self.m_iDataNext,
			}
		return dDetail
	
