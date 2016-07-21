# -*- coding:utf-8 -*-
#用途：获得cpu的数据
import basedev

class CDev(basedev.CBaseDev):
	
	def __init__(self):
		self.m_Name='cpu'
		self.m_ShellCmd="top -bn1 | awk 'NR == 3 {print $0}'|cut -d' ' -f 2-"
		
