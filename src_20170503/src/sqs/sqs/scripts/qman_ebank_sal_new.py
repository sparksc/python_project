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
客户经理电子绩效佣金
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
              SELECT DATE_ID,ORG_CODE,ORG_NAME,SALE_CODE,SALE_NAME, NVL(sum(MB_ADD_NUM_SAL)/100.00,0),NVL(sum(CB_ADD_NUM_SAL)/100.00,0),NVL(SUM(EPAY_ADD_NUM_SAL)/100.00,0),NVL(SUM(ADD_HIGH_POS_SAL)/100.00,0),NVL(SUM(ADD_LOW_POS_SAL)/100.00,0),NVL(SUM(FARM_SERV_SAL)/100.00,0),NVL(SUM(EPAY_ADD_NUM_SAL+MB_ADD_NUM_SAL+CB_ADD_NUM_SAL+ADD_HIGH_POS_SAL+ADD_LOW_POS_SAL+FARM_SERV_SAL)/100.00,0) 
              FROM  REPORT_MANAGER_OTHER WHERE 1=1 %s
              GROUP BY DATE_ID,ORG_CODE,SALE_CODE,SALE_NAME,ORG_NAME order by SALE_CODE 
            """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print sql
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i[0:5])
            for j in i[5:]:
                if j is None:j=0
                j=self.amount_trans_dec(j)
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
            #    if bb != False :
            #        filterstr = filterstr+" and ORG_CODE in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'SALE_CODE','ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return ["统计日期","机构编号","机构名称","员工编号","员工姓名","新增手机银行有效户数效酬","新增企业网银有效户数效酬","新增有效丰收e支付效酬","新增(高扣率)POS机效酬","新增(抵扣率)POS效酬","助农服务点效酬","电子银行总效酬"]

    @property
    def page_size(self):
        return 15
