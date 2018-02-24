# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['org_no', 'kyear', 'user_name']
        filterstr,vlist = self.make_eq_filterstr()
        sql = u"""
        SELECT BG.KYEAR, BR.BRANCH_CODE, BR.BRANCH_NAME, 
        BG.AVE_DBAL_YEAR,BG.AVE_DBAL_YEAR_SCORE, BG.AVE_DBAL_YEAR_WEIGHT, BG.AVE_DBAL_YEAR_WSCORE, 
        BG.AVE_DLOAN,BG.AVE_DLOAN_SCORE, BG.AVE_DLOAN_WEIGHT, BG.AVE_DLOAN_WSCORE, 
        BG.AVE_DLOAN_YEAR,BG.AVE_DLOAN_YEAR_SCORE, BG.AVE_DLOAN_YEAR_WEIGHT, BG.AVE_DLOAN_YEAR_WSCORE, 
        BG.AVE_PROFIT_YEAR,BG.AVE_PROFIT_YEAR_SCORE, BG.AVE_PROFIT_YEAR_WEIGHT, BG.AVE_PROFIT_YEAR_WSCORE, 
        BG.INCOME_YEAR,BG.INCOME_YEAR_SCORE, BG.INCOME_YEAR_WEIGHT, BG.INCOME_YEAR_WSCORE, 
        BG.INTER_SET,BG.INTER_SET_SCORE, BG.INTER_SET_WEIGHT, BG.INTER_SET_WSCORE, 
        BG.EBANK_ACCOUNT_NUM,BG.EBANK_ACCOUNT_NUM_SCORE, BG.EBANK_ACCOUNT_NUM_WEIGHT, BG.EBANK_ACCOUNT_NUM_WSCORE, 
        BG.CREDIT_CARD_NUM,BG.CREDIT_CARD_NUM_SCORE, BG.CREDIT_CARD_NUM_WEIGHT, BG.CREDIT_CARD_NUM_WSCORE,
        BG.LOAN_NUM,BG.LOAN_NUM_SCORE, BG.LOAN_NUM_WEIGHT, BG.LOAN_NUM_WSCORE,
        BG.EBANK_SUB_RATE,BG.EBANK_SUB_RATE_SCORE, BG.EBANK_SUB_RATE_WEIGHT, BG.EBANK_SUB_RATE_WSCORE,
        BG.BRANCH_AVE_HOOK,BG.BRANCH_AVE_HOOK_SCORE, BG.BRANCH_AVE_HOOK_WEIGHT, BG.BRANCH_AVE_HOOK_WSCORE,
        BG.FOR_GRAD_BAD_RATE,BG.FOR_GRAD_BAD_RATE_SCORE, BG.FOR_GRAD_BAD_RATE_WEIGHT, BG.FOR_GRAD_BAD_RATE_WSCORE,
        BG.TOTAL_SCORE, BG.SYS_GRADE, BG.ADJ_GRADE, BG.GRADE, BG.ID 
        FROM BRANCH_GRADE BG
        JOIN BRANCH BR ON BR.BRANCH_CODE = BG.ORG_NO
        WHERE 1=1 %s  ORDER BY BG.KYEAR DESC,BG.ID
        """%(filterstr)

        print sql
        row = self.engine.execute(sql, vlist).fetchall()
        needtrans = {}
        return self.translate(row, needtrans)

    def make_eq_filterstr(self):
        filterstr = ""
        vlist = []
        for k, v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org_no':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr + "and org_no in(%s)"%(vvv)
                else:
                    filterstr = filterstr + "and bg.%s = ?"%k
                    vlist.append(v)
        
        filterstr = "%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'bg.org_no',None))
       
        return filterstr, vlist
    def column_header(self):
        return [
            [{'name':'统计年份','h':2},{'name':'机构编号','h':2},{'name':'机构名称','h':2},{'name':'年度日均存款总量（亿元）','w':4},{'name':'人均日均存款量（万元）','w':4},{'name':'年度日均贷款总量（亿元）','w':4},{'name':'年度人均利润（万元）','w':4},{'name':'年度营业收入（亿元）','w':4},{'name':'国际结算量（万美元）','w':4},{'name':'电子银行开户数（户）','w':4},{'name':'贷记卡发卡量（张）','w':4},{'name':'贷款户数（户）','w':4},{'name':'电子银行替代率（%）','w':4},{'name':'支行贷款户日均存贷挂钩率（%）','w':4},{'name':'四级不良贷款率（%）','w':4},{'name':'综合等级值','h':2},{'name':'系统测算管理等级','h':2},{'name':'调整后等级','h':2},{'name':'管理等级','h':2},{'name':'操作','h':2}],
            [{'name':'实绩','h':1},{'name':'等级','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'等级','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'等级','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'等级','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'等级','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'等级','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'等级','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'等级','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'等级','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'等级','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'等级','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'等级','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1}]
        ]

    @property
    def page_size(self):
        return 10

