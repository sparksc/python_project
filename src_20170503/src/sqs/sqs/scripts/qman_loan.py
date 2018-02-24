# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
客户经理贷款指标报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.id = ""
        self.org = ""
        self.filter = ""
        self.filterlist = ['org','id','S_DATE']
        filterstr,filterstr1,filterstr2,filterstr3,vlist,vlist3,ym = self.make_eq_filterstr()
        #管贷户数
        sql =u"""
                select user_name,name,nvl(amt,0),branch_code,branch_name from
                (select sale_code,count(distinct cst_no) amt
                from f_balance f
                inner join d_sale_manage_rela sm on sm.manage_id=f.manage_id
                inner join d_account_type t on t.id=f.account_type_id and account_owner_type='对公'
                where acct_type='4' and balance>500000 and date_id =%s %s
                group by sale_code) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.ly_date,filterstr,filterstr3)
        row = self.engine.execute(sql,vlist+vlist3).fetchall()
        sqla =u"""
                select user_name,name,nvl(amt,0),branch_code,branch_name from
                (select sale_code,count(distinct cst_no) amt
                from f_balance f
                inner join d_sale_manage_rela sm on sm.manage_id=f.manage_id
                inner join d_account_type t on t.id=f.account_type_id and account_owner_type='对私'
                where acct_type='4' and balance>500000 and date_id =%s %s
                group by sale_code) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.ly_date,filterstr,filterstr3)
        rowa = self.engine.execute(sqla,vlist+vlist3).fetchall()
        #管贷余额 
        sql1 =u"""
                select user_name,name,nvl(amt,0),branch_code,branch_name from
                (select sale_code,sum(balance) amt
                from f_balance f
                inner join d_sale_manage_rela sm on sm.manage_id=f.manage_id
                inner join d_account_type t on t.id=f.account_type_id and account_owner_type='对公'
                where f.acct_type='4' and f.balance>500000 and date_id=%s %s
                group by sale_code) a 
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                 """%(self.ly_date,filterstr,filterstr3)
        row1 = self.engine.execute(sql1,vlist+vlist3).fetchall()
        sql1a =u"""
                select user_name,name,nvl(amt,0),branch_code,branch_name from
                (select sale_code,sum(balance) amt
                from f_balance f
                inner join d_sale_manage_rela sm on sm.manage_id=f.manage_id
                inner join d_account_type t on t.id=f.account_type_id and account_owner_type='对私'
                where f.acct_type='4' and f.balance>500000 and date_id=%s %s
                group by sale_code) a 
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                 """%(self.ly_date,filterstr,filterstr3)
        row1a = self.engine.execute(sql1a,vlist+vlist3).fetchall()
        print '贷款余额OK'
        #贷款增量
        sql2 =u"""
                select user_name,name,nvl(amt,0),branch_code,branch_name from (
                select THIRD_BRANCH_CODE,third_branch_name,sale_code,sale_name,sum(sun_balance) amt
                from m_com_dep sm where account_owner_type='对公' and acct_type='4' and year=%s %s
                group by THIRD_BRANCH_CODE,third_branch_name,sale_code,sale_name) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.ly,filterstr,self.id)
        row2 = self.engine.execute(sql2,vlist).fetchall()
        sql3 =u"""
                select user_name,name,nvl(amt,0),branch_code,branch_name from (
                select THIRD_BRANCH_CODE,third_branch_name,sale_code,sale_name,sum(sun_balance) amt
                from m_com_dep sm where account_owner_type='对私' and acct_type='4' and year=%s %s
                group by THIRD_BRANCH_CODE,third_branch_name,sale_code,sale_name) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.ly,filterstr,self.id)
        row3 = self.engine.execute(sql3,vlist).fetchall()
        sql2a =u"""
                select user_name,name,nvl(amt,0),branch_code,branch_name from (
                select THIRD_BRANCH_CODE,third_branch_name,sale_code,sale_name,sum(sun_balance) amt
                from m_com_dep sm where account_owner_type='对公' and acct_type='4' and year=%s and month=%s %s
                group by THIRD_BRANCH_CODE,third_branch_name,sale_code,sale_name) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.yy,self.mm,filterstr,self.id)
        row2a = self.engine.execute(sql2a,vlist).fetchall()
        sql3a =u"""
                select user_name,name,nvl(amt,0),branch_code,branch_name from (
                select THIRD_BRANCH_CODE,third_branch_name,sale_code,sale_name,sum(sun_balance) amt
                from m_com_dep sm where account_owner_type='对私' and acct_type='4' and year=%s and month=%s %s
                group by THIRD_BRANCH_CODE,third_branch_name,sale_code,sale_name) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.yy,self.mm,filterstr,self.id)
        row3a = self.engine.execute(sql3a,vlist).fetchall()
        sql_m ="""
                select month_days from d_date where id=%s
                """%(self.s_date)
        row_m = self.engine.execute(sql_m.encode('utf-8')).fetchall()
        month_days=1
        if row_m[0][0]:
            month_days=row_m[0][0]
        days=365
        if (self.yy%4) == 0:
            if (self.yy%100) == 0:
                if (self.yy%400) ==0:
                    days=366
            else:
                days=365
        print '贷款日均OK'
        #对公增户扩面增量
        sql4 =u"""
                select user_name,name,nvl(amt,0),branch_code,branch_name from 
                (select  sale_code,sum(cst_num)/count(DAY) as amt
                from(
                select sale_code,count(f.CST_NO) cst_num,d.DAY from F_BALANCE f
                join D_DATE d on f.DATE_ID=d.ID and d.DAY in (5,15,25)
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID 
                where f.ACCT_TYPE='4' and left(f.CST_NO,2)='82' and f.DATE_ID>= %s and f.DATE_ID<%s %s
                group by sale_code,d.DAY)
                group by sale_code) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.tm_date,self.s_date,filterstr,filterstr3)
        row4 = self.engine.execute(sql4.encode('utf-8'),vlist+vlist3).fetchall()
        #对私增户扩面增量
        sql5 =u"""
                select user_name,name,nvl(amt,0),branch_code,branch_name from 
                (select  sale_code,sum(cst_num)/count(DAY) as amt
                from(
                select sale_code,count(f.CST_NO) cst_num,d.DAY from F_BALANCE f
                join D_DATE d on f.DATE_ID=d.ID and d.DAY in (5,15,25)
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID 
                where f.ACCT_TYPE='4' and left(f.CST_NO,2)='83' and f.DATE_ID>=%s and f.DATE_ID<%s %s
                group by sale_code,d.DAY)
                group by sale_code) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.tm_date,self.s_date,filterstr,filterstr3)
        row5 = self.engine.execute(sql5.encode('utf-8'),vlist+vlist3).fetchall()
        print '扩面OK'
        #两卡贷款客户电子渠道办贷率
        sql6 =u"""
                select user_name,name,nvl(amt,0),branch_code,branch_name from 
                (select l.loan_staff as sale_code,count(distinct CUSTID) as amt 
                from F_C_ACCTJRNL f
                join D_T_CHANNEL d on f.CHANNELID = d.ID and d.CHANNELNO in ('IE','AT','ME')
                join D_ACCT_TRAN_TYPE t on f.ACCTTRANTYPEID = t.ID and t.TRANS_CLASSIFY='L'
                join D_LOAN_ACCOUNT l on l.ID = f.ACCTID
                join D_DEBIT_CARD c on l.DEP_ACCOUNT=c.CARD_NO and c.CARD_NATURE in ('支农贷款卡','丰收创业贷款卡')
                where f.TRANDATEID >=%s and f.TRANDATEID <%s %s
                group by l.loan_staff) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.tm_date,self.s_date,filterstr2,filterstr3)
        row6 = self.engine.execute(sql6.encode('utf-8'),vlist+vlist3).fetchall()
        print '办贷OK'
        #电子档案信息采集率
            #手工录入
        #小额信用贷款户数占比指标(当前时点)
        
        '''小额信用贷款 取得 金额参数'''
        sql_num3=u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_NAME='小额贷款金额参数'
        order by d.DETAIL_VALUE
            """
        num = self.engine.execute(sql_num3.encode('utf-8'),vlist+vlist3).fetchall()
        num1 = int(num[0][1])*1000000
        sql7 =u"""
                select user_name,name,nvl(cst_num,0),branch_code,branch_name from (
                select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sale_code,sale_name,count(f.CST_NO) cst_num from F_BALANCE f 
                join D_DATE d on f.DATE_ID=d.ID
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID 
                join D_ACCOUNT_TYPE t on t.ID=f.ACCOUNT_TYPE_ID 
                where f.ACCT_TYPE='4' and t.gua_tp_name='信用' and f.date_id=%s %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sale_code,sale_name
                having count(f.BALANCE)<=30000000) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.s_date,filterstr,self.id)
        row7 = self.engine.execute(sql7.encode('utf-8'),vlist).fetchall()
        sql7a =u"""
                select user_name,name,nvl(cst_num,0),branch_code,branch_name from (
                select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sale_code,sale_name,count(f.CST_NO) cst_num from F_BALANCE f 
                join D_DATE d on f.DATE_ID=d.ID
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID 
                join D_ACCOUNT_TYPE t on t.ID=f.ACCOUNT_TYPE_ID 
                where f.ACCT_TYPE='4' and f.date_id=%s %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sale_code,sale_name
                having count(f.BALANCE)<=30000000) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.s_date,filterstr,self.id)
        row7a = self.engine.execute(sql7a.encode('utf-8'),vlist).fetchall()
        sql7b =u"""
                select branch_code,branch_name,nvl(cst_num,0),user_name,name from (
                select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sale_code,sale_name,sum(f.balance) cst_num from F_BALANCE f 
                join D_DATE d on f.DATE_ID=d.ID
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID 
                join D_ACCOUNT_TYPE t on t.ID=f.ACCOUNT_TYPE_ID 
                where f.ACCT_TYPE='4' and t.gua_tp_name='信用' and f.date_id=%s %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sale_code,sale_name
                having count(f.BALANCE)<=30000000) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.s_date,filterstr,self.id)
        row7b = self.engine.execute(sql7.encode('utf-8'),vlist).fetchall()
        sql7c =u"""
                select branch_code,branch_name,nvl(cst_num,0),user_name,name from (
                select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sale_code,sale_name,sum(f.balance) cst_num from F_BALANCE f 
                join D_DATE d on f.DATE_ID=d.ID
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID 
                join D_ACCOUNT_TYPE t on t.ID=f.ACCOUNT_TYPE_ID 
                where f.ACCT_TYPE='4' and f.date_id=%s %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sale_code,sale_name
                having count(f.BALANCE)<=30000000) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.s_date,filterstr,self.id)
        row7c = self.engine.execute(sql7a.encode('utf-8'),vlist).fetchall()
        print '小额OK'
        #资产管理质量
        sql8 =u"""
                select branch_code,branch_name,nvl(amt,0),user_name,name from( 
                select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sum(f.BALANCE) amt,sale_code,sale_name from F_BALANCE f 
                join D_DATE d on f.DATE_ID=d.ID
                join D_ACCOUNT_STATUS s on f.ACCOUNT_STATUS_ID=s.ID and s.GRADE_FOUR in ('逾期','呆滞','呆账')
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID  
                where f.ACCT_TYPE='4' and f.DATE_ID=%s %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sale_code,sale_name) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.s_date,filterstr,self.id)
        row8 = self.engine.execute(sql8.encode('utf-8'),vlist).fetchall()
        sql8a =u"""
                select branch_code,branch_name,nvl(amt,0),user_name,name from( 
                select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,count(f.cst_no) amt,sale_code,sale_name from F_BALANCE f 
                join D_DATE d on f.DATE_ID=d.ID
                join D_ACCOUNT_STATUS s on f.ACCOUNT_STATUS_ID=s.ID and s.GRADE_FOUR in ('逾期','呆滞','呆账')
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID  
                where f.ACCT_TYPE='4' and f.DATE_ID=%s %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sale_code,sale_name) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.s_date,filterstr,self.id)
        row8a = self.engine.execute(sql8a.encode('utf-8'),vlist).fetchall()
        print '资产管理OK'
        #丰收两卡合同新增户数(当前 月初)
        sql9 =u"""
                select user_name,name,nvl(amt,0),branch_code,branch_name from 
                (select sale_code,count(1) as amt from F_DEBIT_CARD_STATUS f
                join D_DEBIT_CARD c on f.CARD_ID=c.ID and c.CARD_NATURE in ('支农贷款卡','丰收创业贷款卡') and c.OPEN_DATE>=%s and c.OPEN_DATE<%s and f.STATUS='正常'
                join D_ACCOUNT a on c.ACCOUNT_NO=a.ACCOUNT_NO
                join F_BALANCE b on b.ACCOUNT_ID=a.ID and b.DATE_ID=%s
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=b.MANAGE_ID and MANAGE_TYPE='员工管理'
                where f.DATE_ID=%s %s
                group by sale_code) a
                right join teller d on d.user_name = a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.tm_date,self.s_date,self.s_date,self.s_date,filterstr,filterstr3)
        row9 = self.engine.execute(sql9.encode('utf-8'),vlist+vlist3).fetchall()
        print '两卡新增OK'
        #驻勤(驻村)工作
        sql10 =u"""
                select branch_code,branch_name,user_name,name,nvl(amt,0) from 
                (select org_code,staff_code,sum(times) amt
                from village_input
                where 1=1 %s
                group by org_code,staff_code) a
                right join teller t on t.user_name = a.staff_code
                where 1=1 %s
                order by branch_code,user_name
                """%(self.filter,self.id)
        print sql10
        row10 = self.engine.execute(sql10.encode('utf-8')).fetchall()

        i=-1
        rr=[]
        while True:
            i+=1
            if i>=len(row):
                 break
            #对公对私贷款日均
            loan_public=int(row2a[i][2])/self.dd-int(row2[i][2])/days
            loan_private=int(row3a[i][2])/self.dd-int(row3[i][2])/days

            #小额信用户数占比(若其中一个为零,占比赋0)
            if row7[i][2] and row7a[i][2]:
                rate=round(int(row7[i][2])*100/int(row7a[i][2]),2)
            else:
                rate=0

            #小额信用余额占比(若其中一个为零,占比赋0)
            if row7b[i][2] and row7c[i][2]:
                rate1=round(int(row7b[i][2])*100/int(row7c[i][2]),2)
            else:
                rate1=0
            c1 = self.trans_dec(row[i][2])
            c2 = self.trans_dec(rowa[i][2])
            c3 = self.trans_dec(row1[i][2])
            c4 = self.trans_dec(row1a[i][2])
            c5 = self.trans_dec(loan_public)
            c6 = self.trans_dec(loan_private)
            c7 = self.trans_dec(row4[i][2])
            c8 = self.trans_dec(row5[i][2])
            c9 = rate
            c10 = rate1
            c11 = self.trans_dec(row8[i][2])
            c12 = self.trans_dec(row8a[i][2])
            c13 = '0'#self.trans_dec()
            c14 = self.trans_dec(row9[i][2])
            c15 = '0'#self.trans_dec()
            c16 = self.trans_dec(row10[i][4])
            rr.append((ym,row[i][3],row[i][4],row[i][0],row[i][1],c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16))
        needtrans={}
        return self.translate(rr,needtrans)
    def make_eq_filterstr(self):
        filterstr = ""
        filterstr1 = ""
        filterstr2 = ""
        filterstr3 = ""
        ym = ""
        org = ""
        vlist = []
        vlist3 = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k=='id':
                    filterstr = filterstr+" and %s = ? "%'sm.SALE_CODE'
                    filterstr1 = filterstr1+" and %s = ? "%'MANAGER_CODE'
                    filterstr2 = filterstr2+" and %s = ? "%v
                    filterstr3 = filterstr3+" and user_name = ? "
                    vlist.append(v)
                    vlist3.append(v)
                    self.id=v
                if k=='org':
                    vvv = self.dealfilterlist(v)
                    #filterstr = filterstr+" and %s = ? "%'sm.THIRD_BRANCH_CODE'
                    filterstr = filterstr+" and sm.THIRD_BRANCH_CODE IN( %s ) "%(vvv)
                    #filterstr1 = filterstr1+" and %s = ? "%'THIRD_ORG_CODE'
                    filterstr1 = filterstr1+" and THIRD_ORG_CODE IN( %s ) "%(vvv)
                    #filterstr2 = filterstr2+" and %s = ? "%'l.STAT_BRANCH_CODE'
                    filterstr2 = filterstr2+" and l.STAT_BRANCH_CODE IN( %s )"%(vvv)
                    #filterstr3 = filterstr3+" and branch_code = ? "
                    filterstr3 = filterstr3+" and branch_code in( %s )"%(vvv)
                    #vlist.append(v)
                    #vlist3.append(v)
                    self.org = v
                if k=='S_DATE':
                    self.s_date=int(v)
                    self.ly = int(v[0:4])-1
                    self.yy = int(v[0:4])
                    self.mm = int(v[4:6])
                    self.dd = int(v[6:8])
                    self.ly_date=(int(v[0:4])-1)*10000+1231
                    self.tm_date=(int(v[0:6]))*100+01
                    self.yy=int(v[0:4])
                    ym = v[0:6]
        if self.id<>"":
            self.id = " and d.user_name="+self.id+" "
            self.filter = " and staff_code ="+self.id+" "
        if self.org<>"":
            self.id = " and branch_code in (%s) "%(self.org)
            self.filter = " and org_code in (%s) "%(self.org)
        return filterstr,filterstr1,filterstr2,filterstr3,vlist3,vlist,ym
    def column_header(self):
        return ["统计年月","机构号","机构名称","客户经理号","客户经理名称","对公管贷户数","对私管贷户数","对公管贷余额","对私管贷余额","对公贷款增量","对私贷款增量","对公扩面增量","对私扩面增量","小额信用贷款户数占比","小额信用贷余额占比","资产不良贷款户数","资产不良贷款余额","两卡办贷率","丰收两卡合同新增户数","电子档案信息采集率","驻勤(驻村)工作"]
    def trans_dec(self,num):
        tmp = Decimal(num)
        tmp = '{:,}'.format(tmp)
        return tmp
    @property
    def page_size(self):
        return 15

