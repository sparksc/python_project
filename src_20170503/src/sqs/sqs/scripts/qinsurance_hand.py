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
车险人保户数手工维护
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SYEAR','org','ORG_CODE','USER_CODE','CREDENTIAL_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select es.SYEAR,es.ORG_CODE,b.BRANCH_NAME,es.USER_CODE,fu.NAME,es.COUNTS,es.COUNTS_REMARKS,es.ID 
                from addharvest es,BRANCH b,F_USER fu 
                where b.BRANCH_CODE = es.ORG_CODE and fu.USER_NAME=es.USER_CODE %s order by es.SYEAR desc, es.ID
             """%(filterstr)
        print sql

        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        ''' 
        rowlist=[]
        for i in row:
            t=list(i)
            if t[3] is None:t[3]=0
            t[3]=self.amount_trans_dec(t[3])

            if t[4] is None:t[4]=0
            t[4]=self.amount_trans_dec(t[4])
            rowlist.append(t)
        '''
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        print self.args.items()
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and es.ORG_CODE in(%s) "%(vvv)
                else:
                    filterstr = filterstr+"and %s = ?"%k
                    vlist.append(v)           
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'es.USER_CODE','es.ORG_CODE', None))

        return filterstr,vlist
    def column_header(self):
        return ["年份","机构号","机构名称","员工号","员工名","推荐人保公司办理车险户数（户）","备注","操作"]
    @property
    def page_size(self):
        return 10
