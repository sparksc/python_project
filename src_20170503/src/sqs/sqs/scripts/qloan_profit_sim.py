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
贷款利润模拟

"""

class Query(ObjectQuery):
    def exp_str(self):
        return {"start_row":4,"start_col":1,"cols":7}
    
    def group_by(self):
        return [],(4,5,6)

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        SELECT 
        r.THIRD_BRANCH_CODE "机构号",r.THIRD_BRANCH_NAME "网点名",r.SALE_CODE "客户经理号",r.SALE_NAME "客户经理名",
        suM(f.OLD_INTEREST_REV_CORE+f.OLD_INTEREST_REV) "年利息收入"
        ,sum(f.year_pdt*(p.FTP_PRICE*0.000000001/360.00000)) "资金成本"
        ,sum(f.CORE_REMAIN_AMOUNT) "贷款余额"
        FROM YDW.GAS_BI_CUX_LOAN_CHECK_DTL_V f
        inner join D_SALE_MANAGE_RELA r on r.MANAGE_ID  = f.MANAGE_ID
        inner join d_star_price p on p.id = f.PRICE_ID and p.VALIDATE_FLAG='有效'
        where 1 = 1
        %s
        group by r.THIRD_BRANCH_CODE,r.THIRD_BRANCH_NAME,r.SALE_CODE,r.SALE_NAME 
        with ur 
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
                elif k == 'DATE_ID':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr + " and f.DATE_ID = %s"%(vvv)
                else: 
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr+" and %s = %s"%(k,vvv)
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'SALE_CODE','ORG_CODE', None))
        print "***********", filterstr
        return filterstr,vlist

    def column_header(self):
        return [[{'name':"机构号",'h':2},{'name':"网点名",'h':2},{'name':"客户经理号",'h':2},{'name':"客户经理名",'h':2},{'name':"年利息收入",'h':2},{"name":"资金成本",'h':2},{'name':"贷款余额",'h':2}]]

    def trans_dec(self,num):
        tmp = Decimal(num)/Decimal(100)
        tmp = '{:,}'.format(tmp)
        return tmp

    @property
    def page_size(self):
        return 15
