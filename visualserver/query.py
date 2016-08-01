#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-7-28 下午4:22
# @Author  : youzeshun
# 数据查询api,将查询到的机房实时流量数据和机房最大带宽数据进行组合
# 有逻辑上的处理，如排序等
import idcconf
import spider
from public import alert
import collections

g_oSpider = spider.CSpider()


# 不能获得数据则报警，并且记录原因。以便处理
def GetIPTop():
    jIPTop = g_oSpider.ReadJson(idcconf.URL_IDC_TOP)
    # assert jIPTop != {}
    if not jIPTop:
        # 这里需要追加报警
        raise Exception('机房Top10流量不允许为空')
    return jIPTop


def GetIDCTraff():
    jIDCTraff = g_oSpider.ReadJson(idcconf.URL_IDC_TRFF)
    if not jIDCTraff:
        raise Exception('IDC线路流量不允许为空')
    return jIDCTraff


def IsEnableFormat(dData):
    if not isinstance(dData, dict):
        return 0
    if not 'result' in dData:
        return 0
    if not u'netout' in dData['result']:
        return 0
    # if not isinstance(dData['result']['netout'],int):
    #     return 0
    return 1


def GetIPTraff(sIP):
    sUrl = "%s%s" % (idcconf.URL_SERVER_INFO, sIP)
    jServerInfo = g_oSpider.ReadJson(sUrl)
    # if 'wrong' in jServerInfo['result']:
    #     #记录日志并报警
    #     pass
    if not IsEnableFormat(jServerInfo):
        alert.AlertLinux('不可用的服务器信息', 8766)
        return None
    return jServerInfo


# 合并机房流量数据和机房top10数据，转为echart 的接口需要的数据形式。这里可以转为能被echart读取的格式
def GetDataEchart(jIDCTraff, jIPTop):
    dDataEchart = {}
    # 机房各个线路的可用带宽之和
    iTotalBand = 0  # 所有机房的带宽和
    fTotalUsed = 0  # 所有机房已用带宽和
    fTotalTopUsed = 0  # 所有机房Top10使用的流量和
    dAllIP = {}
    dOtherUsedBand = {}
    for sServerRoom in jIDCTraff:
        # 强尧传来的数据是有序的，为了不破坏顺序这里使用有序字典。有序字典能和json互转，且顺序不会破坏
        dIPTraff = collections.OrderedDict()
        fTopUsed = 0
        if not sServerRoom in jIPTop:
            raise Exception('机房%s在流量Top10中' % (sServerRoom))
        for dServerInfo in jIPTop[sServerRoom]:
            sIP = dServerInfo['ip']
            fTraffic = dServerInfo['traffic']
            dIPTraff[sIP] = fTraffic
            dAllIP[sIP] = fTraffic  # 所有机房的Top 10 ip，用于绘制一个所有机房统计信息的Top 10
            # 该机房的流量使用top10带宽用量总和
            fTopUsed += fTraffic
        fTotalTopUsed += fTopUsed  # 所有机房top 10 的流量，用于计算出其他ip的使用量
        # 该机房下所有线路的已用带宽和
        iTotalServerUsedBand = 0
        dDataEchart[sServerRoom] = {}
        for sLine in jIDCTraff[sServerRoom]:
            # iTotalLineBand 线路的总带宽
            iTotalLineBand = jIDCTraff[sServerRoom][sLine][u'band']
            fUsedBand = jIDCTraff[sServerRoom][sLine][u'traffic_out']
            iTotalBand += iTotalLineBand  # 所有机房的带宽和
            fTotalUsed += fUsedBand  # 所有机房已用带宽和
            iTotalServerUsedBand += fUsedBand
            dDataEchart[sServerRoom][sLine] = {
                'inner': {
                    'used': fUsedBand,
                    'total': iTotalLineBand
                },
                'outer': dIPTraff
            }
        # print sServerRoom, iTotalServerUsedBand, fTopUsed
        # print sServerRoom
        dOtherUsedBand[sServerRoom] = int(iTotalServerUsedBand - fTopUsed)
        if dOtherUsedBand[sServerRoom] < 0:
            dOtherUsedBand[sServerRoom] = 0
        if dOtherUsedBand[sServerRoom] < -iTotalServerUsedBand * 0.05:
            # sMsg = '机房流量Top10大于机房已用流量，且误差大于已用流量的5%。机房已用流量：%i，TOp10流量：%i' % (iTotalServerUsedBand, int(fTopUsed))
            # alert.AlertLinux('警告:机房流量Top10大于机房已用流量，且误差大于已用流量的5%', 8766)
            pass

    # sort是又大到小，sorted是由小到大
    lstAllIP = sorted(dAllIP.iteritems(), key=lambda d: d[1], reverse=True)
    lstAllIP = lstAllIP[0:10]
    dTotalTop = collections.OrderedDict()
    # print fTotalUsed, iTotalBand,int(fTotalUsed - fTotalTopUsed)
    for i in lstAllIP:
        sIP = i[0]
        fTraff = i[1]
        dTotalTop[sIP] = fTraff
    dDataEchart['机房总计'] = {}
    dDataEchart['机房总计']['机房总计'] = {
        'inner': {
            'used': int(fTotalUsed),
            'total': iTotalBand
        },
        'outer': dTotalTop
    }
    # print dDataEchart
    dOtherUsedBand['机房总计'] = int(fTotalUsed - fTotalTopUsed)
    return dDataEchart, dOtherUsedBand  # 机房的其他ip使用流量 = 机房的总流量 - 机房top10的IP使用流量


def AddOuterItem(dDataEchart, dOtherUsedBand):
    for sServerRoom in dDataEchart:
        for sLine in dDataEchart[sServerRoom]:
            dDataEchart[sServerRoom][sLine]['outer']['other'] = dOtherUsedBand[sServerRoom]
    return dDataEchart
