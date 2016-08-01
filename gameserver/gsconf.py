# -*- coding:utf-8 -*-
'''
Created on Feb 18, 2016
author: youzeshun  (IM: 8766)
用途：这是一个配置文件，单独写配置文件是为了容易检查配置，避免上线后依然是测试配置

配置务必参考业务流量变化规律：	这是旧dos检查的一段误报。对应游戏服手游的流量在午饭，晚饭和晚上睡前的一两个小时内流量最高，达到2.7M/s左右

2016-01-10 22:32:36 接收总流量 1432396986421 bit 网速 766425 bit/s 速度差 70599 bit/s 速度变化率 3530 bit/s^2 状态 ok 0
2016-01-10 22:32:56 接收总流量 1432414792172 bit 网速 890288 bit/s 速度差 123863 bit/s 速度变化率 6193 bit/s^2 状态 ok 0
2016-01-10 22:33:16 接收总流量 1432435820436 bit 网速 1051413 bit/s 速度差 161125 bit/s 速度变化率 8056 bit/s^2 状态 ok 0
2016-01-10 22:33:36 接收总流量 1432458231615 bit 网速 1120559 bit/s 速度差 69146 bit/s 速度变化率 3457 bit/s^2 状态 ok 0
2016-01-10 22:33:56 接收总流量 1432494929343 bit 网速 1834886 bit/s 速度差 714327 bit/s 速度变化率 35716 bit/s^2 状态 warn 0
2016-01-10 22:34:16 接收总流量 1432548198307 bit 网速 2663448 bit/s 速度差 828562 bit/s 速度变化率 41428 bit/s^2 状态 dos 0
2016-01-10 22:34:36 接收总流量 1432564332984 bit 网速 806734 bit/s 速度差 -1856714 bit/s 速度变化率 -92836 bit/s^2 状态 ok 0
2016-01-10 22:34:56 接收总流量 1432599473250 bit 网速 1757013 bit/s 速度差 950279 bit/s 速度变化率 47514 bit/s^2 状态 warn 0
2016-01-10 22:35:16 接收总流量 1432655966477 bit 网速 2824661 bit/s 速度差 1067648 bit/s 速度变化率 53382 bit/s^2 状态 dos 0
2016-01-10 22:35:36 接收总流量 1432709524994 bit 网速 2677926 bit/s 速度差 -146735 bit/s 速度变化率 -7337 bit/s^2 状态 dos 968081
2016-01-10 22:35:56 接收总流量 1432759501769 bit 网速 2498839 bit/s 速度差 -179087 bit/s 速度变化率 -8954 bit/s^2 状态 dos 968081
2016-01-10 22:36:16 接收总流量 1432808219555 bit 网速 2435889 bit/s 速度差 -62950 bit/s 速度变化率 -3148 bit/s^2 状态 dos 968081
2016-01-10 22:36:36 接收总流量 1432856046243 bit 网速 2391334 bit/s 速度差 -44555 bit/s 速度变化率 -2228 bit/s^2 状态 dos 968081
2016-01-10 22:36:56 接收总流量 1432897716325 bit 网速 2083504 bit/s 速度差 -307830 bit/s 速度变化率 -15392 bit/s^2 状态 dos 968081
2016-01-10 22:37:16 接收总流量 1432949388246 bit 网速 2583596 bit/s 速度差 500092 bit/s 速度变化率 25005 bit/s^2 状态 dos 968081
2016-01-10 22:37:36 接收总流量 1432996938262 bit 网速 2377501 bit/s 速度差 -206095 bit/s 速度变化率 -10305 bit/s^2 状态 dos 968081
2016-01-10 22:37:56 接收总流量 1433039138611 bit 网速 2110017 bit/s 速度差 -267484 bit/s 速度变化率 -13374 bit/s^2 状态 dos 968081
2016-01-10 22:38:16 接收总流量 1433079379914 bit 网速 2012065 bit/s 速度差 -97952 bit/s 速度变化率 -4898 bit/s^2 状态 dos 968081
2016-01-10 22:38:36 接收总流量 1433122774203 bit 网速 2169714 bit/s 速度差 157649 bit/s 速度变化率 7882 bit/s^2 状态 dos 968081
2016-01-10 22:38:56 接收总流量 1433168981778 bit 网速 2310379 bit/s 速度差 140665 bit/s 速度变化率 7033 bit/s^2 状态 dos 968081
2016-01-10 22:39:16 接收总流量 1433211183251 bit 网速 2110074 bit/s 速度差 -200305 bit/s 速度变化率 -10015 bit/s^2 状态 dos 968081
2016-01-10 22:39:36 接收总流量 1433254309890 bit 网速 2156332 bit/s 速度差 46258 bit/s 速度变化率 2313 bit/s^2 状态 dos 968081
2016-01-10 22:39:56 接收总流量 1433299122203 bit 网速 2240616 bit/s 速度差 84284 bit/s 速度变化率 4214 bit/s^2 状态 dos 968081
'''
from public.pubconf import *

#内核缓存日志 - 包含开机自检信息
KERN_BUFF_ALERT			=	OPS_MNT
KERN_BUFF_CRIT			=	OPS_MNT

