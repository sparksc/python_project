# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from utils import config
from decimal import Decimal
"""
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
    
        wandian_level='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='按支行网点等级算薪酬的职位' and h.HEADER_NAME='按网点等级算薪酬的职位' ---副行长(兼网点主任),二级支行副行长(主持),行长助理(兼网点主任),分理处主任
        '''

        Lobby_manager=u'''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='类似大堂经理(享受副股级)级别状况' and h.HEADER_NAME='映射职位' ---大堂经理(享受副股级)\:分理处主任
        '''
        Lobby_manager=self.engine.execute(Lobby_manager).fetchone()
        Lobby_manager=str(Lobby_manager[0]).replace(" ",'')
        Lobby_manager_map={}
        for i in Lobby_manager.split(','):
            Lobby_manager_map[i.split(':')[0]]=i.split(':')[1]

        wandian_level= self.engine.execute(wandian_level).fetchone()
        wandian=str(wandian_level[0]).replace(" ",'').split(',')+Lobby_manager_map.keys()
        print wandian

        his_sql='''

        select a.date_id, --0 
        a.org_code,--1
        a.ORG_NAME,--2
        a.sale_code,--3
        a.sale_name,--4
        b.POSITION_HIS,--5 职位
        b.sale_deg_level,--6等级
        b.is_test,--7试聘
        b.sale_falg,--8安全员
        a.BASE_PAY,--9基本
        a.POSITION_PAY,--10职级
        a.SAFE_FAN_SAL -- 11安全员
        from
        (select  date_id,org_code,ORG_NAME,sale_code,sale_name, BASE_PAY/100.00 BASE_PAY , POSITION_PAY/100.00 POSITION_PAY ,SAFE_FAN_SAL/100.00 SAFE_FAN_SAL from REPORT_MANAGER_OTHER
        where ORG_CODE<>'966000' 
        union all
        select date_id,org_code,ORG_NAME,SALE_CODE,sale_name,HZ_BASE_PAY/100.00,HZ_POSITION_PAY/100.00,HZ_SAFE_FAN_SAL/100.00 from REPORT_MANAGER_HZSAL
        where ORG_CODE<>'966000') a
        join
        (select 
        q.branch_code org_code1,
        q.branch_name org_name,--0机构名
        sale_code sale_code1,--1员工号
        sale_name sale_name1,--2员工名
        property,--3性质
        case when POSITION_HIS IS NOT NULL then POSITION_HIS else '0' END POSITION_HIS,
        case when b.DEG_LEVEL IS NOT NULL   and  length(b.DEG_LEVEL) <>0 then b.DEG_LEVEL ELSE  '0' END sale_deg_level,--职位加等级 --4
        sale_falg,--5 安全员
        workstatus,---6工作状态
        is_viriual,--7 虚拟柜员
        is_test --8测试员
        from GROUP_HIS b
        join branch q on b.org_code=q.branch_name
        where  workstatus ='在职' and is_viriual ='否' and left(START_DATE,6)<= %s and left(end_date,6)>=%s
        )b
        on a.sale_code=b.sale_code1 and a.org_code=b.org_code1
        where 1=1  %s order by sale_code
       '''%(sql_date_mon,sql_date_mon,filterstr)


        sql ="""
        select a.date_id, --0
        a.org_code,--1
        a.ORG_NAME,--2
        a.sale_code,--3
        a.sale_name,--4
        b.JOB,--5 职务
        b.DEG_LEVE,--6等级
        b.is_test,--7试聘
        b.is_safe,--8 安全员
        a.BASE_PAY,--9 基本
        a.POSITION_PAY,--10 职级
        a.SAFE_FAN_SAL --11安全员
        from
        (select  date_id,org_code,ORG_NAME,sale_code,sale_name, BASE_PAY/100.00 BASE_PAY , POSITION_PAY/100.00 POSITION_PAY ,SAFE_FAN_SAL/100.00 SAFE_FAN_SAL from REPORT_MANAGER_OTHER
        where ORG_CODE<>'966000'
        union all
        select date_id,org_code,ORG_NAME,SALE_CODE,sale_name,HZ_BASE_PAY/100.00,HZ_POSITION_PAY/100.00,HZ_SAFE_FAN_SAL/100.00 from REPORT_MANAGER_HZSAL
        where ORG_CODE<>'966000' ) a
        join
        (select user_name,name,org org1,branch_name,property,
        case when JOB IS NOT NULL then JOB else '0' end JOB ,
        case when DEG_LEVE IS NOT NULL  then DEG_LEVE ELSE '0'  END DEG_LEVE,
        is_safe,WORK_STATUS,is_virtual,is_test from v_staff_info_gdxc  where WORK_STATUS='在职' and IS_VIRTUAL = '否')b
        on a.org_code=b.org1 and a.sale_code=b.user_name
        where 1=1  %s order by sale_code

        """%(filterstr)

        sql2_fu='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='副行长工资比例' and h.HEADER_NAME='副行长工资比例(%)' --73
        '''
        sql2_fu=self.engine.execute(sql2_fu).fetchone()
        sql2_fu=float(sql2_fu[0])/100.00
        
        sql_zhu='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='行长助理工资比例' and h.HEADER_NAME='行长助理工资比例(%)' --63
        '''
        sql_zhu=self.engine.execute(sql_zhu).fetchone()
        sql_zhu=float(sql_zhu[0])/100.00

        sql_hangzhang='''
        select sal from V_POSITION_SAL where POSITION='行长(总经理)-1级'
        '''
        sql_hangzhang=self.engine.execute(sql_hangzhang).fetchone()
        sql_hangzhang=float(sql_hangzhang[0])
        sql_hangzhang_fu=sql_hangzhang*sql2_fu
        sql_hangzhang_zhu=sql_hangzhang*sql_zhu

        his_row = self.engine.execute(his_sql.encode('utf-8'),vlist).fetchall()
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        ping_rows={}
        rowlist=[]
        trans_level={u'特级':'特级',u'一级':'1级',u'二级':'2级',u'三级':'3级',u'四级':'4级',u'五级':'5级',u'六级':'6级',u'七级':'7级'}
        for i in his_row:
            i=list(i)
            date_id=str(i[0])
            org=str(i[1])
            sale_code=str(i[3])
            if i[5] in hz_report:
                if i[9]==None or int(i[9])==0 or i[9]=='' or i[10]==None or int(i[10])==0 or    i[10]=='':
                    continue
            if i[5] not in hz_report:
                if i[9] is not None and int(Decimal(str(i[9])))  in [int(Decimal(str(sql_hangzhang))),int(Decimal(str(sql_hangzhang_fu))),int(Decimal(str(sql_hangzhang_zhu)))]:
                    continue
            if date_id+sale_code in ping_rows:
                continue
            else:
                ping_rows[date_id+sale_code]=i
        for i in row:
            i=list(i)
            date_id=str(i[0])
            org=str(i[1])
            sale_code=str(i[3])
            if i[5] in hz_report:
                if i[9]==None or int(i[9])==0 or i[9]=='' or i[10]==None or int(i[10])==0 or i[10]=='':
                    continue
            if i[5] not in hz_report:
                if i[9] is not None and int(Decimal(str(i[9])))  in [int(Decimal(str(sql_hangzhang))),int(Decimal(str(sql_hangzhang_fu))),int(Decimal(str(sql_hangzhang_zhu)))]:
                    continue
            if date_id+sale_code in ping_rows:
                continue
            else:
                ping_rows[date_id+sale_code]=i
        rows=ping_rows.values()
        row_zuizong=[]
        for i in rows:
            i=list(i)
            if i[5] in hz_report:
                k=str(i[1]).split('M')
                if len(k[0])==0:
                    z='M'+k[1]
                else:
                    z='M'+k[0]
                org_sql=u'''
                select deg_level from BRANCH where BRANCH_CODE='%s'
                '''%(z)
                org_sql_row = self.engine.execute(org_sql).fetchone()
                i[6]=trans_level[org_sql_row[0]]
            elif i[5] in wandian:
                k=str(i[1]).split('M')
                if len(k[0])==0:
                    z=k[1]
                else:
                    z=k[0]
                wan_sql=u'''
                select deg_level from BRANCH where BRANCH_CODE='%s'
                '''%(z)
                wan_sql_row = self.engine.execute(wan_sql).fetchone()
                i[6]=trans_level[wan_sql_row[0]]
            row_zuizong.append(i)
        #for i in row_zuizong:
        #    dengji=i[5]+'-'+i[6]
        #    dengji_sql='''
        #      select a.position as pos_lev,a.sal as pos_sal,b.sal as lev_sal
        #      from 
        #      V_POSITION_SAL a
        #      join V_LEVEL_SAL b
        #      on a.POSITION=b.LEVEL
        #      where a.position='%s'
        #    '''%(dengji)
        #    dengji_sql_row = self.engine.execute(dengji_sql.encode('utf-8')).fetchone()
        #    if i[3]=='9660950':
        #        print i
        #    if int(Decimal(i[9]))==int(Decimal(dengji_sql_row[1])) and int(Decimal(i[10]))==int(Decimal(dengji_sql_row[2])):
        #        row_zuizong_ma.append(i)
        #    else:
        #        continue

        for i in row_zuizong:
            t=list(i[0:9])
            for j in i[9:]:
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
        return ["统计日期","机构编号","机构名称","员工编号","员工姓名",'职位','等级','试聘','安全员标志',"基本工资","职位工资","安全防范效酬"]

    @property
    def page_size(self):
        return 15
