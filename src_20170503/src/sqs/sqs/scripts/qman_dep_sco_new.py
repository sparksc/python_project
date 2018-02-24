# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from utils import config
"""
客户经理存款得分
"""

class Query(ObjectQuery):
 
    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql="""
        SELECT DATE_ID,ORG_CODE,ORG_NAME,SALE_CODE,SALE_NAME,DEP_SCORE/100.00 FROM REPORT_MANAGER_DEP 
        where 1=1 %s
        ORDER BY DATE_ID,ORG_CODE,SALE_CODE
        """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print sql 
        needtrans ={}
        i=0
        rowlist=[]
        if len(row) == 0:
            year=None
            month=None
        else:
            year=str(row[0][0])[:4]
            month=str(row[0][0])[4:6]
            print year,month
        for i in row:
            t = list(i[0:5])
            for j in i[5:]:
                if j is None:j=0
                j = round(j,2)
                t.append(j)
                t.append(j)
            #t.insert(0,month)
            #t.insert(0,year)
            rowlist.append(t)
        return self.translate(rowlist,needtrans)


    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        global ymday
        for k,v in self.args.items():
            print k,v
            #if k == 'login_teller_no':
            #    if self.deal_teller_query_auth(v) == True:
            #        filterstr = filterstr+" and SALE_CODE = '%s'"%v
            #elif k == 'login_branch_no':
            #    bb = self.deal_branch_query_auth(v)
            #    if bb != False:
            #        filterstr = filterstr+" and ORG_CODE in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr+" and ORG_CODE in ( %s) "%(vvv)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
            
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'SALE_CODE','ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return ["统计时间","机构号","机构名称","员工号","员工名称","新增日均存款得分","存款绩效得分"]
    @property
    def page_size(self):
        return 15
