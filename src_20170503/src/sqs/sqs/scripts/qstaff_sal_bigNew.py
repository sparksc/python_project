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
客户经理存款绩效佣金
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        self.date_id=''
        filterstr,vlist = self.make_eq_filterstr()
        sql_date='select MONTHEND_ID from d_date where id=%s'%(self.date_id)
        row_date = self.engine.execute(sql_date.encode('utf-8'),vlist).fetchone()
        if int(self.date_id) != int(row_date[0]):
            return (u"未到月末,不能查看")
        sql_date_mon=int(str(self.date_id)[:6])
        ZhiHang_level="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='按支行网点等级算薪酬的职位' and h.HEADER_NAME='按支行等级算薪酬的职位' ---行长(总经理),副行长(主持)
        """
        Fuhang_level="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='按支行网点等级算薪酬的职位' and h.HEADER_NAME='副行长级别待遇的职位' ---副行长
        """
        ZhuLi_level="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='按支行网点等级算薪酬的职位' and h.HEADER_NAME='行长助理级别待遇的职位' ---行长助理
        """
        ZhiHang_level= self.engine.execute(ZhiHang_level).fetchone()
        Fuhang_level= self.engine.execute(Fuhang_level).fetchone()
        ZhuLi_level= self.engine.execute(ZhuLi_level).fetchone()
        hz_report=str(ZhiHang_level[0]).replace(" ",'').split(',')+str(Fuhang_level[0]).replace(" ",'').split(',')+str(ZhuLi_level[0]).replace(" ",'').split(',')
        print 'sss',hz_report

        '''
        存量日均存款效酬和新增日均存款效酬
        '''
        sql1 =u"""
            select date_id,org_code,1,sale_code,sale_name,job,property,sum(nvl(dep_sal,0)) dep_sal ---佣金提成效酬
            from
            (SELECT DATE_ID,ORG_CODE,1,SALE_CODE,SALE_NAME,JOB,property, 
            NVL((SUM(LAST_AVG_SAL))/100000000.00,0)/12+ ----存量日均存款
            NVL((SUM(ADD_AVG_SAL))/100000000.00,0) as dep_sal--新增日均存款
            FROM  REPORT_MANAGER_DEP a
            join v_staff_info b on a.ORG_CODE=b.org and a.SALE_CODE=b.user_name 
            WHERE 1=1 
            GROUP BY DATE_ID,ORG_CODE,SALE_CODE,SALE_NAME,1 ,JOB,property 
            union all
            SELECT DATE_ID,ORG_CODE,1,SALE_CODE,SALE_NAME, JOB,property,
            nvl(sum(TOTAL_NUM_SAL)/100000000.00,0)/12 + --总管贷户数效酬
            nvl(sum(AVG_SAL)/100000000.00,0)/12 +--管贷余额效酬
            nvl(sum(PRI_ADD_NUM_SAL)/100000000.00,0)+--对私
            nvl(sum(PUB_ADD_NUM_SAL)/100000000.00,0)+ --对公增户扩面效酬
            nvl(sum(ADD_AVG_ASL)/100000000.00,0)+ --贷款日均日均增量效酬
            nvl(sum(TWO_CARD_LOANRATE_SAL)/100000000.00,0)+--两卡贷款客户电子渠道办贷率效酬
            nvl(sum(ELEC_FILE_INFO_SAL)/100000000.00,0) as loan_sal--电子档案信息采集效酬效酬
            FROM  REPORT_MANAGER_LOAN a
            join v_staff_info b on a.ORG_CODE=b.org and a.SALE_CODE=b.user_name
            WHERE 1=1 
            GROUP BY DATE_ID,ORG_CODE,SALE_CODE,SALE_NAME,1,JOB,property 
            union all
            select date_id,org_code,1,sale_code,sale_name,JOB,property,
            sum(nvl(salary,0)) as card_sal--贷记卡效酬
            from REPORT_MANAGER_CREDITCARD a
            join v_staff_info b on a.ORG_CODE=b.org and a.SALE_CODE=b.user_name
            where 1=1 
            group by date_id,org_code,1,sale_code,sale_name,JOB,property
            union all
            SELECT 
            a.DATE_ID,  --日期
            a.ORG_CODE, --机构号
            1, --机构名称
            a.SALE_CODE, --员工号
            a.SALE_NAME, --员工名
            b.JOB,    --岗位名称
            b.property, --用工性质
            NVL(sum(MB_ADD_NUM_SAL)/100.00,0)+   --新增手机银行效酬
            NVL(sum(CB_ADD_NUM_SAL)/100.00,0)+  --新增企业网银
            NVL(SUM(EPAY_ADD_NUM_SAL)/100.00,0)+    --新增E支付有效户数效酬
            NVL(SUM(ADD_HIGH_POS_SAL)/100.00,0)+    --新增高POS,助农,信付通效酬
            NVL(SUM(ADD_LOW_POS_SAL)/100.00,0)+ --新增低POS助农,信付通效酬
            NVL(SUM(FARM_SERV_SAL)/100.00,0)+   --助农服务点
            sum(nvl(ADD_THIRD_DEPO_SAL,0))/100.00+  --第三方存管效酬
            sum(nvl(ADD_ETC_NUM_SAL,0))/100.00+    --新增ETC效酬
            sum(nvl(CREDIT_POOL ,0)/100.00)+    --信贷池二次分配
            sum(nvl(INTER_SET_SAL ,0)/100.00)+  --国际结算效酬
            sum(nvl(SALE_VOC_SAL ,0)/100.00)+   --结售汇量效酬
            sum(nvl(ADD_EFC_CURSAL ,0)/100.00)+ --新增有效外汇账户效酬
            sum(nvl(ADD_FUNON_SAL ,0)/100.00)+  --新增福农卡效酬
            sum(nvl(PER_CAR_DANERSAL,0)/100.00)+    --推荐人保公司办理车险业务效酬
            sum(nvl(BUM_HOM_SAL ,0)/100.00)+    --新增丰收家(丰收购)效酬
            sum(nvl(OTHER_ACHI_SAL ,0)/100.00)+ --其他业绩效酬
            sum(nvl(QJ_BAD_LOAN_SAL,0)/100.00) as ebank_sal   -- 欠旧不良贷款清收效酬
            FROM  REPORT_MANAGER_OTHER a  
            join v_staff_info b on a.ORG_CODE=b.org and a.SALE_CODE=b.user_name 
            WHERE 1=1 
            GROUP BY DATE_ID,ORG_CODE,SALE_CODE,SALE_NAME,1 ,JOB,property)
            where 1=1 %s
            group by date_id,org_code,1,sale_code,sale_name,job,property
            """%(filterstr)

        row1 = self.engine.execute(sql1.encode('utf-8'),vlist).fetchall()
        sql2=u'''
            SELECT 
            a.DATE_ID,  --日期
            a.ORG_CODE, --机构号
            1, --机构名称
            a.SALE_CODE, --员工号
            a.SALE_NAME, --员工名
            b.JOB,    --岗位名称
            b.property, --用工性质
            sum(nvl(BASE_PAY,0)/100.00) as BASE_PAY,    --基本工资
            sum(nvl(POSITION_PAY,0)/100.00) as POSITION_PAY ,    --职位工资
            sum(nvl(BRANCH_NET_SAL,0)/100.00)+  --支行及网点关键绩效指标考核效酬
            sum(nvl(MANAGE_BUS_SAL ,0)/100.00) as MANAGE_BUS_SAL, --客户经理业务经营考核效酬 --业务经营考核效酬
            sum(nvl(WORK_QUALITY_SAL,0)/100.00) as WORK_QUALITY_SAL,--  工作质量效酬
            sum(nvl(HIG_CIV_QUAL_SAL,0)/100.00) as HIG_CIV_QUAL_SAL ,--  优质文明服务效酬
            sum(nvl(JOB_SAT_SAL ,0)/100.00) as JOB_SAT_SAL,    --工作满意度效酬
            sum(nvl(DAY_DEP_COMP_PER ,0)/100.00)+ --日均存款完成率(核定到人) 
            sum(nvl(DAY_DEP_SAL ,0)/100.00)+    --日均存款完成率(内后勤池:存款效酬)
            sum(nvl(DAY_DEP_SEC_FEN,0)/100.00) as DAY_DEP_COMP_PER , --日均存款完成率(内后勤池二次分配) 日均存款目标完成率
            sum(nvl(COMPRE_SAL ,0)/100.00) as COMPRE_SAL , --综合效酬
            sum(nvl(LABOR_COMP_SAL ,0)/100.00)+  --   劳动竞赛效酬
            sum(nvl(PROV_FUND_SAL,0)/100.00)+   --临时性资金组织效酬
            sum(nvl(SAFE_FAN_SAL,0)/100.00)+    --安全防范效酬
            sum(nvl(ALL_RISK_SAL,0)/100.00)+    --全面风险管理效酬
            sum(nvl(BAD_LOAN_PERSAL,0)/100.00)+ --不良贷款专项清收效酬
            sum(nvl(FTP_ACH_SAL,0)/100.00)+ --FTP绩效考核效酬
            sum(nvl(COUNT_COMPLE_SAL,0)/100.00)+--  柜面渠道入口营销专项竞赛效酬(完成率)
            sum(nvl(COUNT_COP_SSAL,0)/100.00)+  --柜面渠道入口营销专项竞赛效酬(佣金)
            sum(nvl(HP_FINA_SAL,0)/100.00)+ --普惠金融工程评价考核效酬
            sum(nvl(OTHER_SPEC_SAL1,0)/100.00)+  --   其他专项效酬1
            sum(nvl(OTHER_SPEC_SAL2,0)/100.00)+ --其他专项效酬2
            sum(nvl(OTHER_SPEC_SAL3,0)/100.00)+ --其他专项效酬3
            sum(nvl(OTHER_SPEC_SAL4,0)/100.00)+--   其他专项效酬4
            sum(nvl(OTHER_SPEC_SAL5,0)/100.00) as other_spec, --其他专项效酬5 --专效效酬
            sum(nvl(BRANCH_SECO_FEN1,0)/100.00)+    --支行二次分配1
            sum(nvl(BRANCH_SECO_FEN2,0)/100.00)+    --支行二次分配2
            sum(nvl(BRANCH_SECO_FEN3,0)/100.00)+    --支行二次分配3
            sum(nvl(BRANCH_SECO_FEN4,0)/100.00)+    --支行二次分配4
            sum(nvl(OTHER_ACH_WAGES,0)/100.00) as OTHER_branch , --其他绩效工资  --其他绩效支行二次分配
            sum(nvl(OVER_WORK_SAL,0)/100.00) as OVER_WORK_SAL ,   --加班费
            sum(nvl(OTHER_SAL1_DUAN,0)/100.00)+ --其他效酬1:短期合同工扣减效酬
            sum(nvl(OTHER_SAL2,0)/100.00)+  --其他效酬2
            sum(nvl(OTHER_SAL3_WEI,0)/100.00)+  --其他效酬3:未达2级员工扣减效酬
            sum(nvl(OTHER_SAL4_KE,0)/100.00)+   --其他效酬4:客户经理排名奖
            sum(nvl(OTHER_SAL5_GE,0)/100.00)+   --其他效酬5:各类假期计(扣)
            sum(nvl(OTHER_SAL6,0)/100.00)+  --其他效酬6
            sum(nvl(OTHER_SAL7,0)/100.00)+  --其他效酬7
            sum(nvl(OTHER_SAL8,0)/100.00) as other_sal  --其他效酬8 --其他效酬
            FROM  REPORT_MANAGER_OTHER a  
            join v_staff_info b on a.ORG_CODE=b.org and a.SALE_CODE=b.user_name 
            WHERE 1=1 %s 
            GROUP BY DATE_ID,ORG_CODE,SALE_CODE,SALE_NAME,1 ,JOB,property order by SALE_CODE 

        '''%(filterstr)
        row2 = self.engine.execute(sql2.encode('utf-8'),vlist).fetchall()

        his_sql_property='''
        select 
        sale_code,--0 员工号
        position_his,--1 岗位
        property, --2 员工性质
        org_code,--3机构名
        is_viriual --4虚拟柜员
        from group_his where left(start_date,6)<=%s and left(end_date,6)>=%s
        '''%(sql_date_mon,sql_date_mon)
        his_sql_proprt_row=self.engine.execute(his_sql_property).fetchall()

        now_sql_property='''
        select
        user_name,
        job,
        property,
        branch_name,
        is_virtual
        from V_STAFF_INFO_GDXC
        '''
        now_sql_proprt_row=self.engine.execute(now_sql_property).fetchall()
        zonghe_xinzhi={}
        for i in his_sql_proprt_row:
            i=list(i)
            i[0]=str(i[0])
            if i[0] in zonghe_xinzhi:
                continue
            else:
                zonghe_xinzhi[i[0]] =i

        
        for i in now_sql_proprt_row:
            i=list(i)
            i[0]=str(i[0])
            if i[0] in zonghe_xinzhi:
                continue
            else:
                zonghe_xinzhi[i[0]] =i

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

        rowlist=[]
        for t in tellerlist:
            jgh = t[1]
            ygh = t[3]


            rt=[]
            for i in t:
                rt.append(i)
            total = 0
            total, rt=self.find_same(jgh,ygh,total,row1,rt,1)
            total, rt=self.find_same(jgh,ygh,total,row2,rt,12)

            rt.insert(20, total)
            rowlist.append(tuple(rt))
        needtrans ={}
        row = []

        big_staff={'date':0,'org_code':1,'org_name':2,'sale_code':3,'sale_name':4,'job':5,'property':6,'YJ_sal':7,'base':8,'ZW_sal':9,'YW_sal':10,'GZZL_sal':11,'YZ_dal':12,'GZMY_sal':13,'RJCK_sal':14,'ZH_sal':15,'ZX_sal':16, 'QTJXJC_sal':17, 'JB_sal':18, 'QT_sal': 19,'HJ_sal':20}

#        for i in rowlist:
#            t=list(i)
#            for j in range(7,21):
#                if t[j] is None:t[j]=0
#                t[j]=self.trans_dec(t[j])
#            row.append(t)
        new_row=[]
        weiyi_code=[]
        for i in rowlist:
            i=list(i)
            #if i[5] in [u'行长(总经理)',u'副行长(主持)',u'副行长',u'行长助理']:
            #    continue
            sale_code=str(i[3])
            if sale_code in weiyi_code:
                continue
            else:
                weiyi_code.append(sale_code)
            ganwei=""
            xinzhi=""
            org_name=sale_code
            if sale_code in zonghe_xinzhi:
                if zonghe_xinzhi[sale_code][4]=='是':
                    continue
                else:
                    ganwei=zonghe_xinzhi[sale_code][1]
                    xinzhi=zonghe_xinzhi[sale_code][2]
                    org_name=zonghe_xinzhi[sale_code][3]
            if ganwei in hz_report:
                continue
            new_row_list=[]
            xiaoxin=int(float(i[big_staff['YW_sal']])+float(i[big_staff['GZZL_sal']])+float(i[big_staff['YZ_dal']])+float(i[big_staff['GZMY_sal']])+float(i[big_staff['RJCK_sal']])+float(i[big_staff['YJ_sal']]))
            new_row_list=[i[big_staff['date']],i[big_staff['org_code']],org_name,i[big_staff['sale_code']],i[big_staff['sale_name']],ganwei,xinzhi,i[big_staff['base']],i[big_staff['ZW_sal']],xiaoxin,i[big_staff['ZH_sal']],i[big_staff['ZX_sal']],i[big_staff['QTJXJC_sal']],i[big_staff['JB_sal']],i[big_staff['QT_sal']],i[big_staff['HJ_sal']]]
 
            #new_row_list=[i[big_staff['date']],i[big_staff['org_code']],i[big_staff['org_name']],i[big_staff['sale_code']],i[big_staff['sale_name']],i[big_staff['job']],i[big_staff['property']],i[big_staff['base']],i[big_staff['ZW_sal']],i[big_staff['YW_sal']]+i[big_staff['GZZL_sal']]+i[big_staff['YZ_dal']]+i[big_staff['GZMY_sal']]+i[big_staff['RJCK_sal']]+i[big_staff['YJ_sal']],i[big_staff['ZH_sal']],i[big_staff['ZX_sal']],i[big_staff['QTJXJC_sal']],i[big_staff['JB_sal']],i[big_staff['QT_sal']],i[big_staff['HJ_sal']]]
            new_row.append(new_row_list)
        for i in new_row:
            t=list(i)
            for j in range(7,16):
                if t[j] is None:t[j]=0
                t[j]=self.trans_dec(str(int(t[j])))
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
            #if k == 'login_teller_no':
            #    if self.deal_teller_query_auth(v) == True:
            #        filterstr = filterstr+" and SALE_CODE = '%s'"%v
            #elif k == 'login_branch_no':
            #    bb = self.deal_branch_query_auth(v)
            #    if bb != False :
            #        filterstr = filterstr+" and ORG_CODE in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                elif k=='DATE_ID':
                    filterstr = filterstr+" and DATE_ID = %s "%v
                    self.date_id=int(v)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'SALE_CODE','ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return [u"统计日期",u"机构编号",u"机构名称",u"员工编号",u"员工姓名",u"岗位名称",u"用工性质",u"基本工资",u"职位工资",u"业绩效酬",u"综合效酬",u"专效效酬",u"其他绩效工资",u"加班费",u"其他效酬",u"合计"]
    @property
    def page_size(self):
        return 15
    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        xxx = '{:,}'.format(tmp)
        return xxx
