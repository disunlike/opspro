# -*- coding:utf-8 -*-
# ��������Ϣ���� 
# ����˳
# 2016��1��12��
'''
�������ݵı仯�Ƿ����dos�����µı仯����

�򵥵�˵�����������仯�������ж��Ƿ��쳣(�󱨲�������Ҫԭ����ͻ������)

�¾ɰ汾�Աȣ�
	#	�ɰ汾��			�Ľ���									˵����
	1	û��������ֵ		����������3.2M����dos����					��׷������ľ�׼��׷��ҵ���ϵ�״̬����3.2M�¼�ʹ���쳣����Ҳ��������Ӱ�죬�ʶ�������
	2	û��˲ʱ�������ж�	���������������ж�Ϊwarn->dos�������ж�Ϊdos->����״̬����Ҫ�����ȶ����ڵļ����������̽���
	4	û�о����״̬��ʾ	��������Ϣ���е�ǰ���� /�仯����Ϣ�������ж�״̬
	5	û�б����Ĵ�������	��ͬ�ľ�����һ������֮�ڲ����ظ�������ɧ�ź�ˢ��
	6	ʹ��shell		ʹ��python
	7	û�󲨶�����												2016-4-29 17:00 13s������������700MȻ���ٻ���
�㷨��
	�仯�ʳ�����ֵ����warn״̬����״̬������������¼��ǰ������0.8����Ϊ��̬��ֵ
	warn״̬������������ֵ(SpeedThreshold)����dos״̬,�����ڽ��������ж��г�����ֵ���ж�Ϊ�ǲ������Ա���
	dos�����ʵ��ڶ�̬��ֵ���߾�̬��ֵ�ж�Ϊnormal״̬
	

�㷨��
	normal				
						����ʧȥ����(ǰ�������ڶ����ڼ��ֵ)
	normal	-->	warn 	
						���򼤻���ڼ��ֵ�򼤻��������ڣ��ڼ��ٶȱ仯�ʸ��ڷ�ֵ
	warn	-->	dos		
						1�ٶȱ仯�ʶ�γ�����ֵ���ڼ���¼һ����̬��ֵ��
						2.warn�ڼ��¼������ٶ�ԶԶ���ڷ�ֵ����ȷ�ֵ��50M��
						
						�������˲ʱ��������������(13s�ڴﵽ800M����)����ôm_CountWarn��������Ȼֻ�Ἴ��һ�Σ�
	warn	-->	ok		
						1.����ʧȥ����(ǰ�������ڶ����ڼ��ֵ)
						2.�ٶȱ仯���ڼ���warn״̬�ڼ䲻���ڷ�ֵ(���������������״̬)
	dos		-->	ok		
						1.����ʧȥ����(�������ڼ��ֵ)
						2.�������ڶ�̬��ֵ
	dos		-->	����		
						dos״̬�£���������ά�ּ�������(���ڸ�����״̬)
	
	���򼤻
			1.���򼤻���ά���������ڣ��ڼ�����������ֵ��ˢ�¼������ڡ����������Զ�����normal״̬
			2.��������£�����������ô�ߵģ�3.2M��.û����״ֻ̬����normal,��˼��󽵵����󱨡�
	warn״̬��
			1.warn״̬��������ά���������ڡ��������ܽ���dos���߻ص�ok
			2.˵����ʱ���ٶȱ仯���Ǹߵġ�
			1
			1     --
			1    |
			1   |
			1  |
			1 |
			--------------------------
	dos״̬��
			1.warn״̬��������ɴθ��ٶȱ仯�ʻ����dos
			2.�ж�dos�󲻻����̱������������������������dos״̬�������Ӹ߲�����ᱨ��
	������״̬��
			ʵ�õĹ��ܣ��������ͱ������򵥴ֱ��������״̬�±�����һ���ܳɹ�����Ϣ�����޷���������
	��̬��ֵ��
			һЩ�������������ȷʵ�Ƚϸߣ�Ϊ���ܹ���Ӧ���������ʹ�ö�̬��ֵ���ڵ�һ�ν���warn���¼��ǰ������
			�����dos��������ô�����������������������������ȶ�̬��ֵ��
				���ж�Ϊdosʱ������Ҫ�������䵽�̶���ֵ�Ժ�ֻ��Ҫ�ȶ�С�ڶ�̬��ֵ����normal
				���û���ж�Ϊdos��warn��ص�normal״̬����̬��ֵ�����ͷ�
'''
from analysis import slope
from public.define import *
import gsconf


