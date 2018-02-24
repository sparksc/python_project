# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from flask import current_app
"""
机构存款指标
"""
class Query(ObjectQuery):

    def group_by(self):
        return [0],(4,5,6,7,8,9,10,11)
    def exp_str(self):
        return None
    def prepare_object(self):
        self.filterlist = ['DATE_ID','org']
        filterstr,vlist = self.make_eq_filterstr()
        sql = """
        (SELECT B.PARENT_NAME, R.DATE_ID,R.org_code,R.ORG_NAME,SUM(NVL(R.PRI_LAST_AVG,0))/100.00,SUM(NVL(R.PUB_LAST_AVG,0))/100.00, SUM(NVL(R.FIN_LAST_AVG,0))/100.00,SUM(NVL(R.LAST_AVG,0))/100.00,
        SUM(NVL(R.PRI_THIS_AVG,0)-NVL(R.PRI_LAST_AVG,0))/100.00,SUM(NVL(R.PUB_THIS_AVG,0)-NVL(R.PUB_LAST_AVG,0))/100.00,SUM(NVL(R.FIN_THIS_AVG,0)-NVL(R.FIN_LAST_AVG,0))/100.00,SUM(NVL(R.THIS_AVG,0)-NVL(R.LAST_AVG,0))/100.00 
        FROM REPORT_MANAGER_DEP AS R  
        JOIN (SELECT B.BRANCH_CODE CHILD_CODE,B.BRANCH_NAME,A.BRANCH_CODE PARENT_CODE,A.BRANCH_NAME PARENT_NAME,A.BRANCH_LEVEL FROM BRANCH A
        JOIN BRANCH B ON A.ROLE_ID=B.PARENT_ID WHERE A.BRANCH_LEVEL='支行')B ON R.ORG_CODE=B.CHILD_CODE
        WHERE 1=1 %s GROUP BY R.DATE_ID,R.ORG_CODE,ORG_NAME,B.PARENT_NAME  ORDER BY R.ORG_CODE)
    """%(filterstr)

        
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        current_app.logger.debug(len(row))
        needtrans ={}
        rowlist=[]
        
        for i in row:
            t=list(i[0:4])
            for j in i[4:]:
                if j is None:j=0
                j=self.amount_trans_dec(j)
                t.append(j)
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False :
                    filterstr = filterstr+" and R.ORG_CODE in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and R.ORG_CODE in ( %s ) "%(vvv)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        return filterstr,vlist

    def column_header(self):
        return ["支行汇总","统计日期","机构号","机构名称","对私存量日均存款","对公存量日均存款","理财存量日均","合计值(存款理财)","对私增量日均存款","对公增量日均存款","理财增量日均","合计值(增量含理财)"]

    @property
    def page_size(self):
        return 15
