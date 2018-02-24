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
客户经理存款
"""

class Query(ObjectQuery):

    def group_by(self):
        
        return [0],tuple([x for x in range(4,26)])

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        SELECT SALE_CODE,SALE_NAME,DATE_ID,ORG_CODE, 
         SUM(NVL(PRI_LAST_AVG,0)),SUM(NVL(PRI_THIS_AVG,0)),SUM(NVL(PRI_THIS_AVG,0))-SUM(NVL(PRI_LAST_AVG,0)) AS 存款年日均对私,
         SUM(NVL(PUB_LAST_AVG,0)),SUM(NVL(PUB_THIS_AVG,0)),SUM(NVL(PUB_THIS_AVG,0))-SUM(NVL(PUB_LAST_AVG,0)) AS 存款年日均对公,
         SUM(NVL(FIN_LAST_AVG,0)),SUM(NVL(FIN_THIS_AVG,0)),SUM(NVL(FIN_THIS_AVG,0))-SUM(NVL(FIN_LAST_AVG,0)) AS 理财年日均,
         SUM(NVL(PRI_LAST_AVG,0))+SUM(NVL(PUB_LAST_AVG,0)),SUM(NVL(PRI_THIS_AVG,0))+SUM(NVL(PUB_THIS_AVG,0)),
          SUM(NVL(PRI_THIS_AVG,0))+SUM(NVL(PUB_THIS_AVG,0))-(SUM(NVL(PRI_LAST_AVG,0))+SUM(NVL(PUB_LAST_AVG,0))) AS 存款合计年日均不含理财,
         SUM(NVL(PRI_LAST_AVG,0))+SUM(NVL(PUB_LAST_AVG,0))+SUM(NVL(FIN_LAST_AVG,0)),SUM(NVL(PRI_THIS_AVG,0))+SUM(NVL(PUB_THIS_AVG,0))+SUM(NVL(FIN_THIS_AVG,0)),
          SUM(NVL(PRI_THIS_AVG,0))+SUM(NVL(PUB_THIS_AVG,0))+SUM(NVL(FIN_THIS_AVG,0))-(SUM(NVL(PRI_LAST_AVG,0))+SUM(NVL(PUB_LAST_AVG,0))+SUM(NVL(FIN_LAST_AVG,0))) AS 存款合计年日均含理财,
         SUM(NVL(PRI_MONTH_AVG,0)),SUM(NVL(PUB_MONTH_AVG,0)),SUM(NVL(MONTH_AVG,0)) AS 存款月日均,
         SUM(NVL(PRI_BAL,0)),SUM(NVL(PUB_BAL,0)),SUM(NVL(FIN_BAL,0)),SUM(NVL(PRI_BAL,0)+NVL(PUB_BAL,0)+NVL(FIN_BAL,0)) AS 存款余额
        FROM YDW.REPORT_MANAGER_DEP R
        JOIN V_STAFF_INFO V ON R.SALE_CODE=V.USER_NAME
        JOIN D_ORG DG ON DG.ORG0_CODE=V.ORG AND LEFT(DG.ORG1_CODE,5)=LEFT(R.ORG_CODE,5)
        WHERE 1=1 AND LENGTH(SALE_CODE)!=6  %s
        GROUP BY DATE_ID,ORG_CODE,SALE_CODE,SALE_NAME
            """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
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
        return [
            [{'name':'客户经理号','h':2},{'name':'客户经理名称','h':2},{'name':'统计日期','h':2},{'name':'机构号','h':2},{'name':'存款年日均(对私)','w':3},{'name':'存款年日均(对公)','w':3},{'name':'理财年日均','w':3},{'name':'存款合计年日均(不含理财)','w':3},{'name':'存款合计年日均(含理财)','w':3},{'name':'存款月日均','w':3},{'name':'存款余额','w':4}],
            [{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1},{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1},{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1},{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1},{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1},{'name':'对私','h':1},{'name':'对公','h':1},{'name':'合计','h':1},{'name':'对私','h':1},{'name':'对公','h':1},{'name':'理财','h':1},{'name':'合计','h':1}]
       ] 

    def trans_dec(self,num):
        tmp = Decimal(num)/Decimal(100)
        tmp = '{:,}'.format(tmp)
        return tmp

    @property
    def page_size(self):
        return 15
