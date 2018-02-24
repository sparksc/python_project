# -*- coding:utf-8 -*-
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
客户经理贷款绩效佣金报表
"""

class Query(ObjectQuery):
  
    def prepare_object(self):
        filterlist1 = ['yearend_id','jgbhh1','ygghh1']
        filterlist2 = ['year','jgbhh','ygghh']
        filterlist3 = ['year','month','jgbhh','ygghh']
        filterlist6 = []
        global ny
        filterstr,vlist,ny = self.make_eq_filterstr(filterlist1)
        filterstr2,vlist2,ny2 = self.make_eq_filterstr(filterlist2)
        filterstr3,vlist3,ny3 = self.make_eq_filterstr(filterlist3)
        filterstr4,vlist4,ny3 = self.make_eq_filterstr(filterlist3)
        filterstr6,vlist6,ny3 = self.make_eq_filterstr(filterlist6)
        sql1="""
        select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sm.SALE_CODE,sm.SALE_NAME,count(f.CST_NO) cst_num
        from F_BALANCE f
        join D_DATE d on f.DATE_ID=d.ID 
        join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID 
        where f.ACCT_TYPE='4' %s
        group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sm.SALE_CODE,sm.SALE_NAME
        """%(filterstr)
        row = self.engine.execute(sql1,vlist).fetchall()
        sql2="""
        SELECT THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME, YEAR_DAYS,sum(sun_balance) as clye
        FROM YDW.M_COM_DEP
        where ACCT_TYPE ='4' %s
        group by THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME, MONTH_DAYS, YEAR_DAYS
        """%(filterstr2)
        row2 = self.engine.execute(sql2,vlist2).fetchall()
        sql3="""
        SELECT THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME,sum(count_cst) as xx
        FROM YDW.M_COM_DEP
        where ACCT_TYPE ='4' AND ACCOUNT_OWNER_TYPE='对私' %s
        group by THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME
        """%(filterstr3)
        row3 = self.engine.execute(sql3,vlist3).fetchall()
        sql4="""
        SELECT THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME,sum(count_cst) as xx
        FROM YDW.M_COM_DEP
        where ACCT_TYPE ='4' AND ACCOUNT_OWNER_TYPE='对公' %s
        group by THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME
        """%(filterstr4)
        row4 = self.engine.execute(sql4,vlist4).fetchall()
        sql5="""
        SELECT THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME,sum(SUN_BALANCE) loan_sum 
        FROM YDW.M_COM_DEP
        where ACCT_TYPE ='4' %s 
        group by THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME
        """%(filterstr6)
        row5 = self.engine.execute(sql5,vlist6).fetchall()
        """"两卡"""
        sql6 =u"""
        select l.STAT_BRANCH_CODE,count(distinct CUSTID) 
        from F_C_ACCTJRNL f
        join D_T_CHANNEL d on f.CHANNELID = d.ID and d.CHANNELNO in ('IE','AT','ME')
        join D_ACCT_TRAN_TYPE t on f.ACCTTRANTYPEID = t.ID and t.TRANS_CLASSIFY='L'
        join D_LOAN_ACCOUNT l on l.ID = f.ACCTID
        join D_DEBIT_CARD c on l.DEP_ACCOUNT=c.CARD_NO and c.CARD_NATURE in ('支农贷款卡','丰收创业贷款卡')
        where 1=1
        group by l.STAT_BRANCH_CODE
        """
        row6 = self.engine.execute(sql6.encode('utf-8')).fetchall()
        """电子档案手工录入，这里写0"""
        """参数查询"""
        sql7=u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_key='GDHSJJ' or TYPE_key='GDXCJJ' or TYPE_key='DSZHKM'
        or TYPE_KEY='DKDGZHKM' or TYPE_KEY='DKRJZLXC'  or TYPE_KEY='LDKZQBDL'
        or TYPE_KEY='DDXCJ'
        """
        row7 = self.engine.execute(sql7.encode('utf-8')).fetchall()
        for qm in row7:
            if qm[0]==u'贷款管贷户数计价参数':
                cs1=float(qm[1])
            if qm[0]==u'贷款管贷效酬计价参数':
                cs2=float(qm[1])
            if qm[0]==u'贷款对私增户扩面效酬计价参数':
                cs3=float(qm[1])
            if qm[0]==u'贷款对公增户扩面效酬计价参数':
                cs4=float(qm[1])
            if qm[0]==u'贷款日均增量效酬计价参数':
                cs5=float(qm[1])
            if qm[0]==u'两卡达标率':
                cs61=float(qm[1])
            if qm[0]==u'两卡单价':
                cs62=float(qm[1])
            if qm[0]==u'电子单价':
                cs71=float(qm[1])
            if qm[0]==u'电子单价':
                cs72=float(qm[1])
        needtrans ={}
        i=0
        resultrow=[]
        if(len(row2)>0):
            year_days=row2[0][4]
            while True:
                r1=ny
                r2=row2[i][2]
                """r2员工号"""
                r3=row2[i][3]
                r4=row2[i][0]
                r5=row2[i][1]
                r6=r7=r8=r9=r10=r11=r12=r13=0.00
                for mm in row:
                    if(int(r2)==int(mm[2])):
                        r6=round(float(mm[4])*cs1,2)
                        break
                r7=round(float(row2[i][5])/year_days/10000/100*cs2,2)
                for mm in row3:
                    if(int(r2)==int(mm[2])):
                        r8=round(float(mm[4])*cs3/year_days,2)
                        break
                for mm in row4:
                    if(int(r2)==int(mm[2])):
                        r9=round(float(mm[4])*cs4/year_days,2)
                        break
                for mm in row5:
                    if(int(r2)==int(mm[2])):
                        r10=round(float(mm[4])/year_days/10000/100*cs5,2)
                        break
                for mm in row6:
                    if(int(r1)==int(mm[0])):
                        r11=round(float(mm[1])*20*cs62,2)
                        break
                r13=round(r6+r7+r8+r9+r10+r11+r12,2) 
                
                resultrow.append((r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13))
                i=i+1
                if i>=len(row2):
                    break
        return self.translate(resultrow,needtrans)
    
    def make_eq_filterstr(self,filterlist):
        filterstr =""
        vlist = []
        global yearmonth
        for k,v in self.args.items():
            if(k=='tdate'):
                if(len(v)!=8):
                    v='10000101'
                yearmonth=int(v)/100
            if(k=='ygbhh'):
                ygbh=v
            if(k=='jgbhh'):
                jgbh=v

            if v and k in filterlist:
                if(k=='jgbhh'):
                    filterstr = filterstr+" and THIRD_BRANCH_CODE = ? "
                    vlist.append(v)
                if(k=='ygghh'):
                    filterstr = filterstr+" and SALE_CODE = ? "
                    vlist.append(v)
        for k in filterlist:
            if (k=='month'):
                v=yearmonth%100
                filterstr = filterstr+" and %s = ? "%k
                vlist.append(v)
            if (k=='year'):
                v=yearmonth/100
                filterstr = filterstr+" and %s = ? "%k
                vlist.append(v)
            if (k=='yearend_id'):
                v=yearmonth/100
                v=v*10000+1231
                filterstr = filterstr+" and d.id = ? "
                vlist.append(v)
            if (k=='jgbhh1'):
                v=jgbh
                filterstr = filterstr+" and sm.THIRD_BRANCH_CODE = ? "
                vlist.append(v)
            if (k=='ygbhh1'):
                v=ygbh
                filterstr = filterstr+" and sm.SAKE_CODE = ? "
                vlist.append(v)
        return filterstr,vlist,yearmonth


    def column_header(self):
        return ["统计月份","员工号","员工名称","机构号","机构名称","管贷户数效酬","管贷余额效酬","对私增户扩面效酬","对公增户扩面效酬","贷款日均增量效酬","两卡贷款客户电子渠道办贷率效酬","电子档案信息采集效酬","贷款总效酬"]

    @property
    def page_size(self):    
        return 15
