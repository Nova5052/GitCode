from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
 
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
from datetime import datetime
# Import the backtrader platform
import backtrader as bt
from backtrader.indicators.basicops import Highest
from backtrader.indicators.mabase import MovAv
from backtrader.order import SellOrder
import tushare as ts
import pandas as ps
import matplotlib.pyplot as plt
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
        self.macd=bt.ind.MACD(self.data,period_me1=12,period_me2=26,period_signal=9,movav=MovAv.Exponential)


    def notify_order(self, order):
        if order.status in [order.Submitted,order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('买单执行:%.2f' % order.executed.price)
            elif order.issell():
                self.log('卖单执行:%.2f' % order.executed.price)
        elif order.status in [order.Canceled,order.Margin,order.Rejected]:
            self.log('订单未执行')



    def notify_trader(self,trade):
        if trade.isclosed:
            print('毛收益:%0.2f 扣佣金后收益:%0.2f'%(trade.pnl,trade.pnlcomm))

 
    def next(self):
        # if self.data.open[0] < self.data.close[0] and self.data.low[0] == self.data.open[0] and self.data.high[0] == self.data.close[0]:
        #     self.log('光头光脚阳线 1')
        # if self.data.open[0] > self.data.close[0] and self.data.low[0] == self.data.close[0] and self.data.high[0] == self.data.open[0]:
        #     self.log('光头光脚阴线 2')
        # if self.data.open[0]<self.data.close[0] and self.data.open[0]*1.1<self.data.close[0]:
        #     self.log('涨停 3')


        if self.macd.macd[-1]<self.macd.signal[-1] and self.macd.macd[0]>self.macd.signal[0]:
            self.log('创建买单:')
            self.order_target_value(target=9000)

        if self.macd.macd[-1]>self.macd.signal[-1] and self.macd.macd[0]<self.macd.signal[0]:
            self.log('创建卖单:')
            self.order_target_value(target=500)






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
    start_date='2021-01-01',end_date='2022-12-16',frequency='d',adjustflag="1")


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
        fromdate=datetime(2021, 1, 1),  # 起始日
        todate=datetime(2022, 12, 16)  # 结束日    
        )

    bs.logout()
    plt.switch_backend('agg')


    cerebro.adddata(data)
    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(commission=0.01)
    print('开始资产: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('结束资产: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()