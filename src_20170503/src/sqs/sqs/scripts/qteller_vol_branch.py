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
支行柜员业务量
"""

class Query(ObjectQuery):
    def exp_str(self):
        return {"start_row":5,"start_col":1,"cols":11}

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        self.start_date_id=""
        self.date_id=""
        filterstr,vlist,filterstr1,vlist1 = self.make_eq_filterstr()
        sql1 ="""
        select 
        month1,
        parent_code,
        parent_name,
        --sum(teller_fact_num),
        sum(teller_exam_num) 
        --sum(benpiao_fact_num),
        --sum(benpiao_exam_num),
        --sum(zhipiao_fact_num),
        --sum(zhipiao_eaxm_num)
        from
        (select 
         month1,
         nvl(parent_code,org_code) parent_code,
         nvl(parent_name,org_name) parent_name,
         teller_fact_num,
         teller_exam_num,
         benpiao_fact_num,
         benpiao_exam_num,
         zhipiao_fact_num,
         zhipiao_eaxm_num
         from

         ( select
           "柜员交易业务量29"."月份"  month1, 
           "柜员交易业务量29"."机构号" org_code, --"机构号" 
           "柜员交易业务量29"."机构名称"  org_name, --"机构名称"
           "柜员交易业务量29"."柜员号"  sale_code, --"柜员号"
           "柜员交易业务量29"."柜员姓名" sale_name,-- "柜员姓名" 
           sum("柜员交易业务量29"."柜员实际业务量") teller_fact_num , --"柜员实际业务量" 
           sum(
                   case  when "柜员交易业务量29"."交易码" in('00413091','413091' ) ---批量代发工资
                   then 
                   case  when "柜员交易业务量29"."柜员实际业务量" <= 4500 
                   then "柜员交易业务量29"."柜员考核业务量" * 0.15 when 4500 < "柜员交易业务量29"."柜员实际业务量" 
                   and "柜员交易业务量29"."柜员实际业务量" <= 7500 then ("柜员交易业务量29"."柜员考核业务量" - 4500) * 0.1 + 675 
                   when 7500 < "柜员交易业务量29"."柜员实际业务量" and "柜员交易业务量29"."柜员实际业务量" < 18000 
                   then ("柜员交易业务量29"."柜员考核业务量" - 7500) * 0.05 + 975 else ("柜员交易业务量29"."柜员考核业务量" - 18000) * 0 + 1500 end  else "柜员交易业务量29"."柜员考核业务量" end)  teller_exam_num, --"柜员考核业务量"

           sum(case when "柜员交易业务量29"."交易码" in( '3524','003524') then "柜员实际业务量" else 0 end  ) benpiao_fact_num,--"本票复核实际业务量"
           sum(case when "柜员交易业务量29"."交易码" in( '3524','003524') then "柜员考核业务量" else 0 end  ) benpiao_exam_num , --"本票复核考核业务量"
           sum(case when "柜员交易业务量29"."交易码" in( 'CISTC01', 'CISTC02') then "柜员实际业务量" else 0 end  )zhipiao_fact_num,--"支票影像实际业务量" ,
           sum(case when "柜员交易业务量29"."交易码" in( 'CISTC01', 'CISTC02') then "柜员考核业务量" else 0 end  )zhipiao_eaxm_num--"支票影像考核业务量" 
           from 
         (select
          substr(M_TELLER_TRAN.DATE_ID, 1, 6) "月份" ,
          M_TELLER_TRAN.TEL_TRAN_CODE "交易码" ,
          M_ORG_DATE_FLAT.CHILD_ORG_CODE "机构号" , 
          M_ORG_DATE_FLAT.CHILD_ORG_NAME "机构名称" ,
          M_TELLER_TRAN.TRAN_TELLER_CODE "柜员号" , 
          M_TELLER_TRAN.SALE_NAME "柜员姓名" ,
          sum(M_TELLER_TRAN.CNT) "柜员实际业务量" , 
          sum(M_TELLER_TRAN.TRADE_CNT) "柜员考核业务量"
          from
          M_TELLER_TRAN M_TELLER_TRAN, M_ORG_DATE_FLAT M_ORG_DATE_FLAT
          where  
          M_TELLER_TRAN.DATE_ID>=%s and  
          M_TELLER_TRAN.DATE_ID<=%s
          %s
          and M_ORG_DATE_FLAT.ORG_CODE = '966000'
          and M_TELLER_TRAN.TRAN_BRANCH_CODE = M_ORG_DATE_FLAT.CHILD_ORG_CODE
          and M_TELLER_TRAN.YM = M_ORG_DATE_FLAT.DATE_ID 
          group by
          substr(M_TELLER_TRAN.DATE_ID, 1, 6),
          M_TELLER_TRAN.TEL_TRAN_CODE,M_ORG_DATE_FLAT.CHILD_ORG_CODE,M_ORG_DATE_FLAT.CHILD_ORG_NAME,
          M_TELLER_TRAN.TRAN_TELLER_CODE,M_TELLER_TRAN.SALE_NAME) "柜员交易业务量29"
          group by
          "柜员交易业务量29"."月份","柜员交易业务量29"."机构号", "柜员交易业务量29"."机构名称", "柜员交易业务量29"."柜员号", "柜员交易业务量29"."柜员姓名") a

          left join 
          (select b.BRANCH_CODE child_code,b.BRANCH_NAME,a.BRANCH_CODE parent_code,a.BRANCH_NAME parent_name,a.BRANCH_LEVEL from BRANCH a
           join
           branch b
           on a.ROLE_ID=b.PARENT_ID where a.BRANCH_LEVEL='支行') b
          on a.org_code=b.child_code )--统计到支行)
          group by month1,parent_code,parent_name
        """%(self.start_date_id,self.date_id,filterstr)
        row1 = self.engine.execute(sql1.encode('utf-8'),vlist).fetchall()

        """
        现金发生额37
        """
        sql2 ="""
        select
        month1,
        parent_code,
        parent_name,
        sum(cash_bor_cnt),
        sum(cash_credit_cnt),
        --sum(cash_bor_num),
        --sum(cash_credit_num),
        sum(min_limit_cnt),
        sum(total_wai)
        from
        (
         select 
         month1,
         nvl(parent_code,org_code) parent_code,
         nvl(parent_name,org_name) parent_name,
         cash_bor_cnt,
         cash_credit_cnt,
         cash_bor_num,
         cash_credit_num,
         min_limit_cnt,
         total_wai
         from
         (
        select nvl(a.month1,b.month1) month1,
        nvl(a.org_code,b.org_code) org_code,
        nvl(a.org_name,b.org_name)org_name,
        nvl(a.sale_code,b.sale_code) sale_code,
        nvl(a.sale_name,b.sale_name) sale_name,
        round(nvl(cash_bor_cnt,0),2) cash_bor_cnt, --"现金借方发生额" ,
        round(nvl(cash_credit_cnt,0),2) cash_credit_cnt,--"现金贷方发生额"
        nvl(cash_bor_num,0) cash_bor_num,--"现金借方笔数"
        nvl(cash_credit_num,0) cash_credit_num,--"现金贷方笔数"
        nvl(min_limit_cnt,0) min_limit_cnt, ---小额业务笔数
        round((round(nvl(cash_bor_cnt,0),2))/3.0,2) total_wai ---对外现金收入量笔数
        from
        ( select
          substr(M_CASH_TRAN_AMOUNT.DATE_ID,1,6) month1, --"月份",
          M_ORG_DATE_FLAT.CHILD_ORG_CODE org_code,--"机构号" ,
          M_ORG_DATE_FLAT.CHILD_ORG_NAME org_name,--"机构名称" ,
          M_CASH_TRAN_AMOUNT.TRAN_TELLER_CODE sale_code,--"柜员号" ,
          M_CASH_TRAN_AMOUNT.SALE_NAME sale_name,--"柜员姓名" ,
          sum(M_CASH_TRAN_AMOUNT.D_CNY_AMOUNT * 0.0001) cash_bor_cnt,--"现金借方发生额" ,
          sum(M_CASH_TRAN_AMOUNT.C_CNY_AMOUNT * 0.0001) cash_credit_cnt,--"现金贷方发生额"
          sum(min_limit_cnt) min_limit_cnt  ---小额业务笔数
          from 
          YDW.M_ORG_DATE_FLAT M_ORG_DATE_FLAT,YDW.M_CASH_TRAN_AMOUNT M_CASH_TRAN_AMOUNT 
          where                                                                  
          M_CASH_TRAN_AMOUNT.DATE_ID>=%s and  
          M_CASH_TRAN_AMOUNT.DATE_ID<=%s
          %s
          and 
          M_ORG_DATE_FLAT.ORG_CODE = '966000'and 
          M_CASH_TRAN_AMOUNT.YM = M_ORG_DATE_FLAT.DATE_ID and 
          M_CASH_TRAN_AMOUNT.TRAN_BRANCH_CODE = M_ORG_DATE_FLAT.CHILD_ORG_CODE
          group by 
          substr(M_CASH_TRAN_AMOUNT.DATE_ID,1,6),                                                                       
          M_ORG_DATE_FLAT.CHILD_ORG_CODE, M_ORG_DATE_FLAT.CHILD_ORG_NAME,M_CASH_TRAN_AMOUNT.TRAN_TELLER_CODE, M_CASH_TRAN_AMOUNT.SALE_NAME
          )a
          full join 

          (
           select 
           substr(M_CASH_TRAN_CNT.DATE_ID,1,6) month1,-- "月份",
           M_ORG_DATE_FLAT.CHILD_ORG_CODE org_code,-- "机构号" ,
           M_ORG_DATE_FLAT.CHILD_ORG_NAME  org_name,-- "机构名称" ,
           M_CASH_TRAN_CNT.TRAN_TELLER_CODE sale_code,-- "柜员号" ,
           M_CASH_TRAN_CNT.SALE_NAME sale_name,--"柜员姓名" ,
           sum(M_CASH_TRAN_CNT.D_CNT) cash_bor_num,--"现金借方笔数" ,
           sum(M_CASH_TRAN_CNT.C_CNT) cash_credit_num--"现金贷方笔数"
           from
           YDW.M_ORG_DATE_FLAT M_ORG_DATE_FLAT, YDW.M_CASH_TRAN_CNT M_CASH_TRAN_CNT
           where
           M_CASH_TRAN_CNT.DATE_ID>=%s and  
           M_CASH_TRAN_CNT.DATE_ID<=%s
           %s
           and 
           M_ORG_DATE_FLAT.ORG_CODE = '966000' and 
           M_CASH_TRAN_CNT.YM = M_ORG_DATE_FLAT.DATE_ID and 
           M_CASH_TRAN_CNT.TRAN_BRANCH_CODE = M_ORG_DATE_FLAT.CHILD_ORG_CODE
           group by
           substr(M_CASH_TRAN_CNT.DATE_ID,1,6),
           M_ORG_DATE_FLAT.CHILD_ORG_CODE, M_ORG_DATE_FLAT.CHILD_ORG_NAME,M_CASH_TRAN_CNT.TRAN_TELLER_CODE,
           M_CASH_TRAN_CNT.SALE_NAME
           )b
           on a.month1=b.month1 and a.org_code=b.org_code and a.sale_code=b.sale_code

         ) a

           left join 
           (select b.BRANCH_CODE child_code,b.BRANCH_NAME,a.BRANCH_CODE parent_code,a.BRANCH_NAME parent_name,a.BRANCH_LEVEL from BRANCH a
            join
            branch b
            on a.ROLE_ID=b.PARENT_ID where a.BRANCH_LEVEL='支行') b
           on a.org_code=b.child_code )--统计到支行)
           group by month1,parent_code,parent_name


        """%(self.start_date_id,self.date_id,filterstr,self.start_date_id,self.date_id,filterstr)
        row2 = self.engine.execute(sql2.encode('utf-8'),vlist).fetchall()
        '''
        残损币已除10
        '''
        sql3 ="""
        select 
        month1,
        parent_code,
        parent_name,
        (sum(cash_cnt)*1.0)/10.0
        from
        (select
         month1,
         nvl(parent_code,org_code) parent_code,
         parent_name, 
         cash_cnt
         from
         (select 
          left(b.date_id,6) month1,
          b.exit_org_code org_code,
          sum(a.CASH_CNT) cash_cnt
          from CORE_BHFMCMRD a
          join CORE_BHFMCMRM_DIRECT b
          on a.date_id=b.date_id and a.CMCASNL1=b.CMCASNL1 and a.ACTION !='D' and b.ACTION !='D'
          and b.exit_ORG_CODE !='966000' and b.ON_ORG_CODE='966000'
          and b.FLAG_CAN in ('2','3')
          where a.date_id>=%s and a.date_id<=%s
          %s
          group by b.exit_org_code,left(b.date_id,6))a
         left join 
         (select b.BRANCH_CODE child_code,b.BRANCH_NAME,a.BRANCH_CODE parent_code,a.BRANCH_NAME parent_name,a.BRANCH_LEVEL from BRANCH a
          join
          branch b
          on a.ROLE_ID=b.PARENT_ID where a.BRANCH_LEVEL='支行') b
         on a.org_code=b.child_code )--统计到支行
         group by month1,parent_code,parent_name
        """%(self.start_date_id,self.date_id,filterstr1)
        print sql3
        row3 = self.engine.execute(sql3.encode('utf-8'),vlist1).fetchall()

        """
        先进行员工信息汇总 日期,机构号,机构名称,柜员号,柜员名称
        """
        tellerlist=[]
        for a in row1:
            t = []
            t.insert(0, a[0])   #日期
            t.insert(1, a[1])   #机构号
            t.insert(2, a[2])   #机构名称
            tellerlist.append(t)

        for a in row2:
            t = []
            is_exist = False
            for x in tellerlist:
                if x[1] == a[1]:
                    is_exist = True
            if is_exist == False: 
                t.insert(0, a[0])
                t.insert(1, a[1])
                t.insert(2, a[2])
                tellerlist.append(t)
            
        for a in row3:
            t = []
            is_exist = False
            for x in tellerlist:
                if x[1] == a[1]:
                    is_exist = True
            if is_exist == False: 
                t.insert(0, a[0])
                t.insert(1, a[1])
                t.insert(2, a[2])
                tellerlist.append(t)


        rowlist=[]
        for t in tellerlist:
            jgh = t[1]
            ygh=0
            rt=[]
            for i in t:
                rt.append(i)
            
            rt=self.find_same(jgh,ygh,row1,rt,1) # 柜员实际业务量
            rt=self.find_same(jgh,ygh,row2,rt,4) #柜员调整值
            rt=self.find_same(jgh,ygh,row3,rt,1) #对外现金
            rt.append(rt[3]-rt[6]+rt[7]+rt[8])
            rt.insert(0,self.date_id)
            rowlist.append(tuple(rt))

        needtrans ={}
        row = []
        for i in rowlist:
            t=list(i)
            for j in range(4,len(t)):
                if t[j] is None:t[j]=0
                t[j]=self.trans_dec(t[j])
            row.append(t)    
        return self.translate(row,needtrans)    
    
    def find_same(self,jgh,ygh,rowlist,rt,t):

        is_exist = False
        for x in rowlist:
            if jgh==x[1]:
                for i in range(3,len(x)):
                    rt.append(x[i] or 0)
                    is_exist = True

        if is_exist == False:
            for j in range(t): #因为上面只有一个值,所以只需要填充一个就好,所以t为1
                rt.append(0)        
        return rt        

    def make_eq_filterstr(self):
        filterstr =""
        filterstr1=""
        vlist = []
        vlist1=[]
        for k,v in self.args.items():

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and CHILD_ORG_CODE in ( %s ) "%(vvv)
                    filterstr1 = filterstr1 +" and b.exit_org_code in ( %s ) "%(vvv)
                elif k == 'DATE_ID':
                    self.start_date_id=int(str(v)[:6]+'01')
                    self.date_id = int(v) 
                elif k=='SALE_CODE':
                    filterstr = filterstr+" and TRAN_TELLER_CODE = '%s'"%(v)
                    filterstr1 = filterstr1+" and b.exit_sale_code = '%s'"%(v)
                    print v
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    filterstr1 = filterstr1+" and %s = ?"%k
                    vlist.append(v)
                    vlist1.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'CHILD_ORG_CODE', None))
        filterstr1 ="%s and %s"%(filterstr1,self.get_auth_sql(config.DATATYPE['query'],None,'b.exit_org_code', None))
        return filterstr,vlist,filterstr1,vlist1

    def column_header(self):
        return[
        [{"name":"查询日期",'h':2},{"name":"月份",'h':2},{"name":"机构号",'h':2},{"name":"机构名称",'h':2},{"name":"核心系统换算笔数",'h':2},{"name":"现金收付(万元)",'w':2},{"name":"小额业务笔数",'h':2},{"name":"对外现金笔数",'h':2},{"name":"上缴清算中心残币",'h':2},{"name":"总业务量",'h':2}],
        [{"name": u"现金借方发生额",'h':1},{"name": u"现金贷方发生额",'h':1}]
        ]                                                                            
    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        xxx = '{:,}'.format(tmp)
        return xxx

    @property
    def page_size(self):
        return 15
