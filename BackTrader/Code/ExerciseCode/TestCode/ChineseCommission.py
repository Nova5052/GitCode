import backtrader as bt

class chineseCommission(bt.CommInfoBase):
    params=(
        ('stamp_duty',0.005),
        ('percabs',True),
    )

    def _getcommission(self,size,price,pseudoexec):
        if size>0:
            return size*price*self.p.commission
        elif size<0:
            return -size*price*(self.p.stamp_duty+self.p.commission)
        else:
            return 0