#日志各等级监控
CHECKLOG_ERR			=	IM_GROUP_DEVELOPER
CHECKLOG_CRIT			=	OPS_MNT
CHECKLOG_ALERT			=	OPS_MNT
CHECKLOG_EMERG			=	OPS_MNT

#####################################################具体的配置
'''
	大于4.2M才会激活Dos检查程序，正常而没有活动的情况下，单台服务器的流量（神武端游为准）只有在少数时段超过这个值
	该值不能太大，否则会错误流量变化特征最明显的位置。太小容易引发误报（旧版本中是没有这个值的）
	
	当流量小于4.2M的时候状态将进入normal状态，程序清空所有参数
'''
THR_OPEN				=	4200

'''
	1.每当激活Dos检查程序时，程序会维持激活的周期。检查程序激活就可能会有误报。当流量在可以承受的范围内无论是否有异常流量都不要激活
	2.维持激活而不大于阀值持续激活是因为流量有瞬时波动的特性，例如：
		第一回合:流量5.1M	激活-起始状态：OK
		第二回合：流量6.9M	激活-流量增长过快：warn
		第三回合：流量4.9M	熄灭-清空数据（瞬时波动）
		第四回合：流量7.3M 激活-起始状态：OK
		（流量还在增长）
'''
COUNT_OPEN				=	5	#激活程序的周期

'''
	这是warn状态持续的周期数，在这个周期中，如果流量持续增长那么会判断为dos。周期结束回到normal
	程序如果在失活，那么说明流量持续低，所有的状态状态都是没意义的。所以会回到normal中
'''
COUNT_WARN				=	5	#激活警告状态的周期（判断为warn状态的第一个周期不算。这里5个周期值会执行5次StatusWarn方法）

'''
	warn状态下多少次超过阀值判断为dos
	大流量的情况下波动也是非常大的，dos下流量是抖动上升的。应该使用高阀值和低的稳定计数。
	参考：
		2016-04-11 19:32:24 速度:589 kb/s 速度变化率: 0 kb/s^2 状态: ok 【Debug】StableCount: 0
		2016-04-11 19:32:44 速度:74181 kb/s 速度变化率: 3679 kb/s^2 状态: warn 【Debug】StableCount: 0 动态阀值: 59344 kb/s
		2016-04-11 19:33:04 速度:123120 kb/s 速度变化率: 2446 kb/s^2 状态: warn 【Debug】StableCount: 1 动态阀值: 59344 kb/s
		2016-04-11 19:33:25 速度:122559 kb/s 速度变化率: -29 kb/s^2 状态: warn 【Debug】StableCount: 2 动态阀值: 59344 kb/s
		2016-04-11 19:33:45 速度:120664 kb/s 速度变化率: -95 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
	注意：由于变化率的波动是非常大的。所以这种方式不一定能匹配出dos
'''
COUNT_STABLE_INTO_DOS	=	COUNT_WARN-3	#判断5次，其中3次超过阀值则进入dos。这里和周期还有一定关系，周期太大，dos流量达到顶峰，变化率会变低

'''
	1.dos状态下低于阀值多少次进入normal状态
	2.阀值指的是动态阀值（进入warn状态时的速度*0.8）和静态阀值
	3.在warn和dos状态下检查流量的间隔会缩短，4意味着最快，在dos结束后要40s才会得出dos结束的判断。
'''
COUNT_STABLE_INTO_NORMAL=	4

'''
	检查流量变化的周期
	如果是dos攻击，流量是在短时间内上升的。必须要在流量的上升区间内将dos检查出来。故而周期设置要考虑准确度，负载。
'''
PERIOD_NORMAL			=	20

'''
	异常状态下加快检查的周期，以提高判断的速度。
	dos的攻击持续时间较短
'''
PERIOD_WARN				=	10

'''
	1.速度变化率阀值，当程序被激活后，速度变化率大于该值将进入警告状态（表示流量快速上升）
	之后开启稳定计数器，如果在之后几个周期中，速度变化率没有低于动态阀值（进入warn状态的速度*系数）。
	那么状态将变为dos并发出报警
	2.在可行的基础上追求简单，而不是精确。参考例子中THR_SLOPE=31。(31kb/s^2=速度差/时间=1860/60,既一分钟速度差1.8m/s)
	参考：
	2016-04-11 19:32:24 速度:589 kb/s 速度变化率: 0 kb/s^2 状态: ok 【Debug】StableCount: 0
	2016-04-11 19:32:44 速度:74181 kb/s 速度变化率: 3679 kb/s^2 状态: warn 【Debug】StableCount: 0 动态阀值: 59344 kb/s
	2016-04-11 19:33:04 速度:123120 kb/s 速度变化率: 2446 kb/s^2 状态: warn 【Debug】StableCount: 1 动态阀值: 59344 kb/s
	2016-04-11 19:33:25 速度:122559 kb/s 速度变化率: -29 kb/s^2 状态: warn 【Debug】StableCount: 2 动态阀值: 59344 kb/s
	2016-04-11 19:33:45 速度:120664 kb/s 速度变化率: -95 kb/s^2 状态: dos 【Debug】StableCount: 0 动态阀值: 59344 kb/s
'''
THR_SLOPE				=	310	#kb/s^2

