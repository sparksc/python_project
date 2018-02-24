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
客户经理行长大项
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
        sql ="""
            SELECT a.DATE_ID,a.ORG_CODE,1,a.SALE_CODE,a.SALE_NAME, b.JOB,b.property,
            SUM(NVL(HZ_BASE_PAY,0))/100.00,   --基本工资
            SUM(NVL(HZ_POSITION_PAY ,0))/100.00, --职位工资
            SUM(NVL(HZ_NET_BUS_SAL ,0))/100.00, --业务经营考核效酬
            SUM(NVL(HZ_COMPRE_SAL ,0))/100.00, --综合效酬
            SUM(NVL(HZ_LABOR_COMP_SAL ,0))/100.00+--劳动竞赛效酬
            SUM(NVL(HZ_PROV_FUND_SAL,0))/100.00+--临时性资金组织效酬
            SUM(NVL(HZ_SAFE_FAN_SAL,0))/100.00+--安全防范效酬
            SUM(NVL(HZ_ALL_RISK_SAL,0))/100.00+--全面风险管理效酬
            SUM(NVL(HZ_BAD_LOAN_PERSAL ,0))/100.00+--不良贷款专项清收效酬
            SUM(NVL(HZ_FTP_ACH_SAL,0))/100.00+--FTP绩效考核效酬
            SUM(NVL(HZ_COUNT_COMPLE_SAL,0))/100.00+--柜面渠道入口营销专项竞赛效酬
            SUM(NVL(HZ_OTHER_SPEC_SAL1,0))/100.00+--其他专项效酬1
            SUM(NVL(HZ_OTHER_SPEC_SAL2 ,0))/100.00+--其他专项效酬2
            SUM(NVL(HZ_OTHER_SPEC_SAL3,0))/100.00+--其他专项效酬3
            SUM(NVL(HZ_OTHER_SPEC_SAL4,0))/100.00+--其他专项效酬4
            SUM(NVL(HZ_OTHER_SPEC_SAL5,0))/100.00 as ZX,--其他专项效酬5
            SUM(NVL(HZ_OTHER_SAL1,0))/100.00+--其他效酬1
            SUM(NVL(HZ_OTHER_SAL2,0))/100.00+--其他效酬2
            SUM(NVL(HZ_OTHER_SAL3 ,0))/100.00+--其他效酬3
            SUM(NVL(HZ_OTHER_SAL4 ,0))/100.00+--其他效酬4
            SUM(NVL(HZ_OTHER_SAL5 ,0))/100.00 as QT,--其他效酬5

            SUM(NVL(HZ_BASE_PAY,0))/100.00+   --基本工资
            SUM(NVL(HZ_POSITION_PAY ,0))/100.00+ --职位工资
            SUM(NVL(HZ_NET_BUS_SAL ,0))/100.00+ --业务经营考核效酬
            SUM(NVL(HZ_COMPRE_SAL ,0))/100.00+ --综合效酬
            SUM(NVL(HZ_LABOR_COMP_SAL ,0))/100.00+--劳动竞赛效酬
            SUM(NVL(HZ_PROV_FUND_SAL,0))/100.00+--临时性资金组织效酬
            SUM(NVL(HZ_SAFE_FAN_SAL,0))/100.00+--安全防范效酬
            SUM(NVL(HZ_ALL_RISK_SAL,0))/100.00+--全面风险管理效酬
            SUM(NVL(HZ_BAD_LOAN_PERSAL ,0))/100.00+--不良贷款专项清收效酬
            SUM(NVL(HZ_FTP_ACH_SAL,0))/100.00+--FTP绩效考核效酬
            SUM(NVL(HZ_COUNT_COMPLE_SAL,0))/100.00+--柜面渠道入口营销专项竞赛效酬
            SUM(NVL(HZ_OTHER_SPEC_SAL1,0))/100.00+--其他专项效酬1
            SUM(NVL(HZ_OTHER_SPEC_SAL2 ,0))/100.00+--其他专项效酬2
            SUM(NVL(HZ_OTHER_SPEC_SAL3,0))/100.00+--其他专项效酬3
            SUM(NVL(HZ_OTHER_SPEC_SAL4,0))/100.00+--其他专项效酬4
            SUM(NVL(HZ_OTHER_SPEC_SAL5,0))/100.00+--其他专项效酬5
            SUM(NVL(HZ_OTHER_SAL1,0))/100.00+--其他效酬1
            SUM(NVL(HZ_OTHER_SAL2,0))/100.00+--其他效酬2
            SUM(NVL(HZ_OTHER_SAL3 ,0))/100.00+--其他效酬3
            SUM(NVL(HZ_OTHER_SAL4 ,0))/100.00+--其他效酬4
            SUM(NVL(HZ_OTHER_SAL5 ,0))/100.00--其他效酬5
            FROM  REPORT_MANAGER_HZSAL a 
            join v_staff_info b on a.ORG_CODE=b.org and a.SALE_CODE=b.user_name
            WHERE 1=1 %s
            GROUP BY a.DATE_ID,a.ORG_CODE,a.SALE_CODE,a.SALE_NAME,1 , b.JOB,b.property order by DATE_ID desc

            """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print sql
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


        needtrans ={}
        rowlist=[]
        weiyi_code=[]
        for i in row:
            t=list(i[0:7])
            sale_code=str(t[3])
            if sale_code in weiyi_code:
                continue
            else:
                weiyi_code.append(sale_code)
            ganwei=""
            xinzhi=""
            t[2]=sale_code
            if sale_code in zonghe_xinzhi:
                if zonghe_xinzhi[sale_code][4]=='是':
                    continue
                else:
                    t[5]=zonghe_xinzhi[sale_code][1]
                    t[6]=zonghe_xinzhi[sale_code][2]
                    t[2]=zonghe_xinzhi[sale_code][3]

            if t[5] not in hz_report:
                continue
            for j in i[7:]:
                if j is None:j=0
                j=self.amount_trans_dec(str(int(j)))
                t.append(j)
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)    

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
        return [u"统计日期",u"机构编号",u"机构名称",u"员工编号",u"员工姓名",u"岗位名称",u"用工性质",u"基本工资",u"职位工资",u"业务效酬",u"综合效酬",u"专效效酬",u"其他效酬",u"合计"]

    @property
    def page_size(self):
        return 15
