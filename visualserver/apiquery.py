#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-7-25 上午10:00
# @Author  : youzeshun
# 数据查询api,将查询到的机房实时流量数据和机房最大带宽数据进行组合
# 有逻辑上的处理，如排序等

import idcconf
import spider
import json
import collections
from public import alert
from public import txtlog

g_oSpider = spider.CSpider()
g_oLog = txtlog.CLog()


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


def GetDataEchart(jIDCTraff, jIPTop):
    dDataEchart = {}
    # 机房各个线路的可用带宽之和
    dOtherUsedBand = {}
    for sServerRoom in jIDCTraff:
        # 初始化一个有序字典，有序字典能和json互转，且顺序不会破坏
        dIPTraff = collections.OrderedDict()
        fTopUsed = 0
        if not sServerRoom in jIPTop:
            print sServerRoom
            raise Exception('机房%s在流量Top10中' % (sServerRoom))
        for lstIndex in jIPTop[sServerRoom]:
            dIPTraff[lstIndex[0]] = lstIndex[1]
            # 改机房的流量使用top10带宽用量总和
            fTopUsed += lstIndex[1]

        # 该机房下所有线路的已用带宽和
        iTotalServerUsedBand = 0
        dDataEchart[sServerRoom] = {}
        for sLine in jIDCTraff[sServerRoom]:
            # iTotalLineBand 线路的总带宽
            iTotalLineBand = jIDCTraff[sServerRoom][sLine][u'band']
            fUsedBand = jIDCTraff[sServerRoom][sLine][u'traffic_out']
            iTotalServerUsedBand += fUsedBand
            dDataEchart[sServerRoom][sLine] = {
                'inner': {
                    'used': fUsedBand,
                    'total': iTotalLineBand
                },
                'outer': dIPTraff
            }
        # print sServerRoom, iTotalServerUsedBand, fTopUsed
        dOtherUsedBand[sServerRoom] = int(iTotalServerUsedBand - fTopUsed)
        if dOtherUsedBand[sServerRoom] < 0 and dOtherUsedBand[sServerRoom] < -iTotalServerUsedBand * 0.05:
            # sMsg = '机房流量Top10大于机房已用流量，且误差大于已用流量的5%。机房已用流量：%i，TOp10流量：%i' % (iTotalServerUsedBand, int(fTopUsed))
            alert.AlertLinux('警告:机房流量Top10大于机房已用流量，且误差大于已用流量的5%', 8766)
        dOtherUsedBand[sServerRoom] = 0
    return dDataEchart, dOtherUsedBand


# 机房的其他ip使用流量 = 机房的总流量 - 机房top10的IP使用流量
def AddOuterItem(dDataEchart, dOtherUsedBand):
    for sServerRoom in dDataEchart:
        for sLine in dDataEchart[sServerRoom]:
            dDataEchart[sServerRoom][sLine]['outer']['other'] = dOtherUsedBand[sServerRoom]
    return dDataEchart


def ApiQuery():
    jIDCTraff = GetIDCTraff()
    jIPTop = GetIPTop()
    dDataEchart, dOtherUsedBand = GetDataEchart(jIDCTraff, jIPTop)
    # 将机房的其他ip使用流量增加到dDataEchart的outer下（对应圆饼图的外围）
    dDataEchart = AddOuterItem(dDataEchart, dOtherUsedBand)
    # 不使用json.dumps前端将无法正常解码
    # 有sort_keys（对dict对象进行排序，我们知道默认dict是无序存放的）
    # 由于已经使用了有序字典，所以这里千万不要用sort_keys，会破坏顺序
    jResponse = json.dumps(dDataEchart)
    return jResponse


# 用于解决实时访问速度忙的问题。定时请求数据保存在文本中
def CacheQuery():
    jIDCTraff = GetIDCTraff()
    jIPTop = GetIPTop()
    dDataEchart, dOtherUsedBand = GetDataEchart(jIDCTraff, jIPTop)
    dDataEchart = AddOuterItem(dDataEchart, dOtherUsedBand)
    # json.dumps()将原本的Unicode字符拆分成一个个单独的ASCII码，ensure_ascii=False将不拆分
    jResponse = json.dumps(dDataEchart, ensure_ascii=False)
    # 由于Unicode字符没被拆分为ascll码，不能被python的函数ushi用。需用进行编码
    jResponse = jResponse.encode('utf-8')
    g_oLog.WriteFile('../../static/idc/cache/pie.json', jResponse, 'w+')


if __name__ == '__main__':
    def ShowIDCTraff():
        jIDCTraff = GetIDCTraff()
        for i in jIDCTraff:
            for j in jIDCTraff[i]:
                print i, j, jIDCTraff[i][j], '\n'


    def ShowTopTraff():
        jIPTop = GetIPTop()
        for i in jIPTop:
            print i


    # print ShowIDCTraff()
    # print ShowTopTraff()
    # print ApiQuery()
    CacheQuery()
