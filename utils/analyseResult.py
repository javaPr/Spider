#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Author wangdechang
Time 2018/7/31
"""

import pandas as pd

filePath = r'../result/result_xiaoqu_info_20180731.dat'

with open(filePath,encoding='utf8') as f:
    data = pd.read_csv(f,header=None,sep='\t')
    data.drop_duplicates()
    size = data.groupby([3]).size()
    meanValue = data[4].groupby(data[3]).mean()
    province_city = data[[2,3]].drop_duplicates()

    dfSize = pd.DataFrame(size)
    dfMean = pd.DataFrame(meanValue)
    join = dfMean.join(dfSize)
    province_city.join(join,on=3).to_excel("../result/全国房价数据.xls")