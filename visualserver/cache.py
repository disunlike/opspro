#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-7-27 下午2:37
# @Author  : youzeshun
# 用于解决实时访问速度忙的问题。定时请求数据保存在文本中

import query
import json
import time
from public.define import *


def CacheQuery():
    jIDCTraff = query.GetIDCTraff()
    jIPTop = query.GetIPTop()
    dDataEchart, dOtherUsedBand = query.GetDataEchart(jIDCTraff, jIPTop)
    dDataEchart = query.AddOuterItem(dDataEchart, dOtherUsedBand)
    # json.dumps()将原本的Unicode字符拆分成一个个单独的ASCII码，ensure_ascii=False将不拆分.
    # 这样能以中文字符的形式将数据写到文本中，但是数据由于不是python能识别的编码，在未知情况下会报错
    dDataCache = {
        'date': GetTime(),
        'data': dDataEchart
    }
    # jResponse = json.dumps(dDataEchart, ensure_ascii=False)
    jResponse = json.dumps(dDataCache)
    # 由于Unicode字符没被拆分为ascll码，不能被python的函数ushi用。需用进行编码
    jResponse = jResponse.encode('utf-8')
    # 注意权限！
    ExecManagerFunc('log', 'Cache', '../../visual/static/idc/cache/pie.json', jResponse)


# 周期性地调用缓存代码
def PeriodCache():
    CacheQuery()
    Remove_Call_Out("periodcache")
    Call_Out(PeriodCache, 30, "periodcache")  # 为了不重名，使用文件名作为注册名
