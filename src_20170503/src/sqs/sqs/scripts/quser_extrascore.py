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
员工附加分手工维护
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SYEAR','ORG_CODE','USER_CODE','CREDENTIAL_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
        select es.SYEAR,es.ORG_CODE,b.BRANCH_NAME,es.USER_CODE,fu.NAME,es.CREDENTIAL_CODE,d2.DETAIL_VALUE,es.REMARKS,es.ID 
        from USER_EXTRASCORE es,BRANCH b,F_USER fu,T_PARA_DETAIL d1,T_PARA_DETAIL d2 
        where b.BRANCH_CODE = es.ORG_CODE and fu.USER_NAME=es.USER_CODE and d1.PARA_ROW_ID=d2.PARA_ROW_ID and d2.DETAIL_KEY='credential_name'and d1.DETAIL_VALUE=es.CREDENTIAL_CODE %s 
        order by es.SYEAR desc, es.ID
        """%(filterstr)
        print sql

        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        print self.args.items()
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'ORG_CODE':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr+"and es.ORG_CODE in(%s)"%(vvv)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)           
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'es.USER_CODE','es.ORG_CODE', None))
        return filterstr,vlist
    def column_header(self):
        return ["年份","机构号","机构名称","员工号","员工姓名","证书编号","证书名称","备注","操作"]

    @property
    def page_size(self):
        return 10
