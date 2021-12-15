from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
 
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
from datetime import datetime
# Import the backtrader platform
import backtrader as bt
from backtrader.indicators.basicops import Highest
import tushare as ts
import pandas as ps

import matplotlib
import baostock as bs
import sys
 
# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )
 
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
 
    def __init__(self):
        self.dataclose = self.datas[0].close

 
    def next(self):
        if self.data.open[0] < self.data.close[0] and self.data.low[0] == self.data.open[0] and self.data.high[0] == self.data.close[0]:
            self.log('光头光脚阳线 1')
        if self.data.open[0] > self.data.close[0] and self.data.low[0] == self.data.close[0] and self.data.high[0] == self.data.open[0]:
            self.log('光头光脚阴线 2')
        if self.data.open[0]<self.data.close[0] and self.data.open[0]*1.1<self.data.close[0]:
            self.log('涨停 3')



if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    # Add a strategy
    cerebro.addstrategy(TestStrategy)
    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    code=input('请输入股票代码: \n')
    strCode='sh.'+code

    ####登录系统###
    lg=bs.login()
    print('error_code:'+lg.error_code)
    print('error_msg'+lg.error_msg)

    rs=bs.query_history_k_data_plus(strCode,"date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus",
    start_date='2010-01-01',end_date='2022-11-16',frequency='d',adjustflag="1")


    dataframe=rs.get_data()
    dataframe=dataframe.apply(ps.to_numeric,axis=0,errors='ignore')
    dataframe=dataframe[dataframe.tradestatus==1]
    dataframe['date']=ps.to_datetime(dataframe['date'])

    data =bt.feeds.PandasData(
        dataname=dataframe,
        datetime='date',  # 日期列   
        open=2,  # 开盘价所在列
        high=3,  # 最高价所在列
        low=4,  # 最低价所在列
        close=5,  # 收盘价价所在列
        volume=7,  # 成交量所在列
        openinterest=-1,  # 无未平仓量列.(openinterest是期货交易使用的)
        fromdate=datetime(2010, 1, 1),  # 起始日
        todate=datetime(2022, 11, 16)  # 结束日    
        )

    bs.logout()




    # Add the Data Feed to Cerebro
    cerebro.adddata(data)
    # Set our desired cash start
    cerebro.broker.setcash(1000.0)
    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    # Set the commission
    cerebro.broker.setcommission(commission=0.0)
    # Print out the starting conditions
    # print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # Run over everything
    cerebro.run()
    # Print out the final result
    # print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # Plot the result
    # cerebro.plot()