class CAnalyDos(slope.CAnaly):
	
	def __init__(self):
		super(CAnalyDos,self).__init__()
		self.m_iCountStable	=0					#�ȶ����������ж�״̬�Ƿ��ȶ���ÿ�����µ�״̬����������������
		self.m_iReleaseSpeed=None				#��¼��������ǰ���ٶȣ���Ϊ�쳣�����������жϷ�ֵ
		self.m_iCountWarn	=0
		self.m_iCountDos	=0					#��ʾ����dos��������
		self.m_iCountOpen	=0					#�������ڷ�ֵ�����������ֵ�������������ڽ��з���
		self.m_iCountSummary=0					#��ʶ��ε���Start������û�޸Ĺ�SummaryDict
		self.m_sStatus		='normal'
		#Dos�������Ϣͳ��
		self.m_InfoDosDict	={
							'starttime'	:0,			#��ʼʱ��
							'endtime'	:0,			#����ʱ��
							'maxtraff'	:0,			#��ֵ
							'duration'	:0,			#����ʱ��
						}
		
		self.m_SummaryDict	={
							'title'	:'',			#ʱ��ĸ���
							'detail':{},			#��ϸ��Ϣ
							'stati'	:{},			#ͳ����Ϣ
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
	
	
	#��̬��ֵ���жϷ�ʽ�Ǹ��ӵģ���ο��ĵ�
	def OnCommand(self):
		if not self.IsOpen():						#�����Ƿ񼤻�
			self.IntoNormal()						#��������˵��״̬����
			return
		if self.m_sStatus	==	'normal':
			self.StatusNormal()
		elif self.m_sStatus	==	'warn':
			self.StatusWarn()
		elif self.m_sStatus	==	'dos':
			self.StatusDos()
		else:
			raise RuntimeError("δ֪��״̬: %s"%(self.m_sStatus))
	
	
	def StatusNormal(self):
		if self.IsWarn():							#�ٶȱ仯�ʸ�
			self.IntoWarn()
		else:
			self.IntoNormal()						#������м�����
	
	
	'''
		warn	-->	dos
				�ٶȱ仯�ʶ�γ�����ֵ���ڼ���¼һ����̬��ֵ��
		warn	-->	ok
				1.����ʧȥ����(ǰ�������ڶ����ڼ��ֵ)
				2.�ٶȱ仯���ڼ���warn״̬�ڼ䲻���ڷ�ֵ(���������������״̬)
	'''
	def StatusWarn(self):
		if not self.m_iCountWarn>0:						#����warn״̬�����warn�ڼ���������û�н���dos״̬���ص�normal״̬
			self.IntoNormal()
			return
		self.m_iCountWarn-=1
		if self.IsDos():
			self.IntoDos()
	
	
	'''
		dos		-->	ok
			1.[����]����ʧȥ����(�������ڼ��ֵ)
			2.[����]�������ڶ�̬��ֵ
		dos		-->	����		
			dos״̬�£���������ά�ּ�������(���ڸ�����״̬)
	'''
	def StatusDos(self):
		if self.IsNormal():							#����̫���׻ص�normal״̬�������������������ô����ָ�������normal״̬��������
			self.IntoNormal()
		if self.IsDos():
			self.IntoDos()
		
		
	'''
		���򼤻
			1.���򼤻���ά����������(gsconf.COUNT_OPEN)���ڼ�����������ֵ��ˢ�¼������ڡ������������normal״̬
			2.��������£�����������ô�ߵģ�3.2M��.û����״ֻ̬����normal,��˼��󽵵����󱨡�
	'''
	def IsOpen(self):					
		if self.m_iCountOpen>0:
			self.m_iCountOpen-=1
			return 1
		if self.m_iSpeedNext>gsconf.THR_OPEN:		#ÿ����������THR_OPENʱ���¼�����������ɸ�����
			self.m_iCountOpen=gsconf.COUNT_OPEN
			self.m_iCountOpen-=1
			return 1
		return 0
	
	
	#�����ж�һ���µ�״̬���ȶ��Ļ���������˲ʱ�仯
	def IsStable(self,iCountStable):
		if self.m_iCountStable<iCountStable:
			self.AddCountStable()				#�ȶ�����������1����������ֵ��ʱ�ж�Ϊ�ȶ���
			return 0
		return 1
	
	
	'''
		warn	-->	ok		
			1.������������ʧȥ����(ǰ�������ڶ����ڼ��ֵ)
			2.���������ٶȱ仯���ڼ���warn״̬�ڼ䲻���ڷ�ֵ(���������������״̬)
		dos		-->	ok		
			1.������������ʧȥ����(�������ڼ��ֵ)
			2.�������������ȶ����ڶ�̬��ֵ��ֵ
	'''
	def IsNormal(self):
		#��������ǰ���ٶȣ���ֵ��������һ���жϻָ��������÷�ֵΪ�˷�ֹ����ʱ���������ͣ�
		if self.m_iSpeedNext<self.m_iReleaseSpeed or self.m_iSpeedNext<gsconf.THR_OPEN:
			if self.IsStable(gsconf.COUNT_STABLE_INTO_NORMAL):#�Ƿ���normal״̬�������ȶ�����������normal�ж�Ϊ�ȶ������ڼ�IntoDos����������
				return 1
			else:
				return 0
	
	
	def IsWarn(self):#������������
		if self.m_iSlope>gsconf.THR_SLOPE:
			return 1
		return 0
	
	
	'''
		warn	-->	dos		
			1�ٶȱ仯�ʶ�γ�����ֵ���ڼ���¼һ����̬��ֵ��
			2.warn�ڼ��¼������ٶ�ԶԶ���ڷ�ֵ����ȷ�ֵ��50M��
	'''
	def IsDos(self):
		if self.m_iSpeedNext>gsconf.THR_DOS_TRAFF:
			return 1
		if self.m_iSlope>gsconf.THR_SLOPE:		#Warn״̬�£���������������仯����˵����dos
			if self.IsStable(gsconf.COUNT_STABLE_INTO_DOS):
				return 1
			else:
				return 0
	
	
	def IntoNormal(self):
		self.SetStatus('normal')
		if self.m_iCountDos:#(���������û�����㣬˵��һ��������)
			self.DosEndTime()
			self.DosDuration()
			self.GetStatiInfo()
			self.Summary('�쳣��������')
		self.ResetCountWarn()
		self.ResetCountDos()
		self.ResetCountStable()
		self.ResetReleaseSpeed()
		self.ClearInfoDos()
		self.SetInterval(gsconf.PERIOD_NORMAL)
	
	
	def IntoWarn(self):
		if self.m_sStatus=='normal':
			self.m_iReleaseSpeed=round(self.m_iSpeedNext*0.8)	#��ʹ��roundС�����ܱ����ǳ���λ
		self.m_iCountWarn=gsconf.COUNT_WARN
		self.SetStatus('warn')
		self.ResetCountStable()
		self.SetInterval(gsconf.PERIOD_WARN)
	
	
	def IntoDos(self):
		if not self.m_sStatus=='dos':
			self.Summary('����Dos����')
		self.SetStatus('dos')
		self.DosStati()
		self.ResetCountStable()
	
	def SetStatus(self,sStatus):
		self.m_sStatus=sStatus
	
	
	#ͳ�����dos�ĳ���ʱ�䣬��������ȵ���Ϣ
	def DosStati(self):
		self.m_iCountDos+=1
		self.DosStartTime()
		self.DosMaxTraff()
	
	
	#��¼Dos�ĳ���ʱ��
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
		fMaxTraff=self.m_InfoDosDict['maxtraff']/1000.0 	#kb��ΪM
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
	
	
	def Summary(self,sTitle=''):	#״̬���ܽ�
		if self.m_iCountSummary>0:
			return
		self.m_iCountSummary+=1
		self.m_SummaryDict={
							'title'	:sTitle,				#�¼��ĸ���
							'detail':self.Detail(),			#�¼���ϸ�ڣ�ʹ�ÿɱ����
							'dos'	:self.m_InfoDosDict,
						}
	
	
	def Detail(self):						#״̬��Ϣͳ��
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
	
