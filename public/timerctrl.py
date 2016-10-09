# -*- coding: utf-8 -*-
import time
import threading

'''
计时器，负责异步调用。多线程编程中必须注意计时器与其他线程的资源竟用问题
'''

class CTimerManager(threading.Thread):

	def __init__(self):
		super(CTimerManager,self).__init__()
		#sFlag:(iEndTime,iDelay,cbfunc,bPeriod)
		self.m_TimerDict={} #该类对这个字典进行轮询
		self.m_bStop=False
		self.start()
		
		
	#每秒都检查这个字典
	def run(self):
		while True:
			if self.m_bStop:
				break 
			time.sleep(1)
			self.CheckTimeOut()


	#关闭定时器
	def StopTimer(self):
		self.m_bStop=True


	#注册定时回调函数
	def Register(self,cbfunc,iDelay,sFlag,bPeriod=False):
		curtime=time.time()
		iEndTime=curtime+iDelay
		self.m_TimerDict[sFlag]=(iEndTime,iDelay,cbfunc,bPeriod)


	#取消注册定时回调函数
	def UnRegister(self,sFlag):
		if sFlag in self.m_TimerDict:
			del self.m_TimerDict[sFlag]


	#定时检查是否超时
	def CheckTimeOut(self):
		tmpList=[]
		curtime=time.time()
		for sFlag in self.m_TimerDict:
			iEndTime,iDelay,cbfunc,bPeriod=self.m_TimerDict[sFlag]
			if iEndTime>curtime:
				continue
			tmpList.append(sFlag)

		for sFlag in tmpList:
			iEndTime,iDelay,cbfunc,bPeriod=self.m_TimerDict[sFlag]
			del self.m_TimerDict[sFlag]
			if bPeriod: #这个周期可以改为数字，以控制执行的次数,布尔值状态下是表示是否循环
				iEndTime=curtime+iDelay
				self.m_TimerDict[sFlag]=(iEndTime,iDelay,cbfunc,bPeriod)
			cbfunc()
			