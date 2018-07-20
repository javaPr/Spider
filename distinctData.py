#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Author wangdechang
Time 2018/7/18
"""
import numpy as np
import pandas as pd
filePath = r'D:\PythonWorkSpace\AMap\data\small_hotel.csv'

# ndata = np.loadtxt(open(filePath1,encoding='utf-8'))
with open(filePath) as f:
    data = pd.read_csv(f,sep=',',header=None)
    print(data)
    ids = data[0][data[0] > '2000']
    print(len(ids))
    print(len(ids.duplicated()))
    # with open('data.txt','w') as saveFile:
    #     for id in ids:
    #         saveFile.writelines(id+"\t\n")
