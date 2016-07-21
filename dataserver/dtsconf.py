# -*- coding:utf-8 -*-
'''
Created on Mar 9, 2016
author: youzeshun  (IM: 8766)

数据中心服务的配置文件
'''

DEFAULT_TIME_OUT	=10
HEARTBEAT_INTERVAL	=5


#数据库配置：(使用远程数据库来测试下)
DB_HOST='192.168.63.139'
DB_USER='root'
DB_PSW='youzeshun'
DB_Name='gather'

#用于缓存发送不出去的sql协议数据包
PSQL_CACHE_PARH='data/sqlcache'

