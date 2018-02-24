# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from utils import config
"""
客户经理贷款得分
"""

class Query(ObjectQuery):
 
    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql="""
        SELECT DATE_ID,ORG_CODE,ORG_NAME,SALE_CODE,SALE_NAME,nvl(LOAN_SCO/ 100.00 ,0),nvl(AVG_LOAN_SCO/ 100.00 ,0),nvl(MIN_CARD_SCO/ 100.00 ,0),nvl(ZX_SCO/ 100.00,0),nvl(TWO_CARD_ADD/ 100,00,0),nvl(TWO_CRAD_SCO/ 100.00,0),nvl(VILLAGE_SCO/ 100.00,0),nvl(ALL_SCO/ 100.00, 0)
        FROM REPORT_MANAGER_LOAN 
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
            t = list(i[1:5])
            for j in i[5:]:
                if j is None:j=0
                j = round(j,2)
                t.append(j)
            t.insert(0,month)
            t.insert(0,year)
            rowlist.append(t)
        print rowlist
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
            
        return filterstr,vlist

    def column_header(self):
        return ["统计年份","统计月份","机构号","机构名称","员工号","员工名称","扩面工作得分","日均贷款增加额得分","小额信用贷款户数占比得分","资产质量管理得分","丰收两卡合同新增户数指标得分","两卡贷款电子渠道办贷率得分","驻勤(驻村)工作得分","贷款总得分"]
    @property
    def page_size(self):
        return 15
