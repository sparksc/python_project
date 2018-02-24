# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
机构贷款指标报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.org = ""
        self.filterlist = ['org','S_DATE']
        filterstr,filterstr1,filterstr2,filterstr3,vlist = self.make_eq_filterstr()
        #管贷户数
        sql =u"""
                select branch_code,branch_name,nvl(amt,0) from 
                (select third_branch_code,count(distinct cst_no) amt
                from f_balance f
                inner join d_sale_manage_rela m on m.manage_id=f.manage_id
                inner join d_account_type t on t.id=f.account_type_id and account_owner_type='对公'
                where acct_type='4' and balance>500000 and date_id=%s 
                group by third_branch_code) a
                right join branch b on b.branch_code=a.third_branch_code
                where 1=1 %s
                order by branch_code
                """%(self.s_date,self.org)
        row = self.engine.execute(sql,vlist).fetchall()
        sqla =u"""
                select branch_code,branch_name,nvl(amt,0) from 
                (select third_branch_code,count(distinct cst_no) amt
                from f_balance f
                inner join d_sale_manage_rela m on m.manage_id=f.manage_id
                inner join d_account_type t on t.id=f.account_type_id and account_owner_type='对私'
                where acct_type='4' and balance>500000 and date_id=%s 
                group by third_branch_code) a
                right join branch b on b.branch_code=a.third_branch_code
                where 1=1 %s
                order by branch_code
                """%(self.s_date,self.org)
        rowa = self.engine.execute(sqla,vlist).fetchall()
        #管贷余额
        sql1 =u"""
                 select branch_code,branch_name,nvl(amt,0) from
                 (select third_branch_code,sum(balance) amt
                 from f_balance f
                 inner join d_sale_manage_rela m on m.manage_id=f.manage_id
                 inner join d_account_type t on t.id=f.account_type_id and account_owner_type='对公'
                 where f.acct_type='4' and f.balance>500000 and date_id=%s
                 group by third_branch_code) a 
                 right join branch b on b.branch_code=a.third_branch_code
                 where 1=1 %s
                 order by branch_code 
                 """%(self.s_date,self.org)
        row1 = self.engine.execute(sql1,vlist).fetchall()
        sql1a =u"""
                 select branch_code,branch_name,nvl(amt,0) from
                 (select third_branch_code,sum(balance) amt
                 from f_balance f
                 inner join d_sale_manage_rela m on m.manage_id=f.manage_id
                 inner join d_account_type t on t.id=f.account_type_id and account_owner_type='对私'
                 where f.acct_type='4' and f.balance>500000 and date_id=%s
                 group by third_branch_code) a 
                 right join branch b on b.branch_code=a.third_branch_code
                 where 1=1 %s
                 order by branch_code 
                 """%(self.s_date,self.org)
        row1a = self.engine.execute(sql1a,vlist).fetchall()
        #管贷余额日均增量
        sql2 =u"""
                select branch_code,branch_name,nvl(amt,0) from (
                select THIRD_BRANCH_CODE,third_branch_name,sum(sun_balance) amt
                from m_com_dep sm where account_owner_type='对公' and acct_type='4' and year=%s %s
                group by THIRD_BRANCH_CODE,third_branch_name) a
                right join branch b on b.branch_code = a.third_branch_code 
                where 1=1 %s
                order by branch_code 
                """%(self.ly,filterstr,self.org)
        row2 = self.engine.execute(sql2,vlist).fetchall()
        sql3 =u"""
                select branch_code,branch_name,nvl(amt,0) from (
                select THIRD_BRANCH_CODE,third_branch_name,sum(sun_balance) amt
                from m_com_dep sm where account_owner_type='对私' and acct_type='4' and year=%s %s
                group by THIRD_BRANCH_CODE,third_branch_name) a
                right join branch b on b.branch_code = a.third_branch_code 
                where 1=1 %s
                order by branch_code 
                """%(self.ly,filterstr,self.org)
        row3 = self.engine.execute(sql3,vlist).fetchall()
        sql2a =u"""
                select branch_code,branch_name,nvl(amt,0) from (
                select THIRD_BRANCH_CODE,third_branch_name,sum(sun_balance) amt
                from m_com_dep sm where account_owner_type='对公' and acct_type='4' and year=%s and month=%s %s
                group by THIRD_BRANCH_CODE,third_branch_name) a
                right join branch b on b.branch_code = a.third_branch_code 
                where 1=1 %s
                order by branch_code 
                """%(self.yy,self.mm,filterstr,self.org)
        row2a = self.engine.execute(sql2a,vlist).fetchall()
        sql3a =u"""
                select branch_code,branch_name,nvl(amt,0) from (
                select THIRD_BRANCH_CODE,third_branch_name,sum(sun_balance) amt
                from m_com_dep sm where account_owner_type='对私' and acct_type='4' and year=%s and month=%s %s
                group by THIRD_BRANCH_CODE,third_branch_name) a
                right join branch b on b.branch_code = a.third_branch_code 
                where 1=1 %s
                order by branch_code 
                """%(self.yy,self.mm,filterstr,self.org)
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
        
        #对公增户扩面增量
        sql4 =u"""
                select branch_code,branch_name,nvl(amt,0) from 
                (select  THIRD_BRANCH_CODE,THIRD_BRANCH_NAME,sum(cst_num)/count(DAY) as amt
                from(
                select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,count(f.CST_NO) cst_num,d.DAY from F_BALANCE f
                join D_DATE d on f.DATE_ID=d.ID and d.DAY in (5,15,25)
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID 
                where f.ACCT_TYPE='4' and left(f.CST_NO,2)='82' and f.DATE_ID>=%s and f.DATE_ID<=%s %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,d.DAY)
                group by THIRD_BRANCH_CODE,THIRD_BRANCH_NAME) a
                right join branch b on b.branch_code=a.third_branch_code
                where 1=1 %s
                order by branch_code
                """%(self.tm_date,self.s_date,filterstr,self.org)
        row4 = self.engine.execute(sql4.encode('utf-8'),vlist).fetchall()
        #对私增户扩面增量
        sql5 =u"""
                select branch_code,branch_name,nvl(amt,0) from
                (select  THIRD_BRANCH_CODE,THIRD_BRANCH_NAME,sum(cst_num)/count(DAY) as amt
                from(
                select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,count(f.CST_NO) cst_num,d.DAY from F_BALANCE f
                join D_DATE d on f.DATE_ID=d.ID and d.DAY in (5,15,25)
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID 
                where f.ACCT_TYPE='4' and left(f.CST_NO,2)='83' and f.DATE_ID>=%s and f.DATE_ID<%s %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,d.DAY)
                group by THIRD_BRANCH_CODE,THIRD_BRANCH_NAME) a
                right join branch b on b.branch_code=a.third_branch_code
                where 1=1 %s
                order by branch_code
                """%(self.tm_date,self.s_date,filterstr,self.org)
        row5 = self.engine.execute(sql5.encode('utf-8'),vlist).fetchall()
        #两卡贷款客户电子渠道办贷率
        sql6 =u"""
                select branch_code,branch_name,nvl(amt,0) from 
                (select l.STAT_BRANCH_CODE as ORG,count(distinct CUSTID) as amt 
                from F_C_ACCTJRNL f
                join D_T_CHANNEL d on f.CHANNELID = d.ID and d.CHANNELNO in ('IE','AT','ME')
                join D_ACCT_TRAN_TYPE t on f.ACCTTRANTYPEID = t.ID and t.TRANS_CLASSIFY='L'
                join D_LOAN_ACCOUNT l on l.ID = f.ACCTID
                join D_DEBIT_CARD c on l.DEP_ACCOUNT=c.CARD_NO and c.CARD_NATURE in ('支农贷款卡','丰收创业贷款卡')
                where f.TRANDATEID>=%s and f.TRANDATEID<=%s %s
                group by l.STAT_BRANCH_CODE) a
                right join branch b on b.branch_code=a.ORG
                where 1=1 %s
                order by branch_code
                """%(self.tm_date,self.s_date,filterstr2,self.org)
        row6 = self.engine.execute(sql6.encode('utf-8'),vlist).fetchall()
        #电子档案信息采集率
            #手工录入
        #小额信用贷款户数占比指标(户数)
        sql7 =u"""
                select branch_code,branch_name,nvl(cst_num,0) from (
                select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,count(f.CST_NO) cst_num from F_BALANCE f 
                join D_DATE d on f.DATE_ID=d.ID
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID 
                join D_ACCOUNT_TYPE t on t.ID=f.ACCOUNT_TYPE_ID 
                where f.ACCT_TYPE='4' and t.gua_tp_name='信用' and f.date_id=%s %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME
                having count(f.BALANCE)<=30000000) a
                right join branch b on a.third_branch_code = b.branch_code
                where 1=1 %s
                order by branch_code
                """%(self.s_date,filterstr,self.org)
        row7 = self.engine.execute(sql7.encode('utf-8'),vlist).fetchall()
        sql7a =u"""
                select branch_code,branch_name,nvl(cst_num,0) from (
                select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,count(f.CST_NO) cst_num from F_BALANCE f 
                join D_DATE d on f.DATE_ID=d.ID
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID 
                join D_ACCOUNT_TYPE t on t.ID=f.ACCOUNT_TYPE_ID 
                where f.ACCT_TYPE='4' and f.date_id=%s %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME
                having count(f.BALANCE)<=30000000) a
                right join branch b on a.third_branch_code = b.branch_code
                where 1=1 %s
                order by branch_code
                """%(self.s_date,filterstr,self.org)
        row7a = self.engine.execute(sql7a.encode('utf-8'),vlist).fetchall()
        #小额信用贷款户数占比指标(余额)
        sql7b =u"""
                select branch_code,branch_name,nvl(amt,0) from (
                select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sum(f.balance) amt from F_BALANCE f 
                join D_DATE d on f.DATE_ID=d.ID
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID 
                join D_ACCOUNT_TYPE t on t.ID=f.ACCOUNT_TYPE_ID 
                where f.ACCT_TYPE='4' and t.gua_tp_name='信用' and f.date_id=%s %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME
                having count(f.BALANCE)<=30000000) a
                right join branch b on a.third_branch_code = b.branch_code
                where 1=1 %s
                order by branch_code
                """%(self.s_date,filterstr,self.org)
        row7b = self.engine.execute(sql7b.encode('utf-8'),vlist).fetchall()
        sql7c =u"""
                select branch_code,branch_name,nvl(amt,0) from (
                select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sum(f.balance) amt from F_BALANCE f 
                join D_DATE d on f.DATE_ID=d.ID
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID 
                join D_ACCOUNT_TYPE t on t.ID=f.ACCOUNT_TYPE_ID 
                where f.ACCT_TYPE='4' and f.date_id=%s %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME
                having count(f.BALANCE)<=30000000) a
                right join branch b on a.third_branch_code = b.branch_code
                where 1=1 %s
                order by branch_code
                """%(self.s_date,filterstr,self.org)
        row7c = self.engine.execute(sql7c.encode('utf-8'),vlist).fetchall()
        #资产管理质量(余额)
        sql8 =u"""
                select branch_code,branch_name,nvl(amt,0) from( 
                select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sum(f.BALANCE) amt from F_BALANCE f 
                join D_DATE d on f.DATE_ID=d.ID
                join D_ACCOUNT_STATUS s on f.ACCOUNT_STATUS_ID=s.ID and s.GRADE_FOUR in ('逾期','呆滞','呆账')
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID  
                where f.ACCT_TYPE='4' and f.DATE_ID=%s %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME) a
                right join branch b on b.branch_code=a.third_branch_code 
                where 1=1 %s
                order by branch_code
                """%(self.s_date,filterstr,self.org)
        row8 = self.engine.execute(sql8.encode('utf-8'),vlist).fetchall()
        #资产管理质量(户数)
        sql8a =u"""
                select branch_code,branch_name,nvl(amt,0) from( 
                select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,count(cst_no) amt from F_BALANCE f 
                join D_DATE d on f.DATE_ID=d.ID
                join D_ACCOUNT_STATUS s on f.ACCOUNT_STATUS_ID=s.ID and s.GRADE_FOUR in ('逾期','呆滞','呆账')
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID  
                where f.ACCT_TYPE='4' and f.DATE_ID=%s %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME) a
                right join branch b on b.branch_code=a.third_branch_code 
                where 1=1 %s
                order by branch_code
                """%(self.s_date,filterstr,self.org)
        row8a = self.engine.execute(sql8a.encode('utf-8'),vlist).fetchall()
        #丰收两卡合同新增户数
        sql9 =u"""
                select branch_code,branch_name,nvl(amt,0) from 
                (select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,count(1) amt from F_DEBIT_CARD_STATUS f
                join D_DEBIT_CARD c on f.CARD_ID=c.ID and c.CARD_NATURE in ('支农贷款卡','丰收创业贷款卡') and c.OPEN_DATE>= %s and c.OPEN_DATE<= %s and f.STATUS='正常'
                join D_ACCOUNT a on c.ACCOUNT_NO=a.ACCOUNT_NO
                join F_BALANCE b on b.ACCOUNT_ID=a.ID and b.DATE_ID = %s
                join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=b.MANAGE_ID 
                where 1=1  %s
                group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME
                order by sm.THIRD_BRANCH_CODE) a 
                right join branch b on b.branch_code=a.third_branch_code
                where 1=1 %s
                order by branch_code
                """%(self.tm_date,self.s_date,self.s_date,filterstr,self.org)
        row9 = self.engine.execute(sql9.encode('utf-8'),vlist).fetchall()

        #驻勤(驻村)工作
        sql10 =u"""
                select branch_code,branch_name,nvl(amt,0) from 
                (select org_code,sum(times) amt
                from village_input
                where 1=1 %s
                group by org_code) a
                right join branch b on b.branch_code=a.org_code
                where 1=1 %s
                order by branch_code
                """%(filterstr3,self.org)
        row10 = self.engine.execute(sql10.encode('utf-8'),vlist).fetchall()

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
            c16 = self.trans_dec(row10[i][2])
            # 字段说明:1 对公管贷户数 2 对私管贷户数 3 对公管贷余额 4 对私管贷余额 5 对公贷款增量 6 对私贷款增量 7 对公扩面增量 8 对私扩面增量 9 小额户数占比 10 小额余额占比 11 资产不良户数 12 资产不良余额 13 两卡办贷率 14 丰收两卡新增户数 15 电子档案采集率 16 驻勤驻村
            rr.append((self.ym,row[i][0],row[i][1],c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16))
        needtrans={}
        return self.translate(rr,needtrans)
    def make_eq_filterstr(self):
        filterstr,filterstr1,filterstr2,filterstr3 ="","","", ""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k=='org':
                    if(v[0:1] == 'M'):
                        filterstr = filterstr+" and sm.THIRD_BRANCH_CODE in(select branch_code from branch where parent_id in (select role_id from branch where branch_code='%s'))"%v
                        filterstr1 = filterstr1+" and THIRD_ORG_CODE in(select branch_code from branch where parent_id in (select role_id from branch where branch_code='%s'))"%v
                        filterstr2 = filterstr2+" and l.STAT_BRANCH_CODE in(select branch_code from branch where parent_id in (select role_id from branch where branch_code='%s'))"%v
                        filterstr3 = filterstr3+" and ORG_CODE in(select branch_code from branch where parent_id in (select role_id from branch where branch_code='%s'))"%v
                        self.org="select branch_code from branch where parent_id in (select role_id from branch where branch_code='%s')"%v

                    else:
                        vv = self.dealfilterlist(v)
                        filterstr = filterstr+" and %s in (%s) "%('sm.THIRD_BRANCH_CODE', vv)
                        filterstr1 = filterstr1+" and %s in (%s) "%('THIRD_ORG_CODE', vv)
                        filterstr2 = filterstr2+" and %s in (%s) "%('l.STAT_BRANCH_CODE', vv)
                        filterstr3 = filterstr3+" and %s in (%s) "%('ORG_CODE', vv)
                        self.org=vv
                if k=='S_DATE':
                    self.s_date=int(v)
                    self.ym=int(v[0:6])
                    self.ly=int(v[0:4])-1
                    self.yy=int(v[0:4])
                    self.mm=int(v[4:6])
                    self.dd=int(v[6:8])
                    self.ly_date=(int(v[0:4])-1)*10000+1231
                    self.tm_date=(int(v[0:6]))*100+01
                    self.date=int(v)
        if self.org<>"":
            self.org = " and branch_code in (%s)" %(self.org)
        return filterstr,filterstr1,filterstr2,filterstr3,vlist
    def column_header(self):
        return ["统计年月","机构号","机构名称","对公管贷户数","对私管贷户数","对公管贷余额","对私管贷余额","对公贷款增量","对私贷款增量","对公扩面增量","对私扩面增量","小额信用贷款户数占比","小额信用贷余额占比","资产不良贷款户数","资产不良贷款余额","两卡办贷率","丰收两卡合同新增户数","电子档案信息采集率","驻勤(驻村)工作"]
    def trans_dec(self,num):
        tmp = Decimal(num)
        tmp = '{:,}'.format(tmp)
        return tmp
    @property
    def page_size(self):
        return 15
