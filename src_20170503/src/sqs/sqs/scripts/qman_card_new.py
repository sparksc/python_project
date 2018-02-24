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
客户经理信用卡报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        self.date_id=''
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        SELECT A.DATE_ID, A.ORG_CODE, A.SALE_CODE, A.SALE_NAME, A.LAST_NUM, A.THIS_NUM,NVL(A.THIS_NUM,0)-NVL(B.LAST_MON_NUM,0) ,NVL(A.THIS_NUM,0)-NVL(A.LAST_NUM,0),BAD_BAL/100.0,ROUND((CASE  WHEN NVL(A.ALL_BAL,0) = 0 AND  NVL(A.PPL_BAL,0) = 0 THEN 0 ELSE A.BAD_BAL*1.0/ (NVL(A.ALL_BAL,0) + NVL(A.PPL_BAL,0)) END)*100,2),A.BAD_ALL/ 100.0 
        FROM YDW.REPORT_MANAGER_CREDITCARD a
        left join (select SALE_CODE,ORG_CODE,this_num last_mon_num from YDW.REPORT_MANAGER_CREDITCARD where date_id=(select l_monthend_id from d_date where id=%s) ) b
        on  a.ORG_CODE=b.org_code and a.SALE_CODE=b.sale_code
        where ( nvl( A.LAST_NUM, 0) > 0 or nvl(A.THIS_NUM, 0) > 0 ) %s
            """%(self.date_id,filterstr)
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
            #if k == 'login_teller_no':
            #    if self.deal_teller_query_auth(v) == True:
            #        filterstr = filterstr+" and a.SALE_CODE = '%s'"%v
            #elif k == 'login_branch_no':
            #    bb = self.deal_branch_query_auth(v)
            #    if bb != False :
            #        filterstr = filterstr+" and a.ORG_CODE in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and a.ORG_CODE in ( %s ) "%(vvv)
                elif k=='DATE_ID':
                    filterstr = filterstr +" and a.DATE_ID =  ?  "
                    self.date_id='%s'%(v)
                    vlist.append(v)
                elif k=='SALE_CODE':
                    filterstr = filterstr +" and a.SALE_CODE =  ?  "
                    vlist.append(v)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'a.SALE_CODE','a.ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return ["统计日期","机构号","员工号","员工姓名","信用卡存量","信用卡现量","当月新增信用卡","新增发卡量","不良透支金额","不良率(%)","新增丰收贷记卡逾期本金"]
        '''
        return [
            ["统计日期",{"name":"机构号","h":2},"员工号",{"name":"信用卡现量","w":2},"新增发卡量","不良率","新增贷记卡","新增丰收贷记卡逾期本金"]
            ,["统计日期","信用卡存量","信用卡现量","新增发卡量","不良率",{"name":"新增贷记卡","w":2},"新增丰收贷记卡逾期本金"]
        ]
        '''

    def trans_dec(self,num):
        tmp = num
        #tmp = '{:,}'.format(tmp)
        return tmp

    @property
    def page_size(self):
        return 15
