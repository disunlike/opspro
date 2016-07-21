# -*- coding:utf-8 -*-
'''
创建时间: Apr 13, 2016
作者:youzeshun  (IM: 8766)
用途:解决nagios报警自动分析由于分析的报警样本少而导致的报警结果不同。
	demo:
		a->b	结论：无	
		b->a	结论：线路a-b异常		#由于接受的信息太少，所以不准确
		c->a	结论：故障点a			#新修改得到的报警其实也不一定是正确的，但能减少误报的数量
		
描述:报警将被延迟到一段时间后才会发出，期间能够修改报警的内容

注意:不能替代其他报警方式
'''

from public.alert import CAlertManager
from public.define import *
from alertserver import alsconf

class CDelayAlert(CAlertManager):
	
	def __init__(self,iCountdown=alsconf.TIME_ALERT_DELAY):
		super(CDelayAlert,self).__init__()
		self.m_IsCountdown=False			#是否开始倒计时以发送消息
		self.m_iCountdown=iCountdown
		self.m_IMNumberList=[]
		self.m_AlertMsg=''
		self.m_iReAlertNum=0
		self.m_LogPath=''
	
	def Reset(self):
		self.m_IMNumberList=[]
		self.m_AlertMsg=''
		self.m_iReAlertNum=0
		self.m_LogPath=''
	
	def OpenCountdown(self):
		self.m_IsCountdown=True
	
	def CloseCountdown(self):
		self.m_IsCountdown=False			#是否开始倒计时以发送消息
	
	#倒计时执行某个函数
	def Countdown(self):
		self.OpenCountdown()
		Call_Out(Functor(self.DelayAlert),self.m_iCountdown,'delay alert') #为了不重名，使用文件名作为注册名
		
	def DelayAlert(self):
		Alert(self.m_AlertMsg,self.m_IMNumberList,self.m_iReAlertNum,self.m_LogPath)
		#报警后充值参数
		self.CloseCountdown()
		self.Reset()
		
	def Alert(self,AlertMsg,IMNumberList,iReAlertNum=0,sLogName=PATH_LOG_ALERT_HISTORY):
		self.m_IMNumberList=IMNumberList
		self.m_AlertMsg=AlertMsg
		self.m_iReAlertNum=iReAlertNum
		self.m_LogPath=sLogName
		
		if self.m_IsCountdown:
			return
		else:
			self.Countdown()
			
if __name__=='__main__':
	#初始化这个代码文件需要的环境
	def Init():
		from public import timerctrl
		oTimerMgr=timerctrl.CTimerManager()
		SetGlobalManager("timer",oTimerMgr)
		
		from public import alert
		SetGlobalManager("alert",alert.CAlertManager())
		
		from public import txtlog
		SetGlobalManager("txtlog",txtlog.CLog('/tmp/tmp'))
	
	def Demo():
		oDelayAlert=CDelayAlert(2)			#报警被延迟2秒后报警
		oDelayAlert.Alert(8766,'test')	#不会被报出
		oDelayAlert.Alert(8766,'test2')	#报警内容替换掉前者
		
	Init()
	Demo()
	
