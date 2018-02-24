# -*- coding:utf-8 -*-
#!/bin/python  
import datetime
from flask import json, g,current_app
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all
import xlrd
from ..base import utils
import os, time, random,sys
from datetime import datetime,timedelta
from decimal import Decimal
class staff_sal_countService():
    def add_count(self,**kwargs):
        date_id = int(kwargs.get('count')['count_date'])
        sql="""
        select MONTHEND_ID from d_date where id=%s
       """%(date_id)
        aa=g.db_session.execute(sql).fetchone()
        if date_id != int(aa[0]):
            raise Exception(u"未到月末,不能计算")
        wortdate=int(str(date_id)[:6])           

        sql_shiping='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='试聘人员工资比例' and h.HEADER_NAME='试聘人员工资比例(%)'  --90
        '''
        sql_shiping=g.db_session.execute(sql_shiping).fetchone()
        sql_shiping=float(sql_shiping[0])/100.00
        current_app.logger.debug(sql_shiping)
        sql2_fu='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='副行长工资比例' and h.HEADER_NAME='副行长工资比例(%)' --73
        '''
        sql2_fu=g.db_session.execute(sql2_fu).fetchone()
        sql2_fu=float(sql2_fu[0])/100.00
        current_app.logger.debug(sql2_fu)

        sql_zhu='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='行长助理工资比例' and h.HEADER_NAME='行长助理工资比例(%)' --63
        '''
        sql_zhu=g.db_session.execute(sql_zhu).fetchone()
        sql_zhu=float(sql_zhu[0])/100.00
        current_app.logger.debug(sql_zhu)


        sql_yiji='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='安全防范效酬' and h.HEADER_NAME='第一等级安全防范效酬' --150
        '''
        sql_yiji=g.db_session.execute(sql_yiji).fetchone()
        sql_yiji=float(sql_yiji[0])
        current_app.logger.debug(sql_yiji)


        sql_erji='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='安全防范效酬' and h.HEADER_NAME='第二等级安全防范效酬' --120
        '''
        sql_erji=g.db_session.execute(sql_erji).fetchone()
        sql_erji=float(sql_erji[0])
        current_app.logger.debug(sql_erji)


        sql_sanji='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='安全防范效酬' and h.HEADER_NAME='第三等级安全防范效酬' --100
        '''
        sql_sanji=g.db_session.execute(sql_sanji).fetchone()
        sql_sanji=float(sql_sanji[0])
        current_app.logger.debug(sql_sanji)


        sql_anquan='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='是否是安全员' and h.HEADER_NAME='安全员效酬' --100
        '''
        sql_anquan=g.db_session.execute(sql_anquan).fetchone()
        sql_anquan=float(sql_anquan[0])
        current_app.logger.debug(sql_anquan)


        sql_rijuncun='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='日均存款完成率(存款效酬)比例' and h.HEADER_NAME='存量日均存款效酬比例(万/年)'  --8
        '''
        sql_rijuncun=g.db_session.execute(sql_rijuncun).fetchone()
        sql_rijuncun=float(sql_rijuncun[0])
        current_app.logger.debug(sql_rijuncun)


        sql_rijunzeng='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='日均存款完成率(存款效酬)比例' and h.HEADER_NAME='新增日均存款效酬比例(万/月)' --4.6
        '''
        sql_rijunzeng=g.db_session.execute(sql_rijunzeng).fetchone()
        sql_rijunzeng=float(sql_rijunzeng[0])
        current_app.logger.debug(sql_rijunzeng)


        sql_zhihangcun='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='支行二次分配效酬比例' and h.HEADER_NAME='存量日均存款效酬比例(万/年) ' --8
        '''
        sql_zhihangcun=g.db_session.execute(sql_zhihangcun).fetchone()
        sql_zhihangcun=float(sql_zhihangcun[0])
        current_app.logger.debug(sql_zhihangcun)


        sql_zhihangzeng='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='支行二次分配效酬比例' and h.HEADER_NAME='新增日均存款效酬比例(万/月)' --0.4
        '''
        sql_zhihangzeng=g.db_session.execute(sql_zhihangzeng).fetchone()
        sql_zhihangzeng=float(sql_zhihangzeng[0])
        current_app.logger.debug(sql_zhihangzeng)


        sql_duan='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='短期合同工' and h.HEADER_NAME='短期合同工扣减效酬(元/月)' --  -1700
        '''
        sql_duan=g.db_session.execute(sql_duan).fetchone()
        sql_duan=float(sql_duan[0])
        current_app.logger.debug(sql_duan)



        his_sql='''
        select
        d.branch_code,--0机构号
        d.branch_name,--1机构名
        a.sale_code,--2员工号
        a.sale_name,--3员工名
        property,--4工作性质
        a.workstatus,--5工作状态
        a.level,--6工作等级
        a.sale_falg,--7安全员
        a.is_viriual, --8虚拟柜员
        a.is_test, --9试聘
        b.sal as pos_sal, --10 职务工资
        c.sal as lev_sal --11等级工作
        from
        (select 
        org_code,--0机构名
        sale_code,--1员工号
        sale_name,--2员工名
        property,--3性质
        case when POSITION_HIS IS NOT NULL and DEG_LEVEL IS NOT NULL   and  length(DEG_LEVEL) <>0 then  POSITION_HIS||'-'||DEG_LEVEL ELSE  POSITION_HIS END level,--职位加等级 --4
        sale_falg,--5 安全员
        workstatus,---6工作状态
        is_viriual,--7 虚拟柜员
        is_test --8测试员
        from GROUP_HIS where  workstatus ='在职' and left(START_DATE,6)<=%s and left(end_date,6)>=%s)a
        join  V_POSITION_SAL b
        on a.level =b.position
        join  V_LEVEL_SAL c
        on a.level =c.level
        join branch d
        on a.org_code =d.branch_name
        '''%(wortdate,wortdate)

        sql2="""
        select 
        org, --0
        branch_name,--1
        user_name, --2
        name, --3
        property,--性质 --4
        WORK_STATUS,--工作状态 --5
        b.level,--工作-等级 --6
        is_safe,--安全员 --7
        is_virtual,--虚拟柜员--8
        is_test,--试聘--9
        c.sal as pos_sal,--职务工资--10
        a.sal as lev_sal --等级工资 --11
        from 
        (select user_name,name,org,branch_name,property,
        case when JOB IS NOT NULL and DEG_LEVE IS NOT NULL  and length(DEG_LEVE) <>0 then JOB ||'-'||DEG_LEVE ELSE job  END level,
        is_safe,WORK_STATUS,is_virtual,is_test from v_staff_info_gdxc  where WORK_STATUS='在职')b
        join V_POSITION_SAL c
        on b.level =c.position
        join 
        V_LEVEL_SAL a
        on b.LEVEL=  a.level
        """
        his_row=g.db_session.execute(his_sql).fetchall()
        row2=g.db_session.execute(sql2).fetchall()
        rowlist={}
        trans_level={u'特级':'特级',u'一级':'1级',u'二级':'2级',u'三级':'3级',u'四级':'4级',u'五级':'5级',u'六级':'6级',u'七级':'7级'}
        for i in his_row:
            i=list(i)
            org=str(i[0])
            sale=str(i[2])
            if org+'-'+sale in rowlist:
                continue;
            else:
                rowlist[org+'-'+sale]=i

        for i in row2:
            i=list(i)
            org=str(i[0])
            sale=str(i[2])
            if org+'-'+sale in rowlist:
                continue;
            else:
                rowlist[org+'-'+sale]=i
        result=rowlist.values()#历史的和现在的放在了一起
        current_app.logger.debug(rowlist['966083-9660928'])
        finally_result=[]
        safe=0
        duanqi=0
        for i in result:
            if i[2]=='9660928':
                current_app.logger.debug(i[6])
            if (i[6].split('-')[0])=='大堂经理(享受副股级)':
                datanfu_sql='''select deg_level from BRANCH where BRANCH_code='%s'
                 '''%(i[0])
                datanfu_sql_row=g.db_session.execute(datanfu_sql).fetchone()
                fenlizhuren=u'分理处主任'+'-'+trans_level[datanfu_sql_row[0]]
                fenlichuren_sql='''
                select sal from V_LEVEL_SAL
                where level='%s'
                '''%(fenlizhuren)
                fenlichuren_sql_row=g.db_session.execute(fenlichuren_sql).fetchone()
                i[11]=float(fenlichuren_sql_row[0])

            if i[9]=='是':
                i[11]=float(i[11])*sql_shiping
            if i[7]=='是':
                staff=i[6].split('-')[0]
                #if staff=='行长(总经理)'or staff=='副行长(主持)':
                #    safe=sql_yiji+sql_anquan
                #elif staff=='副行长' :
                #    safe=sql_yiji*sql2_fu+sql_anquan
                #elif staff=='行长助理':
                #    safe=sql_yiji*sql_zhu+sql_anquan
                if staff=='委派会计主管(副股级)' or staff=='委派会计主管' or  staff=='大堂经理(享受副股级)' or staff=='委派风险经理':
                    safe=sql_erji+sql_anquan
                elif staff=='客户经理' or  staff=='大堂经理' or staff=='助理会计' or staff=='综合柜员' or staff=='一般员工' or staff=='见习人员' or staff=='后勤人员' or staff=='集中加钞员' or staff=='借用人员' or staff=='存款类客户经理':
                    safe=sql_sanji+sql_anquan
                elif staff=='委派会计主管(副股级)' or staff=='委派会计主管' or staff== '大堂经理(享受副股级)' or staff=='委派风险经理' or staff=='客户经理' or  staff=='大堂经理' or staff=='助理会计' or staff=='综合柜员' or staff=='一般员工' or staff=='见习人员' or staff=='后勤人员' or staff=='集中加钞员' or staff=='借用人员' or staff=='存款类客户经理':
                    safe=sql_anquan
                else:
                    safe=0
            else:
                staff=i[6].split('-')[0]
                #if staff=='行长(总经理)'or staff=='副行长(主持)':
                #    safe=sql_yiji
                #elif staff=='副行长':
                #    safe=sql_yiji*sql2_fu
                #elif staff=='行长助理':
                #    safe=sql_yiji*sql_zhu
                if staff=='委派会计主管(副股级)' or staff=='委派会计主管' or staff=='大堂经理(享受副股级)' or staff=='委派风险经理':
                    safe=sql_erji
                elif staff=='客户经理' or  staff=='大堂经理' or staff=='助理会计' or staff=='综合柜员' or staff=='一般员工' or staff=='见习人员' or staff=='后勤人员' or staff=='集中加钞员' or staff=='借用人员' or staff=='存款类客户经理':
                    safe=sql_sanji
                else:
                    safe=0

            i.append(safe) #--12
            if i[4]=='短期合同工':
                duanqi=sql_duan
            else:
                duanqi=0
            i.append(duanqi)#-13
            finally_result.append(i)
            
        for i in finally_result:
            other_sql='''
            update REPORT_MANAGER_OTHER set BASE_PAY=%s , POSITION_PAY=%s , SAFE_FAN_SAL=%s , OTHER_SAL1_DUAN =%s where ORG_CODE='%s' and  SALE_CODE ='%s' and date_id=%s 
            '''%(int(Decimal(i[10])*100),int(Decimal(i[11])*100),int(i[12]*100),int(i[13]*100),i[0],i[2],date_id)
            g.db_session.execute(other_sql)
        g.db_session.commit()


        his_sql_hz='''
        select
        d.branch_code,--0机构号
        d.branch_name,--1机构名
        a.sale_code,--2员工号
        a.sale_name,--3员工名
        property,--4工作性质
        a.level,--5工作等级
        a.sale_falg,--6安全员
        a.workstatus,--7工作状态
        a.is_viriual, --8虚拟柜员
        a.is_test --9试聘
        from 
        (select 
         org_code,--0机构名
         sale_code,--1员工号
         sale_name,--2员工名
         property,--3性质
         case when POSITION_HIS IS NOT NULL and DEG_LEVEL IS NOT NULL and  length(DEG_LEVEL) <>0 then  POSITION_HIS||'-'||DEG_LEVEL ELSE  POSITION_HIS END level,--职位加等级 --4
         sale_falg,--5 安全员
         workstatus,---6工作状态
         is_viriual,--7 虚拟柜员
         is_test --8测试员
         from GROUP_HIS where  workstatus ='在职' and left(START_DATE,6)<=%s and left(end_date,6)>=%s)a
         join branch d
         on a.org_code =d.branch_name
        '''%(wortdate,wortdate)


        sql_hz='''
        select 
        org, --0
        branch_name,--1
        user_name,--2
        name,--3
        property,--4
        case when JOB IS NOT NULL and DEG_LEVE IS NOT NULL  and length(DEG_LEVE) <>0 then JOB ||'-'||DEG_LEVE ELSE job  END level,--职位加等级 --5
        is_safe,  --安全员 --6
        WORK_STATUS,--工作状态 --7
        is_virtual,--虚拟柜员--8
        is_test --测试员--9
        from v_staff_info_gdxc 
        where WORK_STATUS='在职'
        '''
        his_row_hz=g.db_session.execute(his_sql_hz).fetchall()
        row_hz=g.db_session.execute(sql_hz).fetchall()
        his_com_branch=his_row_hz #用来算员工的存款效酬和二次分配
        now_com_branch=row_hz# 用来算员工的存款效酬和二次分配
        rowlist_hz={} #算行长的
        rowlist_sec_hz={} #算网点的
        for i in his_row_hz:
            i=list(i)
            i.append(i[0])#--10 i[10]这是员工所在的机构号,i[0]已变成算等级的机构号了
            org=str(i[0])
            sale=str(i[2])
            if i[5]=='行长(总经理)' or i[5]=='副行长(主持)' or i[5]=='副行长' or i[5]=='行长助理':
                k=str(i[0]).split('M')
                if len(k[0])==0:
                    z='M'+k[1]
                else:
                    z='M'+k[0]
                i[0]=z #i[0]已变成算等级的机构号了
                if i[5]=='行长(总经理)':
                    i.append(i[5])#--11
                elif i[5]=='副行长(主持)':
                    i.append(i[5])#--11
                else:
                    i.append('行长(总经理)') #--11 i[11]用来算副行长等职位的工资(依赖行长来算的)
                if org+'-'+sale in rowlist_hz: #支行等级
                    continue
                else:
                    rowlist_hz[org+'-'+sale]=i #rowlist_hz 行长有12个长度0-11

            elif i[5]=='副行长(兼网点主任)' or i[5]=='二级支行副行长(主持)' or i[5]=='行长助理(兼网点主任)' or i[5]=='分理处主任':
                k=str(i[0]).split('M')
                if len(k[0])==0:
                    z=k[1]
                else:
                    z=k[0]
                i[0]=z #i[0]已变成算等级的机构号了
                if org+'-'+sale in rowlist_sec_hz: #机构网点等级排版
                    continue
                else:
                    rowlist_sec_hz[org+'-'+sale]=i #rowlist_sec_hz只有11个长度0-10
            else:
                pass

        for i in row_hz:
            i=list(i)
            i.append(i[0])#--10 i[10]这是员工所在的机构号,i[0]已变成算等级的机构号了
            org=str(i[0])
            sale=str(i[2])
            if i[5]=='行长(总经理)' or i[5]=='副行长(主持)' or i[5]=='副行长' or i[5]=='行长助理':
                k=str(i[0]).split('M')
                if len(k[0])==0:
                    z='M'+k[1]
                else:
                    z='M'+k[0]
                i[0]=z #i[0]已变成算等级的机构号了
                if i[5]=='行长(总经理)':
                    i.append(i[5])#--11
                elif i[5]=='副行长(主持)':
                    i.append(i[5])#--11
                else:
                    i.append('行长(总经理)') #--11 i[11]用来算副行长等职位的工资(依赖行长来算的)
                if org+'-'+sale in rowlist_hz: #支行等级
                    continue
                else:
                    rowlist_hz[org+'-'+sale]=i #0-11
            elif i[5]=='副行长(兼网点主任)' or i[5]=='二级支行副行长(主持)' or i[5]=='行长助理(兼网点主任)' or i[5]=='分理处主任':
                k=str(i[0]).split('M')
                if len(k[0])==0:
                    z=k[1]
                else:
                    z=k[0]
                i[0]=z #i[0]已变成算等级的机构号了
                if org+'-'+sale in rowlist_sec_hz: #机构网点等级排版 
                    continue
                else:
                    rowlist_sec_hz[org+'-'+sale]=i #0-10
            else:
                pass

        trans_level={u'特级':'特级',u'一级':'1级',u'二级':'2级',u'三级':'3级',u'四级':'4级',u'五级':'5级',u'六级':'6级',u'七级':'7级'}
        '''
        算网点等级
        '''
        result_sec=rowlist_sec_hz.values()
        finally_sec=[]
        for i in result_sec:
            sql_sec='''select deg_level from branch  where branch_code= '%s' '''%i[0]
            row_sec=g.db_session.execute(sql_sec).fetchone()
            row_sec=list(row_sec)
            #if i[0]=='966010':
            #    row_sec[0]=row_sec[0].split('-')[0]
            dengji=i[5]+'-'+trans_level[row_sec[0]]
            i[5]=i[5]+'-'+trans_level[row_sec[0]]
            sql_lev='''
            select a.position as pos_lev,a.sal as pos_sal,b.sal as lev_sal
            from 
            V_POSITION_SAL a
            join V_LEVEL_SAL b
            on a.POSITION=b.LEVEL
            where a.position='%s'
            '''%(dengji)
            dengji_sal=g.db_session.execute(sql_lev).fetchone()
            i.append(dengji_sal[1])#--职务工资11
            i.append(dengji_sal[2])#-职级(位)12
            if i[9]=='是':
                i[12]=float(i[12])*sql_shiping
            if i[6]=='是':
                staff=i[5].split('-')[0]
                if staff=="副行长(兼网点主任)" or staff== '二级支行副行长(主持)' or staff=='行长助理(兼网点主任)'or staff=='分理处主任':
                    safe_sec=sql_erji+sql_anquan
                else:
                    safe_sec=sql_anquan
            else:
                staff=i[5].split('-')[0]
                if staff=="副行长(兼网点主任)" or staff== '二级支行副行长(主持)' or staff=='行长助理(兼网点主任)'or staff=='分理处主任':
                    safe_sec=sql_erji
                else:
                    safe_sec=0
            i.append(safe_sec)#-13
            if i[4]=='短期合同工':
                duanqi=sql_duan
            else:
                duanqi=0
            i.append(duanqi)#-14
            finally_sec.append(i)
        for i in finally_sec:
            other_sql='''
            update REPORT_MANAGER_OTHER set BASE_PAY=%s , POSITION_PAY=%s , SAFE_FAN_SAL=%s , OTHER_SAL1_DUAN =%s where ORG_CODE='%s' and  SALE_CODE ='%s' and date_id=%s 
            '''%(int(Decimal(i[11])*100),int(Decimal(i[12])*100),int(i[13]*100),int(i[14]*100),i[10],i[2],date_id)
            g.db_session.execute(other_sql)
        g.db_session.commit()
        '''
           算行长
        '''
        '''
          org, --0 已变成算等级的机构号了
          branch_name,--1
          user_name,--2
          name,--3
          property,--4
          职位 --5
          is_safe,  --安全员 --6
          WORK_STATUS,--工作状态 --7
          is_virtual,--虚拟柜员--8
          is_test --测试员--9
          10这是员工所在的机构号
          11 行长(总经理)等固定职位--等级
        '''
        second_HZ=rowlist_hz.values()
        finally_hz=[]
        for i in second_HZ:
            #if i[0]=='M966010':
            #    i[0]='966010'
            #if i[0]=='M966220':
            #    i[0]='966220'
            sql_hz_deg='''select deg_level from branch  where branch_code= '%s' '''%(i[0])
            row_hz_deg=g.db_session.execute(sql_hz_deg).fetchone()
            row_hz_deg=list(row_hz_deg)
            #if i[0]=='966010':
            #    row_hz_deg[0]=row_hz_deg[0].split('-')[1]
            if row_hz_deg==None or row_hz_deg=='':
                continue
            dengji_hz=i[11]+'-'+trans_level[row_hz_deg[0]] #对应行长副行长的等级
            i[11]=i[11]+'-'+trans_level[row_hz_deg[0]]
            sql_hz_deg='''
            select a.position as pos_lev,a.sal as pos_sal,b.sal as lev_sal
            from 
            V_POSITION_SAL a
            join V_LEVEL_SAL b
            on a.POSITION=b.LEVEL
            where a.position='%s'
            '''%(dengji_hz)
            dengji_sal_hz=g.db_session.execute(sql_hz_deg).fetchone()
            if i[5]=='行长(总经理)' or i[5]=='副行长(主持)':
                i.append(dengji_sal_hz[1]) #--职务工资12
                i.append(dengji_sal_hz[2]) #职级(位)13
            elif i[5]=='副行长':
                i.append(float(dengji_sal_hz[1])*sql2_fu)#--职务工资12
                i.append(float(dengji_sal_hz[2])*sql2_fu)#职级(位)13
            else :
                i.append(float(dengji_sal_hz[1])*sql_zhu)#--职务工资12
                i.append(float(dengji_sal_hz[2])*sql_zhu)#职级(位)13
            if i[9]=='是':
                i[13]=float(i[13])*sql_shiping
            if i[6]=='是':
                staff=i[5]
                if staff=='行长(总经理)'or staff=='副行长(主持)':
                    safe=sql_yiji+sql_anquan
                elif staff=='行长助理':
                    safe=sql_yiji*sql_zhu+sql_anquan
                elif staff=='副行长':
                    safe=sql_yiji*sql2_fu+sql_anquan
                else:
                    safe=sql_anquan
            else:
                staff=i[5]
                if staff=='行长(总经理)'or staff=='副行长(主持)':
                    safe=sql_yiji
                elif staff=='副行长':
                    safe=sql_yiji*sql2_fu
                elif staff=='行长助理':
                    safe=sql_yiji*sql_zhu
                else:
                    safe=0
            i.append(safe)#--14安全员
            if i[4]=='短期合同工':
                duanqi=sql_duan
            else:
                duanqi=0
            i.append(duanqi)#-15短期
            finally_hz.append(i)
        for i in finally_hz:
            sql_is_value_hz="""
            select * from REPORT_MANAGER_HZSAL where org_code='%s' and sale_code='%s' and date_id=%s
            """%(i[10],i[2],date_id)
            is_value=g.db_session.execute(sql_is_value_hz).fetchone()
            if is_value:
                sql_update_hz='''
                update REPORT_MANAGER_HZSAL set HZ_BASE_PAY=%s,HZ_POSITION_PAY=%s,HZ_SAFE_FAN_SAL=%s where org_code='%s' and sale_code='%s' and date_id=%s
                '''%(int(Decimal(i[12])*100),int(Decimal(i[13])*100),int(Decimal(i[14])*100),i[10],i[2],date_id)
                g.db_session.execute(sql_update_hz)
            else:
                sql_insert_hz='''
                insert into REPORT_MANAGER_HZSAL(date_id,org_code,org_name,sale_code,SALE_NAME,HZ_BASE_PAY,HZ_POSITION_PAY,HZ_SAFE_FAN_SAL) 
                values(%s,'%s','%s','%s','%s',%s,%s,%s)
                '''%(date_id,i[10],i[1],i[2],i[3],int(Decimal(i[12])*100),int(Decimal(i[13])*100),int(Decimal(i[14])*100))
                g.db_session.execute(sql_insert_hz)
        g.db_session.commit()


        '''
        日均存款完成率(存款效酬)
        '''
        day_row_list={}
        branch_sec_rowList={}
        for i in his_com_branch:
            i=list(i)
            his_pos=i[5].split('-')[0]
            if his_pos in ['助理会计','大堂经理','后勤人员','见习人员','集中加钞员','综合柜员']:
                org=str(i[0])
                sale=str(i[2])
                if org+'-'+sale in day_row_list:
                    continue;
                else:
                    day_row_list[org+'-'+sale]=i

        for i in now_com_branch:
            i=list(i)
            his_pos=i[5].split('-')[0]
            if his_pos in ['助理会计','大堂经理','后勤人员','见习人员','集中加钞员','综合柜员']:
                org=str(i[0])
                sale=str(i[2])
                if org+'-'+sale in day_row_list:
                    continue;
                else:
                    day_row_list[org+'-'+sale]=i #日均存款完成率
        for i in his_com_branch:#二次分配
            i=list(i)
            his_pos=i[5].split('-')[0]
            if his_pos in ['派遣柜员','存款类客户经理','大堂引导员','外包人员','其他人员','试用期人员']:
                org=str(i[0])
                sale=str(i[2])
                if org+'-'+sale in branch_sec_rowList:
                    continue;
                else:
                    branch_sec_rowList[org+'-'+sale]=i

        for i in now_com_branch:
            i=list(i)
            his_pos=i[5].split('-')[0]
            if his_pos in ['派遣柜员','存款类客户经理','大堂引导员','外包人员','其他人员','试用期人员']:
                org=str(i[0])
                sale=str(i[2])
                if org+'-'+sale in branch_sec_rowList:
                    continue;
                else:
                    branch_sec_rowList[org+'-'+sale]=i#二次分配

        for i in day_row_list.values():

            sql_cunkun='''
            select 
            case when nvl(b.last_avg,0) >=0 and nvl(b.add_avg,0)>=0 then round((nvl(b.last_avg,0)+nvl(b.add_avg,0))*100) else round(nvl(b.last_avg,0)*100) end mon_avg,
            b.date_id, b.org_code,b.sale_code
            from
            ( SELECT DATE_ID,ORG_CODE,SALE_CODE, 
            SUM(nvl(LAST_AVG,0))/1000000.00 * %s /12 LAST_AVG , --算到月除以12 --8
            SUM(nvl(MONTH_AVG,0)-nvl(LAST_AVG,0) )/1000000.00 * %s add_avg  --4.6
            FROM YDW.REPORT_MANAGER_DEP
            join V_STAFF_INFO on SALE_CODE= USER_NAME
            WHERE DATE_ID = %s
            GROUP BY DATE_ID,ORG_CODE,SALE_CODE)b
            where b.ORG_CODE='%s' and b.sale_code ='%s'
            '''%(sql_rijuncun,sql_rijunzeng,date_id,i[0],i[2])
            row_cunkun=g.db_session.execute(sql_cunkun).fetchall()
            row_list=[]
            for i in row_cunkun:
                i=list(i)
                i[0]=int(i[0])
                i[1]=int(i[1])
                row_list.append(i)
            for i in row_list:

                update_sql='''
                update REPORT_MANAGER_OTHER set DAY_DEP_SAL=%s where date_id=%s and org_code='%s' and sale_code='%s'
                '''%(i[0],date_id,i[2],i[3])
                g.db_session.execute(update_sql)
        g.db_session.commit()

        '''
           支行二次分配:
        '''

        for i in branch_sec_rowList.values():

            zh_sec_sql='''
            select 
            case when nvl(b.last_avg,0) >=0 and nvl(b.add_avg,0)>=0 then round(nvl(b.last_avg,0)+nvl(b.add_avg,0)*100) else round(nvl(b.last_avg,0)*100) end mon_avg,
            b.date_id, b.org_code,b.sale_code
            from
            (SELECT DATE_ID,ORG_CODE,SALE_CODE, 
            SUM(nvl(LAST_AVG,0))/1000000.00 * %s /12 LAST_AVG , --算到月除以12 --8
            SUM(nvl(MONTH_AVG,0)-nvl(LAST_AVG,0) )/1000000.00 * %s add_avg --0.4
            FROM YDW.REPORT_MANAGER_DEP
            join V_STAFF_INFO on SALE_CODE= USER_NAME
            WHERE DATE_ID = %s
            GROUP BY DATE_ID,ORG_CODE,SALE_CODE)b
            where b.org_code='%s' and b.sale_code='%s'
            '''%(sql_zhihangcun,sql_zhihangzeng,date_id,i[0],i[2])
              
            row_sec_fen=g.db_session.execute(zh_sec_sql).fetchall()
            row_ls=[]
            for i in row_sec_fen:
                i=list(i)
                i[0]=int(i[0])
                i[1]=int(i[1])
                row_ls.append(i)
            for i in row_ls:

                update_sql='''
                update REPORT_MANAGER_OTHER set BRANCH_SECO_FEN1=%s where date_id=%s and org_code='%s' and sale_code='%s'
                '''%(i[0],date_id,i[2],i[3])
                g.db_session.execute(update_sql)
        g.db_session.commit()
        current_app.logger.debug('-----结束------')
        return u'计算成功'
    def edit_save(self,**kwargs):
        salary = kwargs.get('info')
        now_date_id=int(salary['now_date_id'])
        org_code=str(salary['org_code'])
        sale_code=str(salary['sale_code'])
        zw=str(salary['zw'])
        base_pay=float(''.join(str(salary['base_pay']).split(',')))
        position_pay=float(''.join(str(salary['position']).split(',')))
        safe_salary=float(''.join(str(salary['safe_salary']).split(',')))

        if zw in [u'行长(总经理)',u'副行长(主持)',u'副行长',u'行长助理','行长(总经理)','副行长(主持)','副行长','行长助理']:
            edit_update_sql='''
            update REPORT_MANAGER_HZSAL set HZ_BASE_PAY=%s,HZ_POSITION_PAY=%s,HZ_SAFE_FAN_SAL=%s where org_code='%s' and sale_code='%s' and date_id=%s    
            '''%(int(base_pay*100),int(position_pay*100),int(safe_salary*100),org_code,sale_code,now_date_id)
            g.db_session.execute(edit_update_sql)
        else:
            edit_update_otherSql='''
            update REPORT_MANAGER_OTHER set BASE_PAY=%s , POSITION_PAY=%s , SAFE_FAN_SAL=%s where ORG_CODE='%s' and  SALE_CODE ='%s' and date_id=%s 
            '''%(int(base_pay*100),int(position_pay*100),int(safe_salary*100),org_code,sale_code,now_date_id)
            g.db_session.execute(edit_update_otherSql)
        g.db_session.commit()
        return '编辑成功'




if __name__=='__main__':
    gdxc_salary()
