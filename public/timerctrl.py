# -*- coding: utf-8 -*-
import time
import threading

'''
��ʱ���������첽���á����̱߳���б���ע���ʱ���������̵߳���Դ��������
'''

class CTimerManager(threading.Thread):

	def __init__(self):
		super(CTimerManager,self).__init__()
		#sFlag:(iEndTime,iDelay,cbfunc,bPeriod)
		self.m_TimerDict={} #���������ֵ������ѯ
		self.m_bStop=False
		self.start()
		
		
	#ÿ�붼�������ֵ�
	def run(self):
		while True:
			if self.m_bStop:
				break 
			time.sleep(1)
			self.CheckTimeOut()


	#�رն�ʱ��
	def StopTimer(self):
		self.m_bStop=True


	#ע�ᶨʱ�ص�����
	def Register(self,cbfunc,iDelay,sFlag,bPeriod=False):
		curtime=time.time()
		iEndTime=curtime+iDelay
		self.m_TimerDict[sFlag]=(iEndTime,iDelay,cbfunc,bPeriod)


	#ȡ��ע�ᶨʱ�ص�����
	def UnRegister(self,sFlag):
		if sFlag in self.m_TimerDict:
			del self.m_TimerDict[sFlag]


	#��ʱ����Ƿ�ʱ
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
			if bPeriod: #������ڿ��Ը�Ϊ���֣��Կ���ִ�еĴ���,����ֵ״̬���Ǳ�ʾ�Ƿ�ѭ��
				iEndTime=curtime+iDelay
				self.m_TimerDict[sFlag]=(iEndTime,iDelay,cbfunc,bPeriod)
			cbfunc()
			