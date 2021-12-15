# coding:utf-8
# 量化交易回测类


import backtrader as bt
import backtrader.analyzers as btay
import tushare as ts
import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import baostock as bs


# 回测类
class BackTest:
    def __init__(self, strategy, start, end, code, name):
        self.__cerebro = None
        self.__strategy = strategy
        self.__start = start
        self.__end = end
        self.__code = code
        self.__name = name
        self.__result = None
        self.__commission = 0.0003
        self.__initcash = 100000
        self.__backtestResult = pd.Series()
        self.__returns = pd.Series()
        self.init()
        
    # 真正进行初始化的地方
    def init(self):
        self.__cerebro = bt.Cerebro()
        self.__cerebro.addstrategy(self.__strategy)
        self.settingCerebro()
        self.createDataFeeds()
        plt.switch_backend('agg')
        
    # 设置cerebro
    def settingCerebro(self):
        # 添加回撤观察器
        self.__cerebro.addobserver(bt.observers.DrawDown)
        # 设置手续费
        self.__cerebro.broker.setcommission(commission=self.__commission)
        # 设置初始资金为0.01
        self.__cerebro.broker.setcash(self.__initcash)
        # 添加分析对象
        self.__cerebro.addanalyzer(btay.SharpeRatio, _name = "sharpe", riskfreerate = 0.02)
        self.__cerebro.addanalyzer(btay.AnnualReturn, _name = "AR")
        self.__cerebro.addanalyzer(btay.DrawDown, _name = "DD")
        self.__cerebro.addanalyzer(btay.Returns, _name = "RE")
        self.__cerebro.addanalyzer(btay.TradeAnalyzer, _name = "TA")
        
    # 建立数据源
    def createDataFeeds(self):
        for i in range(len(self.__code)):
            df_data = self._getData(self.__code[i])
            self.__cerebro.adddata(df_data, name = self.__name[i])
            
    # 获取账户总价值
    def getValue(self):
        return self.__cerebro.broker.getvalue()
        
    # 执行回测
    def run(self):
        self.__backtestResult["期初账户总值"] = self.getValue()
        self.__results = self.__cerebro.run()
        self.__backtestResult["期末账户总值"] = self.getValue()
        # self._Result()
        return self.getResult()
        
    # 输出回测结果
    def output(self):
        print("期初账户总值:", self.__backtestResult["期初账户总值"])
        print("期末账户总值:", self.__backtestResult["期末账户总值"])
        print("夏普比例:", self.__results[0].analyzers.sharpe.get_analysis()["sharperatio"])
        print("年化收益率:", self.__results[0].analyzers.AR.get_analysis())
        print("最大回撤:%.2f，最大回撤周期:%d" % (self.__results[0].analyzers.DD.get_analysis().max.drawdown, self.__results[0].analyzers.DD.get_analysis().max.len))
        print("总收益率:%.2f" % (self.__results[0].analyzers.RE.get_analysis()["rtot"]))
        self.__results[0].analyzers.TA.print()


        self.__cerebro.plot()
        plt.savefig("result.png")



    # 计算并保存回测结果指标
    def _Result(self):
        self.__backtestResult["账户总额"] = self.getValue()
        self.__backtestResult["总收益率"] = self.__results[0].analyzers.RE.get_analysis()["rtot"]
        self.__backtestResult["年化收益率"] = self.__results[0].analyzers.RE.get_analysis()["rnorm"]
        self.__backtestResult["夏普比率"] = self.__results[0].analyzers.sharpe.get_analysis()["sharperatio"]
        self.__backtestResult["最大回撤"] = self.__results[0].analyzers.DD.get_analysis().max.drawdown
        self.__backtestResult["最大回撤期间"] = self.__results[0].analyzers.DD.get_analysis().max.len
        # 计算胜率信息
        self._winInfo()

    # 计算胜率信息
    def _winInfo(self):
        trade_info = self.__results[0].analyzers.TA.get_analysis()
        total_trade_num = trade_info["total"]["total"]
        win_num = trade_info["won"]["total"]
        lost_num = trade_info["lost"]["total"]
        self.__backtestResult["交易次数"] = total_trade_num
        self.__backtestResult["胜率"] = win_num/total_trade_num
        self.__backtestResult["败率"] = lost_num/total_trade_num
 
 
    # 获取回测指标
    def getResult(self):
        return self.__backtestResult



    # 获取数据
    def _getData(self, code):
        lg=bs.login()
        print('登录 code:'+lg.error_code)
        print('登录 msg:'+lg.error_msg)

        strCode='sh.'+code
        begDate=self.__start
        endDate=self.__end
        rs=bs.query_history_k_data_plus(strCode,"date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus",start_date=begDate,end_date=endDate,frequency='d',adjustflag="1")
        dataframe=rs.get_data()
        dataframe=dataframe.apply(pd.to_numeric,axis=0,errors='ignore')
        dataframe=dataframe[dataframe.tradestatus==1]
        dataframe['date']=pd.to_datetime(dataframe['date'])

        data =bt.feeds.PandasData(
            dataname=dataframe,
            datetime='date',  # 日期列   
            open=2,  # 开盘价所在列
            high=3,  # 最高价所在列
         low=4,  # 最低价所在列
         close=5,  # 收盘价价所在列
         volume=7,  # 成交量所在列
         openinterest=-1,  # 无未平仓量列.(openinterest是期货交易使用的)
         fromdate=pd.to_datetime(begDate),  # 起始日
         todate=pd.to_datetime(endDate)  # 结束日    
         )
        bs.logout()
        return data