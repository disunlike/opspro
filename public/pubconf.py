# -*- coding:utf-8 -*-
'''
Created on 2016-4-27
@author: admin
��;��
	��������
����
	�����-С����-������Ŀ
	PATH_SCRIPT_xxxx
'''

WangCong				=	2344
XiaoGuiZhi				=	2693
LuHuan					=	4564
TanBin					=	6414
CaiBoXin				=	8563
YouZeShun				=	8766
QiangYao				=	8838
#��ر���Ⱥ
OPS_MNT					=	12672

'''
ҵ��֧����
'''
IM_GROUP_SUPPORT		=	[LuHuan,CaiBoXin,QiangYao,TanBin]

'''
������
'''
IM_GROUP_NETWORK		=	[LuHuan,WangCong]

'''
���򿪷��ߵĻ���
��Bug��Ϣ,������Ϣ���͸���������б�
ע�⣺û�г�����ֵ�ķ�����Ϣ�Ǳ��뷢�͵ĵ�����Ϣ�����򱨾���֪�������Ƿ����
'''
IM_GROUP_DEVELOPER		=	[YouZeShun]

#��ʷ������¼
PATH_LOG_ALERT_HISTORY	=	'alert/history'

#��־�ּ������������˴����ֲ����ó���ͣ������ʱ�򣬾�ֻ���ȼ�¼��
PATH_LOG_EMERG			=	'level/level0_emerg'		#�Ѿ�ȷ����������һ�������������Ȼ���������߻�Ӱ�����������
PATH_LOG_ALERT			=	'level/level1_alert'		#�Ѿ�ȷ�ϵ����ִ���һ�������������Ȼ����
PATH_LOG_CRIT			=	'level/level2_crit'			#�߼�û����Ԥ�ڵ�Ч�������ܵ��³������������ǵ����Ӷȣ��߼����ᴦ�����п����ԣ�
PATH_LOG_ERR			=	'level/level3_error'			#�磺����ʧ��,����������������
PATH_LOG_WARNNING		=	'level/level4_warnning'	#�磺���ݵĲ����������return���µ��²��ֹ��ܲ�����
PATH_LOG_DEBUG			=	'level/level5_debug'		#�磺һЩ�����������������ĵط�
PATH_LOG_INFO			=	'level/level6_info'			#����ʱ��Ҫprint����Ϣ�����ߺ��ΪInfo��Debug

COUNT_ALERT_RETRY		=	3

TIME_REALERT			=	60*10

