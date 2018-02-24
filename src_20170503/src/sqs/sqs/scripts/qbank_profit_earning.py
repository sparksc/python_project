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
支行年度利润和年度营业收入手工维护
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SYEAR','ORG_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT SYEAR, ORG_CODE,BRANCH_NAME, YEAR_PROFIT, YEAR_EARNING, ID FROM bank_pe_input,branch WHERE 1=1 and branch_code=org_code %s order by syear desc,id"""%(filterstr)
        print sql

        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        
        rowlist=[]
        for i in row:
            t=list(i)
            if t[3] is None:t[3]=0
            t[3]=self.amount_trans_dec(t[3])

            if t[4] is None:t[4]=0
            t[4]=self.amount_trans_dec(t[4])
            rowlist.append(t)
        
        return self.translate(rowlist,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        print self.args.items()
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'ORG_CODE':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr+"and ORG_CODE in(%s)"%(vvv)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)

        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'ORG_CODE', None))

        return filterstr,vlist
    def column_header(self):
        return ["年份","机构号","机构名称","年度利润/万元","年度营业收入/亿元","操作"]

    @property
    def page_size(self):
        return 10
