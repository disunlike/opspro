# -*- coding:utf-8 -*-
'''
Created on Feb 23, 2016
author: youzeshun  (IM: 8766)

#用途：文件ＤＮＳ，将ＩＰ，网段进行替换
'''
from xml.dom.minicompat import NodeList
from public.define import *

#IP和机房之间的关系
#佛山
FS_1={
	'abbr':'FS-1',
	'sw':'10.82.195.81',
	'dx':'219.132.195.81',
	'lt':'163.177.154.81',
	}
MONITOR_NODE_FS={
				'name':'佛山',
				'abbr':'FS',
				'node':[FS_1],
				}

#顺德
SD={
	'abbr':'SD',
	'sw':'10.82.198.124',
	'dx':'183.60.198.124',
	}
MONITOR_NODE_SD={
				'name':'顺德',
				'abbr':'SD',
				'node':[SD],
				}

#常州
CZ={
	'abbr':'CZ',
	'dx':'112.73.64.4',
	#'lt':'222.132.63.4', 路线取消
	'sw':'10.82.64.4',
	}
MONITOR_NODE_CZ={
				'name':'常州',
				'abbr':'CZ',
				'node':[CZ],
				}

#济南
JN_1={
	'abbr':'JN-1',
	'lt':'123.129.209.12',
	'sw':'10.82.209.12',
	}
JN_2={
	'abbr':'JN-2',
	'lt':'119.188.15.147',
	'sw':'10.82.15.147',
	}
MONITOR_NODE_JN={
				'name':'济南',
				'abbr':'JN',
				'node':[JN_1,JN_2],
				}


#惠州
HZ={
	'abbr':'HZ',
	'dx':'113.106.204.124',
	'sw':'10.82.204.124',
	}
MONITOR_NODE_HZ={
				'name':'惠州',
				'abbr':'HZ',
				'node':[HZ],
				}


#南方基地
GYD={
	'abbr':'GYD',
	'yd':'183.232.9.3',
	'sw':'10.82.9.3',
	}
MONITOR_NODE_GYD={
				'name':'南方基地',
				'abbr':'GYD',
				'node':[GYD],
				}


#沈阳
SY={
	'abbr':'SY',
	'lt':'124.95.140.119',
	'sw':'10.82.140.119',
	}
MONITOR_NODE_SY={
				'name':'沈阳',
				'abbr':'SY',
				'node':[SY],
				}


#中山
ZS_1={
	'abbr':'ZS-1',
	'dx':'121.201.116.28',
	'lt':'120.31.146.28',
	'sw':'10.82.116.28',
	}
ZS_2={
	'abbr':'ZS-2',
	'dx':'121.201.116.191',
	'lt':'120.31.146.12',
	'sw':'10.82.116.191',
	}
ZS_3={
	'abbr':'ZS-3',
	'dx':'121.201.102.19',
	'lt':'120.31.146.19',
	'sw':'10.82.102.19',
	}
MONITOR_NODE_ZS={
				'name':'中山',
				'abbr':'ZS',
				'node':[ZS_1,ZS_2,ZS_3],
				}

WH_1={
	'abbr':'WH',
	'dx':'116.211.88.20',
	'lt':'218.106.114.166',
	'sw':'10.82.88.20',
	}
MONITOR_NODE_WH={
				'name':'武汉金银湖',
				'abbr':'WH',
				'node':[WH_1],
				}

'''
ZS_1={
	'abbr':'ZS-1',
	'dx':'183.61.86.28',
	'lt':'163.177.182.28',
	'sw':'10.82.86.28',
	}
ZS_2={
	'abbr':'ZS-2',
	'dx':'183.61.80.191',
	'lt':'120.31.145.12',
	'sw':'10.82.80.191',
	}
MONITOR_NODE_ZS={
				'name':'中山',
				'abbr':'ZS',
				'node':[ZS_1,ZS_2],
				}
'''

#成都
CD={
	'abbr':'CD',
	'dx':'222.211.64.201',
	'sw':'10.80.64.201',
	}
MONITOR_NODE_CD={
				'name':'成都',
				'abbr':'CD',
				'node':[CD],
				}

#阿里北京B,
MONITOR_NODE_ALI_BJ_B={
					'name':'阿里北京B',
					'abbr':'ALI-BJ-B',
					'node':[{
								'abbr':'ALI-BJ-B',
								'bgp':'112.126.86.140',
								'sw':'10.79.33.140'
							}],
					}

