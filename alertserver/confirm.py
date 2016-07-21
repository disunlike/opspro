# -*- coding:utf-8 -*-
'''
创建时间: Apr 21, 2016
作者: youzeshun  (IM: 8766)
用途:验证分析的结果是否正确

分析的结果是线路故障，则在两端做mtr
	1.分析mtr中丢包最大的点

分析的的结果是机房故障，则使用snmp查看机房的信息
	1.过去五分钟的最大峰值判断是否是带宽饱和导致的丢包
'''
import yaml
import time
from db import dbmgr
import MySQLdb
	
def idc_bound_now():	#
	with open('idc.yaml') as f:
		switch_out=yaml.load(f.read())

	db = MySQLdb.connect("10.32.64.64","zabbix","duoyi","new_zabbix")
	cursor=db.cursor()
	value={}
	for idc in switch_out:
		idc_value=[]
		switch_xianlu=switch_out[idc]
		for xianlu in switch_xianlu:
			xianlu_value={}
			sql1="select itemid from items where hostid=(select interface.hostid from interface where ip='%s') and \
	(key_='ifHCInOctets[%s]' or key_='ifHCOutOctets[%s]')" % (switch_xianlu[xianlu][0],switch_xianlu[xianlu][1],switch_xianlu[xianlu][1])
			cursor.execute(sql1)
			con=cursor.fetchall()
			print 'con',con
			itemid_in=con[0][0]
			itemid_out=con[1][0]
			sql2="select value from history_uint where itemid=%s order by clock DESC LIMIT 1" %itemid_in
			cursor.execute(sql2)
			traffic_in=cursor.fetchall()[0][0]
			sql3="select value from history_uint where itemid=%s order by clock DESC LIMIT 1" %itemid_out
			cursor.execute(sql3)
			traffic_out=cursor.fetchall()[0][0]
			traffic=max(traffic_in,traffic_out)
			print xianlu,round(float(traffic)/1024/1024,2)
	db.close()

def idc_bound_duration(days=30):
	with open('idc.yaml') as f:
		switch_out=yaml.load(f.read())

	db = MySQLdb.connect("10.32.64.64","zabbix","duoyi","new_zabbix")
	cursor=db.cursor()
	value={}
	for idc in switch_out:
		idc_value=[]
		switch_xianlu=switch_out[idc]
		for xianlu in switch_xianlu:
			xianlu_value={}
			sql1="select itemid from items where hostid=(select interface.hostid from interface where ip='%s') and \
	(key_='ifHCInOctets[%s]' or key_='ifHCOutOctets[%s]')" % (switch_xianlu[xianlu][0],switch_xianlu[xianlu][1],switch_xianlu[xianlu][1])
			cursor.execute(sql1)
			con=cursor.fetchall()
			itemid_in=con[0][0]
			itemid_out=con[1][0]
			sql2="select value from history_uint where itemid=%s order by clock DESC LIMIT 1" %itemid_in
			cursor.execute(sql2)
			traffic_in=cursor.fetchall()[0][0]
			sql3="select value from history_uint where itemid=%s order by clock DESC LIMIT 1" %itemid_out
			cursor.execute(sql3)
			traffic_out=cursor.fetchall()[0][0]
			traffic=max(traffic_in,traffic_out)
			print xianlu,round(float(traffic)/1024/1024,2)
	db.close()



idc_bound_now()

