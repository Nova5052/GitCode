from datetime import date, datetime, timedelta
from os import close
import backtrader as bt
import os.path
import sys
from backtrader import cerebro

from backtrader.order import Order, SellOrder

class SmaCross(bt.Strategy):
    # 定义参数
    params = dict(period=5  # 移动平均期数
                  )

    def log(self,txt,dt=None):
        dt= dt or self.datetime.date(0)
        print('%s,%s' % (dt.isoformat(),txt))

    def __init__(self):
        # 移动平均线指标
        self.move_average = bt.ind.SMA(self.data.close,period=self.params.period)
        self.order=None

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
        self.order=None

    def notify_trader(self,trade):
        if trade.isclosed:
            print('毛收益:%0.2f 扣佣金后收益:%0.2f'%(trade.pnl,trade.pnlcomm))

    def next(self):
        if self.order:
            return
        if not self.position.size:  # 还没有仓位
            # 当日收盘价上穿5日均线，创建买单，买入100股
            if self.datas[0].close[-1] < self.move_average.sma[-1] and self.data > self.move_average:
                validday=self.data.datetime.datetime(0)+timedelta(days=7)
                self.order=self.buy(size=100,exectype=bt.Order.Limit,price=0.99*self.data,valid=validday)
        # 有仓位，并且当日收盘价下破5日均线，创建卖单，卖出100股
        elif self.datas[0].close[-1] > self.move_average.sma[-1] and self.data < self.move_average:
            self.order=self.sell(size=100)


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
cerebro.broker.setcommission(0.001)
cerebro.broker.set_slippage_fixed(0.05)
print('初始市值: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('最终市值: %.2f' % cerebro.broker.getvalue())
cerebro.plot(style='candlestick')



