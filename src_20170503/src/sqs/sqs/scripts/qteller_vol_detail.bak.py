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
柜员业务量
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        self.start_date_id=""
        self.date_id=""
        filterstr,vlist = self.make_eq_filterstr()
        """
        交易业务量
        """
        sql1 ="""
        select
            "柜员交易业务量29"."月份"  month1, --0
            TEL_TRAN_CODE "交易码",
            TRANNAME "交易名称",
            "柜员交易业务量29"."机构号" org_code, --"机构号" 1
            "柜员交易业务量29"."机构名称"  org_name, --"机构名称" 2
            "柜员交易业务量29"."柜员号"  sale_code, --"柜员号"3
            "柜员交易业务量29"."柜员姓名" sale_name,-- "柜员姓名"4 
            sum(case when  sale_role  in ('录入柜员','理财录入柜员','网银录入柜员') then   "柜员交易业务量29"."柜员实际业务量" else 0 end ) teller_fact_num , --"柜员交易业务量" 7
            sum(
            case when sale_role in ('录入柜员','理财录入柜员','网银录入柜员')
            then
            case  when "柜员交易业务量29"."交易名称" = '批量代发工资' 
            then 
            case  when "柜员交易业务量29"."柜员实际业务量" <= 4500 
            then "柜员交易业务量29"."柜员考核业务量" * 0.15 when 4500 < "柜员交易业务量29"."柜员实际业务量" 
            and "柜员交易业务量29"."柜员实际业务量" <= 7500 then ("柜员交易业务量29"."柜员考核业务量" - 4500) * 0.1 + 675 
            when 7500 < "柜员交易业务量29"."柜员实际业务量" and "柜员交易业务量29"."柜员实际业务量" < 18000 
            then ("柜员交易业务量29"."柜员考核业务量" - 7500) * 0.05 + 975 
            else ("柜员交易业务量29"."柜员考核业务量" - 18000) * 0 + 1500 end  
            else "柜员交易业务量29"."柜员考核业务量" end
            else 0 end )  teller_exam_num , --"柜员交易业务量"8

            sum(case when  sale_role    LIKE '复核柜员%%' then   "柜员交易业务量29"."柜员实际业务量" else 0 end ) fuhe_fact_num , --"复核交易业务量" 7
            sum(
            case when sale_role  LIKE '复核柜员%%' 
            then
            case  when "柜员交易业务量29"."交易名称" = '批量代发工资' 
            then 
            case  when "柜员交易业务量29"."柜员实际业务量" <= 4500 
            then "柜员交易业务量29"."柜员考核业务量" * 0.15 when 4500 < "柜员交易业务量29"."柜员实际业务量" 
            and "柜员交易业务量29"."柜员实际业务量" <= 7500 then ("柜员交易业务量29"."柜员考核业务量" - 4500) * 0.1 + 675 
            when 7500 < "柜员交易业务量29"."柜员实际业务量" and "柜员交易业务量29"."柜员实际业务量" < 18000 
            then ("柜员交易业务量29"."柜员考核业务量" - 7500) * 0.05 + 975 
            else ("柜员交易业务量29"."柜员考核业务量" - 18000) * 0 + 1500 end  
            else "柜员交易业务量29"."柜员考核业务量" end
            else 0 end )  fuhe_exam_num,  --"复核交易业务量"8
            sum(case when  sale_role in ('授权柜员1','授权柜员2','网银授权柜员')  then   "柜员交易业务量29"."柜员实际业务量" else 0 end ) shouquan_teller_fact_num , --"授权交易业务量" 7
            sum(
            case when sale_role in ('授权柜员1','授权柜员2','网银授权柜员')
            then
            case  when "柜员交易业务量29"."交易名称" = '批量代发工资' 
            then 
            case  when "柜员交易业务量29"."柜员实际业务量" <= 4500 
            then "柜员交易业务量29"."柜员考核业务量" * 0.15 when 4500 < "柜员交易业务量29"."柜员实际业务量" 
            and "柜员交易业务量29"."柜员实际业务量" <= 7500 then ("柜员交易业务量29"."柜员考核业务量" - 4500) * 0.1 + 675 
            when 7500 < "柜员交易业务量29"."柜员实际业务量" and "柜员交易业务量29"."柜员实际业务量" < 18000 
            then ("柜员交易业务量29"."柜员考核业务量" - 7500) * 0.05 + 975 
            else ("柜员交易业务量29"."柜员考核业务量" - 18000) * 0 + 1500 end  
            else "柜员交易业务量29"."柜员考核业务量" end
            else 0 end )  shouquan_exam_num  --"授权交易业务量"8
        from 
            (select
             substr(M_TELLER_TRAN.DATE_ID, 1, 6) "月份" ,
             M_TELLER_TRAN.TRANNAME "交易名称" ,
             M_ORG_DATE_FLAT.CHILD_ORG_CODE "机构号" , 
             M_ORG_DATE_FLAT.CHILD_ORG_NAME "机构名称" ,
             M_TELLER_TRAN.TRAN_TELLER_CODE "柜员号" ,
             M_TELLER_TRAN.SALE_ROLE,
             M_TELLER_TRAN.SALE_NAME "柜员姓名" ,
             sum(M_TELLER_TRAN.CNT) "柜员实际业务量" , 
             sum(M_TELLER_TRAN.TRADE_CNT) "柜员考核业务量" ,
             sum(M_TELLER_TRAN.DISCOUNT_CNT) "柜员加计业务量" ,
             TEL_TRAN_CODE,TRANNAME
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
            M_TELLER_TRAN.TRANNAME,M_ORG_DATE_FLAT.CHILD_ORG_CODE,M_ORG_DATE_FLAT.CHILD_ORG_NAME,SALE_ROLE,
            M_TELLER_TRAN.TRAN_TELLER_CODE,M_TELLER_TRAN.SALE_NAME,M_TELLER_TRAN.PST_DISCOUNT,TEL_TRAN_CODE,TRANNAME) "柜员交易业务量29"
            group by
            "柜员交易业务量29"."月份","柜员交易业务量29"."机构号", "柜员交易业务量29"."机构名称", "柜员交易业务量29"."柜员号", "柜员交易业务量29"."柜员姓名",
            TEL_TRAN_CODE,TRANNAME
        """%(self.start_date_id,self.date_id,filterstr)
        row1 = self.engine.execute(sql1.encode('utf-8'),vlist).fetchall()

        """
        现金借方发生额
        """
        sql2 ="""
        select
            substr(M_CASH_TRAN_AMOUNT.DATE_ID,1,6) month1, --"月份",
            TEL_TRAN_CODE,
            TRANNAME,
            M_ORG_DATE_FLAT.CHILD_ORG_CODE org_code,--"机构号" ,
            M_ORG_DATE_FLAT.CHILD_ORG_NAME org_name,--"机构名称" ,
            M_CASH_TRAN_AMOUNT.TRAN_TELLER_CODE sale_code,--"柜员号" ,
            M_CASH_TRAN_AMOUNT.SALE_NAME sale_name,--"柜员姓名" ,
            sum(M_CASH_TRAN_AMOUNT.D_CNY_AMOUNT * 0.0001) cash_bor_cnt,--"现金借方发生额" ,
            sum(M_CASH_TRAN_AMOUNT.C_CNY_AMOUNT * 0.0001) cash_credit_cnt--"现金贷方发生额"
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
            substr(M_CASH_TRAN_AMOUNT.DATE_ID,1,6),M_ORG_DATE_FLAT.CHILD_ORG_CODE, M_ORG_DATE_FLAT.CHILD_ORG_NAME,M_CASH_TRAN_AMOUNT.TRAN_TELLER_CODE, M_CASH_TRAN_AMOUNT.SALE_NAME,TEL_TRAN_CODE,TRANNAME
        """%(self.start_date_id,self.date_id,filterstr)
        row2 = self.engine.execute(sql2.encode('utf-8'),vlist).fetchall()

        """
        现金借方笔数35
        """
        sql3 ="""
        select 
            substr(M_CASH_TRAN_CNT.DATE_ID,1,6) month1,-- "月份",
            TEL_TRAN_CODE,
            TRANNAME,
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
            M_CASH_TRAN_CNT.SALE_NAME,TEL_TRAN_CODE,TRANNAME
        """%(self.start_date_id,self.date_id,filterstr)
        row3 = self.engine.execute(sql3.encode('utf-8'),vlist).fetchall()

        """
        先进行员工信息汇总 日期,机构号,机构名称,柜员号,柜员名称
        """
        tellerlist=[]
        for a in row1:
            t = []
            t.insert(0, a[0])   #日期
            t.insert(1, a[1])   #交易码
            t.insert(2, a[2])   #交易名称
            t.insert(3, a[3])   #机构号
            t.insert(4, a[4])   #机构名称
            t.insert(5, a[5])  #柜员号
            t.insert(6, a[6])  #柜员名称
            tellerlist.append(t)

        for a in row2:
            t = []
            is_exist = False
            for x in tellerlist:
                if x[1] == a[1] and x[3] == a[3] and x[5]==a[5]:
                    is_exist = True
                    break
            if is_exist == False: 
                t.insert(0, a[0])   #日期
                t.insert(1, a[1])   #交易码
                t.insert(2, a[2])   #交易名称
                t.insert(3, a[3])   #机构号
                t.insert(4, a[4])   #机构名称
                t.insert(5, a[5])  #柜员号
                t.insert(6, a[6])  #柜员名称
                tellerlist.append(t)
            
        for a in row3:
            t = []
            is_exist = False
            for x in tellerlist:
                if x[1] == a[1] and x[3] == a[3] and x[5]==a[5]:
                    is_exist = True
                    break
            if is_exist == False: 
                t.insert(0, a[0])   #日期
                t.insert(1, a[1])   #交易码
                t.insert(2, a[2])   #交易名称
                t.insert(3, a[3])   #机构号
                t.insert(4, a[4])   #机构名称
                t.insert(5, a[5])  #柜员号
                t.insert(6, a[6])  #柜员名称
                tellerlist.append(t)



        rowlist=[]
        for t in tellerlist:
            tran_code=t[1]
            jgh = t[3]
            ygh = t[5]
            
            rt=[]
            for i in t:
                rt.append(i)
            
            rt=self.find_same(tran_code,jgh,ygh,row1,rt,6) # 柜员实际业务量
            rt=self.find_same(tran_code,jgh,ygh,row2,rt,2) #现金金额
            rt=self.find_same(tran_code,jgh,ygh,row3,rt,2) #现金笔数

            rt.insert(0,self.date_id)
            rowlist.append(tuple(rt))

        needtrans ={}
        row = []
        for i in rowlist:
            t=list(i)
            for j in range(8,len(t)):
                if t[j] is None:t[j]=0
                t[j]=self.trans_dec(t[j])
            row.append(t)    
        return self.translate(row,needtrans)    
    
    def find_same(self,tran_code,jgh,ygh,rowlist,rt,t):

        is_exist = False
        for x in rowlist:
            if tran_code==x[1] and jgh==x[3] and ygh==x[5]:
                for i in range(7,len(x)):
                    rt.append(x[i] or 0)
                    is_exist = True

        if is_exist == False:
            for j in range(t): #因为上面只有一个值,所以只需要填充一个就好,所以t为1
                rt.append(0)        
        return rt        

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and CHILD_ORG_CODE in ( %s ) "%(vvv)
                elif k == 'DATE_ID':
                    self.start_date_id=int(str(v)[:6]+'01')
                    self.date_id = int(v) 
                elif k=='SALE_CODE':
                    filterstr = filterstr+" and TRAN_TELLER_CODE = ?"
                    vlist.append(v)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'TRAN_TELLER_CODE','CHILD_ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return[
        [{"name":"查询日期",'h':2},{"name":"月份",'h':2},{"name":"交易码",'h':2},{"name":"交易名称",'h':2},{"name":"机构号",'h':2},{"name":"机构名称",'h':2},{"name":"员工号",'h':2},{"name":"员工姓名",'h':2},{"name":"交易业务量",'w':2},{"name":"复核业务量",'w':2},{"name":"授权业务量",'w':2},{"name":"现金收付",'w':4}],

        [{"name": u"折算前",'h':1},{"name": u"折算后",'h':1},{"name": u"折算前",'h':1},{"name": u"折算后",'h':1},{"name": u"折算前",'h':1},{"name": u"折算后",'h':1},{"name": u"借方发生额",'h':1},{"name": u"贷方发生额",'h':1},{"name": u"借方发生笔数",'h':1},{"name": u"贷方发生笔数",'h':1}
        ]]                                                                            
    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        xxx = '{:,}'.format(tmp)
        return xxx

    @property
    def page_size(self):
        return 15
