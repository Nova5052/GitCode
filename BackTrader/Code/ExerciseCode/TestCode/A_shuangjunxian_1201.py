# coding:utf-8
# 双均线策略实现


import backtrader as bt
import A_CommBackTraderClass
import math
import pandas as pd
import matplotlib.pyplot as plt


# 双均线策略类
class SmaCross(bt.Strategy):
    params = dict(
            pfast = 5,
            pslow = 14
    )
    
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    

    def __init__(self):
        sma1=bt.ind.SMA(period=self.params.pfast)
        sma2=bt.ind.MovingAverageSimple(period=self.params.pslow)
        self.crossover=bt.ind.CrossOver(sma1,sma2)
        self.dataclose=self.datas[0].close
        self.order=None

    def next(self):
        if not self.position:
            if self.crossover>0:
                cash=self.broker.get_cash()
                price=self.datas[0].close[0]
                stock=math.ceil(cash/price/100)*100-100
                print('数量:',stock)
                self.order = self.buy(size = stock, price = self.datas[0].close)
                self.log('买入')
        elif self.crossover < 0:
            self.order = self.close()
            self.log("卖出")
            
            
# 基准策略类，用于计算α，β等回测指标
# 采用第一天全仓买入并持有的策略
class Benchmark(bt.Strategy):
    def __init__(self):
        self.order = None
        self.bBuy = False
        self.dataclose = self.datas[0].close
        
    def next(self):
        if self.bBuy == True:
            return
        else:
            cash = self.broker.get_cash()
            stock = math.ceil(cash/self.dataclose/100)*100 - 100
            self.order = self.buy(size = stock, price = self.datas[0].close)
            self.bBuy = True
            
    def stop(self):
        self.order = self.close()


if __name__ == "__main__":
    start = "2018-01-01"
    end = "2022-01-01"
    name = ["nasetf"]
    code = ["600030"]
    backtest = A_CommBackTraderClass.BackTest(SmaCross, start, end, code, name, 10000)
    result = backtest.run()
    # print(result)
    # backtest.output()

    # result = backtest.optRun(pslow = range(13, 16))
    # print(result)
    # plt.figure()
    # plt.plot(result.年化收益率)
    # plt.savefig("SmaCross参数优化.png")