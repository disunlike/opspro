# -*- coding: utf-8 -*-
'''
用于im火星报警

测试指令：
	 python opspro/debugals.py --mod=alert --func=Alert --argv=8766,ff
'''
from define import *
import os

g_SpecialSymbol={
				#'%':'%25',这个符号必须单独进行替换
				'+'		:	'%2B',
				' '		:	'%20',
				'/'		:	'%2F',
				'?'		:	'%3F',
				'#'		:	'%23',
				'&'		:	'%26',
				'\n'	:	'%0a',
				'='		:	'%3D',
				}

#一些在url出现的字符必须被过滤掉，比如空格等
def ContentFilter(sContent):
	if not isinstance(sContent,str):
		return sContent #只有字符串才需要进行编码的检查
	sContent=sContent.replace('%','%25')#单独替换百分号，然后再遍历替换其他特殊符号。否则其他符号会被百分号替换掉
	for sSpecialSymbol,sUrlEncoding in g_SpecialSymbol.items():
		sContent=sContent.replace(sSpecialSymbol,sUrlEncoding)
	return sContent


def GetAlertUrl(sContent,sIMNumber):
	sIMNumber=str(sIMNumber)
	sContent=str(sContent)
	sUrl="http://im.2980.com:8088/sendmsg?key=public_server_waring&accounts=%s&content=%s"%(sIMNumber,sContent)
	return sUrl


#基于wget命令的报警，需在linux中使用。
#wget对一些特殊符号会出现报警不正常的情况
def AlertLinux(sContent,sIMNumber):
	sEncodingContent=ContentFilter(sContent)
	sUrl=GetAlertUrl(sEncodingContent,sIMNumber)
	#--quiet 安静模式，--spider 不下载  --tries表示报警次数  & 后台进行，当网络不可访问的时候不会引起阻塞
	#可能是wget命令的bug。当使用--tries部分报价会失败
	sShellCmd="wget --quiet -O /dev/null '%s' &"%(sUrl)
	os.popen(sShellCmd)
