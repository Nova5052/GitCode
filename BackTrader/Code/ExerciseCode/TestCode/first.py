from datetime import datetime
from os import close
import backtrader as bt
import os.path
import sys
from backtrader import cerebro

from backtrader.order import SellOrder

class SmaCross(bt.Strategy):
    # 定义参数
    params = dict(period=5  # 移动平均期数
                  )

    def __init__(self):
        # 移动平均线指标
        self.move_average = bt.ind.MovingAverageSimple(self.datas[0].close,period=self.params.period)
        #print(self.data.lines.getlinealiases())
        #print(self.move_average.lines.getlinealiases())
        #print(self.lines.getlinealiases()) 线对象包含的类型



    def next(self):
        #print(self.datetime.datetime(0))
        #print(self.data.datetime.datetime(0))
        #print(self.data.buflen()) 总bar数
        #print(len(self.data)) 当前bar数
        #print(self.data._name) 数据名称
        if not self.position.size:  # 还没有仓位
            # 当日收盘价上穿5日均线，创建买单，买入100股
            if self.datas[0].close[-1] < self.move_average.sma[
                    -1] and self.data > self.move_average:
                self.buy(size=100)
        # 有仓位，并且当日收盘价下破5日均线，创建卖单，卖出100股
        elif self.datas[0].close[-1] > self.move_average.sma[-1] and self.data < self.move_average:
            self.sell(size=100)






cerebro=bt.Cerebro()
data=bt.feeds.GenericCSVData(
    dataname=r'e:\BackTrader\TestCode\datas\600000qfq.csv',
    datetime=2,
    open=3,
    high=4,
    low=5,
    close=6,
    volume=10,
    openinterest=-1,
    dtformat=('%Y%m%d'),
    fromdate=datetime(2019,1,1),
    todate=datetime(2020,7,8))

cerebro.adddata(data,'xxx')
cerebro.addstrategy(SmaCross)
cerebro.broker.setcash(10000.0)
cerebro.run()
#print('最终市值: %.2f' % cerebro.broker.getvalue())
#cerebro.plot(style='candlestick')