#阿里杭州B,
MONITOR_NODE_ALI_HZ_B={
					'name':'阿里杭州B',
					'abbr':'ALI-HZ-B',
					'node':[{
							'abbr':'ALI-HZ-B',
							'bgp':'120.26.161.48',
							'sw':'10.79.33.48',
							}],
					}

#阿里深圳B,
MONITOR_NODE_ALI_SZ_B={
					'name':'阿里深圳B',
					'abbr':'ALI-SZ-B',
					'node':[{
								'abbr':'ALI-SZ-B',
								'bgp':'120.25.199.237',
								'sw':'10.79.34.237',
							}],
					}

#阿里上海B,
MONITOR_NODE_ALI_SH_B={
					'name':'阿里上海B',
					'abbr':'ALI-SH-B',
					'node':[{
								'abbr':'ALI-SH-B',
								'bgp':'139.196.252.251',
								'sw':'10.79.64.251',
							}],
					}

#阿里杭州D,
MONITOR_NODE_ALI_HZ_D={
					'name':'阿里杭州D',
					'abbr':'ALI-HZ-D',
					'node':[{
								'abbr':'ALI-HZ-D',
								'bgp':'120.26.0.237',
								'sw':'10.79.35.237',
							}]
					}

#腾讯北京1区,
MONITOR_NODE_QQ_BJ_1={
					'name':'腾讯北京1区',
					'abbr':'QQ-BJ-1',
					'node':[{
								'abbr':'QQ-BJ-1',
								'bgp':'123.206.51.36',
								'sw':'10.79.22.36',
							}],
					}

#腾讯广州1区,
MONITOR_NODE_QQ_GZ_1={
					'name':'腾讯广州1区',
					'abbr':'QQ-GZ-1',
					'node':[{
								'abbr':'QQ-GZ-1',
								'bgp':'119.29.121.123',
								'sw':'10.79.22.123',
							}],
					}


#腾讯上海1区
MONITOR_NODE_QQ_SH_1={
					'name':'腾讯上海1区',
					'abbr':'QQ-SH-1',
					'node':[{
								'abbr':'QQ-SH-1',
								'bgp':'115.159.190.168',
								'sw':'10.79.22.168',
							}],
					}

#监控结点和机房的对应关系,这个字典的结构是最复杂的。逻辑代码通常不要使用这个字典。
#这个字典的用途在于提供给下面的解析程序解析为简单的结构
MONITOR_NODE_DICT={
			'fs':MONITOR_NODE_FS,
			'sd':MONITOR_NODE_SD,
			'cz':MONITOR_NODE_CZ,
			'jn':MONITOR_NODE_JN,
			'hz':MONITOR_NODE_HZ,
			'gyd':MONITOR_NODE_GYD,
			'sy':MONITOR_NODE_SY,
			'zs':MONITOR_NODE_ZS,
			'cd':MONITOR_NODE_CD,
			'wh':MONITOR_NODE_WH,
			'ALI-BJ-B':MONITOR_NODE_ALI_BJ_B,
			'ALI-HZ-B':MONITOR_NODE_ALI_HZ_B,
			'ALI-SZ-B':MONITOR_NODE_ALI_SZ_B,
			'ALI-SH-B':MONITOR_NODE_ALI_SH_B,
			'ALI-HZ-D':MONITOR_NODE_ALI_HZ_D,
			'QQ-BJ-1':MONITOR_NODE_QQ_BJ_1,
			'QQ-GZ-1':MONITOR_NODE_QQ_GZ_1,
			'QQ-SH-1':MONITOR_NODE_QQ_SH_1,
			}

##################################################
#下面的配置是通过对上面的配置进行计算得到的，这样不需要维护
#如果不知道计算得到的是什么东西,请print
##################################################

def IsOperator(NodeList,OperatorType):
	for NodeDict in NodeList:
		if NodeDict.has_key(OperatorType):
			return 1
	
def GetOperatorsSRList(OperatorType):
	TmpList=[]
	for k,MNTDict in MONITOR_NODE_DICT.items():
		NodeList=MNTDict['node']
		if not IsOperator(NodeList,OperatorType):
			continue
		TmpList.append(k)
	return TmpList
	
