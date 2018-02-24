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

    def prepare_object(self):
        self.filterlist = ['FROM_DATE_ID', 'END_DATE_ID', 'org','SALE_CODE']
        self.kaishi=''
        self.jieshu=''
        filterstr, vlist = self.make_eq_filterstr()
        sql ="""
        --最新关系查询存款，明细核对
        select %s, %s, n.*,n.lc+n.ck from (
            select ah.ORG_NO,hh.BRANCH_NAME, ah.MANAGER_NO, x.NAME,
            sum(case when f.ACCT_TYPE = '8' and d.CLOSE_DATE_ID > f.DATE_ID then nvl(f.BALANCE, 0) * ah.PERCENTAGE / 10000.00 / (days(to_date(%s,'yyyymmdd'))-days(to_date(%s,'yyyymmdd')) +1)  else 0 END) as lc,
            sum(case when f.ACCT_TYPE = '1' then nvl(f.BALANCE, 0) * ah.PERCENTAGE / 10000.00 / (days(to_date(%s,'yyyymmdd'))-days(to_date(%s,'yyyymmdd')) +1)   else 0 END) as ck 
            from f_balance f
            join d_account d on d.ID = f.ACCOUNT_ID
            join ACCOUNT_HOOK ah on d.ACCOUNT_NO = ah.ACCOUNT_NO and ah.END_DATE > (select l_yearend_id from d_date where id = %s) and ah.START_DATE <= (select yearend_id from d_date where id = %s) and ah.STATUS in ('待审批','已审批','预提交审批','正常','录入已审批')   --<<开始日期<=终止日期的年底,  结束日期>=开始日期的去年年底
            --join d_org o on o.ID = f.ORG_ID and o.ORG0_CODE = ah.ORG_NO
            left join v_staff_info x on ah.MANAGER_NO=x.USER_NAME
            left join branch hh on ah.org_no=hh.branch_code
            where 1 = 1 %s
            group by ah.ORG_NO, hh.branch_name, ah.Manager_no,x.name 
            ) n
        with ur

        """%(self.kaishi, self.jieshu, self.jieshu,self.kaishi,self.jieshu, self.kaishi, self.kaishi, self.jieshu,filterstr)
        print sql
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print "0000000000000000000000000", sql
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i[0:6])
            for j in i[6:]:
                if j is None:j=0
                j=self.amount_trans_dec(j)
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
                    filterstr = filterstr +" and ah.ORG_NO in ( %s ) "%(vvv)
                elif k == 'FROM_DATE_ID':
                    filterstr = filterstr +" and f.date_id >= %s "%v
                    self.kaishi=int(v)
                elif k == 'END_DATE_ID':
                    filterstr = filterstr +" and f.date_id <= %s "%v
                    self.jieshu=int(v)
                elif k == 'SALE_CODE':
                    filterstr = filterstr +" and ah.Manager_no = '%s' "%v
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'ah.Manager_no','ah.ORG_NO', None))
        return filterstr,vlist

    def column_header(self):
        return ["开始时间","结束时间","机构编号", "机构名称", "员工编号","员工姓名","理财日均","存款日均", "日均合计值"]

    @property
    def page_size(self):
        return 15
