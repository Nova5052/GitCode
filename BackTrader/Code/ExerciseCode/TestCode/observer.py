from datetime import datetime
from os import close
import backtrader as bt
import os.path  # 管理路径
import sys
from backtrader import errors
from backtrader import comminfo
from backtrader.feeds.pandafeed import PandasData  # 发现脚本名字(in argv[0])
import baostock as bs
import pandas as pd
from ChineseCommission import chineseCommission

from PrintFunction import printTradeAnalysis

class PandasData_PE(PandasData):
    lines=('pe',)
    params=(('pe',8),)


# 创建策略类
class SmaCross(bt.Strategy):
    # 定义参数
    params = dict(period=5  # 移动平均期数
                  )

    # 日志函数
    def log(self, txt, dt=None):
        '''日志函数'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # 订单状态 submitted/accepted，无动作
            return

        # 订单完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('买单执行, %.2f' % order.executed.price)

            elif order.issell():
                self.log('卖单执行, %.2f' % order.executed.price)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单 Canceled/Margin/Rejected')



    # 记录交易收益情况（可省略，默认不输出结果）
    def notify_trade(self, trade):
        if trade.isclosed:
            print('毛收益 %0.2f, 扣佣后收益 % 0.2f, 佣金 %.2f' %
                  (trade.pnl, trade.pnlcomm, trade.commission))

    def __init__(self):
        # 移动平均线指标
        self.move_average = bt.ind.MovingAverageSimple(
            self.data, period=self.params.period)

        # 交叉信号指标
        self.crossover = bt.ind.CrossOver(self.data, self.move_average)

    def next(self):

        if not self.position:  # 还没有仓位
            # 当日收盘价上穿5日均线，创建买单，买入100股
            if self.crossover > 0:
                self.log('创建买单')
                self.buy(size=100)
        # 有仓位，并且当日收盘价下破5日均线，创建卖单，卖出100股
        elif self.crossover < 0:
            self.log('创建卖单')
            self.sell(size=100)



##########################
# 主程序开始
#########################

# 创建大脑引擎对象
cerebro = bt.Cerebro(stdstats=False)
cerebro.addobserver(bt.observers.DrawDown)
cerebro.addobserver(bt.observers.Trades)


####登录系统###
lg=bs.login()
print('error_code:'+lg.error_code)
print('error_msg'+lg.error_msg)

rs=bs.query_history_k_data_plus("sh.600000","date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus",start_date='2010-01-01',end_date='2021-10-16',frequency='d',adjustflag="1")


dataframe=rs.get_data()
dataframe=dataframe.apply(pd.to_numeric,axis=0,errors='ignore')
dataframe=dataframe[dataframe.tradestatus==1]
dataframe['date']=pd.to_datetime(dataframe['date'])

data = PandasData_PE(
    dataname=dataframe,
    datetime='date',  # 日期列   
    open=2,  # 开盘价所在列
    high=3,  # 最高价所在列
    low=4,  # 最低价所在列
    close=5,  # 收盘价价所在列
    volume=7,  # 成交量所在列
    openinterest=-1,  # 无未平仓量列.(openinterest是期货交易使用的)
    fromdate=datetime(2020, 1, 1),  # 起始日
    todate=datetime(2021, 10, 16)  # 结束日    
)

cerebro.adddata(data)  # 将行情数据对象注入引擎
cerebro.addstrategy(SmaCross)  # 将策略注入引擎

cerebro.broker.setcash(10000.0)  # 设置初始资金

#自定义佣金
comminfo1=chineseCommission(stamp_duty=0.05,commission=0.01)
cerebro.broker.addcommissioninfo(comminfo1)
#cerebro.broker.setcommission(0.001)  # 佣金费率
# 固定滑点，也可用cerebro.broker.set_slippage_perc()设置百分比滑点
cerebro.broker.set_slippage_fixed(0.05)


print('初始市值: %.2f' % cerebro.broker.getvalue())
thestrats = cerebro.run()  # 运行
thestrat=thestrats[0]
print('最终市值: %.2f' % cerebro.broker.getvalue())



cerebro.plot()