# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
客户经理存款绩效佣金
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        '''
        存量日均存款效酬和新增日均存款效酬
        '''
        sql1 =u"""
            SELECT DATE_ID,ORG_CODE,ORG_NAME,SALE_CODE,SALE_NAME,JOB,property, 
            NVL((SUM(LAST_AVG_SAL))/100000000.00,0)/12, ----存量日均存款
            NVL((SUM(ADD_AVG_SAL))/100000000.00,0)--新增日均存款
            FROM  REPORT_MANAGER_DEP a
            join v_staff_info b on a.ORG_CODE=b.org and a.SALE_CODE=b.user_name 
            WHERE 1=1 %s 
            GROUP BY DATE_ID,ORG_CODE,SALE_CODE,SALE_NAME,ORG_NAME ,JOB,property order by SALE_CODE
            """%(filterstr)
        row1 = self.engine.execute(sql1.encode('utf-8'),vlist).fetchall()
        '''
        贷款薪酬报表
        '''
        sql2 =u"""
            SELECT DATE_ID,ORG_CODE,ORG_NAME,SALE_CODE,SALE_NAME, JOB,property,
            nvl(sum(TOTAL_NUM_SAL)/100000000.00,0), --总管贷户数效酬
            nvl(sum(AVG_SAL)/100000000.00,0),--管贷余额效酬
            nvl(sum(PRI_ADD_NUM_SAL)/100000000.00,0),--对私
            nvl(sum(PUB_ADD_NUM_SAL)/100000000.00,0), --对公增户扩面效酬
            nvl(sum(ADD_AVG_ASL)/100000000.00,0), --贷款日均日均增量效酬
            nvl(sum(TWO_CARD_LOANRATE_SAL)/100000000.00,0),--两卡贷款客户电子渠道办贷率效酬
            nvl(sum(ELEC_FILE_INFO_SAL)/100000000.00,0)--电子档案信息采集效酬效酬
            FROM  REPORT_MANAGER_LOAN a
            join v_staff_info b on a.ORG_CODE=b.org and a.SALE_CODE=b.user_name
            WHERE 1=1 %s
            GROUP BY DATE_ID,ORG_CODE,SALE_CODE,SALE_NAME,ORG_NAME,JOB,property order by SALE_CODE 

           """%(filterstr)
        row2 = self.engine.execute(sql2.encode('utf-8'),vlist).fetchall()
        sql3=u"""
                select date_id,org_code,org_name,sale_code,sale_name,JOB,property,
                sum(salary) --贷记卡效酬
                from REPORT_MANAGER_CREDITCARD a
                join v_staff_info b on a.ORG_CODE=b.org and a.SALE_CODE=b.user_name
                where 1=1 %s
                group by date_id,org_code,org_name,sale_code,sale_name,JOB,property
                order by sale_code 
              """%(filterstr)
        row3 = self.engine.execute(sql3.encode('utf-8'),vlist).fetchall()
        sql4=u'''
                SELECT 
                a.DATE_ID,  --日期
                a.ORG_CODE, --机构号
                a.ORG_NAME, --机构名称
                a.SALE_CODE, --员工号
                a.SALE_NAME, --员工名
                b.JOB,    --岗位名称
                b.property, --用工性质
                NVL(sum(MB_ADD_NUM_SAL)/100.00,0),--    新增手机银行效酬
                NVL(sum(CB_ADD_NUM_SAL)/100.00,0),  --新增企业网银
                NVL(SUM(EPAY_ADD_NUM_SAL)/100.00,0),    --新增E支付有效户数效酬
                NVL(SUM(ADD_HIGH_POS_SAL)/100.00,0),    --新增高POS,助农,信付通效酬
                NVL(SUM(ADD_LOW_POS_SAL)/100.00,0), --新增低POS助农,信付通效酬
                NVL(SUM(FARM_SERV_SAL)/100.00,0),   --助农服务点
                sum(nvl(ADD_THIRD_DEPO_SAL,0))/100.00,  --第三方存管效酬
                sum(nvl(ADD_ETC_NUM_SAL,0))/100.00,     --新增ETC效酬
                sum(nvl(BASE_PAY,0)/100.00),    --基本工资
                sum(nvl(POSITION_PAY,0)/100.00),    --职位工资
                sum(nvl(BRANCH_NET_SAL,0)/100.00),  --支行及网点关键绩效指标考核效酬
                sum(nvl(MANAGE_BUS_SAL ,0)/100.00), --客户经理业务经营考核效酬
                sum(nvl(WORK_QUALITY_SAL,0)/100.00),--  工作质量效酬
                sum(nvl(HIG_CIV_QUAL_SAL,0)/100.00),--  优质文明服务效酬
                sum(nvl(JOB_SAT_SAL ,0)/100.00),    --工作满意度效酬
                sum(nvl(DAY_DEP_COMP_PER ,0)/100.00),-- 日均存款完成率(核定到人)
                sum(nvl(DAY_DEP_SAL ,0)/100.00),    --日均存款完成率(内后勤池:存款效酬)
                sum(nvl(DAY_DEP_SEC_FEN,0)/100.00), --日均存款完成率(内后勤池二次分配)
                sum(nvl(CREDIT_POOL ,0)/100.00),    --信贷池二次分配
                sum(nvl(INTER_SET_SAL ,0)/100.00),  --国际结算效酬
                sum(nvl(SALE_VOC_SAL ,0)/100.00),   --结售汇量效酬
                sum(nvl(ADD_EFC_CURSAL ,0)/100.00), --新增有效外汇账户效酬
                sum(nvl(ADD_FUNON_SAL ,0)/100.00),  --新增福农卡效酬
                sum(nvl(PER_CAR_DANERSAL,0)/100.00),    --推荐人保公司办理车险业务效酬
                sum(nvl(BUM_HOM_SAL ,0)/100.00),    --新增丰收家(丰收购)效酬
                sum(nvl(OTHER_ACHI_SAL ,0)/100.00), --其他业绩效酬
                sum(nvl(COMPRE_SAL ,0)/100.00), --综合效酬
                sum(nvl(LABOR_COMP_SAL ,0)/100.00),--   劳动竞赛效酬
                sum(nvl(PROV_FUND_SAL,0)/100.00),   --临时性资金组织效酬
                sum(nvl(SAFE_FAN_SAL,0)/100.00),    --安全防范效酬
                sum(nvl(ALL_RISK_SAL,0)/100.00),    --全面风险管理效酬
                sum(nvl(BAD_LOAN_PERSAL,0)/100.00), --不良贷款专项清收效酬
                sum(nvl(FTP_ACH_SAL,0)/100.00), --FTP绩效考核效酬
                sum(nvl(COUNT_COMPLE_SAL,0)/100.00),--  柜面渠道入口营销专项竞赛效酬(完成率)
                sum(nvl(COUNT_COP_SSAL,0)/100.00),  --柜面渠道入口营销专项竞赛效酬(佣金)
                sum(nvl(HP_FINA_SAL,0)/100.00), --普惠金融工程评价考核效酬
                sum(nvl(OTHER_SPEC_SAL1,0)/100.00),--   其他专项效酬1
                sum(nvl(OTHER_SPEC_SAL2,0)/100.00), --其他专项效酬2
                sum(nvl(OTHER_SPEC_SAL3,0)/100.00), --其他专项效酬3
                sum(nvl(OTHER_SPEC_SAL4,0)/100.00),--   其他专项效酬4
                sum(nvl(OTHER_SPEC_SAL5,0)/100.00), --其他专项效酬5
                sum(nvl(BRANCH_SECO_FEN1,0)/100.00),    --支行二次分配1
                sum(nvl(BRANCH_SECO_FEN2,0)/100.00),    --支行二次分配2
                sum(nvl(BRANCH_SECO_FEN3,0)/100.00),    --支行二次分配3
                sum(nvl(BRANCH_SECO_FEN4,0)/100.00),    --支行二次分配4
                sum(nvl(OTHER_ACH_WAGES,0)/100.00), --其他绩效工资
                sum(nvl(OVER_WORK_SAL,0)/100.00),   --加班费
                sum(nvl(OTHER_SAL1_DUAN,0)/100.00), --其他效酬1:短期合同工扣减效酬
                sum(nvl(OTHER_SAL2,0)/100.00),  --其他效酬2
                sum(nvl(OTHER_SAL3_WEI,0)/100.00),  --其他效酬3:未达2级员工扣减效酬
                sum(nvl(OTHER_SAL4_KE,0)/100.00),   --其他效酬4:客户经理排名奖
                sum(nvl(OTHER_SAL5_GE,0)/100.00),   --其他效酬5:各类假期计(扣)
                sum(nvl(OTHER_SAL6,0)/100.00),  --其他效酬6
                sum(nvl(OTHER_SAL7,0)/100.00),  --其他效酬7
                sum(nvl(OTHER_SAL8,0)/100.00),  --其他效酬8
                sum(nvl(QJ_BAD_LOAN_SAL,0)/100.00)   -- 欠旧不良贷款清收效酬
                FROM  REPORT_MANAGER_OTHER a  
                join v_staff_info b on a.ORG_CODE=b.org and a.SALE_CODE=b.user_name 
                WHERE 1=1 %s
                GROUP BY DATE_ID,ORG_CODE,SALE_CODE,SALE_NAME,ORG_NAME ,JOB,property order by SALE_CODE 
        '''%(filterstr)
        row4 = self.engine.execute(sql4.encode('utf-8'),vlist).fetchall()

        tellerlist=[]
        for a in row1:
            t = []
            t.insert(0, a[0])   #日期
            t.insert(1, a[1])   #机构号
            t.insert(2, a[2])   #机构名称
            t.insert(3, a[3])   #柜员号
            t.insert(4, a[4])   #柜员名称
            t.insert(5, a[5])  #岗位名称
            t.insert(6, a[6])  #用工性质
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
                 t.insert(5, a[5])
                 t.insert(6, a[6])
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
                t.insert(5, a[5])
                t.insert(6, a[6])
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
                t.insert(5, a[5])
                t.insert(6, a[6])
                tellerlist.append(t)

        rowlist=[]
        for t in tellerlist:
            jgh = t[1]
            ygh = t[3]



            rt=[]
            for i in t:
                rt.append(i)
            total = 0
            total, rt=self.find_same(jgh,ygh,total,row1,rt,2)
            total, rt=self.find_same(jgh,ygh,total,row2,rt,7)
            total, rt=self.find_same(jgh,ygh,total,row3,rt,1)
            total, rt=self.find_same(jgh,ygh,total,row4,rt,56)

            rt.insert(73, total)
            rowlist.append(tuple(rt))
        needtrans ={}
        row = []

        for i in rowlist:
            t=list(i)
            for j in range(7,74):
                if t[j] is None:t[j]=0
                t[j]=self.trans_dec(t[j])
            row.append(t)
        return self.translate(row,needtrans)

    def find_same(self,jgh,ygh,total, rowlist,rt,t):
        is_exist = False
        for x in rowlist:
            if jgh==x[1] and ygh==x[3]:
                for i in range(7,len(x)):
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
            print k,v
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
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        return filterstr,vlist

    def column_header(self):
        return [u"统计日期",u"机构编号",u"机构名称",u"员工编号",u"员工姓名",u"岗位名称",u"用工性质",u"存量日均存款",u'新增日均存款',u'管贷户数效酬',u'管贷余额效酬',u'对私增户扩面效酬',u'对公增户扩面效酬',u'贷款日均日均增量效酬',u'两卡贷款客户电子渠道办贷率效酬',u'电子档案信息采集效酬效酬',u'贷记卡效酬',u'新增手机银行效酬',u'新增企业网银',u'新增E支付有效户数效酬',u'新增高POS',u'新增低POS',u'助农服务点',u'第三方存管效酬',u'新增ETC效酬',u'基本工资',u'职位工资',u'支行及网点关键绩效效酬',u'客户经理经营考核效酬',u'工作质量效酬',u'优质文明服务效酬',u'工作满意度效酬',u'日均存款完成率(核定到人)',u'日均存款完成率(存款效酬)',u'日均存款完成率(二次分配)',u'信贷池二次分配',u'国际结算效酬',u'结售汇量效酬',u'新增有效外汇账户效酬',u'新增福农卡效酬',u'推荐人保公司办理车险业务效酬',u'新增丰收家',u'其他业绩效酬',u'综合效酬',u'劳动竞赛效酬',u'临时性资金组织效酬',u'安全防范效酬',u'全面风险管理效酬',u'不良贷款专项清收效酬',u'FTP绩效考核效酬',u'柜面渠道入口营销专项竞赛效酬(完成率)',u'柜面渠道入口营销专项竞赛效酬(佣金)',u'普惠金融工程评价考核效酬',u'其他专项效酬1',u'其他专项效酬2',u'其他专项效酬3',u'其他专项效酬4',u'其他专项效酬5',u'支行二次分配1',u'支行二次分配2',u'支行二次分配3',u'支行二次分配4',u'其他绩效工资',u'加班费',u'其他效酬1:短期合同工扣减效酬',u'其他效酬2',u'其他效酬3:未达2级员工扣减效酬',u'其他效酬4:客户经理排名奖',u'其他效酬5:各类假期计(扣)',u'其他效酬6',u'其他效酬7',u'其他效酬8',u'欠旧不良贷款清收效酬',u'合计',u'操作']
    @property
    def page_size(self):
        return 15
    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        xxx = '{:,}'.format(tmp)
        return xxx
