# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
机构存款
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['date','org']
        filterstr3,filterstr2,filterstr1,vlist3,vlist2,vlist1,yy,ly,dd,date = self.make_eq_filterstr()
        sql1 ="""
                select branch_code,branch_name,nvl(amt,0) from (
                select THIRD_BRANCH_CODE,third_branch_name,sum(sun_balance) amt
                from m_com_dep where account_owner_type='对私' and acct_type='1' and year=%s %s
                group by THIRD_BRANCH_CODE,third_branch_name) a 
                right join branch b on b.branch_code = a.third_branch_code 
                where 1=1 %s
                order by branch_code 
                """%(ly,filterstr2,filterstr3)
        row1 = self.engine.execute(sql1.encode('utf-8'),vlist2+vlist3).fetchall()
        sql2 ="""
                select branch_code,branch_name,nvl(amt,0) from (
                select THIRD_BRANCH_CODE,third_branch_name,sum(sun_balance) amt
                from m_com_dep where account_owner_type='对公' and acct_type='1' and year=%s %s
                group by THIRD_BRANCH_CODE,third_branch_name) a 
                right join branch b on b.branch_code = a.third_branch_code
                where 1=1 %s
                order by branch_code 
                """%(ly,filterstr2,filterstr3)
        row2 = self.engine.execute(sql2.encode('utf-8'),vlist2+vlist3).fetchall()
        sql3 ="""
                select branch_code,branch_name,nvl(amt,0) from (
                select THIRD_BRANCH_CODE,third_branch_name,sum(sun_balance) amt
                from m_com_dep where account_owner_type='对私' and acct_type='1' and year=%s %s
                group by THIRD_BRANCH_CODE,third_branch_name) a
                right join branch b on b.branch_code = a.third_branch_code
                where 1=1 %s
                order by branch_code 
                """%(yy,filterstr1,filterstr3)
        row3 = self.engine.execute(sql3.encode('utf-8'),vlist1+vlist3).fetchall()
        sql4 ="""
                select branch_code,branch_name,nvl(amt,0) from (
                select THIRD_BRANCH_CODE,third_branch_name,sum(sun_balance) amt
                from m_com_dep where account_owner_type='对公' and acct_type='1' and year=%s %s
                group by THIRD_BRANCH_CODE,third_branch_name) a
                right join branch b on b.branch_code = a.third_branch_code
                where 1=1 %s
                order by branch_code 
                """%(yy,filterstr1,filterstr3)
        row4 = self.engine.execute(sql4.encode('utf-8'),vlist1+vlist3).fetchall()

        sql5 ="""
                select month_days from d_date where id=%s
                """%(date)
        row5 = self.engine.execute(sql5.encode('utf-8')).fetchall()
        i=-1
        rr=[]
        month_days=1
        if row5[0][0]:
            month_days=row5[0][0]
        days=365
        if (yy%4) == 0:
            if (yy%100) == 0:
                if (yy%400) ==0:
                    days=366
            else:
                days=365
        while True:
            i+=1
            if i>=len(row1):
                break
            add_dg=int(row3[i][2])/month_days-int(row1[i][2])/days
            add_ds=int(row4[i][2])/month_days-int(row2[i][2])/days
            sum1 = int(row1[i][2])+int(row2[i][2])
            sum2 = add_dg + add_ds
            c1 = self.trans_dec(row2[i][2])
            c2 = self.trans_dec(row1[i][2])
            c3 = self.trans_dec(sum1)
            c4 = self.trans_dec(add_ds)
            c5 = self.trans_dec(add_dg)
            c6 = self.trans_dec(sum2)
            rr.append((self.ym,row1[i][0],row1[i][1],c1,c2,c3,c4,c5,c6))
        needtrans ={}
        return self.translate(rr,needtrans)
    def make_eq_filterstr(self):
        filterstr1 = ""
        filterstr2 = ""
        filterstr3 = ""
        vlist1 = []
        vlist2 = []
        vlist3 = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'date':
                    date = v
                    self.ym = v[0:6]
                    mm = int(v[4:6])
                    yy = int(v[0:4])
                    ly = int(v[0:4])-1
                    dd = int(v[6:8])
                    self.ly_date=(int(v[0:4])-1)*10000+1231
                    filterstr1 = filterstr1+"and month = ? "
                    vlist1.append(int(mm))
                if k == 'org':
                    if(v[0:1] == 'M'):
                        filterstr1 = filterstr1+" and third_branch_code in(select branch_code from branch where parent_id in (select role_id from branch where branch_code='%s'))"%v
                        filterstr2 = filterstr2+" and third_branch_code in(select branch_code from branch where parent_id in (select role_id from branch where branch_code='%s'))"%v
                        filterstr3 = filterstr3+" and branch_code in(select branch_code from branch where parent_id in (select role_id from branch where branch_code='%s'))"%v
                    else:
                        vvv = self.dealfilterlist(v)
                        filterstr1 = filterstr1+" and third_branch_code in( %s ) "%(vvv)
                        filterstr2 = filterstr2+" and third_branch_code in( %s ) "%(vvv)
                        filterstr3 = filterstr3+" and branch_code in( %s ) " %(vvv)
        return filterstr3,filterstr2,filterstr1,vlist3,vlist2,vlist1,yy,ly,dd,date
    def column_header(self):
        return ["统计日期","机构编号","机构名称","对私日均存款存量","对公日均存款存量","日均存量合计","对私存款日均增量","对公存款日均增量","日均增量合计"]
    def trans_dec(self,num):
        tmp = Decimal(num)
        tmp = '{:,}'.format(tmp)
        return tmp
    @property
    def page_size(self):
        return 15
