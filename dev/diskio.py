# -*- coding:utf-8 -*-
#获得磁盘的数据
import basedev

class CDev(basedev.CBaseDev):
	
	def __init__(self):
		self.m_Name='disk io'
		self.m_ShellCmd='vmstat|awk \'NR==3 {print "{\\"bi\\":" $9 ",\\"bo\\":" $10"}"}\''
		
