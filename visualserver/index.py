# -*- coding:utf-8 -*-

from structdata import IP_HEAD_TOUR
from spider import CSpider

sUrl = '121.201.102.33'


def GetUrl(sIP):
    sUrl = 'http://10.32.18.176:8088/zapi/lastvalue/?id=2&ip=%s' % (sIP)
    return sUrl


def IsEnableFormat(dData):
    if not isinstance(dData, dict):
        return 0
    if not 'result' in dTraff:
        return 0
    if not u'netin' in dTraff['result']:
        return 0
    return 1


g_oSpider = CSpider()


def TraffSum(listIP):
    lstNetIn = []
    for sIP in IP_HEAD_TOUR:
        sUrl = GetUrl(sIP)
        print sUrl
        dTraff = g_oSpider.ReadJson(sUrl)
        if IsEnableFormat(dTraff):
            lstNetIn.append(dTraff['result'][u'netin'])
        else:
            print 'ip%s获得的数据格式错误' % (sIP)


# TraffSum(IP_HEAD_TOUR)

sUrl = 'http://10.32.64.64:8000/info/getidc/'
sIDCTaff = g_oSpider.ReadRespond(sUrl)
dIDCTraff = eval(sIDCTaff)
print type(dIDCTraff)

for sServerRoom in dIDCTraff:
    print eval("u'%s'" % (sServerRoom))


