import backtrader as bt
import datetime 
import os.path
import sys
from backtrader.indicators import priceoscillator
import baostock as bs
import pandas as ps
import math
import A_CommBackTraderClass

class ShuangJunXian(bt.Strategy):
    params=dict(
        pfast=5,
        pslow=30
    )

    def log(self,txt,dt=None):
        dt=dt or self.datas[0].datetime.date(0)
        print('%s,%s'%(dt.isoformat(),txt))

    def __init__(self):
        sma1=bt.ind.SMA(period=self.params.pfast)
        sma2=bt.ind.MovingAverageSimple(period=self.params.pslow)
        self.crossover=bt.ind.CrossOver(sma1,sma2)
        self.close=self.datas[0].close
        self.order=None

    def next(self):
        if not self.position:
            if self.crossover>0:
                cash=self.broker.get_cash()
                price=self.datas[0].close[0]
                stock=math.ceil(cash/price/100)*100-100
                print('数量:',stock)
                self.order=self.buy(size=stock)
                self.log('买入')
        else:
            if self.crossover<0:
                cash=self.broker.getvalue()
                price=self.datas[0].close[0]
                stock=math.ceil(cash/price/100)*100-100
                self.order=self.sell(size=stock)
                self.log('卖出')


    # def __init__(self):
    #     sma1 = bt.ind.SMA(period = self.p.pfast)
    #     sma2 = bt.ind.SMA(period = self.p.pslow)
    #     self.crossover = bt.ind.CrossOver(sma1, sma2)
    #     self.dataclose = self.datas[0].close
    #     self.order = None

    # def next(self):
    #     if not self.position:
    #         if self.crossover > 0:
    #             cash = self.broker.get_cash()
    #             stock = math.ceil(cash/self.dataclose/100)*100 - 100
    #             self.order = self.buy(size = stock, price = self.datas[0].close)
    #             self.log("买入")
    #     elif self.crossover < 0:
    #         self.order = self.close()
    #         self.log("卖出")

if __name__=='__main__':
    start = "2018-01-01"
    end = "2020-07-05"
    name = ["300etf"]
    code = ["600030"]
    backtest = A_CommBackTraderClass.BackTest(ShuangJunXian, start, end, code, name)
    backtest.run()
    backtest.output()