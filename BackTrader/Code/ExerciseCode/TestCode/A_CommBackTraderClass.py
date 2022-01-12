# coding:utf-8
# 量化交易回测类

import backtrader as bt
import backtrader.analyzers as btay
import tushare as ts
import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import empyrical as ey
import math
import tushare as ts
import numpy as np
from scipy import stats
from backtrader.utils.py3 import map
from backtrader import Analyzer, TimeFrame
from backtrader.mathsupport import average, standarddev
from backtrader.analyzers import AnnualReturn
import operator
from pathlib import Path
import A_PrintFunction


# 回测类
class BackTest:
    def __init__(self, strategy, start, end, code, name, cash=0.01, commission=0.0003, benchmarkCode="510300",
                 bDraw=True):
        self.__cerebro = None
        self.__strategy = strategy  # 策略实体
        self.__startDate = start  # 数据查询开始日期
        self.__endDate = end  # 数据查询结束日期
        self.__code = code  # 股票代码
        self.__name = name
        self.__result = None
        self.__commission = commission
        self.__initcash = cash
        self.__backtestResult = pd.Series()
        self.__returns = pd.Series()
        self.__benchmarkCode = benchmarkCode
        self.__benchReturns = pd.Series()
        self.__benchFeed = None
        self.__bDraw = bDraw
        self._init()

    # 真正进行初始化的地方
    def _init(self):
        self.__cerebro = bt.Cerebro()
        self.__cerebro.addstrategy(self.__strategy)
        self._createDataFeeds()
        self._settingCerebro()
        plt.switch_backend('agg')

    # 执行回测
    def run(self):
        self.__backtestResult["期初账户总值"] = self.getValue()
        self.__results = self.__cerebro.run()
        self.__backtestResult["期末账户总值"] = self.getValue()

        aResult = self.__results[0]
        A_PrintFunction.printTradeAnalysis(self.__cerebro, aResult.analyzers)

        self._Result()
        if self.__bDraw == True:
            self._drawResult()
        self.__returns = self._timeReturns(self.__results)
        self.__benchReturns = self._getBenchmarkReturns(self.__results)
        self._riskAnaly(self.__returns, self.__benchReturns, self.__backtestResult)
        return self.getResult()

    # 执行参数优化的回测
    def optRun(self, *args, **kwargs):
        self._optStrategy(*args, **kwargs)
        results = self.__cerebro.run()
        if len(kwargs) == 1:
            testResults = self._optResult(results, **kwargs)
        elif len(kwargs) > 1:
            testResults = self._optResultMore(results, **kwargs)
        self._init()
        return testResults

    # 进行参数优化
    def _optStrategy(self, *args, **kwargs):
        self.__cerebro = bt.Cerebro(maxcpus=1)
        self.__cerebro.optstrategy(self.__strategy, *args, **kwargs)
        self._createDataFeeds()
        self._settingCerebro()

    # 获取账户总价值
    def getValue(self):
        return self.__cerebro.broker.getvalue()

    # 获取回测指标
    def getResult(self):
        return self.__backtestResult

    # 获取策略及基准策略收益率的序列
    def getReturns(self):
        return self.__returns, self.__benchReturns

    # # 输出回测结果
    # def output(self):
    #     print("夏普比例:", self.__results[0].analyzers.sharpe.get_analysis()["sharperatio"])
    #     print("年化收益率:", self.__results[0].analyzers.AR.get_analysis())
    #     print("最大回撤:%.2f，最大回撤周期%d" % (self.__results[0].analyzers.DD.get_analysis().max.drawdown,
    #     self.__results[0].analyzers.DD.get_analysis().max.len))
    #     print("总收益率:%.2f" % (self.__results[0].analyzers.RE.get_analysis()["rtot"]))
    #     # self.__results[0].analyzers.TA.pprint()

    # 设置cerebro
    def _settingCerebro(self):
        # 添加回撤观察器
        self.__cerebro.addobserver(bt.observers.DrawDown)
        # 添加基准观察器
        self.__cerebro.addobserver(bt.observers.Benchmark, data=self.__benchFeed, timeframe=bt.TimeFrame.NoTimeFrame)
        # 设置手续费
        self.__cerebro.broker.setcommission(commission=self.__commission)
        # 设置初始资金
        self.__cerebro.broker.setcash(self.__initcash)
        # 添加分析对象
        self.__cerebro.addanalyzer(btay.SharpeRatio, _name="sharpe", riskfreerate=0.02, stddev_sample=True,
                                   annualize=True)
        self.__cerebro.addanalyzer(btay.AnnualReturn, _name="AR")
        self.__cerebro.addanalyzer(btay.DrawDown, _name="DD")
        self.__cerebro.addanalyzer(btay.Returns, _name="RE")
        self.__cerebro.addanalyzer(btay.TradeAnalyzer, _name="TA")
        self.__cerebro.addanalyzer(btay.TimeReturn, _name="TR")
        self.__cerebro.addanalyzer(btay.TimeReturn, _name="TR_Bench", data=self.__benchFeed)
        self.__cerebro.addanalyzer(btay.SQN, _name="SQN")

    # 建立数据源
    def _createDataFeeds(self):
        # 建立回测数据源
        for i in range(len(self.__code)):
            dataFeed = self._createDataFeedsProcess(self.__code[i], self.__name[i])
            self.__cerebro.adddata(dataFeed, name=self.__name[i])  # 向大脑添加数据
        self.__benchFeed = self._createDataFeedsProcess(self.__benchmarkCode, "benchMark")
        self.__cerebro.adddata(self.__benchFeed, name="benchMark")

    # 建立数据源的具体过程
    def _createDataFeedsProcess(self, code, name):
        df_data = self._getData(code)
        dataFeed = bt.feeds.PandasData(dataname=df_data, name=name, fromdate=pd.to_datetime(self.__startDate),
                                       todate=pd.to_datetime(self.__endDate))
        return dataFeed

        # 从 tushare 获取数据

    def _getData(self, code):
        filename = code + ".csv"
        path = "./data/"
        # 如果数据目录不存在，创建目录
        if not os.path.exists(path):
            os.makedirs(path)
        # 已有数据文件，直接读取数据
        if os.path.exists(path + filename):
            df = pd.read_csv(path + filename)
        else:  # 没有数据文件，用tushare下载
            df = ts.get_k_data(code, autype="qfq", start=self.__startDate, end=self.__endDate)
            df.to_csv(path + filename)
        df.index = pd.to_datetime(df.date)
        df['openinterest'] = 0
        df = df[['open', 'high', 'low', 'close', 'volume', 'openinterest']]
        return df

    # region
    # # 从baostock获取数据 并直接返回 datefeed
    # def _getData(self, code):
    #     lg=bs.login()
    #     print('登录 code:'+lg.error_code)
    #     print('登录 msg:'+lg.error_msg)

    #     strCode='sh.'+code
    #     begDate=self.__start
    #     endDate=self.__end
    #     rs=bs.query_history_k_data_plus(strCode,"date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus",start_date=begDate,end_date=endDate,frequency='d',adjustflag="1")
    #     dataframe=rs.get_data()
    #     dataframe=dataframe.apply(pd.to_numeric,axis=0,errors='ignore')
    #     dataframe=dataframe[dataframe.tradestatus==1]
    #     dataframe['date']=pd.to_datetime(dataframe['date'])

    #     data =bt.feeds.PandasData(
    #         dataname=dataframe,
    #         datetime='date',  # 日期列   
    #         open=2,  # 开盘价所在列
    #         high=3,  # 最高价所在列
    #      low=4,  # 最低价所在列
    #      close=5,  # 收盘价价所在列
    #      volume=7,  # 成交量所在列
    #      openinterest=-1,  # 无未平仓量列.(openinterest是期货交易使用的)
    #      fromdate=pd.to_datetime(begDate),  # 起始日
    #      todate=pd.to_datetime(endDate)  # 结束日    
    #      )
    #     bs.logout()
    #     return data

    # endregion

    # 计算胜率信息
    def _winInfo(self, trade_info, result):
        total_trade_num = trade_info["total"]["total"]
        if total_trade_num > 1:
            win_num = trade_info["won"]["total"]
            lost_num = trade_info["lost"]["total"]
            result["交易次数"] = total_trade_num
            result["胜率"] = win_num / total_trade_num
            result["败率"] = lost_num / total_trade_num

    # 根据SQN值对策略做出评估
    # 按照backtrader文档写的
    def _judgeBySQN(self, sqn):
        result = None
        if 1.6 <= sqn <= 1.9:
            result = "低于平均"
        elif 1.9 < sqn <= 2.4:
            result = "平均水平"
        elif sqn > 2.4 and sqn <= 2.9:
            result = "良好"
        elif sqn > 2.9 and sqn <= 5.0:
            result = "优秀"
        elif sqn > 5.0 and sqn <= 6.9:
            result = "卓越"
        elif sqn > 6.9:
            result = "大神?"
        else:
            result = "很差"
        self.__backtestResult["策略评价(根据SQN)"] = result
        return result

    # 计算并保存回测结果指标
    def _Result(self):
        self.__backtestResult["账户总额"] = self.getValue()
        self.__backtestResult["总收益率"] = self.__results[0].analyzers.RE.get_analysis()["rtot"]
        self.__backtestResult["年化收益率"] = self.__results[0].analyzers.RE.get_analysis()["rnorm"]
        # self.__backtestResult["交易成本"] = self.__cerebro.strats[0].getCommission()
        self.__backtestResult["夏普比率"] = self.__results[0].analyzers.sharpe.get_analysis()["sharperatio"]
        self.__backtestResult["最大回撤"] = self.__results[0].analyzers.DD.get_analysis().max.drawdown
        self.__backtestResult["最大回撤期间"] = self.__results[0].analyzers.DD.get_analysis().max.len
        self.__backtestResult["SQN"] = self.__results[0].analyzers.SQN.get_analysis()["sqn"]
        self._judgeBySQN(self.__backtestResult["SQN"])

        # # 计算胜率信息
        # trade_info = self.__results[0].analyzers.TA.get_analysis()
        # self._winInfo(trade_info, self.__backtestResult)

    # 取得优化参数时的指标结果
    def _getOptAnalysis(self, result):
        temp = dict()
        temp["总收益率"] = result[0].analyzers.RE.get_analysis()["rtot"]
        temp["年化收益率"] = result[0].analyzers.RE.get_analysis()["rnorm"]
        temp["夏普比率"] = result[0].analyzers.sharpe.get_analysis()["sharperatio"]
        temp["最大回撤"] = result[0].analyzers.DD.get_analysis().max.drawdown
        temp["最大回撤期间"] = result[0].analyzers.DD.get_analysis().max.len
        sqn = result[0].analyzers.SQN.get_analysis()["sqn"]
        temp["SQN"] = sqn
        temp["策略评价(根据SQN)"] = self._judgeBySQN(sqn)
        # trade_info = self.__results[0].analyzers.TA.get_analysis()
        # self._winInfo(trade_info, temp)
        return temp

    # 在优化多个参数时计算并保存回测结果
    def _optResultMore(self, results, **kwargs):
        testResults = pd.DataFrame()
        i = 0
        for key in kwargs:
            for value in kwargs[key]:
                temp = self._getOptAnalysis(results[i])
                temp["参数名"] = key
                temp["参数值"] = value
                # returns = self._timeReturns(results[i])
                # benchReturns = self._getBenchmarkReturns(results[i])
                # self._riskAnaly(returns, benchReturns, temp)
                testResults = testResults.append(temp, ignore_index=True)
            # testResults.set_index(["参数值"], inplace = True)
        return testResults

    # 在优化参数时计算并保存回测结果
    def _optResult(self, results, **kwargs):
        testResults = pd.DataFrame()
        params = []
        for k, v in kwargs.items():
            for t in v:
                params.append(t)
        i = 0
        for result in results:
            temp = self._getOptAnalysis(result)
            temp["参数名"] = k
            temp["参数值"] = params[i]
            i += 1
            # returns = self._timeReturns(result)
            # benchReturns = self._getBenchmarkReturns(result)
            # self._riskAnaly(returns, benchReturns, temp)
            testResults = testResults.append(temp, ignore_index=True)
        # testResults.set_index(["参数值"], inplace = True)
        return testResults

    # 计算收益率序列
    def _timeReturns(self, result):
        return pd.Series(result[0].analyzers.TR.get_analysis())

    # 运行基准策略，获取基准收益值
    def _getBenchmarkReturns(self, result):
        return pd.Series(result[0].analyzers.TR_Bench.get_analysis())

    # 分析策略的风险指标
    def _riskAnaly(self, returns, benchReturns, results):
        risk = riskAnalyzer(returns, benchReturns)
        result = risk.run()
        results["阿尔法"] = result["阿尔法"]
        results["贝塔"] = result["贝塔"]
        results["信息比例"] = result["信息比例"]
        results["策略波动率"] = result["策略波动率"]
        results["欧米伽"] = result["欧米伽"]
        # self.__backtestResult["夏普值"] = result["夏普值"]
        results["sortino"] = result["sortino"]
        results["calmar"] = result["calmar"]

    # 回测结果绘图
    def _drawResult(self):
        self.__cerebro.plot(numfigs=2)
        figname = type(self).__name__ + ".png"
        plt.savefig(figname)


