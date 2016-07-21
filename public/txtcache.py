# -*- coding:utf-8 -*-
'''
创建时间: Mar 25, 2016
作者: youzeshun  (IM: 8766)
用途:用于将数据缓存在本地
'''
import os
import path

class CCache(object):
	
	#结构化存储数据
	def Save(self,Data,sFilePath=''):
		if not sFilePath:
			raise Exception('路径变量为空')
		self.InitPath(sFilePath)
		if not self.IsWrite(sFilePath):
			sText='文件无法写入%s，权限不够或文件不存在'%(sFilePath)
			print sText
			raise Exception(sText)
		sData=self.AllToStr(Data)
		self.Write(sData,sFilePath)
	
	def IsWrite(self,sFilePath):
		if os.access(sFilePath,os.W_OK):
			return 1
		return 0	
		
	def Write(self,Data,sPath):
		if not isinstance(Data,str):
			raise Exception('写入文本的对象必须是字符串,AllToStr函数没有做正确的转换')
		fLocal=open(sPath,'a+')
		print '正在保存数据',Data
		print type(Data)
		fLocal.write(Data+'\n')
		fLocal.close()
		
	def AllToStr(self,Data):
		sData=str(Data)
		return sData
	
	def InitPath(self,sPath):
		if os.path.exists(sPath):
			return
		path.Create(sPath)
		
	def Read(self,sFilePath,BoolClean=True):
		if not sFilePath:
			raise Exception('路径变量为空')
		if not os.path.isfile(sFilePath):		#文件不存在
			print '文件%s不存在'%(sFilePath)
			return
		if not os.stat(sFilePath).st_size:		#文件没内容
			print '文件%s没有数据'%(sFilePath)
			return
		CacheList=[]
		for sLine in open(sFilePath):			#注意：这里对内存的占用不可预期
			CacheList.append(sLine[:-1])
		if BoolClean:
			self.Clean(sFilePath)
		return CacheList
	
	def CheckCache(self):
		pass
	
	def Clean(self,sFilePath):
		open(sFilePath,"w").truncate()

#Data=({'a':'a'},1)
#oCache=CCache('/home/yzs/Test/as.txt')
#oCache.Save(Data)
#print oCache.Read()

