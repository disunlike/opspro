# -*- coding:utf-8 -*-
'''
兼容问题说明：
/proc/net/dev
	debian6
		eth0:数值(没有空格)
	debian7
		eth0: 数值(有空格)
	处理方式：将‘:’转为空格。
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
	
	
	#默认情况下得到eth0网卡收到的数据bytes
	def Traff(self,sNetCark='eth0',sDirection='recv',sType='bytes'):
		dTraff=self.Start()
		if not sNetCark in dTraff:
			sErr='不存在网卡%s'%(sNetCark)
			raise Exception(sErr)
		
		if not sDirection in dTraff[sNetCark]:
			sErr='只有收和发两个方向,recv,send'
			raise Exception(sErr)
		
		if not sType in dTraff[sNetCark][sDirection]:
			sErr='计量单位只能是byte或packets'
			raise Exception(sErr)
		return dTraff[sNetCark][sDirection][sType]
		