#机房和运营商的对应关系
OPERATORS_SR_DICT={
			'dx':GetOperatorsSRList('dx'),	#所有的电信机房作为一个列表:['hz', 'fs', 'cd', 'cz', 'zs', 'sd']
			'lt':GetOperatorsSRList('lt'),
			'yd':GetOperatorsSRList('yd'),
			'bgp':GetOperatorsSRList('bgp'),
			}

#ip和运营商的对应关系
def GetMNTIPList(MNTList,OperatorType):
	TmpList=[]
	for NodeDict in MNTList:
		if not OperatorType in NodeDict:
			continue
		TmpList.append(NodeDict[OperatorType])
	return TmpList
			
def GetOperatorsIPList(OperatorType):
	TmpList=[]
	for k,MNTDict in MONITOR_NODE_DICT.items():
		NodeList=MNTDict['node']
		TmpList+=GetMNTIPList(NodeList,OperatorType)
	return TmpList

#运营商和IP的对应关系.(私网的运营商是自己)
OPERATORS_IP_DICT={
			'dx':GetOperatorsIPList('dx'),			#所有的电信IP作为一个列表
			'lt':GetOperatorsIPList('lt'),
			'yd':GetOperatorsIPList('yd'),
			'bgp':GetOperatorsIPList('bgp'),
			'sw':GetOperatorsIPList('sw'),
			}

#计算一个IP所属的运营商
def CalOperator(sIP):
	for sOperator,lstIP in OPERATORS_IP_DICT.items():
		if sIP in lstIP:
			return sOperator


def GetIPList(SRDict):		#得到一个监控结点下IP的列表
	TmpList=[]
	for k,v in SRDict.items():
		if k=='sw' or k=='dx' or k=='lt' or k=='yd' or k=='bgp':
			TmpList.append(v)
	return TmpList


def GetMNTIpList(NodeList):							#得到一个监控节点列表的IP列表
	IPList=[]
	for NodeDict in NodeList:
		IPList+=GetIPList(NodeDict)
	return IPList


def TranDictToList():								#为了减低程序的复杂度，需要使用降低数据的嵌套。所以把监控结点的ip放在一个列表中
	TmpDict={}
	for k,MNTDict in MONITOR_NODE_DICT.items():
		NodeList=MNTDict['node']
		TmpDict[k]=GetMNTIpList(NodeList)
	return TmpDict

#机房和IP的对应关系
SERVER_ROOM_DICT=TranDictToList()					#所有的ip按照机房进行分类

#所有的ip仅按照监控结点进行组织为字典，然后不分类
MONITOR_NODE_LIST=[]
for Dict in MONITOR_NODE_DICT.itervalues():
	MONITOR_NODE_LIST+=Dict['node']

#简称翻译
def GetNameDict():
	TmpDict={}
	for k,MNTDict in MONITOR_NODE_DICT.items():
		sAbbr=MNTDict['abbr']
		sName=MNTDict['name']
		TmpDict[sAbbr]=sName
	return TmpDict

NAME_DICT=GetNameDict()

#################################################
#这里提供查询接口
#################################################
def AbbrToName(sAbbr):
	if not sAbbr:
		return
	sAbbr=sAbbr.upper() 							#所有字母都转换成大写  
	if NAME_DICT.has_key(sAbbr):
		return NAME_DICT[sAbbr]
	elif sAbbr=='DX':
		return '电信'
	elif sAbbr=='LT':
		return '联通'
	elif sAbbr=='YD':
		return '移动'
	elif sAbbr=='BGP':
		return 'BGP'
	elif sAbbr=='SW':
		return '私网'
	
	
def SearchSR(sIP):
	for sSRName,IPList in SERVER_ROOM_DICT.items():
		if sIP in IPList:
			return sSRName
	sErr='ip:%s 没有找到对应的机房简称'%(sIP)
	Alert(sErr,IM_GROUP_DEVELOPER)
	
def IPToName(sIP):
	sAbbr=SearchSR(sIP)
	sSRName=AbbrToName(sAbbr)
	return sSRName
	
def IPToOperator(sIP):
	sAbbrOperator=CalOperator(sIP)
	sFullName=AbbrToName(sAbbrOperator)
	return sFullName
	
if __name__=='__main__':
	print '将简称QQ-GZ-1转为汉字:%s'%(AbbrToName('QQ-GZ-1'))
	print '小写的简称cz自动转为大写进行转换:%s'%(AbbrToName('cz'))
	
