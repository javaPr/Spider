#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Author wangdechang
Time 2018/7/18
"""
import numpy as np
import pandas as pd
filePath = r'D:\PythonWorkSpace\AMap\data\small_hotel.csv'
filePath1 = r'data\resapi.txt'
# ndata = np.loadtxt(open(filePath1,encoding='utf-8'))
with open(filePath1,encoding='utf-8') as f:
    data = pd.read_csv(f,delimiter="\t",header=None)
    print(data)
    print(data.size)
    data = data.drop_duplicates()
    print(len(data))
    data.to_csv(r'data\data_1.csv',header=None, index=None, sep='\t',encoding='utf-8')