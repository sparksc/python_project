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
理财流水号转移数据
TBD 由于数据跑数问题，需要再次处理日期
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['account_no','org_no','note','status','cst_typ','manager_no','ld']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select a.id,o.branch_code,o.branch_name,s.user_name,s.NAME,a.ACCOUNT_NO,i.cust_long_no,i.CUST_NAME,a.PERCENTAGE,nvl(a.BALANCE/100.00,0),nvl(a.add_avg_balance/100.00,0),a.note
                from account_hook a
                join d_cust_info i on i.cust_no=a.cust_in_no
                join f_user s on s.user_name=a.manager_no
                join branch o on o.branch_code=a.org_no
                where a.TYP='理财' and a.follow_cust='账号优先' %s
                order by id desc
                """%(filterstr)
        print sql
        print vlist
        row = self.engine.execute(sql,vlist).fetchall()
        row = list(row)
        for i in range(0,len(row)):
            row[i] = list(row[i])
            row[i][9] = self.trans_dec('%.2f' % row[i][9])
            row[i][10] = self.trans_dec('%.2f' % row[i][10])
        print len(row)    
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr,filterstr2 ="",""
        vlist,vlist2 = [],[]
        for k,v in self.args.items():

            if v and k in self.filterlist:
                if k == 'org_no':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and a.org_no in ( %s ) "%(vvv)
                elif k == 'manager_no':
                    filterstr = filterstr + " and a.manager_no = ? "
                    vlist.append(v)
                elif k == 'account_no':
                    filterstr = filterstr + " and a.account_no like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                elif k == 'status':
                    filterstr = filterstr + " and a.status = ? "
                    vlist.append(v)
                elif k == 'note':
                    filterstr = filterstr + " and note like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                elif k == 'ld':
                    filterstr = filterstr + " and bal/10000 >= ? "
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['transfer'],'a.manager_no','a.org_no', None))        
        return filterstr,vlist
    def column_header(self):
        return ["机构号","机构名","员工号","员工名","流水号","客户号","客户名","占比(%)","余额(元)","当前日均(元)","地址信息"]

    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        xxx = '{:,}'.format(tmp)
        return xxx
    @property
    def page_size(self):
        return 10
