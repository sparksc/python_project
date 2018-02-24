# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config
"""
客户经理附加绩效佣金报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT SYEAR, SMOUTH, ORG_CODE, ORG_NAME, STAFF_CODE, STAFF_NAME, sum(SCORE/100.00) FROM YDW.M_MANAGER_ADD_SCO WHERE TYP='佣金' %s group by SYEAR, SMOUTH, ORG_CODE, ORG_NAME, STAFF_CODE, STAFF_NAME order by SYEAR,SMOUTH desc"""%(filterstr)

        row = self.engine.execute(sql).fetchall()
        print sql
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i)
            if t[6] is None:t[6]=0
            t[6]=self.amount_trans_dec(t[6])
            rowlist.append(t)
        return self.translate(rowlist,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            #if k == 'login_teller_no':
            #    if self.deal_teller_query_auth(v) == True:
            #        filterstr = filterstr+" and STAFF_CODE = '%s'"%v
            #elif k == 'login_branch_no':
            #    bb = self.deal_branch_query_auth(v)
            #    if bb != False :
            #        filterstr = filterstr+" and ORG_CODE in ( %s )"%bb
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                elif k=='DATE_ID':
                    v1=v[:4]
                    v2=v[4:]
                    filterstr=filterstr+" and  SYEAR= '%s' and SMOUTH='%s'"%(v1,v2)
                elif k=='SALE_CODE':
                    filterstr=filterstr+" and STAFF_CODE='%s'"%v
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'STAFF_CODE','ORG_CODE', None))
        return filterstr,vlist
    def column_header(self):
        return ["统计年份","统计月份","机构号","机构名称","员工号","员工名称","附加效酬","操作"]

    @property
    def page_size(self):
        return 10
