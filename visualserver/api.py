#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-7-25 上午10:00
# @Author  : youzeshun
# api:提供各种查询的接口


import json
import query


def ApiIDCTraff():
    jIDCTraff = query.GetIDCTraff()
    jIPTop = query.GetIPTop()
    dDataEchart, dOtherUsedBand = query.GetDataEchart(jIDCTraff, jIPTop)
    # 将机房的其他ip使用流量增加到dDataEchart的outer下（对应圆饼图的外围）
    dDataEchart = query.AddOuterItem(dDataEchart, dOtherUsedBand)
    # 不使用json.dumps前端将无法正常解码
    # 有sort_keys（对dict对象进行排序，我们知道默认dict是无序存放的）
    # 由于已经使用了有序字典，所以这里千万不要用sort_keys，会破坏顺序
    jResponse = json.dumps(dDataEchart)
    return jResponse


def ApiQueryImgTraff():
    pass
