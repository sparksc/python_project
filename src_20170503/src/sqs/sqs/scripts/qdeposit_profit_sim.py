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
    def exp_str(self):
        return {"start_row":4,"start_col":1,"cols":7}
    
    def group_by(self):
        return [],(4,5,6)

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        select 
        s.ORG_CODE "机构号",b.BRANCH_NAME "网点名" ,gr.SALE_CODE "客户经理号" ,fu.NAME "客户经理名"     
        , sum(            
        case when f.ACCOUNT_class='D' and  t.INTEREST_TYPE='不计息' then  0 else  f.PAY_INTEREST+f.PLAN_INTEREST-nvl(f2.PAY_INTEREST,0)-nvl(f2.PLAN_INTEREST,0)  end 
        )/100.00 as   "年利息支出"       
        , sum( case when f.ACCOUNT_class='D' and  t.INTEREST_TYPE='不计息' then 0 else f.BALANCE end )/100.00 as "余额" 
        ,sum(f.YEAR_PDT*(p.FTP_PRICE*0.000000001/360.00000)) as "资金转移收入"
        from F_ACCOUNT_BALANCE_back  f
        inner join d_org_stat s on  s.id = f.ORG_ID
        inner join d_account_type_extend t on t.id = f.ACCOUNT_TYPE_ID
        inner join D_AC_MAP da on t.SUBJ_NO=da.AC_CODE
        inner join d_group_relation  gr on gr.GROUP_ID = f.GROUP_ID
        inner join f_user fu on fu.USER_NAME=gr.SALE_CODE
        inner join branch b on b.BRANCH_CODE = s.ORG_CODE
        inner join d_star_price p on p.id = f.PRICE_ID and p.VALIDATE_FLAG='有效'
        left join F_ACCOUNT_BALANCE f2 on f2.ACCOUNT_ID=f.ACCOUNT_ID and f2.DATE_ID=20151231
        where
        da.SUBJ_NO in ('20010101','20020101','20020102','20030101','20030102','20040101','20040105','20040106','20050201','20060101','20140106', '20140109', '20140199', '20140201', '20140204', '20140206')
        %s
        group by  s.ORG_CODE,gr.SALE_CODE,fu.NAME,b.BRANCH_NAME
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
        return [[{'name':"机构号",'h':2},{'name':"网点名",'h':2},{'name':"客户经理号",'h':2},{'name':"客户经理名",'h':2},{'name':"年利息支出",'h':2},{"name":"余额",'h':2},{'name':"资金转移收入",'h':2}]]

    def trans_dec(self,num):
        tmp = Decimal(num)/Decimal(100)
        tmp = '{:,}'.format(tmp)
        return tmp

    @property
    def page_size(self):
        return 15
