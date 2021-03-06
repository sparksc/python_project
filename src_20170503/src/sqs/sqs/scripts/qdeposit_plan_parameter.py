# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config
"""
存款业务计划数参数
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['BE_YEAR','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT P.DBYEAR,P.THIRD_ORG_CODE,B.BRANCH_NAME,P.MANAGER_CODE,F.NAME,P.BASE/100.00,P.TARGET/100.00,P.ID FROM P_DEP_NUM as P join BRANCH as B on  P.THIRD_ORG_CODE = B.BRANCH_CODE join F_USER as F on P.MANAGER_CODE=F.USER_NAME
        WHERE 1=1  %s
        ORDER BY DBYEAR,ID"""%(filterstr)


        
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        i=0
        rowlist=[]

        for i in row:
            t = list(i[0:5])
            for j in i[5:]:
                if j is None: j=0
                j = self.amount_trans_dec(j)
                t.append(j)
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            print k,v

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr+" and THIRD_ORG_CODE in ( %s) "%(vvv)
                elif k=='BE_YEAR':
                    if v != '':
                        filterstr = filterstr+" and DBYEAR = '%s'"%v
                elif k=='SALE_CODE':
                    if v !='':
                        filterstr = filterstr+" and MANAGER_CODE = '%s'"%v
        filterstr = "%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'MANAGER_CODE','THIRD_ORG_CODE',None))
 
        print filterstr,vlist
        return filterstr,vlist
    def column_header(self):
        return ["所属年份","网点编号","网点名称","客户经理编号","客户经理名称","考核基数","目标任务","操作"]

    @property
    def page_size(self):
        return 15
