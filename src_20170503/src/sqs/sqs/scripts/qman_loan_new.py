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
客户经理贷款指标报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        SELECT DATE_ID, ORG_CODE, ORG_NAME, SALE_CODE, SALE_NAME, 
        NVL(PRI_LAST_NUM,0),NVL(PRI_NUM,0),NVL(PRI_NUM,0)-NVL(PRI_LAST_NUM,0) AS 对私管贷户数新增,NVL(PUB_LAST_NUM,0),NVL(PUB_NUM,0),NVL(PUB_NUM,0)-NVL(PUB_LAST_NUM,0) AS 对公管贷户数新增, 
        NVL(PRI_LAST_NUM,0)+NVL(PUB_LAST_NUM,0),NVL(PRI_NUM,0)+NVL(PUB_NUM,0),NVL(PRI_NUM,0)+NVL(PUB_NUM,0)-(NVL(PRI_LAST_NUM,0)+NVL(PUB_LAST_NUM,0)) AS 管贷户数新增,
        NVL(PRI_LAST_BAL,0),NVL(PRI_BAL,0),NVL(PRI_BAL,0)-NVL(PRI_LAST_BAL,0) AS 对私管贷余额新增,NVL(PUB_LAST_BAL,0),NVL(PUB_BAL,0),NVL(PUB_BAL,0)-NVL(PUB_LAST_BAL,0) AS 对公管贷余额新增,
        NVL(PRI_LAST_BAL,0)+NVL(PUB_LAST_BAL,0),NVL(PRI_BAL,0)+NVL(PUB_BAL,0),NVL(PRI_BAL,0)+NVL(PUB_BAL,0) - (NVL(PRI_LAST_BAL,0)+NVL(PUB_LAST_BAL,0)) AS 管贷余额新增,
        NVL(PRI_LAST_AVG,0),NVL(PRI_THIS_AVG,0),NVL(PRI_THIS_AVG,0)-NVL(PRI_LAST_AVG,0) AS 对私管贷年日均新增,NVL(PUB_LAST_AVG,0),NVL(PUB_THIS_AVG,0),NVL(PUB_THIS_AVG,0)-NVL(PUB_LAST_AVG,0) AS 对公管贷年日均新增,
        NVL(PRI_LAST_AVG,0)+NVL(PUB_LAST_AVG,0),NVL(PRI_THIS_AVG,0)+NVL(PUB_THIS_AVG,0),NVL(PRI_THIS_AVG,0)+NVL(PUB_THIS_AVG,0)-(NVL(PRI_LAST_AVG,0)+NVL(PUB_LAST_AVG,0)) AS 管贷年日均新增 ,
        PRI_MONTH_AVG,PUB_MONTH_AVG,MONTH_AVG , ----管贷月日均
        ROUND(CASE MIN_NUM WHEN 0 THEN 0 ELSE MIN_CRD_NUM*1.0/ MIN_NUM END ,2), ----小额信用贷款户数占比
        ROUND(CASE MIN_BAL WHEN 0 THEN 0 ELSE MIN_CRD_BAL*1.0/ MIN_BAL END ,2), ----小额信用贷款户数占比
        BAD_NUM AS 资产不良贷款户数, BAD_BAL AS 资产不良贷款余额,OUT_BAL AS 管理核销贷款余额,NVL(TWO_THSI_NUM,0) AS 两卡有效合同数,
        NVL(ROUND( CASE TWO_CARD_ALL WHEN 0 THEN 0 ELSE TWO_CARD_BY_EBANK*1.0/ TWO_CARD_ALL END,2),0) AS 两卡电子渠道办贷率
        FROM YDW.REPORT_MANAGER_LOAN
        WHERE SALE_NAME IS NOT NULL AND (NVL(PRI_NUM, 0) > 0 OR  NVL(PUB_NUM, 0) > 0) %s
        ORDER BY ORG_CODE,SALE_CODE
            """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print sql
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i[0:14])
            for j in i[14:35]:
                if j is None:j=0
                j=self.trans_dec(j)
                t.append(j)
            t.append(i[35])
            t.append(i[36])
            t.append(i[37])
            for j in i[38:40]:
                if j is None:j=0
                j=self.trans_dec(j)
                t.append(j)
            t.append(i[40])
            t.append(i[41])
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
            [{'name':'统计日期','h':2},{'name':'机构号','h':2},{'name':'机构名称','h':2},{'name':'客户经理号','h':2},{'name':'客户经理名称','h':2},{'name':'对私管贷户数','w':3},{'name':'对公管贷户数','w':3},{'name':'管贷户数合计','w':3},{'name':'对私管贷余额','w':3},{'name':'对公管贷余额','w':3},{'name':'管贷余额合计','w':3},{'name':'对私管贷年日均','w':3},{'name':'对公管贷年日均','w':3},{'name':'管贷年日均合计','w':3},{'name':'管贷月日均','w':3},{'name':'小额信用贷款户数占比','h':2},{'name':'小额信用贷余额占比','h':2},{'name':'资产不良贷款户数(管理)','h':2},{'name':'资产不良贷款余额(管理)','h':2},{'name':'管理核销贷款余额','h':2},{'name':'两卡有效合同数','h':2},{'name':'两卡电子渠道办贷率','h':2}],
            [{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1},{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1},{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1},{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1},{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1},{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1},{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1},{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1},{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1},{'name':'存量','h':1},{'name':'现量','h':1},{'name':'新增','h':1}]
        ]
        
    def trans_dec(self,num):
        tmp = Decimal(num)/Decimal(100)
        tmp = '{:,}'.format(tmp)
        return tmp
    @property
    def page_size(self):
        return 15

