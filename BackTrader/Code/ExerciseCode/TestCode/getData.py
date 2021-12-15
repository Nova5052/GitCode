from sys import path
from typing import Mapping
import tushare as ts
import pandas as pd
import os

def get_data(code,start='2021-05-01',end='2021-09-07'):
    df=ts.get_k_data(code,autype='qfq',start=start,end=end)
    df.index=pd.to_datetime(df.date)
    df['openinterest']=0
    df=df[['open','high','low','close','volume','openinterest']]
    return df
