# -*- coding:utf-8 -*-
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
客户经理国际业务佣金报表
"""

class Query(ObjectQuery):
  
    def prepare_object(self):
        filterlist1 = ['date_ym','jgbhh','ygghh']
        filterlist2 = ['rq']
        filterlist3 = ['SPCCDATE']
        filterlist6 = []
        global r1
        filterstr,vlist = self.make_eq_filterstr(filterlist1)
        filterstr2,vlist2 = self.make_eq_filterstr(filterlist2)
        filterstr3,vlist3 = self.make_eq_filterstr(filterlist3)
        filterstr6,vlist6 = self.make_eq_filterstr(filterlist6)
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

        """参数查询"""
        sql7=u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where  TYPE_KEY='JSHLJJ'  or TYPE_KEY='GJJSL' or type_key='XKWHZH'
        """
        row7 = self.engine.execute(sql7.encode('utf-8')).fetchall()
        for qm in row7:
            if qm[0]==u'国际结算量效酬计价参数':
                cs1=float(qm[1])
            if qm[0]==u'结售汇量效酬计价参数':
                cs2=float(qm[1])
            if qm[0]==u'新开有效外汇账户效酬计价参数':
                cs3=float(qm[1])
        
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
                p1=round(r22*cs1/10000,2)
                p2=round(r23*cs1/10000,2)
                qp1=qp2=qp3=qp4=qp5=qp6=qp7=qp8=0.00
                for mm in row3:
                    if(int(r4)==int(mm[2])):
                        qp3=round(float(mm[5])*float(mm[3]/dhhl),2)
                        qp4=round(float(mm[5])*float(mm[3]),2)
                qp7=round(qp1+qp3+qp5,2)
                qp8=round(qp2+qp4+qp6,2)
                p3=round(qp7*cs2/10000/100,2)
                p4=round(qp8*cs2/10000/100,2)
                p5=p6=0.00
                p7=round(p1+p3+p5,2)
                #p2,p4,p6,为对应的cny金额
                resultrow.append((r1,r2,r3,r4,r5,p1,p3,p5,p7,))
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
                    ymday='10000101'
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
        return filterstr,vlist
    
        
    def column_header(self):
        return ["统计月份","机构号","机构名称","员工编号","员工姓名","国际结算量效酬USD","结售汇量效酬USD","新开有效外汇账户效酬USD","国际业务总效酬USD"] 
    @property
    def page_size(self):
        return 15
