# -*- coding:utf-8 -*-
# 作者：youzeshun
# 用途：urllib2封装

import urllib2
import json

# 返回的中文是unicode格式,print方法会自动将该格式按照当前系统的编码来转换
class CSpider:
    def init(self):
        pass

    def ReadRespond(self, sUrl):
        oResponse = urllib2.urlopen(sUrl)
        sResponse = oResponse.read()
        return sResponse

    def ReadJson(self, sUrl):
        oResponse = urllib2.urlopen(sUrl)
        dResponse = json.load(oResponse)
        return dResponse


if __name__ == '__main__':
    oSpider = CSpider()
    print oSpider.ReadRespond('http://10.32.18.176:8088/zapi/lastvalue/?id=2&ip=121.201.102.33')
    print oSpider.ReadJson('http://10.32.18.176:8088/zapi/lastvalue/?id=2&ip=121.201.102.33')
