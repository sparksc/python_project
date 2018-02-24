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
信用卡不良报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        self.date_id=''
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        SELECT A.DATE_ID, A.ORG_CODE, A.SALE_CODE, A.SALE_NAME, ROUND((CASE  WHEN NVL(A.ALL_BAL,0) = 0 AND  NVL(A.PPL_BAL,0) = 0 THEN 0 ELSE A.BAD_BAL*1.0/ (NVL(A.ALL_BAL,0) + NVL(A.PPL_BAL,0)) END)*100,2)
        FROM YDW.REPORT_CREDIT_BAD A
        where 1=1 %s
        ORDER BY ORG_CODE,SALE_CODE
            """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print sql
        print filterstr
        print vlist
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i[0:4])
            for j in i[4:]:
                if j is None:j=0
                j=self.trans_dec(j)
                t.append(j)
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and A.ORG_CODE in ( %s ) "%(vvv)
                elif k=='DATE_ID':
                    filterstr = filterstr +" and A.DATE_ID =  ?  "
                    self.date_id='%s'%(v)
                    vlist.append(v)
                elif k=='SALE_CODE':
                    filterstr = filterstr +" and A.SALE_CODE =  ?  "
                    vlist.append(v)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'A.SALE_CODE','A.ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return ["统计日期","机构号","员工号","员工姓名","不良率(%)"]

    def trans_dec(self,num):
        tmp = num
        #tmp = '{:,}'.format(tmp)
        return tmp

    @property
    def page_size(self):
        return 15
