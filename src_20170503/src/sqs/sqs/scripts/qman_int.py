# -*- coding:utf-8 -*-
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
客户经理国际业务指标报表
"""

class Query(ObjectQuery):
  
    def prepare_object(self):
        filterlist1 = ['date_ym','jgbhh','ygghh']
        filterlist4 = ['year','jgbhh','ygghh']
        filterlist2 = ['rq']
        filterlist3 = ['SPCCDATE']
        filterlist6 = []

        filterstr,vlist,ny = self.make_eq_filterstr(filterlist1)
        filterstr2,vlist2,ny2 = self.make_eq_filterstr(filterlist2)
        filterstr3,vlist3,ny3 = self.make_eq_filterstr(filterlist3)
        filterstr4,vlist4,ny4 = self.make_eq_filterstr(filterlist4)
        filterstr6,vlist6,ny3 = self.make_eq_filterstr(filterlist6)
        sql="""
        select f.DATE_YM,sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sm.SALE_CODE,sm.SALE_NAME,SUM(EXBPAMT),SUM(EXAGENTAMT),SUM(EXINREMITAMT),SUM(IMLCAMT),SUM(IMICAMT),SUM(IMOUTREMTIAMT),SUM(FIINREMITAMT),SUM(FIOUTREMITAMT)
        from F_EBILLS_QRY_SETTLEMENT_CORP f
        inner join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID
        where 1=1 %s
        group by f.DATE_YM,sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sm.SALE_CODE,sm.SALE_NAME
        order by f.DATE_YM,sm.THIRD_BRANCH_CODE,sm.SALE_CODE
        """%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        sql3="""
        select SPCACCYC,SPCASTAF,SPCABRNO,SPCAEXRT,SPCCDATE,sum(SPCAAMT) 
        from F_CORE_AFFMSPTS
        where (SPCATDTP='1' or SPCATDTP='2') %s
        group by SPCATDTP,SPCACCYC,SPCASTAF,SPCABRNO,SPCAEXRT,SPCCDATE
        """%(filterstr3)
        row3 = self.engine.execute(sql3,vlist3).fetchall()
        sql4="""
        select sm.THIRD_BRANCH_CODE,sm.SALE_CODE,d.YEAR_DAYS,sum(balance) as clye
        from F_BALANCE f
        join D_DATE d on f.DATE_ID=d.ID and d.day<02
        join D_ACCOUNT a on a.ID =f.ACCOUNT_ID and a.ccy<>'CNY' and a.CCY<>'000'
        join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID 
        where f.ACCT_TYPE='1' and f.DATE_ID>=20150101 and f.DATE_ID<20150116 %s
        group by sm.THIRD_BRANCH_CODE,sm.SALE_CODE,d.YEAR_DAYS
        """%(filterstr4)
        row4 = self.engine.execute(sql4,vlist4).fetchall()
        """美元汇率dhhl"""
        dhhl=6.5723
        sql8="""
        select SMCACUNO,SMCAEXRT
        from D_CORE_AFFMSMBD
        where SMCACCYC='USD' %s
        """%(filterstr2)
        row8 = self.engine.execute(sql8,vlist2).fetchall()
        if(len(row8)>0):
            dhhl=float(row8[0][1])/float(row8[0][0])
        needtrans ={}
        i=0
        resultrow=[]
        if(len(row)>0):
            while True:
                r1=row[i][0]
                r2=row[i][1]
                r3=row[i][2]
                r4=row[i][3]
                """r4是员工号"""
                r5=row[i][4]
                r6=round(float(row[i][5])/dhhl/100,2) 
                r7=round(float(row[i][5])/100,2) 
                r8=round(float(row[i][6])/dhhl/100,2) 
                r9=round(float(row[i][6])/100,2) 
                r10=round(float(row[i][7])/dhhl/100,2) 
                r11=round(float(row[i][7])/100,2) 
                r12=round(float(row[i][8])/dhhl/100,2) 
                r13=round(float(row[i][8])/100,2) 
                r14=round(float(row[i][9])/dhhl/100,2) 
                r15=round(float(row[i][9])/100,2) 
                r16=round(float(row[i][10])/dhhl/100,2) 
                r17=round(float(row[i][10])/100,2) 
                r18=round(float(row[i][11])/dhhl/100,2) 
                r19=round(float(row[i][11])/100,2) 
                r20=round(float(row[i][12])/dhhl/100,2) 
                r21=round(float(row[i][12])/100,2) 
                r22=round(r6+r8+r10+r12+r14+r16+r18+r20,2)
                r23=round(r7+r9+r11+r13+r15+r17+r19+r21,2)
                p1=p2=p3=p4=p5=p6=p7=p8=0.00
                for mm in row3:
                    if(int(r4)==int(mm[2])):
                        p3=round(float(mm[5])*float(mm[3]/dhhl),2)
                        p4=round(float(mm[5])*float(mm[3]),2)
                p7=round(p1+p3+p5,2)
                p8=round(p2+p4+p6,2)
                p9=p10=p11=p12=p13=0.00#p9,p10,p11,p12需求不知道，计算规则未知
                for mm in row4:
                    if(int(r4)==int(mm[1])):
                        q13=round(float(mm[3])/float(mm[2])/100,2)
                resultrow.append((r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,r18,r19,r20,r21,r22,r23,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13))
                i=i+1
                if i>=len(row):
                    break
        return self.translate(resultrow,needtrans)
    def make_eq_filterstr(self,filterlist):
        filterstr =""
        vlist = []
        
        global yearmonthday
        for k,v in self.args.items():
            if(k=='tdate'):
                if(len(v)!=8):
                    v='10000101'
                yearmonthday=int(v)
            if v and k in filterlist:
                if(k=='jgbhh'):
                    filterstr = filterstr+" and sm.THIRD_BRANCH_CODE = ? "
                    vlist.append(v)
                if(k=='ygghh'):
                    filterstr = filterstr+" and sm.SALE_CODE = ? "
                    vlist.append(v)
        for k in filterlist:
            if (k=='date_ym'):
                v=yearmonthday/100
                filterstr = filterstr+" and f.%s = ? "%k
                vlist.append(v)
            if (k=='rq'):
                v=yearmonthday
                filterstr = filterstr+" and date_id = ? "
                vlist.append(v)
            if (k=='SPCCDATE'):
                qp=str(yearmonthday/10000)+'-'+str(yearmonthday/100%100)+'-'+str(yearmonthday%100)
                filterstr = filterstr+" and %s = ? "%k
                vlist.append(qp)
            if (k=='year'):
                v=yearmonthday/10000
                filterstr = filterstr+" and d.%s = ? "%k
                vlist.append(v)
        return filterstr,vlist,yearmonthday/100
    
    def column_header(self):
        return ["统计月份","机构号","机构名称","员工编号","员工姓名","出口议付USD","出口议付CNY","出口托收USD","出口托收CNY","汇入汇款USD","汇入汇款CNY","进口开证USD","进口开证CNY","进口代收USD","进口代收CNY","汇出汇款USD","汇出汇款CNY","汇入汇款2USD","汇入汇款2CNY","汇出汇款2USD","汇出汇款2CNY","美元合计","人民币合计","远期USD","远期CNY","即期USD","即期CNY","跨境USD","跨境CNY","美元合计2","人民币合计2","当年新开外汇","上年新开外汇","1年以上未发生业务又重启用","合计值","存款日均增量"] 
    @property
    def page_size(self):
        return 15
