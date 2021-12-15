import backtrader as bt
import datetime 
import os.path
import sys
import baostock as bs
import pandas as ps
from  pytdx.hq import TdxHq_API 


class BOLLStrategy(bt.Strategy):
    params=(
        ("period",20), #布林线周期
        ("devfactor",2),#偏离因子
        ("size",20),#订单数量
        ("debug",False)#是否调试
    )

    def __init__(self):
        self.boll=bt.indicators.BollingerBands(period=self.params.period,devfactor=self.p.devfactor)

    def next(self):
        #未决订单列表
        orders=self.broker.get_orders_open()
        #取消所有未决订单
        if orders:
            for order in orders:
                self.broker.cancel(order)

        #无仓位，准备建仓入市
        if not self.position:#没有仓位
            if self.datas[0].close>self.boll.lines.top:
                self.sell(exectype=bt.Order.Stop,price=self.boll.lines.top[0],size=self.p.size)

            if self.data.close<self.boll.lines.bot:
                self.buy(exectype=bt.Order.Stop,price=self.boll.lines.bot[0],size=self.p.size)
        else:
            if self.position.size>0:
                self.sell(exectype=bt.Order.Limit,price=self.boll.lines.mid[0],size=self.p.size)
            else:
                self.buy(exectype=bt.Order.Limit,price=self.boll.lines.mid[0],size=self.p.size)

cerebro=bt.Cerebro()

lg=bs.login()
print('登录 code:'+lg.error_code)
print('登录 msg:'+lg.error_msg)

code=input('请输入股票代码:\n')
strCode='sh.'+code

begDate='2010-01-01'
endDate='2022-01-01'

rs=bs.query_history_k_data_plus(strCode,"date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus",start_date=begDate,end_date=endDate,frequency='d',adjustflag="1")
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
    fromdate=ps.to_datetime(begDate),  # 起始日
    todate=ps.to_datetime(endDate)  # 结束日    
    )

bs.logout()

# api=TdxHq_API()
# if api.connect('119.147.212.81',7709):
#     data=api.get_security_bars(9,0,'000001',4,10)
#     print(data)
#     data=api.to_df(data)
#     print(data)
#     api.disconnect()


cerebro.adddata(data)
cerebro.broker.setcash(10000.0)
cerebro.broker.setcommission(commission=0.01)
print('开始资产: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('结束资产: %.2f' % cerebro.broker.getvalue())
cerebro.plot()

