# -*- coding:utf-8 -*-
import basedev

'''
获得eth0的ip，#子接口的ip不匹配。要匹配'grep eth0$' 改为 'grep eth0'
'''

class CDev(basedev.CBaseDev):
	
	def __init__(self):
		self.m_Name='eth0 ip'
		self.m_ShellCmd="ip a|grep eth0$|grep brd|awk '{print $2}'|awk -F '/' '{print $1}'"
		#尽量不要使用ifconfig，必须使用则用/sbin/iconfig