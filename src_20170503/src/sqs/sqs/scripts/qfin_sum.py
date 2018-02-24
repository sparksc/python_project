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
理财汇总查询 by cchen 2017-04-05
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['org','remark']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select e.remark,e.prod_name,e.org_no,d.branch_name,
                sum(case when e.contract_no='银行柜台' then e.balance else 0 end)/1000000 ,
                sum(case when e.contract_no='自助终端' then e.balance
                                when e.contract_no='自助终端(发卡)' then e.balance else 0 end)/1000000 ,
                sum(case when e.contract_no='企业网银' then e.balance
                                when e.contract_no='网银' then e.balance else 0 end) /1000000 ,
                sum(case when e.contract_no='手机客户端' then e.balance else 0 end) /1000000 ,
                sum(case when 1=1 then e.balance else 0 end) /1000000 
                from (
                                select a.*,b.remark,b.contract_no,p.prod_name from (select distinct org_no,account_no,balance from account_hook where typ='理财' ) a,d_account b, fms_prod p  
                                where b.ACCOUNT_CLASS='理财账户'  and a.account_no=b.account_no and p.prod_code=b.remark %s
                     ) e ,branch d
                where e.org_no=d.branch_code
                group by e.remark,e.prod_name,e.org_no,d.branch_name
            """%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
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
                    filterstr = filterstr+" and ORG_NO in ( %s )"%bb
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_NO in ( %s ) "%(vvv)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)

        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'], None, 'ORG_NO', None))
        return filterstr,vlist

    def column_header(self):
        return ["理财产品代码","理财产品名称","机构编号","机构名称","柜面销售(万元)","自助终端(万元)","网银销售(万元)","手机销售(万元)","网点销售总额(万元)"]

    def trans_dec(self,num):
        tmp = Decimal(num)/Decimal(100)
        tmp = '{:,}'.format(tmp)
        return tmp

    @property
    def page_size(self):
        return 15
