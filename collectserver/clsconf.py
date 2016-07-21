# -*- coding:utf-8 -*-
'''
Created on Mar 9, 2016
author: youzeshun  (IM: 8766)

#用途：数据采集客户端的配置文件
'''

RECODE_NORMAL=1
DEFAULT_TIME_OUT=10
HEARTBEAT_INTERVAL	=5

DATACENTER_SOCKET_INFO=[
			('192.168.63.139',65534),
			]

#用于缓存发送不出去的sql协议数据包
PSQL_CACHE_PARH='data/cache/psql.txt'

