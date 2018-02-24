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
柜员等级报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['syear','smonth','ORG_CODE','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        print u'',filterstr,vlist
        sql ="""
        select syear, smonth, ORG_CODE, ORG_NAME, REPORT_CREDITVILL_NUM, REMARK ,id from report_credit_villagnum where 1=1 %s order by syear,SMONTH, ORG_CODE
            """%(filterstr)
        print u'sql语句：',sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i)
            for j in range(3,len(i)-1):
                if t[j]==None:
                    t[j]=0
                if j==5:
                    t[j]=""
            rowlist.append(t)
        return self.translate(rowlist,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            print k,v
            if v and k in self.filterlist:
                if k == 'ORG_CODE':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr+"and ORG_CODE in (%s)"%(vvv)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'SALE_CODE','ORG_CODE', None))
        print u'',filterstr,vlist
        return filterstr,vlist  
    def column_header(self):
        return ['年份','月份','机构号','机构名称','报告期已整村授信个数','备注','操作']
    @property
    def page_size(self):
        return 10
