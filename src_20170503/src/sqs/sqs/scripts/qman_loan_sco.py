# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
客户经理贷款绩效得分报表
"""

class Query(ObjectQuery):
 
    def prepare_object(self):
        self.filterlist = ['BRANCH_CODE','SALE_CODE','S_DATE']
        filterstr,filterstr1,filterstr2,filterstr4,vlist = self.make_eq_filterstr()
        '''客户经理扩面工作 对公'''
        sql1 =u"""
        SELECT THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME,sum(count_cst) /YEAR_DAYS as d
        FROM YDW.M_COM_DEP
        where ACCT_TYPE ='4' and account_owner_type='对公' and year=%s %s
        group by THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME, YEAR_DAYS
        """%(self.yyear,filterstr)
        row1 = self.engine.execute(sql1.encode('utf-8'),vlist).fetchall()

        '''客户经理扩面工作 对私'''
        sql11 =u"""
        SELECT THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME,sum(count_cst) /YEAR_DAYS as d
        FROM YDW.M_COM_DEP
        where ACCT_TYPE ='4' and account_owner_type='对私' and year=%s %s
        group by THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME, YEAR_DAYS
        """%(self.yyear,filterstr)
        row11 = self.engine.execute(sql11.encode('utf-8'),vlist).fetchall()

        '''扩面工作 计划 '''
        sql_plan1 = u"""
        select THIRD_ORG_CODE,MANAGER_CODE,ES_P_BASE,ES_P_TARGET,ES_C_BASE,ES_NC_BASE from P_LOAN_NUM where 1=1 %s
            """%(filterstr1)
        plan1 = self.engine.execute(sql_plan1.encode('utf-8'),vlist).fetchall()
        
        '''扩面工作 标准分 最高分 最低分 '''
        sql_sco1 = u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_NAME='扩面工作得分参数'
        order by d.DETAIL_VALUE
            """
        sco1 = self.engine.execute(sql_sco1.encode('utf-8'),vlist).fetchall()

        '''管贷奖励分值参数  '''
        sql_sco11 = u"""
        select h.HEADER_NAME,d.DETAIL_VALUE,d.PARA_ROW_ID from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID  
        where TYPE_NAME='管贷奖励分值参数'
        order by d.DETAIL_VALUE
            """
        self.sco11 = self.engine.execute(sql_sco11.encode('utf-8'),vlist).fetchall()

        '''客户经理日均贷款增加额 '''
        sql2 =u"""
        SELECT THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME,sum(sun_balance) /MONTH_DAYS as d
        FROM YDW.M_COM_DEP
        where ACCT_TYPE ='4' and month=%s and year=%s %s
        group by THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME, MONTH_DAYS
        """%(self.ymonth,self.yyear,filterstr)
        row2 = self.engine.execute(sql2.encode('utf-8'),vlist).fetchall()

        '''日均贷款增加额 计划 '''
        sql_plan2 = u"""
        select THIRD_ORG_CODE,MANAGER_CODE,AVE_BASE, AVE_TARGET from P_LOAN_NUM where 1=1 %s
        """%(filterstr1)
        plan2 = self.engine.execute(sql_plan2.encode('utf-8'),vlist).fetchall()
        
        '''日均贷款增加额 标准分 最高分 最低分 '''
        sql_sco2 = u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_NAME='日均贷款增加额得分参数'
        order by d.DETAIL_VALUE
            """
        sco2 = self.engine.execute(sql_sco2.encode('utf-8'),vlist).fetchall()

        '''小额信用贷款 取得 金额参数'''
        sql_num3=u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_NAME='小额贷款金额参数'
        order by d.DETAIL_VALUE
            """
        num3 = self.engine.execute(sql_num3.encode('utf-8'),vlist).fetchall()
        num33 = int(num3[0][1])*1000000
        
        '''客户经理小额信用贷款户数占比 信用'''
        sql3 =u"""
        select  THIRD_BRANCH_CODE,THIRD_BRANCH_NAME,SALE_CODE,SALE_NAME,sum(cst_num) 
        from( 
        select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sm.SALE_CODE,SALE_NAME,count(f.CST_NO) cst_num,d.DAY from F_BALANCE f 
        join D_DATE d on f.DATE_ID=d.ID
        join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID and sm.SALE_ROLE<>'机构管理' 
        join D_ACCOUNT_TYPE t on t.ID=f.ACCOUNT_TYPE_ID and t.GUA_TP_NAME='信用'
        where f.ACCT_TYPE='4' and f.DATE_ID=%s  %s
        group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sm.SALE_CODE,sm.SALE_NAME,d.DAY
        having count(f.BALANCE)<= %s ) 
        group by THIRD_BRANCH_CODE,THIRD_BRANCH_NAME,SALE_CODE,SALE_NAME 
        order by SALE_CODE
            """%(self.s_date,filterstr,num33)
        row3 = self.engine.execute(sql3.encode('utf-8'),vlist).fetchall()
        '''客户经理小额信用贷款户数占比 全部'''
        sql33 =u"""
        select  THIRD_BRANCH_CODE,THIRD_BRANCH_NAME,SALE_CODE,SALE_NAME,sum(cst_num) 
        from( 
        select sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sm.SALE_CODE,SALE_NAME,count(f.CST_NO) cst_num,d.DAY from F_BALANCE f 
        join D_DATE d on f.DATE_ID=d.ID
        join D_SALE_MANAGE_RELA sm on sm.MANAGE_ID=f.MANAGE_ID and sm.SALE_ROLE<>'机构管理' 
        where f.ACCT_TYPE='4' and f.DATE_ID=%s  %s
        group by sm.THIRD_BRANCH_CODE,sm.THIRD_BRANCH_NAME,sm.SALE_CODE,sm.SALE_NAME,d.DAY
        having count(f.BALANCE)<= %s ) 
        group by THIRD_BRANCH_CODE,THIRD_BRANCH_NAME,SALE_CODE,SALE_NAME 
        order by SALE_CODE
            """%(self.s_date,filterstr,num33)
        row33 = self.engine.execute(sql33.encode('utf-8'),vlist).fetchall()
        
        '''小额信用贷款 占比计划'''
        sql_plan3 = u"""
        select THIRD_ORG_CODE,MANAGER_CODE,CRE_M_TARGET, CRE__H_TARGET, CRE__ES_C_H_TARGET from P_LOAN_NUM where 1=1 %s
            """%(filterstr1)
        plan3 = self.engine.execute(sql_plan3.encode('utf-8'),vlist).fetchall()
        
        '''小额信用贷款 标准分 最高分 最低分 '''
        sql_sco3 = u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_NAME='小额信用贷款户数占比指标得分参数'
        order by d.DETAIL_VALUE
            """
        sco3 = self.engine.execute(sql_sco3.encode('utf-8'),vlist).fetchall()


        '''客户经理资产质量管理 上年末'''
        sql4 =u"""
        SELECT THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME,sum(sun_balance) /YEAR_DAYS as d
        FROM YDW.M_COM_DEP
        where ACCT_TYPE ='4'and year=%s and GRADE_FOUR in ('逾期','呆滞','呆账') %s
        group by THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME, YEAR_DAYS
        """%(self.yyear,filterstr)
        row4 = self.engine.execute(sql4.encode('utf-8'),vlist).fetchall()
        '''客户经理资产质量管理 时点值'''
        sql44 =u"""
        SELECT THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME,sum(sun_balance) /MONTH_DAYS as d
        FROM YDW.M_COM_DEP
        where ACCT_TYPE ='4'and MONTH=%s AND year=%s and GRADE_FOUR in ('逾期','呆滞','呆账') %s
        group by THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME, MONTH_DAYS
        """%(self.ymonth,self.yyear,filterstr)
        row44 = self.engine.execute(sql44.encode('utf-8'),vlist).fetchall()
        
        '''资产管理质量得分 标准分 最高分 最低分 '''
        sql_sco4 = u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_NAME='资产管理质量得分参数'
        order by d.DETAIL_VALUE
            """
        sco4 = self.engine.execute(sql_sco4.encode('utf-8'),vlist).fetchall()
        
        '''资产管理质量得分 加扣分参数 '''
        sql_sco44 = u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_NAME='四级不良贷款加扣分参数'
        order by d.DETAIL_VALUE
            """
        sco44 = self.engine.execute(sql_sco44.encode('utf-8'),vlist).fetchall()

        '''资产管理质量得分 得分参数 '''
        sql_sco444 = u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_NAME='四级不良贷款得分参数'
        order by h.HEADER_NAME
            """
        sco444 = self.engine.execute(sql_sco444.encode('utf-8'),vlist).fetchall()

        '''丰收两卡合同新增数 '''
        sql5 =u"""
        select ORG0_CODE,ORG0_NAME,SALE_CODE,SALE_NAME,SUM(AMT)
        FROM M_COM_LIANGKA
        WHERE OPEN_TIME=%s %s
        GROUP BY ORG0_CODE,ORG0_NAME,SALE_CODE,SALE_NAME
        """%(self.yyearmonth,filterstr4)
        row5 = self.engine.execute(sql5.encode('utf-8'),vlist).fetchall()
        
        '''丰收两卡 标准分 最高分 最低分 '''
        sql_sco5 = u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_NAME='丰收两卡合同新增户数得分参数'
        order by h.HEADER_NAME 
            """
        sco5 = self.engine.execute(sql_sco5.encode('utf-8'),vlist).fetchall()
        
        '''丰收两卡 计划'''
        sql_plan5 = u"""
        select THIRD_ORG_CODE,MANAGER_CODE, CARD_BASE, CARD_TARGET from P_LOAN_NUM where 1=1 %s
            """%(filterstr1)
        plan5 = self.engine.execute(sql_plan5.encode('utf-8'),vlist).fetchall()
 
        '''两卡贷款客户电子渠道办贷率 '''
        sql6 =u"""
        select l.STAT_BRANCH_CODE,count(distinct CUSTID) from F_C_ACCTJRNL f
        join D_T_CHANNEL d on f.CHANNELID = d.ID and d.CHANNELNO in ('IE','AT','ME')
        join D_ACCT_TRAN_TYPE t on f.ACCTTRANTYPEID = t.ID and t.TRANS_CLASSIFY='L'
        join D_LOAN_ACCOUNT l on l.ID = f.ACCTID
        join D_DEBIT_CARD c on l.DEP_ACCOUNT=c.CARD_NO and c.CARD_NATURE in ('支农贷款卡','丰收创业贷款卡')
        where f.TRANDATEID >= %s and f.TRANDATEID <= %s %s
        group by l.STAT_BRANCH_CODE
            """%(self.tm_date,self.s_date,filterstr2)
        row6 = self.engine.execute(sql6.encode('utf-8'),vlist).fetchall()

       
        rr=[]
        while len(row1)+len(row2)+len(row3)+len(row4)+len(row5)+len(row6)+len(row11)+len(row33)+len(row44):
            jgh=''
            ygh=''
            rt = []
            rs=[]
            jgh,ygh,rt=self.find_same(jgh,ygh,row1,rt)
            jgh,ygh,rt=self.find_same(jgh,ygh,row11,rt)
            jgh,ygh,rt=self.find_same(jgh,ygh,row2,rt)
            jgh,ygh,rt=self.find_same(jgh,ygh,row3,rt)
            jgh,ygh,rt=self.find_same(jgh,ygh,row33,rt)
            jgh,ygh,rt=self.find_same(jgh,ygh,row4,rt)
            jgh,ygh,rt=self.find_same(jgh,ygh,row44,rt)
            jgh,ygh,rt=self.find_same(jgh,ygh,row5,rt)
            jgh,ygh,rt=self.find_same(jgh,ygh,row6,rt)
            rt.insert(0,(self.s_date/100)%100)
            rt.insert(0,self.s_date/10000)
            '''扩面得分 计算开始'''
            stdc=maxc=minc=0
            for i in sco1:
                if i[0]==u'标准分（分）':
                    stdc=int(i[1])
                elif i[0]==u'最高分（分）':
                    maxc=int(i[1])
                elif i[0]==u'最低分（分）':
                    minc=int(i[1])
            score = (rt[7]/int(plan1[0][3]))*stdc
            if score>maxc:score=maxc
            if score<minc:score=minc
            if rt[7]==0:
                perc=maxc=0
                for i in self.sco11:
                    if i[1]==u'纯公司类贷款的客户经理':
                        cid=i[2]
                        break
                for i in self.sco11:
                    if i[0]==u'单户奖励分值' and i[2]==cid:
                        perc=int(i[1])
                    elif i[0]==u'单户奖励分值上限' and i[2]==cid:
                        maxc=int(i[1])
                ascore = (rt[6]-int(plan1[0][4]))*perc
                if ascore>maxc:ascore=maxc
                if ascore<0:ascore=0
                score=score+ascore
            else:
                perc=maxc=0
                for i in self.sco11:
                    if i[1]==u'非公司类贷款的客户经理':
                        cid=i[2]
                        break
                for i in self.sco11:
                    if i[0]==u'单户奖励分值' and i[2]==cid:
                        perc=int(i[1])
                    elif i[0]==u'单户奖励分值上限' and i[2]==cid:
                        maxc=int(i[1])
                ascore = (rt[6]-int(plan1[0][5]))*perc
                if ascore>maxc:ascore=maxc
                if ascore<0:ascore=0
                score=score+ascore
            rs.append(score)
            '''扩面工作得分 计算完成'''
            '''日均贷款增加额 计算开始'''
            stdc=maxc=minc=0
            for i in sco2:
                if i[0]==u'标准分（分）':
                    stdc=int(i[1])
                elif i[0]==u'最高分（分）':
                    maxc=int(i[1])
                elif i[0]==u'最低分（分）':
                    minc=int(i[1])
            score = (rt[8]/int(plan2[0][3]))*stdc
            if score>maxc:score=maxc
            if score<minc:score=minc
            rs.append(score)
            '''日均贷款增加额得分 计算完成'''    
            '''小额信用贷款户数得分 计算开始'''
            stdc=maxc=minc=0
            for i in sco2:
                if i[0]==u'标准分（分）':
                    stdc=int(i[1])
                elif i[0]==u'最高分（分）':
                    maxc=int(i[1])
                elif i[0]==u'最低分（分）':
                    minc=int(i[1])
            if rt[10]:
                score = int(float(rt[9]/rt[10])/int(plan3[0][2][0:2]))*stdc
            else: 
                score=0    
            if score>maxc:score=maxc
            if score<minc:score=minc
            rs.append(score)
            '''小额信用贷款户数得分 计算完成'''    
            '''资产质量管理得分 计算开始'''   
            if rt[11]<=int(sco444[2][1]):
                score=int(sco444[1][1])
            score=score+((rt[11]-rt[12])/1000000)*0.1    
            rs.append(round(score,2))
            '''资产质量管理得分 计算完成'''    
            '''丰收两卡合同新增得分 计算开始'''    
            stdc=maxc=minc=0
            for i in sco2:
                if i[0]==u'标准分（分）':
                    stdc=int(i[1])
                elif i[0]==u'最高分（分）':
                    maxc=int(i[1])
                elif i[0]==u'最低分（分）':
                    minc=int(i[1])
            score = (rt[13]/int(plan5[0][3]))*stdc 
            if score>maxc:score=maxc
            if score<minc:score=minc
            rs.append(score)
            '''丰收两卡合同新增得分 计算完成'''    
            '''两卡贷款客户电子渠道办贷率 计算开始'''
            rs.append(0)
            '''两卡贷款客户电子渠道办贷率 计算完成'''    
            '''驻勤（驻村）工作 计算开始 '''
            rs.append(0)
            '''驻勤（驻村）工作 计算完成 '''
            sumsco=0
            for i in rs:
                sumsco+=i
            rs.append(round(sumsco,2))
            rt=rt[0:6]
            rt.extend(rs)
            #print rt
            #print rs
            rr.append(tuple(rt))
        needtrans ={}
        return self.translate(rr,needtrans)
    
    def find_same(self,jgh,ygh,rowlist,rt):
        for x in rowlist:
            if jgh=='' and ygh=='':
                jgh=x[0]
                ygh=x[2]
                rt.insert(0,x[3])
                rt.insert(0,x[2])
                rt.insert(0,x[1])
                rt.insert(0,x[0])
            if jgh==x[0] and ygh==x[2]:
                rt.append(x[4])
                rowlist.pop(rowlist.index(x))
                return jgh,ygh,rt
        rt.append(0)        
        return jgh,ygh,rt        

    def make_eq_filterstr(self):
        filterstr = ""
        filterstr1 = ""
        filterstr2 = ""
        filterstr4 = ""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k=='SALE_CODE':
                    filterstr = filterstr+" and %s = ? "%'SALE_CODE'
                    filterstr1 = filterstr1+" and %s = ? "%'MANAGER_CODE'
                    filterstr2 = filterstr2+" and %s = ? "%v
                    filterstr4 = filterstr4+" and %s = ? "%'SALE_CODE'
                    vlist.append(v)
                if k=='BRANCH_CODE':
                    filterstr = filterstr+" and %s = ? "%'THIRD_BRANCH_CODE'
                    filterstr1 = filterstr1+" and %s = ? "%'THIRD_ORG_CODE'
                    filterstr4 = filterstr4+" and %s = ? "%'ORG0_CODE'
                    vlist.append(v)
                if k=='S_DATE':
                    self.s_date=int(v)
                    self.yyear=int(v)/10000
                    self.ymonth=int(v)/100%100
                    self.yyearmonth=int(v)/100
                    self.ly_date=(int(v[0:4])-1)*10000+1231
                    self.tm_date=(int(v[0:6]))*100+01
        return filterstr,filterstr1,filterstr2,filterstr4,vlist

    def column_header(self):
        return ["统计年份","统计月份","机构号","机构名称","员工号","员工名称","扩面工作得分","日均贷款增加额得分","小额信用贷款户数占比得分","资产质量管理得分","丰收两卡合同新增户数得分","两卡贷款客户电子渠道办贷率得分","驻勤(驻村)工作得分","贷款总得分"]

    @property
    def page_size(self):
        return 15
