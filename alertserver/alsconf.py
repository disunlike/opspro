# -*- coding:utf-8 -*-
'''
Created on Feb 19, 2016
author: youzeshun  (IM: 8766)

#用途：配置alertserver
'''
from public.pubconf import *

PATH_LOG_ALERT			 = 	'analyfault/imalert'  # 报警路径使用：文件名＋函数名

'''
和程序有间接关联性的人，他们的工作会使程序间接不可用（如影响ipsort内容）
把这个程序正常分析到的结论发给这个火星列表
'''
IM_GROUP_MATINTAIN		 = 	[YouZeShun, XiaoGuiZhi, QiangYao]

'''
程序使用者，业务支撑组和开发人员
'''
IM_USER					 = 	IM_GROUP_MATINTAIN + [LuHuan,QiangYao]

'''
检查数据库读取最近一次更新的数据的频率
'''
PERIOD_CHECK_DB			 = 20  # 目前nagios的监控间隔是1分钟，这个检查数据库de

'''
#这个时间间隔的目的是把报警算在一个事故中进行分析。
#除非10分钟能把两个故障引起的报警算法在一起，否则他不会有什么不利影响。这里把时间精确到3分钟不会带来其他好处
'''
STABLE_COUNT			 = 15  # 20*15=300,所有5m内的消息会被算在一起进行分析.

TIME_ALERT_DELAY		 = 60

'''
7个互相监控的机房
3个报警说a机房有问题，则可信度：3/7约等于0.43
2个报警说a机房有问题：则可信度：2/7约等于0.29
'''
THR_SR					 = 0.50

'''
混合上行和下行进行统计时，某个机房报警超过0.33算故障
'''
THR_SR_MERGE			 = 0.32

'''
混合统计的开启阀值
'''
THR_SR_MERGE_OPEN		 = 8

'''
一长串的报警，其中
两条线路之间的互报警超过了70%说明问题在于这两条线路之间
'''
THR_LINE				 = 0.70

'''
最少需要xx条报警才进行分析，条数少打扰会多。而且分析出来的数据只能知道哪有证明波动
'''
THR_MIN_ANALY			 = 2

'''
最少需要xx条报警才正常发送。开发者的调试信息依然是有结果就报警，不受影响
'''
THR_MIN_USER_SEND		 = 3

'''
频率为x秒每条时被视为故障
'''
THR_Fault_FREQUENCY		 = 3

'''
最少多少条报警发送到报警群中
'''
# THR_MIN_MNT_SEND		=10

# nagios ping 监控报警信息分析结果的报警配置
NAGIOS_PING_DICT		 = {
		'imalert':IM_GROUP_MATINTAIN,  # 火星号增减使用列表，不报警使用空列表
		'alertnum':2,  # 报警次数，当出现网络问题时会延迟重报的次数
		'log':'nagios/ping'  # 日志是相对路径，基础路径是脚本所在的路径。
		}

'''
	存放nagios报警信息的mysql数据库信息
'''
DB_NAGIOS_HOST			 = '10.32.64.139'
DB_NAGIOS_USER			 = 'nagios'
DB_NAGIOS_PSW			 = 'duoyi'
DB_NAGIOS_NAME			 = 'alarms'
DB_NAGIOS_TABLE			 = 'content'  # 监视这个表的内容增长

'''
	存放ZABBIX采集信息的数据库，用于读取故障点的相关信息
'''
DB_ZABBIX_HOST			 = "10.32.64.64"
DB_ZABBIX_USER			 = "zabbix"
DB_ZABBIX_PSW			 = "duoyi"
DB_ZABBIX_NAME			 = "new_zabbix"

'''
是否分析私网
'''
IS_ANALYSIS_PRI_NET		 = True

#########################################################下面是测试配置
'''
为了避免错误发送，在使用测试配置的时候把关键的正确报警位置给注销下
如：pubconf中的OPS_MNT暂时先注销

DB_HOST	='172.168.128.1'
DB_USER	='root'
DB_PSW	='youzeshun'

PERIOD_CHECK_DB = 5

TIME_ALERT_DELAY = 2

IM_USER				 = 	IM_GROUP_DEVELOPER
IM_MATINTAIN		 = 	IM_GROUP_DEVELOPER
OPS_MNT				 = 	IM_GROUP_DEVELOPER

'''

