# -*- coding:utf-8 -*-
#!/bin/python  
import datetime
from flask import json, g,current_app
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all
import xlrd
from ..base import utils
from ..model.ebills import EbillsManager,EbillsHook
import os, time, random,sys
from datetime import datetime,timedelta
from decimal import Decimal
from ..model import EBILLS_QRY_SETTLEMENT_MANAGER as QRY_SETTLEMENT_MANAGER

class Ebills_ManagerService():
    def edit_save(self,**kwargs):
        manager = kwargs.get('info')
        org_code=str(manager['org_code'])
        sale_code=str(manager['f_user_no'])
        sale_name=str(manager['manager_name'])
        ebills_sale_code=str(manager['manager_no'])

        exist_flag_sql = '''
        select count(*) from EBILLS_MANAGER where f_user_no = %s
        '''%(sale_code)
        exist_flag = g.db_session.execute(exist_flag_sql).fetchone()
        exist_flag=int(exist_flag[0])

        if exist_flag == 0:
            ##无则新增
            self.ckyy = ['f_user_no','manager_no','manager_name']
            newdata =  kwargs.get('info')
            data ={}
            for k,v in newdata.items():
                if k in self.ckyy : data[k] = v
            g.db_session.add(EbillsManager(**data))
        else:
            ##有则更新
            edit_update_sql='''
                update EBILLS_MANAGER set manager_no='%s', manager_name='%s' where f_user_no='%s'
            '''%(ebills_sale_code, sale_name, sale_code)
            g.db_session.execute(edit_update_sql)

        g.db_session.commit()
        return '编辑成功'


    def manager_upload(self, filepath,filename):
        """
            批量录入
        """
        print '导入开始'
        try:

            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            #行
            nrows = sheet.nrows
            current_app.logger.debug(nrows)
            if nrows in [0,1,2]:
                raise Exception(u"警告:文件为空")
            bill_type_sign = ""
            list = []
        except Exception,e:
            return str(e)
        for r in range(2,nrows):
            try:
                f_user_no= str(int(sheet.cell(r,0).value))
                manager_no= str(sheet.cell(r,1).value)
                manager_name= sheet.cell(r,2).value

                if f_user_no.strip()=='':
                    raise Exception(u'请填写员工编号')
                if manager_name.strip()=='':
                    raise Exception(u'请填写员工名')
                if manager_no.strip()=='':
                    raise Exception(u'请填写国际业务客户编号')
                custinfo={
                'f_user_no':f_user_no,
                'manager_no':manager_no,
                'manager_name':manager_name
                 }
                current_app.logger.debug(custinfo)

                man_dep_value=g.db_session.query(EbillsManager).filter(EbillsManager.f_user_no==custinfo['f_user_no']).all()
                if man_dep_value:
                    g.db_session.query(EbillsManager).filter(EbillsManager.f_user_no==custinfo['f_user_no']).update(custinfo)
                else :
                    g.db_session.add(EbillsManager(**custinfo))

            except Exception,e:    
                g.db_session.rollback()
                print Exception,':',e
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        return u'导入成功'




    def internation_count(self,**kwargs):
        date_id = int(kwargs.get('internation_date'))
        sql="""
            select MONTHEND_ID from d_date where id=%s
        """%(date_id)
        aa=g.db_session.execute(sql).fetchone()
        if date_id != int(aa[0]):
            raise Exception(u"未到月末,不能计算")
        month=int(str(date_id)[:6])
        ebills_sql_count='''
        select count(*) from EBILLS_QRY_SETTLEMENT_MANAGER where month=%s
        '''%(month)
        count_num=g.db_session.execute(ebills_sql_count).fetchone()
        if count_num[0]==0:
            raise Exception(u"本月数据还未跑批完成,请耐心等待")
        ebills_sql_hook ="""
        select count(*) from ebills_hook where month=%s
        """%(month)
        count_hook_num=g.db_session.execute(ebills_sql_hook).fetchone()
        if count_hook_num[0]:
            raise Exception(u"本月国际业务已计算,无需重复计算")
        pa_manager="""
        merge into ebills_hook e
        using
        (select 
        MONTH,  --0
        v.org,  --1
        v.BRANCH_NAME,--2
        MANAGERID,--3
        v.USER_NAME,--4
        v.name,--5
        sum( EXLCCNT) as EXLCCNT, --6
        sum( EXLCAMT_THIS) as EXLCAMT_THIS,---出口来证通知金额本次 --7
        sum( EXBPCNT) as EXBPCNT,       --8
        sum( EXBPAMT_THIS) as EXBPAMT_THIS,---出口议付金额本次 --9
        sum( EXAGENTCNT) as EXAGENTCNT, --10
        sum( EXAGENTAMT_THIS) as EXAGENTAMT_THIS ,--出口托收金额本次 --11
        sum( EXCLEANCNT) as EXCLEANCNT,  --12
        sum( EXCLEANAMT_THIS) as EXCLEANAMT_THIS,---出口光票托收金额本次 --13
        sum( EXINREMITCNT) as EXINREMITCNT, --14
        sum( EXINREMITAMT_THIS) as EXINREMITAMT_THIS,--出口汇入汇款金额本次 --15
        sum( IMLCCNT) as IMLCCNT, --16
        sum( IMLCAMT_THIS) as IMLCAMT_THIS,----进口开证金额本次 --17
        sum( IMICCNT) as IMICCNT, --18
        sum( IMICAMT_THIS) as IMICAMT_THIS,---进口托收金额本次--19 
        sum( IMOUTREMITCNT) as IMOUTREMITCNT, --20
        sum( IMOUTREMTIAMT_THIS) as IMOUTREMTIAMT_THIS,----进口汇出汇款金额本次 --21
        sum( NTINREMITCNT) as NTINREMITCNT,   --22
        sum( NTINREMITAMT_THIS) as NTINREMITAMT_THIS,-----非贸易汇入汇款金额本次 --23
        sum( NTOUTREMITCNT) as NTOUTREMITCNT, --24
        sum( NTOUTREMITAMT_THIS) as NTOUTREMITAMT_THIS,------非贸易汇出汇款金额本次 --25
        sum( NTCLEANCNT) as NTCLEANCNT, --26
        sum( NTCLEANAMT_THIS) as NTCLEANAMT_THIS,-----非贸易光盘托收金额本次 --27
        sum( FIINREMITCNT) as FIINREMITCNT, --28
        sum( FIINREMITAMT_THIS) as FIINREMITAMT_THIS,-----资本项下汇入汇款金额本次 --29
        sum( FIOUTREMITCNT) as FIOUTREMITCNT, --30
        sum( FIOUTREMITAMT_THIS)as FIOUTREMITAMT_THIS,---资本项下汇出汇款金额本次 --31
        sum( CHARGECNT) as CHARGECNT, --32
        sum( CHARGEAMT_THIS) as CHARGEAMT_THIS,----手续费金额本次--33 
        0 as LGCNT, --34
        0 as LGAMT_THIS,  ----保函金额--35
        sum( IMLGCNT) as IMLGCNT, --36
        sum( IMLGAMT_THIS) as IMLGAMT_THIS ----进口保函金额本次--37
        from 
        EBILLS_QRY_SETTLEMENT_MANAGER e
        inner join EBILLS_MANAGER em on em.MANAGER_NO = e.MANAGERID----客户经理编码
        inner join V_STAFF_INFO v on v.USER_NAME=em.F_USER_NO
        where 1=1 and month=%s
        group by month,v.org,v.BRANCH_NAME,v.USER_NAME,v.name,MANAGERID) t
        on (e.MONTH=t.MONTH and e.ORG_CODE=t.org and e.SALE_CODE=t.USER_NAME and e.MANAGERID=t.MANAGERID)
        when matched then update set
        e.MONTH=t.MONTH , e.ORG_CODE=t.org , e.ORG_NAME=t.BRANCH_NAME, e.MANAGERID=t.MANAGERID,e.SALE_CODE=t.USER_NAME,e.SALE_NAME=t.name,
        e.EXLCCNT                =        t. EXLCCNT,
        e.EXLCAMT_THIS           =        t. EXLCAMT_THIS,
        e.EXBPCNT                =        t. EXBPCNT,
        e.EXBPAMT_THIS           =        t. EXBPAMT_THIS,
        e.EXAGENTCNT             =        t. EXAGENTCNT,
        e.EXAGENTAMT_THIS        =        t. EXAGENTAMT_THIS,
        e.EXCLEANCNT             =        t. EXCLEANCNT,
        e.EXCLEANAMT_THIS        =        t. EXCLEANAMT_THIS,
        e.EXINREMITCNT           =        t. EXINREMITCNT,
        e.EXINREMITAMT_THIS      =        t. EXINREMITAMT_THIS,
        e.IMLCCNT                =        t. IMLCCNT,
        e.IMLCAMT_THIS           =        t. IMLCAMT_THIS,
        e.IMICCNT                =        t. IMICCNT,
        e.IMICAMT_THIS           =        t. IMICAMT_THIS,
        e.IMOUTREMITCNT          =        t. IMOUTREMITCNT,
        e.IMOUTREMTIAMT_THIS     =        t. IMOUTREMTIAMT_THIS,
        e.NTINREMITCNT           =        t. NTINREMITCNT,
        e.NTINREMITAMT_THIS      =        t. NTINREMITAMT_THIS,
        e.NTOUTREMITCNT          =        t. NTOUTREMITCNT,
        e.NTOUTREMITAMT_THIS     =        t. NTOUTREMITAMT_THIS,
        e.NTCLEANCNT             =        t. NTCLEANCNT,
        e.NTCLEANAMT_THIS        =        t. NTCLEANAMT_THIS,
        e.FIINREMITCNT           =        t. FIINREMITCNT,
        e.FIINREMITAMT_THIS      =        t. FIINREMITAMT_THIS,
        e.FIOUTREMITCNT          =        t. FIOUTREMITCNT,
        e.FIOUTREMITAMT_THIS     =        t. FIOUTREMITAMT_THIS,
        e.CHARGECNT              =        t. CHARGECNT,
        e.CHARGEAMT_THIS         =        t. CHARGEAMT_THIS,
        e.LGCNT                  =        t. LGCNT,
        e.LGAMT_THIS             =        t. LGAMT_THIS,
        e.IMLGCNT                =        t. IMLGCNT,
        e.IMLGAMT_THIS           =        t. IMLGAMT_THIS
        when not matched then insert (
        e.MONTH,
        e.ORG_CODE,
        e.ORG_NAME,
        e.MANAGERID,
        e.SALE_CODE,
        e.SALE_NAME,
        e.EXLCCNT           ,
        e.EXLCAMT_THIS      ,
        e.EXBPCNT           ,
        e.EXBPAMT_THIS      ,
        e.EXAGENTCNT        ,
        e.EXAGENTAMT_THIS   ,
        e.EXCLEANCNT        ,
        e.EXCLEANAMT_THIS   ,
        e.EXINREMITCNT      ,
        e.EXINREMITAMT_THIS ,
        e.IMLCCNT           ,
        e.IMLCAMT_THIS      ,
        e.IMICCNT           ,
        e.IMICAMT_THIS      ,
        e.IMOUTREMITCNT     ,
        e.IMOUTREMTIAMT_THIS,
        e.NTINREMITCNT      ,
        e.NTINREMITAMT_THIS ,
        e.NTOUTREMITCNT     ,
        e.NTOUTREMITAMT_THIS,
        e.NTCLEANCNT        ,
        e.NTCLEANAMT_THIS   ,
        e.FIINREMITCNT      ,
        e.FIINREMITAMT_THIS ,
        e.FIOUTREMITCNT     ,
        e.FIOUTREMITAMT_THIS,
        e.CHARGECNT         ,
        e.CHARGEAMT_THIS    ,
        e.LGCNT             ,
        e.LGAMT_THIS        ,
        e.IMLGCNT           ,
        e.IMLGAMT_THIS 
        )values(
        t.MONTH,
        t.org,
        t.BRANCH_NAME,
        t.MANAGERID,
        t.USER_NAME,
        t.name,
        t.EXLCCNT           ,
        t.EXLCAMT_THIS      ,
        t.EXBPCNT           ,
        t.EXBPAMT_THIS      ,
        t.EXAGENTCNT        ,
        t.EXAGENTAMT_THIS   ,
        t.EXCLEANCNT        ,
        t.EXCLEANAMT_THIS   ,
        t.EXINREMITCNT      ,
        t.EXINREMITAMT_THIS ,
        t.IMLCCNT           ,
        t.IMLCAMT_THIS      ,
        t.IMICCNT           ,
        t.IMICAMT_THIS      ,
        t.IMOUTREMITCNT     ,
        t.IMOUTREMTIAMT_THIS,
        t.NTINREMITCNT      ,
        t.NTINREMITAMT_THIS ,
        t.NTOUTREMITCNT     ,
        t.NTOUTREMITAMT_THIS,
        t.NTCLEANCNT        ,
        t.NTCLEANAMT_THIS   ,
        t.FIINREMITCNT      ,
        t.FIINREMITAMT_THIS ,
        t.FIOUTREMITCNT     ,
        t.FIOUTREMITAMT_THIS,
        t.CHARGECNT         ,
        t.CHARGEAMT_THIS    ,
        t.LGCNT             ,
        t.LGAMT_THIS        ,
        t.IMLGCNT           ,
        t.IMLGAMT_THIS )
        """%(month)
        g.db_session.execute(pa_manager)
        insert_virtual="""
        insert into ebills_hook(month,org_code,org_name,sale_code,sale_name)
        select %s,org,branch_name,user_name,name from V_STAFF_INFO where USER_NAME like 'F%%' 
        """%(month)
        g.db_session.execute(insert_virtual)
        balance_sql='''
        merge into EBILLS_HOOK eh
        using
        (
        select org_no,sale_code,v.branch_name org_name,v.name sale_name,MANAGER_NO,sum(nvl(balance,0)) as balance  from report_sale_rmb_exg e
        left join  ebills_manager f on f.f_user_no=e.sale_code
        join  v_staff_info v on  e.org_no=v.org and e.sale_code=v.user_name
        where e.date_id=%s
        group by org_no,sale_code,MANAGER_NO,v.name,v.branch_name
        ) a on   ---余额
        (eh.month=%s and eh.org_code=a.org_no and eh.sale_code=a.sale_code)
        when matched then update set eh.BALANCE=a.balance,eh.MANAGERID=a.MANAGER_NO,eh.org_name=a.org_name,eh.sale_name=a.sale_name
        when not matched then insert (eh.month,eh.org_code,eh.sale_code,eh.MANAGERID,eh.balance,eh.org_name,eh.sale_name) values(%s,a.org_no,a.sale_code,a.MANAGER_NO,a.balance,a.org_name,a.sale_name) 
        '''%(date_id,month,month)
        g.db_session.execute(balance_sql)#余额
        month_avg='''
        merge into EBILLS_HOOK eh
        using
        (
        select MANAGER_NO,d.ym,beg_month_days,org_no,sale_code,v.branch_name org_name,v.name sale_name,((sum(nvl(balance,0))*1.0)/d.beg_month_days) as avn_month   from report_sale_rmb_exg e 
        join d_date d on d.id=e.date_id
        left join  ebills_manager f on f.f_user_no=e.sale_code
        join  v_staff_info v on  e.org_no=v.org and e.sale_code=v.user_name
        where d.id=%s
        group by MANAGER_NO,d.ym,org_no,sale_code,beg_month_days,v.name,v.branch_name
        ) a on   ---月日均
        (eh.month=%s and eh.org_code=a.org_no and eh.sale_code=a.sale_code)
        when matched then update set eh.MONTHAMT=a.avn_month,eh.MANAGERID=a.MANAGER_NO,eh.org_name=a.org_name,eh.sale_name=a.sale_name
        when not matched then insert (eh.month,eh.org_code,eh.sale_code,eh.MANAGERID,eh.MONTHAMT,eh.org_name,eh.sale_name) values(%s,a.org_no,a.sale_code,a.MANAGER_NO,a.avn_month,a.org_name,a.sale_name) 
        '''%(date_id,month,month)
        g.db_session.execute(month_avg)#月日均
        year_avg='''
        merge into EBILLS_HOOK eh
        using
        (
        select MANAGER_NO,d.year,beg_year_days,org_no,sale_code,v.branch_name org_name,v.name sale_name,(sum(nvl(balance,0))*1.0)/d.beg_year_days  as avg_year from report_sale_rmb_exg e 
        join d_date d on d.id=e.date_id
        left join  ebills_manager f on f.f_user_no=e.sale_code
        join  v_staff_info v on  e.org_no=v.org and e.sale_code=v.user_name
        where d.id=%s
        group by MANAGER_NO,d.year,org_no,sale_code,beg_year_days,v.name,v.branch_name
        ) a on --年日均
        (eh.month=%s  and eh.org_code=a.org_no and eh.sale_code=a.sale_code)
        when matched then update set eh.DAYAMT=a.avg_year,eh.MANAGERID=a.MANAGER_NO,eh.org_name=a.org_name,eh.sale_name=a.sale_name
        when not matched then insert (eh.month,eh.org_code,eh.sale_code,eh.MANAGERID,eh.DAYAMT,eh.org_name,eh.sale_name) values(%s,a.org_no,a.sale_code,a.MANAGER_NO,a.avg_year,a.org_name,a.sale_name)
        '''%(date_id,month,month)
        g.db_session.execute(year_avg)#月日均
        g.db_session.commit()
        
        #'''
        #新开外汇账户
        #'''
        #yearbeg=int(str(month)[:4]+'0101')
        #newopen_this_dir={}
        #account_list=[]
        #foreign_exange1="""
        #select
        #ah.ORG_NO,
        #ah.MANAGER_NO,
        #d.ACCOUNT_NO
        #from d_account d
        #join ACCOUNT_HOOK ah on d.ACCOUNT_NO=ah.account_no 
        #join F_JRN_TRANSACTION f on d.ACCOUNT_NO=f.ACCT_NO --会计流水表
        #where d.ccy in ( 'AUD','EUR','GBP','HKD','JPY','SGD','USD' )
        #and ah.HOOK_TYPE='管户'
        #and f.DATE_ID>=%s and f.DATE_ID<=%s ----交易一定是在本年的
        #and f.AMOUNT!=0
        #and d.OPEN_DATE_ID>=%s and d.OPEN_DATE_ID<=%s ---本年开户的
        #group by ah.ORG_NO,ah.MANAGER_NO,d.ACCOUNT_NO
        #having count(*)>0
        #with ur
        #"""%(yearbeg,date_id,yearbeg,date_id)
        #newopen_thisyear=g.db_session.execute(foreign_exange1).fetchall()
        #for i in newopen_thisyear:
        #    if i[0]+'-'+i[1] in newopen_this_dir
        #    newopen_this_dir[i[0]+'-'+i[1]]=
        return '计算成功'


    def hook_edit_save(self,**kwargs):
        custinfo_ebills =kwargs.get('custinfo')
        for i in custinfo_ebills.keys():
            if i in ['MONTH','ID','ORG_CODE','ORG_NAME','MANAGERID','SALE_CODE','SALE_NAME']:
                pass
            else:
                custinfo_ebills[i]=int(Decimal(''.join(str(custinfo_ebills[i]).split(',')))*100)
        g.db_session.query(EbillsHook).filter(EbillsHook.ID==custinfo_ebills['ID']).update(custinfo_ebills)
        return '修改成功'

    def total_sum_save(self,**kwargs):
        original_row=kwargs.get('original_row')
        new_row=kwargs.get('new_row')
        current_app.logger.debug(original_row)
        current_app.logger.debug(new_row)
        for i in original_row.keys():
            if i in ['MONTH','ID','ORG_CODE','ORG_NAME','MANAGERID','SALE_CODE','SALE_NAME']:
                pass
            else:
                original_row[i]=int(Decimal(''.join(str(original_row[i]).split(',')))*100)
        g.db_session.query(EbillsHook).filter(EbillsHook.ID==original_row['ID']).update(original_row)

        for i in new_row.keys():
            if i in ['MONTH','ID','ORG_CODE','ORG_NAME','MANAGERID','SALE_CODE','SALE_NAME']:
                pass
            else:
                new_row[i]=int(Decimal(''.join(str(new_row[i]).split(',')))*100)
        g.db_session.query(EbillsHook).filter(EbillsHook.ID==new_row['ID']).update(new_row)

        return '修改成功'







if __name__=='__main__':
    #Ebills_ManagerService()
    pass
