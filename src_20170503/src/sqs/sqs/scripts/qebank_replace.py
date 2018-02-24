# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from utils import config
"""
电子银行替代率手工维护
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE','BRANCH_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        print filterstr,vlist
        sql ="""
            select ern.date,ern.BRANCH_CODE,ern.BRANCH_NAME,ern.ATMBH,ern.ATMTDB,ern.ATMBDT,ern.ATM_TOTAL,ern.POSBH,ern.POSTDB,ern.POSBDT,ern.POS_TOTAL,ern.EBANK_INDI,ern.EBANK_ENTERPRISE,ern.EBANK_TOTAL,ern.CELLPHONE_BANK,ern.TELL_BANK,ern.MESS_BANK,ern.AUTO_BANK,ern.E_PAY,ern.ALIPAY_FIVE,ern.NUM1,ern.NUM2,ern.TERM_NUM,ern.REPLACE_NUM1,ern.REPLACE_NUM2,ern.REPLACE_AMOUNT1 ,ern.REPLACE_AMOUNT2 from ebank_replace_num ern where 1=1 %s
            """%(filterstr)
        print sql
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'DATE':
                    filterstr = filterstr + " and ern.date = ? "
                    vlist.append(v)
                if k == 'BRANCH_CODE':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr + " and ern.branch_code in ( %s ) " % (vvv)
        return filterstr,vlist

    def column_header(self):
        return ["日期","机构号","行社名称","ATM本行笔数","ATM他代本笔数","ATM本代他笔数","ATM笔数小计","POS本行笔数","POS他代本笔数","POS本代他笔数","POS笔数小计","个人网银笔数","企业网银笔数","网银笔数小计","手机银行笔数","电话银行笔数","短信银行笔数","自助终端笔数","电子支付笔数","支付宝、财付通单卡单日超过5笔的交易（T列）","电子渠道交易笔数1合计","电子渠道交易笔数2合计（剔除T列）","柜面渠道交易笔数","电子银行交易笔数替代率1","电子银行交易笔数替代率2","电子银行交易金额替代率1","电子银行交易金额替代率2"]
    @property
    def page_size(self):
        return 15
