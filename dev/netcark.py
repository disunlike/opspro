# -*- coding:utf-8 -*-
'''
��������˵����
/proc/net/dev
	debian6
		eth0:��ֵ(û�пո�)
	debian7
		eth0: ��ֵ(�пո�)
	����ʽ������:��תΪ�ո�
'''
import basedev

class CDev(basedev.CBaseDev):
	
	def __init__(self):
		self.m_Name='net cark'
		self.m_ShellCmd='cat /proc/net/dev|grep :|tr ":" " "|awk \'{print $1" "$2" "$3" "$10" "$11}\''
	
	
	def InitDict(self):
		return {
				'recv':{'bytes':0,'packets':0},
				'send':{'bytes':0,'packets':0}
				}
		
		
	def FormatResult(self,sResult):
		dNetworkCark={}
		if not sResult:
			return dNetworkCark
		sResult=sResult.rstrip()
		lstTraff=sResult.split()	#['lo:', '0', '0', '0', '0', 'eth0:', '1190600', '2600', '300918', '2193']
		for sNetCark in lstTraff[::5]:
			iIndex=lstTraff.index(sNetCark)
			dNetworkCark[sNetCark]=self.InitDict()
			dNetworkCark[sNetCark]['recv']['bytes']=int(lstTraff[iIndex+1])
			dNetworkCark[sNetCark]['recv']['packets']=int(lstTraff[iIndex+2])
			dNetworkCark[sNetCark]['send']['bytes']=int(lstTraff[iIndex+3])
			dNetworkCark[sNetCark]['send']['packets']=int(lstTraff[iIndex+4])
		return dNetworkCark
	
	
	#Ĭ������µõ�eth0�����յ�������bytes
	def Traff(self,sNetCark='eth0',sDirection='recv',sType='bytes'):
		dTraff=self.Start()
		if not sNetCark in dTraff:
			sErr='����������%s'%(sNetCark)
			raise Exception(sErr)
		
		if not sDirection in dTraff[sNetCark]:
			sErr='ֻ���պͷ���������,recv,send'
			raise Exception(sErr)
		
		if not sType in dTraff[sNetCark][sDirection]:
			sErr='������λֻ����byte��packets'
			raise Exception(sErr)
		return dTraff[sNetCark][sDirection][sType]
		
