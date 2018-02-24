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
        self.filterlist = ['org_no', 'kyear']
        filterstr,vlist = self.make_eq_filterstr()
        sql = u"""
        SELECT OP.KYEAR,OP.ORG_NO,B.BRANCH_NAME,OP.PEO_COUNT,OP.REMARKS,OP.ID 
        FROM ORG_PEO_COUNT OP JOIN BRANCH B ON B.BRANCH_CODE=OP.ORG_NO 
        WHERE 1=1 %s  ORDER BY OP.KYEAR,OP.ORG_NO
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
                    filterstr = filterstr + "and op.org_no in(%s) "%(vvv)
                else:
                    filterstr = filterstr + "and %s=?"%k
                    vlist.append(v)
        
        filterstr = "%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'op.org_no',None))
       
        return filterstr, vlist
    def column_header(self):
        return ["所属年份","机构号","机构名称","网点人数","备注","操作"]

    @property
    def page_size(self):
        return 10

