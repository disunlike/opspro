# -*- coding:utf-8 -*-
import xml.etree.cElementTree as ET
import os 

'''
#使用示范：
import time
b=time.time()
a=CBaseTree('a.xml')
a.InsertNode()
print time.time()-b
'''
class CBaseTree(object):
	def __init__(self,sXmlFile,dFormat={}):
		self.m_XmlFile=sXmlFile#保存的文件路径
		self.m_TreeObj=None#树对象
		self.m_NodeRoot=None#树的根节点
		self.m_Attr=dFormat #节点属性和默认值的初始化
		self.Init()#初始化
		self.SaveTree()#保存文件
	
	def Init(self):
		if os.path.isfile(self.m_XmlFile):
			self.m_TreeObj = ET.parse(self.m_XmlFile)
			self.m_NodeRoot=self.m_TreeObj.getroot()#获得根节点
		else:
			self.m_NodeRoot=ET.Element('root')#创建一个节点
			self.m_TreeObj=ET.ElementTree(self.m_NodeRoot)#将这个节点作为根节点，获得一个节点树
			self.InitNode()
	
	#创建的时候初始化dom
	def InitNode(self):
		pass
					
	def SaveTree(self):#基类的名字千万不要太短，否则非常容易被子类不小心重写
		self.m_TreeObj.write(self.m_XmlFile)
	
	#在根节点下插入first标签然后保存
	#ET.SubElement(self.m_NodeRoot,'first')
	#self.SaveTree()
	def InsertNode(self,oNode=None,sTag=''):
		ET.SubElement(oNode,sTag)
		self.SaveTree()
	
	def DeleteNode(self):
		pass
	
	#查找一个节点的值
	#参数：节点的路径，属性的名称（默认以字典形式返回该节点的所有属性）
	def SearchNodeValue(self,sPath,sAttrib=''):
		oNode=self.GetCustomNode(sPath)
		if sAttrib:
			#返回字符串形式
			return oNode.attrib[sAttrib]
		#返回字典形式
		return oNode.attrib
	
	#自定义的获得节点对象的方法
	def GetCustomNode(self,sPath):
		#遍历根节点的所有子节点
		#find 返回第一个匹配的子元素， findall 以列表的形式返回所有匹配的子元素， iterfind 为所有匹配项提供迭代器
		oNode=self.m_TreeObj.find(sPath)
		return oNode
	
	#这里没有保存！自行调用SaveTree方法
	def SetAttr(self,oNode,dAttr={}):
		if not dAttr:
			dAttr=self.m_Attr
		for k,v in dAttr.iteritems():
			oNode.set(k,str(v))
			
	def Debug(self):
		import sys
		self.m_TreeObj.write(sys.stdout) 
