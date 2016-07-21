# -*- coding:utf-8 -*-
import xml.etree.cElementTree as ET
import basetree
import time

'''
c=time.time()
d=CMinuteTree('e.xml')
dNet={'bytes':'adf','speed':'112','slope':'113','status':'114'}
d.SetAttr(dNet)
print d.SearchNode()
print time.time()-c

运维-小桂子(2693) 2016-2-25 09:09:21
对于主机来说，应可以学习到其历史正常阀值
历史正常阀值=除去异常状态时的最高值
运维-尤泽顺(8766) 2016-2-25 09:14:21
这个方法我试过了，有下面几个主要问题：
1.瞬时流量：历史流量的瞬时过高和过低，当前流量流量的瞬时过高和过低。这四个都是普遍存在的。
在图形化上的反应是，历史流量和当前流量的两条线并不拟合

2.性能占用。一分钟保存一次，保存一周，数据条数上万。这部分数据是需要保存在磁盘的，因此会同时影响到磁盘io和内存。
运行的瞬间占用达到6%cpu，磁盘io没仔细观察。虽然可以优化，但不建议使用
'''

class CTrafficTree(basetree.CBaseTree):
	def __init__(self,sXmlFile,dFormat={}):
		self.m_Attr=dFormat
		super(CTrafficTree,self).__init__(sXmlFile,dFormat)
		
	def InitNode(self):
		for iWeek in range(1,8):
			oNodeWeek=ET.SubElement(self.m_NodeRoot,'w'+str(iWeek))
			for iHour in range(1,25):
				oNodeHour=ET.SubElement(oNodeWeek,'h'+str(iHour))
				for iMinute in range(1,61):
					oNodeMinute=ET.SubElement(oNodeHour,'m'+str(iMinute))
					super(CTrafficTree, self).SetAttr(oNodeMinute,self.m_Attr)#使用指定的格式来初始化属性
					
	def GetTagWeek(self,sWeek):
		if isinstance(sWeek,int):
			sWeek=str(sWeek)
		sTagWeek='w'+sWeek
		return sTagWeek
		
	def GetTagHour(self,sHour):
		if isinstance(sHour,int):
			sHour=str(sHour)
		sTagHour='h'+sHour
		return sTagHour
		
	def GetTagMinute(self,sMinute):
		if isinstance(sMinute,int):
			sMinute=str(sMinute)
		sTagMinute='m'+sMinute
		return sTagMinute
	
	def GetNodeChild(self,sChildNodeName,oNodeFather=None):
		if not oNodeFather:
			oNodeFather=self.m_oNodeRoot
		NodeList = oNodeFather.getElementsByTagName(sChildNodeName)
		oNode=NodeList[0]
		return oNode
	
	def GetXPath(self,iWeek,iHour,iMinute):
		sTagWeek=self.GetTagWeek(iWeek)
		sTagHour=self.GetTagHour(iHour)
		sTagMinute=self.GetTagMinute(iMinute)
		sPath=sTagWeek+'/'+sTagHour+'/'+sTagMinute
		return sPath
	
	#指定时分秒，获得该Node
	def GetCustomNode(self,iWeek,iHour,iMinute):
		sPath=self.GetXPath(iWeek, iHour, iMinute)
		oNode=self.m_TreeObj.find(sPath)#find 返回第一个匹配的子元素， findall 以列表的形式返回所有匹配的子元素， iterfind 为所有匹配项提供迭代器
		return oNode
	
	#我使用时区的方式计算，即'第n'的方式计量
	def GetNowDate(self):
		iWeek=time.localtime().tm_wday+1
		iHour=time.localtime().tm_hour+1
		iMinute=time.localtime().tm_min+1
		return (iWeek,iHour,iMinute)

	def SetAttr(self,dNet):
		iWeek,iHour,iMinute=self.GetNowDate()
		oNodeMinute=self.GetCustomNode(iWeek,iHour,iMinute)#得到这分钟的Node
		super(CTrafficTree, self).SetAttr(oNodeMinute,dNet)
		#self.SaveTree() #为了提高效率，减少对磁盘的频繁读写，不自动进行保存。要保存时自行手动调用
		
	def SearchNode(self,DateList=()):
		if DateList:
			iWeek,iHour,iMinute=DateList
		else:
			iWeek,iHour,iMinute=self.GetNowDate()
		oNodeMinute=self.GetCustomNode(iWeek,iHour,iMinute)#得到这分钟的Node
		return oNodeMinute.attrib
		
