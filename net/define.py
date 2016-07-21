# -*- coding:utf-8 -*-
'''
Created on Mar 3, 2016
author: youzeshun  (IM: 8766)
用途：网络编程常用的函数
'''

def ConvertIntToByte(num,iLen=4):
	result=""
	for i in xrange(iLen):
		iByte=(num>>(8*i)) & 0xff
		result+=chr(iByte)
	return result

def ConverByteToInt(byteStr):
	num=0
	i=0
	for char in byteStr:
		iByte=ord(char)
		num+=iByte<<i*8
		i+=1
	return num

#n=ConvertIntToByte(1212)
#print ConverByteToInt(n)

#用于网络传输的序列化，可行性有待验证
def ConverDictToStr(dData):
	sData=str(dData)
	return sData

#数据中心绝对不能出错
def ConverStrToDict(sData):
	if not sData:
		print '空数据'
		return None
	#if not ist(sData,dict):
	#	sText='传值错误：参数必须是一个字符串格式的字典.错误的值：{0}'.format(sData)
	#	raise Exception(sText)
	try:
		dData=eval(sData)
	except:
		print '警告：转换出错'	#
		return None
	else:
		return dData