'''
	1.warn期间，如果流量超过了该值会直接进入dos状态。
	2.这不意味着流量超过42M一定会报警。如果流量在激活程序后，缓慢增长（不触发warn,或warn状态下缓慢增长，让warn回到normal）是能到达42m/s的
'''
THR_DOS_TRAFF			=	THR_OPEN*10

#分析本地流量检查Dos，疑似Dos发送火星报警和相关统计信息
IM_DOS					=	OPS_MNT

#三个键名依次为：严重程度，火星号，日志相对路径
#空值表示不处理
KERN_BUFF_DEAL_DICT		={
			'alert'			:{'imalert':KERN_BUFF_ALERT,'log':'dmesg/level1'},#报警并且记录
			'crit'			:{'imalert':KERN_BUFF_CRIT,	'log':'dmesg/level2'},#报警并且记录
			'error'			:{'imalert':'',				'log':'dmesg/level3'},#记录但不报警
			'warn'			:{'imalert':'',				'log':''}#不记录不报警
		}

#自检的周期
KERN_BUFF_PERIOD		=	300

#按照键值得匹配方式，如果能匹配到键值，那么这个错误信息会被忽视（意料之内的错误）
KERN_BUFF_WHITE_LIST	={
				'Package power limit notification'	:'cut -d "]" -f2-|cut -d" " -f3-6',
				'Core power limit notification'		:'cut -d "]" -f2-|cut -d" " -f3-6',
			}

#检查日志的周期
CHECKLOG_PERIOD			=	300

#检查下面的日志，当内容增加时，增加的内容会被发送到火星。（日志必须存在）
CHECKLOG_LOG_DICT		={
			'/var/log/kern.err.log'		:{'imalert':CHECKLOG_ERR},
			'/var/log/kern.crit.log'	:{'imalert':CHECKLOG_CRIT},
			'/var/log/kern.alert.log'	:{'imalert':CHECKLOG_ALERT},
			'/var/log/kern.emerg.log'	:{'imalert':CHECKLOG_EMERG},
		}

#报警脚本的路径
PATH_SCRIPT_ALERT		=	'/home/dy1/shellpublic/sendrtx.sh'

#获得IP的脚本路径
PATH_SCRIPT_GET_IP		=	'/home/dy1/shellpublic/getip.sh'

#历史报警信息
PATH_LOG_ALERT_HISTORY	=	'alert/history'
#模块运行的状态日志
PATH_LOG_STATUS_TRAFF	=	'status/trafficanalyze'
#流量检查dos,根据网卡eth0
PATH_LOG_TRAFF			=	'checkdos/eth0'

####################################################完毕，下面是测试时使用的配置。测试配置必须默认注释，到了测试环境再手动打开
'''
下面是测试配置,不要改动部署配置
需要调试则直接在下面重新声明宏以覆盖部署配置。避免忘记改回部署配置

#检查下面的日志，当内容增加时，增加的内容会被发送到火星。（日志必须存在）

#自检的周期
KERN_BUFF_PERIOD		=	5

#检查日志的周期
CHECKLOG_PERIOD			=	5
KERN_BUFF_DEAL_DICT={
			'alert'			:{'imalert':IM_GROUP_DEVELOPER,	'log':'dmesg/level1'},#报警并且记录
			'crit'			:{'imalert':IM_GROUP_DEVELOPER,	'log':'dmesg/level2'},#报警并且记录
			'error'			:{'imalert':IM_GROUP_DEVELOPER,	'log':'dmesg/level3'},#记录但不报警
			'warn'			:{'imalert':'',					'log':''}#不记录不报警
		}
		
PERIOD_NORMAL			=	2
PERIOD_WARN				=	1
THR_OPEN				=	1200
THR_SLOPE				=	30	#kb/s^2
THR_DOS_TRAFF			=	THR_OPEN*3
IM_DOS					=	IM_GROUP_DEVELOPER


#开机自检各等级监控
KERN_BUFF_ALERT			=	IM_GROUP_DEVELOPER
KERN_BUFF_CRIT			=	IM_GROUP_DEVELOPER


#日志各等级监控
CHECKLOG_ERR			=	IM_GROUP_DEVELOPER
CHECKLOG_CRIT			=	IM_GROUP_DEVELOPER
CHECKLOG_ALERT			=	IM_GROUP_DEVELOPER
CHECKLOG_EMERG			=	IM_GROUP_DEVELOPER


CHECKLOG_LOG_DICT		={
			'/var/log/kern.err.log'		:{'imalert':IM_GROUP_DEVELOPER},
			'/var/log/kern.crit.log'	:{'imalert':IM_GROUP_DEVELOPER},
			'/var/log/kern.alert.log'	:{'imalert':IM_GROUP_DEVELOPER},
			'/var/log/kern.emerg.log'	:{'imalert':IM_GROUP_DEVELOPER},
		}

'''

