# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
客户经理绩效薪酬
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        """
        存款
        """
        sql1 ="""
            SELECT DATE_ID,ORG_CODE,ORG_NAME,SALE_CODE,SALE_NAME,nvl(DEP_BAL/100.00,0),nvl(DEP_EXIST/100.00,0),nvl(DEP_ADD/100.00,0)
        FROM YDW.REPORT_MANAGER_DEP_RWD
            WHERE 1=1 %s
        ORDER BY DATE_ID,ORG_CODE,SALE_CODE
            """%(filterstr)
        row1 = self.engine.execute(sql1.encode('utf-8'),vlist).fetchall()

        """
        贷款
        """
        sql2 ="""
            SELECT DATE_ID,ORG_CODE,ORG_NAME,SALE_CODE,SALE_NAME,nvl(LOAN_IMI/100.00,0),nvl(EXT_EXIST/100.00,0),nvl(EXT_ADD/100.00,0)
            FROM YDW.REPORT_MANAGER_LOAN_RWD 
            WHERE 1=1 %s 
        ORDER BY DATE_ID,ORG_CODE,SALE_CODE
            """%(filterstr)
        row2 = self.engine.execute(sql2.encode('utf-8'),vlist).fetchall()

        """
        中间业务
        """
        sql3 ="""
        SELECT *
            FROM YDW.REPORT_MANAGER_MID_RWD
            WHERE 1=1 %s
            ORDER BY DATE_ID,ORG_CODE,SALE_CODE
            """%(filterstr)
        row3 = self.engine.execute(sql3.encode('utf-8'),vlist).fetchall()
        """
        其他效酬
        """
        sql4 ="""
        SELECT *
            FROM YDW.REPORT_MANAGER_OTHER_RWD
            WHERE 1=1 %s
            ORDER BY DATE_ID,ORG_CODE,SALE_CODE
            """%(filterstr)
        row4 = self.engine.execute(sql4.encode('utf-8'),vlist).fetchall()

        """
        先进行员工信息汇总 日期,机构号,机构名称,柜员号,柜员名称
        """
        tellerlist=[]
        for a in row1:
            t = []
            t.insert(0, a[0])   #日期
            t.insert(1, a[1])   #机构号
            t.insert(2, a[2])   #机构名称
            t.insert(3, a[3])   #柜员号
            t.insert(4, a[4])   #柜员名称
            tellerlist.append(t)

        for a in row2:
            t = []
            is_exist = False
            for x in tellerlist:
                if x[1] == a[1] and x[3] == a[3]:
                    is_exist = True
            if is_exist == False: 
                t.insert(0, a[0])
                t.insert(1, a[1])
                t.insert(2, a[2])
                t.insert(3, a[3])
                t.insert(4, a[4])
                tellerlist.append(t)
            
        for a in row3:
            t = []
            is_exist = False
            for x in tellerlist:
                if x[1] == a[1] and x[3] == a[3]:
                    is_exist = True
            if is_exist == False: 
                t.insert(0, a[0])
                t.insert(1, a[1])
                t.insert(2, a[2])
                t.insert(3, a[3])
                t.insert(4, a[4])
                tellerlist.append(t)

        rowlist=[]
        for t in tellerlist:
            jgh = t[1]
            ygh = t[3]

            rt=[]
            for i in t:
                rt.append(i)
            total = 0
            total, rt=self.find_same(jgh,ygh,total,row1,rt,3)
            total, rt=self.find_same(jgh,ygh,total,row2,rt,3)
            total, rt=self.find_same(jgh,ygh,total,row3,rt,23)
            total, rt=self.find_same(jgh,ygh,total,row4,rt,4)
            rt.insert(38, total)

            rowlist.append(tuple(rt))

        needtrans ={}
        row = []
        for i in rowlist:
            t=list(i)
            for j in range(5,39):
                if t[j] is None:t[j]=0
                t[j]=self.trans_dec(t[j])
            row.append(t)    
        return self.translate(row,needtrans)    
    
    def find_same(self,jgh,ygh,total, rowlist,rt,t):

        is_exist = False
        for x in rowlist:
            if jgh==x[1] and ygh==x[3]:
                for i in range(5,len(x)):
                    rt.append(x[i])
                    total = total + x[i]
                    is_exist = True

        if is_exist == False:
            for j in range(t):
                rt.append(0)        
        return total, rt        

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if k == 'login_teller_no':
                if self.deal_teller_query_auth(v) == True:
                    filterstr = filterstr+" and SALE_CODE = '%s'"%v
            elif k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False :
                    filterstr = filterstr+" and ORG_CODE in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                elif k == 'DATE_ID':
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
                    self.date_id = v 
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        return filterstr,vlist

    def column_header(self):
        return ["统计日期","机构号","机构名称","员工号","员工姓名","日均存款增量绩效薪酬","日均存款存量绩效薪酬","日均存款效益绩效薪酬","贷款模拟利润绩效薪酬","贷款增户扩面存量绩效薪酬","贷款增户扩面增量绩效薪酬","新增个人网银活跃客户绩效薪酬","新增手机银行活跃客户绩效薪酬","新增企业网银活跃客户绩效薪酬","新增丰收E支付有效客户绩效薪酬","新增POS机绩效薪酬","新增POS机活跃客户绩效薪酬","新增ETC活跃客户绩效薪酬","网银代发工资业务绩效薪酬","存款有效客户绩效薪酬","贷记卡绩效薪酬","有效烟草代扣户数绩效薪酬","有效一户通与支付宝卡通绩效薪酬","有效第三方存管绩效薪酬","单位结算户绩效薪酬","行级银村合作信用村绩效薪酬","市级银村合作信用村绩效薪酬","省级银村合作信用村绩效薪酬","社保卡激活绩效薪酬","代理销售金条绩效薪酬","代理销售银条绩效薪酬","代理销售题材产品绩效薪酬","其他业务绩效薪酬","中间业务绩效薪酬合计值","关联度绩效薪酬","公共存款二次分配绩效薪酬","日常履职二次分配绩效薪酬","优质文明服务绩效薪酬","绩效薪酬合计值"]
                                                                                    
    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        xxx = '{:,}'.format(tmp)
        return xxx

    @property
    def page_size(self):
        return 15
