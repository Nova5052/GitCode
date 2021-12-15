import backtrader as bt
import sys
import datetime
from datetime import datetime
from backtrader import errors
import baostock as bs
from backtrader import trade
from backtrader import cerebro
import pandas as ps
from pandas.core.tools.datetimes import to_datetime



class SmaCross(bt.Strategy):
    params=dict(period=5)

    def log(self,txt,dt=None):
        dt=dt or self.datetime.date(0)
        print('%s,%s'%(dt.isoformat(),txt))

    def __init__(self):
        self.move_average=bt.ind.MovingAverageSimple(self.datas[0].close,period=self.params.period)
        self.order=None

    def notify_order(self,order):
        if order.status in [order.Submitted,order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('买单执行:%.2f' % order.executed.price)
            elif order.issell():
                self.log('卖单执行:%.2f' % order.executed.price)
        elif order.status in [order.Canceled,order.Margin,order.Rejected]:
            self.log('订单未执行')
        self.order=None

    def notify_trader(self,trader):
        if trade.isclosed:
            print('毛收益:%0.2f 扣佣金后收益:%0.2f' % (trade.pnl,trade.pnlcomm))

    def next(self):
        if self.order:
            return
        if not self.position.size:
            if self.datas[0].close[-1]<self.move_average.sma[-1] and self.data.close>self.move_average:
                validday=self.data.datetime.datetime(0)+datetime.timedelta(days=7)
                self.order = self.buy(size=100,exectype=bt.Order.Limit,price=0.99*self.data,valid=validday)
            elif self.datas[0].close[-1]>self.move_average.sma[-1] and self.data.close<self.move_average:
                self.order=self.sell(size=200)


cerebro=bt.Cerebro()

lg=bs.login()
print('登录 code:'+lg.error_code)
print('登录 msg:'+lg.error_msg)

code=input('请输入股票代码:\n')
strCode='sh.'+code

begDate='2021-01-01'
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
cerebro.adddata(data)
cerebro.broker.setcash(10000.0)
cerebro.broker.setcommission(commission=0.01)
print('开始资产: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('结束资产: %.2f' % cerebro.broker.getvalue())
cerebro.plot()
