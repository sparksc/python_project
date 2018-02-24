# -*- coding:utf-8 -*-
import sys
import datetime
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from utils import config
"""
客户经理信用卡业务绩效佣金报表
"""
class Query(ObjectQuery):
  
    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql=u"""
        select date_id,org_code,org_name,sale_code,sale_name,salary from REPORT_MANAGER_CREDITCARD
        where 1=1 %s
        order by date_id  desc
        """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print sql 
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
        return ["统计月份","机构号","机构名称","员工号","员工姓名","当月新增发卡量效酬"]
    
    @property
    def page_size(self):    
        return 15
