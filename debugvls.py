#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-7-27 下午8:48
# @Author  : youzeshun
import visualserver
import json


def ShowIDCTraff():
    jIDCTraff = visualserver.query.GetIDCTraff()
    jIDCTraff = json.dumps(jIDCTraff, ensure_ascii=False)
    jIDCTraff = jIDCTraff.encode('utf-8')
    return jIDCTraff
    # for i in jIDCTraff:
    #     for j in jIDCTraff[i]:
    #         print i, j, jIDCTraff[i][j], '\n'


def ShowTopTraff():
    jIPTop = visualserver.query.GetIPTop()
    jIPTop = json.dumps(jIPTop, ensure_ascii=False)
    jIPTop = jIPTop.encode('utf-8')
    return jIPTop

# dData = visualserver.apiquery.GetIPTraff('113.106.204.230')


# print CheckFormat(dData)
# print dData['result']['netout']
# print ShowIDCTraff()
# print ShowTopTraff()
print visualserver.api.ApiIDCTraff()
