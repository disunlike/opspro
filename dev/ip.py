# -*- coding:utf-8 -*-
import basedev

'''
���eth0��ip��#�ӽӿڵ�ip��ƥ�䡣Ҫƥ��'grep eth0$' ��Ϊ 'grep eth0'
'''

class CDev(basedev.CBaseDev):
	
	def __init__(self):
		self.m_Name='eth0 ip'
		self.m_ShellCmd="ip a|grep eth0$|grep brd|awk '{print $2}'|awk -F '/' '{print $1}'"
		#������Ҫʹ��ifconfig������ʹ������/sbin/iconfig