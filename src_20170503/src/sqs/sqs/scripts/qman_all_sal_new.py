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
           SELECT DATE_ID,ORG_CODE,ORG_NAME,SALE_CODE,SALE_NAME,NVL((SUM(ADD_AVG_SAL))/100000000.00,0)+NVL((SUM(LAST_AVG_SAL))/100000000.00,0)/12 
           FROM  REPORT_MANAGER_DEP WHERE 1=1 %s
           GROUP BY DATE_ID,ORG_CODE,SALE_CODE,SALE_NAME,ORG_NAME order by DATE_ID desc
            """%(filterstr)
        row1 = self.engine.execute(sql1.encode('utf-8'),vlist).fetchall()

        """
        贷款
        """
        sql2 ="""
            SELECT DATE_ID,ORG_CODE,ORG_NAME,SALE_CODE,SALE_NAME, nvl(sum(TOTAL_NUM_SAL+AVG_SAL+PRI_ADD_NUM_SAL+PUB_ADD_NUM_SAL+ADD_AVG_ASL+TWO_CARD_LOANRATE_SAL+ELEC_FILE_INFO_SAL)/100000000.00,0)
            FROM  REPORT_MANAGER_LOAN WHERE 1=1 %s
            GROUP BY DATE_ID,ORG_CODE,SALE_CODE,SALE_NAME,ORG_NAME order by DATE_ID desc
            """%(filterstr)
        row2 = self.engine.execute(sql2.encode('utf-8'),vlist).fetchall()

        """
        电子银行
        """
        sql3 ="""
            SELECT DATE_ID,ORG_CODE,ORG_NAME,SALE_CODE,SALE_NAME,NVL(SUM(EPAY_ADD_NUM_SAL+MB_ADD_NUM_SAL+CB_ADD_NUM_SAL+ADD_HIGH_POS_SAL+ADD_LOW_POS_SAL+FARM_SERV_SAL)/100.00,0) 
           FROM  REPORT_MANAGER_OTHER WHERE 1=1 %s
           GROUP BY DATE_ID,ORG_CODE,SALE_CODE,SALE_NAME,ORG_NAME order by DATE_ID desc
            """%(filterstr)
        row3 = self.engine.execute(sql3.encode('utf-8'),vlist).fetchall()
        """
        信用卡
        """
        sql4 ="""
           select date_id,org_code,org_name,sale_code,sale_name,salary from REPORT_MANAGER_CREDITCARD
           where 1=1 %s
           order by date_id  desc
            """%(filterstr)
        row4 = self.engine.execute(sql4.encode('utf-8'),vlist).fetchall()
        '''
        附加佣金
        '''
        sql5 ="""
            SELECT SYEAR||SMOUTH, ORG_CODE, ORG_NAME, STAFF_CODE, STAFF_NAME, sum(SCORE/100.00) FROM YDW.M_MANAGER_ADD_SCO WHERE TYP='佣金' %s group by SYEAR, SMOUTH, ORG_CODE, ORG_NAME, STAFF_CODE, STAFF_NAME
            """%(self.addsal)
        row5 = self.engine.execute(sql5.encode('utf-8')).fetchall()
        print sql5
        '''
            中间业务
        '''
        sql6 ="""
            select date_id ,ORG_code,ORG_NAME,SALE_CODE,SALE_NAME,sum(nvl(ADD_ETC_NUM_SAL,0)+nvl(ADD_THIRD_DEPO_SAL,0))/100.00 from REPORT_MANAGER_OTHER where 1=1 %s group by DATE_ID,ORG_code,ORG_NAME,SALE_CODE,SALE_NAME order by DATE_ID desc
            """%(filterstr)
        row6 = self.engine.execute(sql6.encode('utf-8'),vlist).fetchall()
        print sql6

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

        for a in row4:
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

        for a in row5:
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

        for a in row6:
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
            total, rt=self.find_same(jgh,ygh,total,row1,rt,1) #1是得到的数据值
            total, rt=self.find_same(jgh,ygh,total,row2,rt,1)
            total, rt=self.find_same(jgh,ygh,total,row3,rt,1)
            total, rt=self.find_same(jgh,ygh,total,row4,rt,1)
            total, rt=self.find_same(jgh,ygh,total,row5,rt,1)           
            total, rt=self.find_same(jgh,ygh,total,row6,rt,1)

            rt.insert(11, total)

            rowlist.append(tuple(rt))

        needtrans ={}
        row = []
        for i in rowlist:
            t=list(i)
            for j in range(5,12):
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
                    total = total + x[i]  #总金额
                    is_exist = True

        if is_exist == False:
            for j in range(t): #因为上面只有一个值,所以只需要填充一个就好,所以t为1
                rt.append(0)        
        return total, rt        

    def make_eq_filterstr(self):
        filterstr =""
        self.addsal=""
        vlist = []
        for k,v in self.args.items():
            if k == 'login_teller_no':
                if self.deal_teller_query_auth(v) == True:
                    filterstr = filterstr+" and SALE_CODE = '%s'"%v
                    self.addsal=self.addsal+" and STAFF_CODE='%s'"%v
            elif k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False :
                    filterstr = filterstr+" and ORG_CODE in ( %s )"%bb
                    self.addsal=self.addsal+" and ORG_CODE in ( %s)"%bb
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                    self.addsal=self.addsal+" and ORG_CODE in (%s)"%(vvv)
                elif k == 'DATE_ID':
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
                    v1=v[:4]
                    v2=v[4:]
                    self.addsal=self.addsal+" and  SYEAR= '%s' and SMOUTH='%s'"%(v1,v2)
                    self.date_id = v 
                elif k=='SALE_CODE':
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
                    self.addsal=self.addsal+" and STAFF_CODE='%s'"%v
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        return filterstr,vlist

    def column_header(self):
        return [u"统计日期",u"机构号",u"机构名称",u"员工号",u"员工姓名",u"存款总效酬",u"贷款总效酬",u"电子银行总效酬",u"发卡量效酬",u"附加效酬",u"中间业务效酬",u"绩效薪酬合计值"]
                                                                                    
    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        xxx = '{:,}'.format(tmp)
        return xxx

    @property
    def page_size(self):
        return 15
