# -*- coding:utf-8 -*-
'''
Created on 2016-4-27
@author: admin
用途：
	公共配置
规则：
	大分类-小分类-具体项目
	PATH_SCRIPT_xxxx
'''

WangCong				=	2344
XiaoGuiZhi				=	2693
LuHuan					=	4564
TanBin					=	6414
CaiBoXin				=	8563
YouZeShun				=	8766
QiangYao				=	8838
#监控报警群
OPS_MNT					=	12672

'''
业务支撑组
'''
IM_GROUP_SUPPORT		=	[LuHuan,CaiBoXin,QiangYao,TanBin]

'''
网络组
'''
IM_GROUP_NETWORK		=	[LuHuan,WangCong]

'''
程序开发者的火星
把Bug信息,调试信息发送给这个火星列表
注意：没有超过阀值的分析信息是必须发送的调试信息，否则报警后不知道程序是否活着
'''
IM_GROUP_DEVELOPER		=	[YouZeShun]

#历史报警记录
PATH_LOG_ALERT_HISTORY	=	'alert/history'

#日志分级：当程序发生了错误又不能让程序停下来的时候，就只能先记录着
PATH_LOG_EMERG			=	'level/level0_emerg'		#已经确定这种问题一旦发生，程序必然死亡，或者会影响服务器性能
PATH_LOG_ALERT			=	'level/level1_alert'		#已经确认的这种错误一旦发生，程序必然死亡
PATH_LOG_CRIT			=	'level/level2_crit'			#逻辑没有起到预期的效果，可能导致程序死亡（考虑到复杂度，逻辑不会处理所有可能性）
PATH_LOG_ERR			=	'level/level3_error'			#如：报警失败,不会引起程序的死亡
PATH_LOG_WARNNING		=	'level/level4_warnning'	#如：传递的参数格出问题return导致导致部分功能不可用
PATH_LOG_DEBUG			=	'level/level5_debug'		#如：一些引起过或可能引起错误的地方
PATH_LOG_INFO			=	'level/level6_info'			#测试时需要print的信息在上线后改为Info和Debug

COUNT_ALERT_RETRY		=	3

TIME_REALERT			=	60*10

