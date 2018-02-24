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
客户经理其他业务
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        self.date_id=''
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        SELECT DATE_ID, ORG_CODE, SALE_CODE, SALE_NAME,MB_LAST_NUM, MB_THIS_NUM, PB_LAST_NUM, PB_THIS_NUM, CB_LAST_NUM, CB_THIS_NUM, KT_THIS_NUM, KJ_THIS_NUM, EPAY_LAST_NUM, EPAY_THIS_NUM, ETC_THIS_NUM ,nvl(ADD_HIGH_POS_NUM,0)-nvl(l_ADD_HIGH_POS_NUM,0),nvl(ADD_LOW_POS_NUM,0)-nvl(l_ADD_LOW_POS_NUM,0),LAST_THIRD_DEPO_NUM,FARM_SERV_HIGH_NUM,FARM_SERVICE_LOW_NUM
        FROM YDW.REPORT_MANAGER_OTHER 
        left join
        (SELECT ORG_CODE l_org_code , SALE_CODE l_sale_code,
        ADD_HIGH_POS_NUM l_ADD_HIGH_POS_NUM,ADD_LOW_POS_NUM l_ADD_LOW_POS_NUM
        FROM YDW.REPORT_MANAGER_OTHER where DATE_ID=(select l_monthend_id from d_date where id=%s)) 
        on ORG_CODE=l_org_code and SALE_CODE=l_sale_code
        WHERE 1=1 %s order by SALE_CODE
            """%( self.date_id,filterstr)
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
            #        filterstr = filterstr+" and SALE_CODE = '%s'"%v
            #elif k == 'login_branch_no':
            #    bb = self.deal_branch_query_auth(v)
            #    if bb != False :
            #        filterstr = filterstr+" and ORG_CODE in ( %s )"%bb
            if v and k in self.filterlist:
                if k == 'org':
                    if(v[0:1] == 'M'):
                        filterstr = filterstr+" and ORG_CODE in (select branch_code from branch where parent_id in (select role_id from branch where branch_code='%s'))"%v
                    else:
                        vvv = self.dealfilterlist(v)
                        filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                elif k=='DATE_ID':
                    filterstr = filterstr +" and DATE_ID=  %s  "%(v)
                    self.date_id="%s"%(v)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'SALE_CODE','ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return ["统计日期","机构编号","员工编号","员工姓名","手机银行总户数","手机银行有效户数","个人网上银行总户数","个人网上银行有效户数","企业网银总户数","企业网银有效户数","支付宝卡通总户数","支付宝快捷方式总户数","丰收e支付总户数","有效丰收e支付户数","ETC总户数","当月新增POS机(高扣率)","当月新增POS机(抵扣率)","第三方存量户数","助农服务点(达到活点率)","助农服务点(未达到活点率)"]

    def trans_dec(self,num):
        tmp = Decimal(num)
        tmp = '{:,}'.format(tmp)
        return tmp

    @property
    def page_size(self):
        return 15
