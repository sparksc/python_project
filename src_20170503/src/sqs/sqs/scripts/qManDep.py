# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
客户经理存款
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            SELECT DATE_ID,ORG_CODE,SALE_CODE, SALE_NAME, SUM(nvl(LAST_AVG,0)),SUM(nvl(FIN_LAST_AVG,0)),SUM(PRI_THIS_AVG), SUM(PUB_THIS_AVG), SUM(FIN_THIS_AVG), SUM(THIS_AVG), SUM(PRI_THIS_AVG-nvl(PRI_LAST_AVG,0)), SUM(PUB_THIS_AVG-nvl(PUB_LAST_AVG,0)),SUM(FIN_THIS_AVG-nvl(FIN_LAST_AVG,0)) ,SUM(THIS_AVG-nvl(LAST_AVG,0)),SUM(PRI_BAL),SUM(PUB_BAL),SUM(FIN_BAL),SUM(PRI_BAL+PUB_BAL+FIN_BAL)
            FROM YDW.REPORT_MANAGER_DEP
            WHERE 1=1 %s
            GROUP BY DATE_ID,ORG_CODE,SALE_CODE,SALE_NAME
            """%(filterstr)
#        暂时只展示表头
#        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        row=[]
        print sql
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
            if k == 'login_teller_no':
                if self.deal_teller_query_auth(v) == True:
                    filterstr = filterstr+" and SALE_CODE = '%s'"%v
            elif k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False :
                    filterstr = filterstr+" and ORG_CODE in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        return filterstr,vlist

    def column_header(self):
        return ["统计日期","机构号","机构名称","员工号","员工姓名","日均存款","日均存款存量","日均存款增量","日均派生存款","日均自营存款","日均理财","日均派生存款存量","日均自营存款存量","日均理财存量","日均自营存款增量","日均派生存款增量","日均理财增量","全行百元付息率基准值","客户经理百元付息率","日均存款效益"]

    def trans_dec(self,num):
        tmp = Decimal(num)/Decimal(100)
        tmp = '{:,}'.format(tmp)
        return tmp

    @property
    def page_size(self):
        return 15