# 用empyrical库计算风险指标
class riskAnalyzer:
    def __init__(self, returns, benchReturns, riskFreeRate=0.02):
        self.__returns = returns
        self.__benchReturns = benchReturns
        self.__risk_free = riskFreeRate
        self.__alpha = 0.0
        self.__beta = 0.0
        self.__info = 0.0
        self.__vola = 0.0
        self.__omega = 0.0
        self.__sharpe = 0.0
        self.__sortino = 0.0
        self.__calmar = 0.0

    def run(self):
        # 计算各指标
        self._alpha_beta()
        self._info()
        self._vola()
        self._omega()
        self._sharpe()
        self._sortino()
        self._calmar()
        result = pd.Series(dtype="float64")
        result["阿尔法"] = self.__alpha
        result["贝塔"] = self.__beta
        result["信息比例"] = self.__info
        result["策略波动率"] = self.__vola
        result["欧米伽"] = self.__omega
        result["夏普值"] = self.__sharpe
        result["sortino"] = self.__sortino
        result["calmar"] = self.__calmar
        return result

    def _alpha_beta(self):
        self.__alpha, self.__beta = ey.alpha_beta(returns=self.__returns, factor_returns=self.__benchReturns,
                                                  risk_free=self.__risk_free, annualization=1)

    def _info(self):
        self.__info = ey.excess_sharpe(returns=self.__returns, factor_returns=self.__benchReturns)

    def _vola(self):
        self.__vola = ey.annual_volatility(self.__returns, period='daily')

    def _omega(self):
        self.__omega = ey.omega_ratio(returns=self.__returns, risk_free=self.__risk_free)

    def _sharpe(self):
        self.__sharpe = ey.sharpe_ratio(returns=self.__returns, annualization=1)

    def _sortino(self):
        self.__sortino = ey.sortino_ratio(returns=self.__returns)

    def _calmar(self):
        self.__calmar = ey.calmar_ratio(returns=self.__returns)
