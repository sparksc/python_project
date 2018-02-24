# -*- coding:utf-8 -*-
#!/bin/python  
import datetime
from flask import json, g,current_app
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all
import xlrd
from ..base import utils
from ..model.ebills import EbillsHook,EbillsHook_DISINFO,EbillsHook_ORG,EbillsHook_CUNKUAN
import os, time, random,sys
from datetime import datetime,timedelta
from decimal import Decimal
from ..model.QRY_SETTLEMENT_MANAGER import EBILLS_QRY_SETTLEMENT_CORP
sys.path.append('/home/develop/src/')
from etl.star.model.odsfile import PA_MANAGERCORPINFO,PA_MANAGERINFO,PA_CORP
from etl.base.util import cust_in_fo

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

    def org_stand_update(self,**kwargs):
        date_id = kwargs.get('month')
        month=int(str(date_id)[:6])
        ebills_hook_org_s="""select month,org_flag from ebills_hook_org where month=%s """%(month)
        set_org=g.db_session.execute(ebills_hook_org_s).fetchone()
        if set_org:
            if set_org[1]=='Y':
                raise Exception(u"此月%s数据已生效"%(month))
            else:
                g.db_session.execute("update ebills_hook_org set org_flag='Y' where month=%s"%(month))
        else:
            raise Exception(u"此月%s没有数据"%(month))
        g.db_session.commit()
        return '生效成功'

    def org_stand_delete(self,**kwargs):
        date_id = kwargs.get('month')
        month=int(str(date_id)[:6])
        g.db_session.execute("delete from  ebills_hook_org  where month=%s"%(month))
        g.db_session.commit()
        return '删除成功'


    def org_cunkuan_update(self,**kwargs):
        date_id = kwargs.get('month')
        month=int(str(date_id)[:6])
        ebills_hook_org_s="""select month,org_flag from EBILLS_HOOK_CUNKUAN where month=%s """%(month)
        set_org=g.db_session.execute(ebills_hook_org_s).fetchone()
        if set_org:
            if set_org[1]=='Y':
                raise Exception(u"此月%s数据已生效"%(month))
            else:
                g.db_session.execute("update EBILLS_HOOK_CUNKUAN set org_flag='Y' where month=%s"%(month))
        else:
            raise Exception(u"此月%s没有数据"%(month))
        g.db_session.commit()
        return '生效成功'

    def org_cunkuan_delete(self,**kwargs):
        date_id = kwargs.get('month')
        month=int(str(date_id)[:6])
        g.db_session.execute("delete from  EBILLS_HOOK_CUNKUAN  where month=%s"%(month))
        g.db_session.commit()
        return '删除成功'


    def ebills_hook_upload(self, filepath,filename):
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
            if nrows <5:
                raise Exception(u"警告:文件为空")
        except Exception,e:
            return str(e)
        f_user_dict={}
        f_user_sql="""select user_name,NAME from F_USER"""
        f_user_sql=g.db_session.execute(f_user_sql).fetchall()
        for i in f_user_sql:
            f_user_dict[i[0]]=i[1]

        org_dict={}
        org_sql="""select branch_code,BRANCH_NAME from branch"""
        org=g.db_session.execute(org_sql).fetchall()
        for i in org:
            org_dict[i[0]]=i[1]
        org_month_list=[]
        org_month=""" select distinct month from ebills_hook_org """
        org_month=g.db_session.execute(org_month).fetchall()
        for i in org_month:
            org_month_list.append(int(i[0]))

        for r in range(4,nrows):
            try:
                MONTH= str(sheet.cell(r,0).value).replace('.0',"").replace('.00',"").strip()
                ORG_CODE= str(sheet.cell(r,1).value).replace('.0',"").replace('.00',"").strip()
                ORG_NAME= str(sheet.cell(r,2).value)
                CUST_IN_NO= str(sheet.cell(r,3).value).replace('.0',"").replace('.00',"").strip()
                CORPNAME= str(sheet.cell(r,4).value)
                SALE_CODE= str(sheet.cell(r,5).value).replace('.0',"").replace('.00',"").strip()
                SALE_NAME= str(sheet.cell(r,6).value)
                TOTAL_SET= str(sheet.cell(r,7).value)
                TOTAL_CROSS= str(sheet.cell(r,8).value)
                IS_OPEN_NEW_WH= str(sheet.cell(r,9).value)

                if MONTH.strip()=='':
                    raise Exception(u'请填写月份')
                if ORG_CODE.strip()=='':
                    raise Exception(u'请填写机构号')
                if CUST_IN_NO.strip()=='':
                    raise Exception(u'请填写客户内码')
                if CORPNAME.strip()=='':
                    raise Exception(u'请填写客户名')
                if ORG_CODE in org_dict:
                    ORG_NAME=org_dict.get(ORG_CODE)
                else:
                    raise Exception(u'第%s行此机构号"%s"不存在'%(r+1,ORG_CODE))
                if SALE_CODE in f_user_dict:
                    SALE_NAME=f_user_dict.get(SALE_CODE)

                if int(MONTH) in org_month_list:
                    raise Exception(u'此月份%s已导入,无需再次导入'%(str(MONTH)))
                    
                custinfo={
                'MONTH':int(MONTH),
                'ORG_CODE':ORG_CODE,
                'ORG_NAME':ORG_NAME,
                'CUST_IN_NO':CUST_IN_NO,
                'CORPNAME':CORPNAME,
                'SALE_CODE':SALE_CODE,
                'SALE_NAME':SALE_NAME,
                'TOTAL_SET':Decimal(TOTAL_SET)*1000000,
                'TOTAL_CROSS':Decimal(TOTAL_CROSS)*1000000,
                'IS_OPEN_NEW_WH':IS_OPEN_NEW_WH
                }

                g.db_session.add(EbillsHook_ORG(**custinfo))

            except Exception,e:    
                g.db_session.rollback()
                print Exception,':',e
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        return u'导入成功'



    def ebills_hook_cunkuan_upload(self, filepath,filename):
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
            if nrows <5:
                raise Exception(u"警告:文件为空")
        except Exception,e:
            return str(e)
        org_dict={}
        org_sql="""select branch_code,BRANCH_NAME from branch"""
        org=g.db_session.execute(org_sql).fetchall()
        for i in org:
            org_dict[i[0]]=i[1]
        org_month_list=[]
        org_month=""" select distinct month from ebills_hook_cunkuan """
        org_month=g.db_session.execute(org_month).fetchall()
        for i in org_month:
            org_month_list.append(int(i[0]))

        for r in range(4,nrows):
            try:
                MONTH= str(sheet.cell(r,0).value).replace('.0',"").replace('.00',"").strip()
                ORG_CODE= str(sheet.cell(r,1).value).replace('.0',"").replace('.00',"").strip()
                ORG_NAME= str(sheet.cell(r,2).value)
                CUST_IN_NO= str(sheet.cell(r,3).value).replace('.0',"").replace('.00',"").strip()
                CORPNAME= str(sheet.cell(r,4).value)
                BALANCE= str(sheet.cell(r,5).value)
                MONTHAMT= str(sheet.cell(r,6).value)
                DAYAMT= str(sheet.cell(r,7).value)

                if MONTH.strip()=='':
                    raise Exception(u'请填写月份')
                if ORG_CODE.strip()=='':
                    raise Exception(u'请填写机构号')
                if CUST_IN_NO.strip()=='':
                    raise Exception(u'请填写客户内码')
                if CORPNAME.strip()=='':
                    raise Exception(u'请填写客户名')
                if ORG_CODE in org_dict:
                    ORG_NAME=org_dict.get(ORG_CODE)
                else:
                    raise Exception(u'第%s行此机构号"%s"不存在'%(r+1,ORG_CODE))

                if int(MONTH) in org_month_list:
                    raise Exception(u'此月份%s已导入,无需再次导入'%(str(MONTH)))
                    
                custinfo={
                'MONTH':int(MONTH),
                'ORG_CODE':ORG_CODE,
                'ORG_NAME':ORG_NAME,
                'CUST_IN_NO':CUST_IN_NO,
                'CORPNAME':CORPNAME,
                'BALANCE':Decimal(BALANCE)*1000000,
                'MONTHAMT':Decimal(MONTHAMT)*1000000,
                'DAYAMT':Decimal(DAYAMT)*1000000
                }

                g.db_session.add(EbillsHook_CUNKUAN(**custinfo))

            except Exception,e:    
                g.db_session.rollback()
                print Exception,':',e
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        return u'导入成功'



    def fix_seq_id(self,tabname,seqname):
        sql ="""select max(id) from %s"""%tabname
        maxid =g.db_session.execute(sql).fetchone()
        sqll="""select nextval for %s from sysibm.dual"""%seqname
        idd=g.db_session.execute(sqll).fetchone()
        while idd[0]<=maxid[0]:
            idd=g.db_session.execute(sqll).fetchone()
        g.db_session.execute("alter table EBILLS_HOOK alter column id restart with %s"%(idd[0]))





    def managerfno(self,date):
        self.pa_corp_list={}
        managerid = PA_MANAGERCORPINFO(date).loadfile2dict()
        self.manager=PA_MANAGERINFO(date).loadfile2dict()

        pa_corp=PA_CORP(date).loadfile2dict()
        for i in pa_corp:
            self.pa_corp_list[pa_corp[i]['MAINCORPNO']]=i
        self.managerid={}
        for i in managerid:
            self.managerid['-'.join([i.split('-')[1],i.split('-')[2]])]=managerid[i]

    def SIGHTAM_SALE(self,month,date_id,userinfo,cust_in_noinfo,devlop_base):#结售汇 
        self.IMMEDIATE={}#即期
        self.FUTURE_SPFE_TYPE={}#远期
        self.FOREIGN_SPFE_TYPE={}#跨境
        SIGHTAMT_sql="""
        select   
        to_char(f.LAUNCHDATE,'yyyyMM') month1,sum(f.USD_AMOUNT),f.CORP_NAME,f.IN_CST_NO,CORPNO,BELONGORGNO,br.BRANCH_NAME
        from SNAP_EBILLS_BU_TRANSACTIONINFO f
        inner join  d_ebills_tran_type t on t.id = f.TRAN_TYPE_ID
        join BRANCH br on BELONGORGNO=br.BRANCH_CODE
        where 
        t.immediate_SPFE_TYPE='即期结售汇'
        and amount !=0 
        and to_char(f.LAUNCHDATE,'yyyyMM')='%s' and DATE_ID=%s
        and IN_CST_NO is not null
        group by to_char(LAUNCHDATE,'yyyyMM'),f.IN_CST_NO,CORP_NAME,IN_CST_NO,CORPNO,BELONGORGNO,BRANCH_NAME
        """%(str(month),date_id)
        SIGHTAMT_sql=g.db_session.execute(SIGHTAMT_sql).fetchall()
        current_app.logger.debug(SIGHTAMT_sql)
        if len(SIGHTAMT_sql):
            for i in SIGHTAMT_sql:
                if str(i[3]) in cust_in_noinfo:
                    continue
                ebills_all={}
                ebills_all['MONTH']=int(i[0])
                ebills_all['SIGHTAMT']=i[1]
                ebills_all['CORPNAME']=(i[2])
                ebills_all['CUST_IN_NO']=(i[3])
                ebills_all['CORPNO']=(i[4])
                ebills_all['ORG_CODE']=(i[5])
                ebills_all['ORG_NAME']=(i[6])
                ebills_all['SALE_CODE']=""
                ebills_all['SALE_NAME']=""
                ebills_all['OPEN_DATE']=0

                sql_open="""
                    select cst_no,OPEN_DATE_ID
                    from
                    (select cst_no,OPEN_DATE_ID from D_ACCOUNT where CCY!='CNY' and  OPEN_DATE_ID <=%d and cst_no='%s' group by CST_NO,OPEN_DATE_ID)
                    order by OPEN_DATE_ID desc
                """%(date_id,str(ebills_all['CUST_IN_NO']))            
                opendate=g.db_session.execute(sql_open).fetchone()
                if opendate:
                    ebills_all['OPEN_DATE']=int(opendate[1] or 0)
                manager1=ebills_all['CORPNO']+'-'+'I'
                manager2=ebills_all['CORPNO']+'-'+'A'
                if self.managerid.get(manager2):
                    managerinfo=self.managerid.get(manager2)
                else:
                    managerinfo=self.managerid.get(manager1)
                if managerinfo is not None:
                    managerid=managerinfo.get('MANAGERID')
                    sale_name=self.manager.get(managerid)
                    if sale_name is not None:
                        ebills_all["SALE_NAME"]=sale_name.get('MANAGERNAME').decode("gbk").encode("utf-8")
                        if sale_name.get('WORKNO'):
                            ebills_all["SALE_CODE"]=sale_name.get('WORKNO')
                        else:
                            ebills_all["SALE_CODE"]=userinfo.get(ebills_all["SALE_NAME"])
                if str(ebills_all['CUST_IN_NO']) in self.IMMEDIATE:
                    self.IMMEDIATE[str(ebills_all['CUST_IN_NO'])]['SIGHTAMT']+=ebills_all['SIGHTAMT']
                else:
                    self.IMMEDIATE[str(ebills_all['CUST_IN_NO'])]=ebills_all
        current_app.logger.debug(self.IMMEDIATE)

        USANCEAMT_sql="""
        select   
        to_char(f.finisheddate,'yyyyMM') month1,sum(f.USD_AMOUNT),f.CORP_NAME,f.IN_CST_NO,CORPNO,BELONGORGNO,br.BRANCH_NAME
        from SNAP_EBILLS_BU_TRANSACTIONINFO f
        inner join  d_ebills_tran_type t on t.id = f.TRAN_TYPE_ID
        join BRANCH br on BELONGORGNO=br.BRANCH_CODE
        where 
        t.FUTURE_SPFE_TYPE='远期结售汇'
        and amount !=0 
        and to_char(f.finisheddate,'yyyyMM')='%s' and DATE_ID=%s
        and IN_CST_NO is not null
        group by to_char(finisheddate,'yyyyMM'),f.IN_CST_NO,CORP_NAME,IN_CST_NO,CORPNO,BELONGORGNO,BRANCH_NAME
        """%(str(month),date_id)
        USANCEAMT_sql=g.db_session.execute(USANCEAMT_sql).fetchall()
        if len(USANCEAMT_sql):
            for i in USANCEAMT_sql:
                if str(i[3]) in cust_in_noinfo:
                    continue
                ebills_all={}
                ebills_all['MONTH']=int(i[0])
                ebills_all['USANCEAMT']=i[1]
                ebills_all['CORPNAME']=(i[2])
                ebills_all['CUST_IN_NO']=(i[3])
                ebills_all['CORPNO']=(i[4])
                ebills_all['ORG_CODE']=(i[5])
                ebills_all['ORG_NAME']=(i[6])
                ebills_all['SALE_CODE']=""
                ebills_all['SALE_NAME']=""
                ebills_all['OPEN_DATE']=0
                sql_open="""
                    select cst_no,OPEN_DATE_ID
                    from
                    (select cst_no,OPEN_DATE_ID from D_ACCOUNT where CCY!='CNY' and  OPEN_DATE_ID <=%d and cst_no='%s' group by CST_NO,OPEN_DATE_ID)
                    order by OPEN_DATE_ID desc
                """%(date_id,str(ebills_all['CUST_IN_NO']))            
                opendate=g.db_session.execute(sql_open).fetchone()
                if opendate:
                    ebills_all['OPEN_DATE']=int(opendate[1] or 0)

                manager1=ebills_all['CORPNO']+'-'+'I'
                manager2=ebills_all['CORPNO']+'-'+'A'
                if self.managerid.get(manager2):
                    managerinfo=self.managerid.get(manager2)
                else:
                    managerinfo=self.managerid.get(manager1)
                if managerinfo is not None:
                    managerid=managerinfo.get('MANAGERID')
                    sale_name=self.manager.get(managerid)
                    if sale_name is not None:
                        ebills_all["SALE_NAME"]=sale_name.get('MANAGERNAME').decode("gbk").encode("utf-8")
                        if sale_name.get('WORKNO'):
                            ebills_all["SALE_CODE"]=sale_name.get('WORKNO')
                        else:
                            ebills_all["SALE_CODE"]=userinfo.get(ebills_all["SALE_NAME"])

                if str(ebills_all['CUST_IN_NO']) in self.FUTURE_SPFE_TYPE:
                    self.FUTURE_SPFE_TYPE[str(ebills_all['CUST_IN_NO'])]['USANCEAMT']+=ebills_all['USANCEAMT']
                else:
                    self.FUTURE_SPFE_TYPE[str(ebills_all['CUST_IN_NO'])]=ebills_all

        CROSSBORDERAMT_sql="""
        select   
        to_char(f.LAUNCHDATE,'yyyyMM') month1,sum(f.USD_AMOUNT)*(1+%s),f.CORP_NAME,f.IN_CST_NO,CORPNO,BELONGORGNO,br.BRANCH_NAME
        from SNAP_EBILLS_BU_TRANSACTIONINFO f
        inner join  d_ebills_tran_type t on t.id = f.TRAN_TYPE_ID
        join BRANCH br on BELONGORGNO=br.BRANCH_CODE
        where 
        t.FOREIGN_SPFE_TYPE='跨境结售汇'
        and amount !=0
        and IN_CST_NO is not null
        and to_char(f.LAUNCHDATE,'yyyyMM')='%s' and DATE_ID=%s
        group by to_char(LAUNCHDATE,'yyyyMM'),f.IN_CST_NO,CORP_NAME,IN_CST_NO,CORPNO,BELONGORGNO,BRANCH_NAME
        """%(devlop_base,str(month),date_id)
        current_app.logger.debug(CROSSBORDERAMT_sql)
        CROSSBORDERAMT_sql=g.db_session.execute(CROSSBORDERAMT_sql).fetchall()
        if len(CROSSBORDERAMT_sql):
            for i in CROSSBORDERAMT_sql:
                if str(i[3]) in cust_in_noinfo:
                    continue
                ebills_all={}
                ebills_all['MONTH']=int(i[0])
                ebills_all['CROSSBORDERAMT']=i[1]
                ebills_all['CORPNAME']=(i[2])
                ebills_all['CUST_IN_NO']=(i[3])
                ebills_all['CORPNO']=(i[4])
                ebills_all['ORG_CODE']=(i[5])
                ebills_all['ORG_NAME']=(i[6])
                ebills_all['SALE_CODE']=""
                ebills_all['SALE_NAME']=""
                ebills_all['OPEN_DATE']=0
                sql_open="""
                    select cst_no,OPEN_DATE_ID
                    from
                    (select cst_no,OPEN_DATE_ID from D_ACCOUNT where CCY!='CNY' and  OPEN_DATE_ID <=%d and cst_no='%s' group by CST_NO,OPEN_DATE_ID)
                    order by OPEN_DATE_ID desc
                """%(date_id,str(ebills_all['CUST_IN_NO']))            
                opendate=g.db_session.execute(sql_open).fetchone()
                if opendate:
                    ebills_all['OPEN_DATE']=int(opendate[1] or 0)
                manager1=ebills_all['CORPNO']+'-'+'I'
                manager2=ebills_all['CORPNO']+'-'+'A'
                if self.managerid.get(manager2):
                    managerinfo=self.managerid.get(manager2)
                else:
                    managerinfo=self.managerid.get(manager1)
                if managerinfo is not None:
                    managerid=managerinfo.get('MANAGERID')
                    sale_name=self.manager.get(managerid)
                    if sale_name is not None:
                        ebills_all["SALE_NAME"]=sale_name.get('MANAGERNAME').decode("gbk").encode("utf-8")
                        if sale_name.get('WORKNO'):
                            ebills_all["SALE_CODE"]=sale_name.get('WORKNO')
                        else:
                            ebills_all["SALE_CODE"]=userinfo.get(ebills_all["SALE_NAME"])
                if str(ebills_all['CUST_IN_NO']) in self.FOREIGN_SPFE_TYPE:
                    self.FOREIGN_SPFE_TYPE[str(ebills_all['CUST_IN_NO'])]['CROSSBORDERAMT']+=ebills_all['CROSSBORDERAMT']
                else:
                    self.FOREIGN_SPFE_TYPE[str(ebills_all['CUST_IN_NO'])]=ebills_all

        

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
        select count(*) from EBILLS_QRY_SETTLEMENT_CORP where month=%s
        '''%(month)
        count_num=g.db_session.execute(ebills_sql_count).fetchone()
        if count_num[0]==0:
            raise Exception(u"本月数据还未跑批完成,请耐心等待")

        #ebills_sql_hook ="""
        #select count(*) from ebills_hook where month=%s
        #"""%(month)
        #count_hook_num=g.db_session.execute(ebills_sql_hook).fetchone()
        #if count_hook_num[0]:
        #    raise Exception(u"本月国际业务已计算,无需重复计算")
        ebills_sql_hook ="""delete from ebills_hook where month=%s"""%(month)
        g.db_session.execute(ebills_sql_hook)
        g.db_session.commit()
        self.managerfno(date_id)
        userinfo={}
        f_user="""
        select f.user_name,f.NAME from f_user f
        join
        (select NAME from F_USER group by NAME having count(*)=1) eh
        on f.name=eh.name
        """
        f_userinfo=g.db_session.execute(f_user).fetchall()
        for i in f_userinfo:
            userinfo[i[1].encode('utf-8')]=i[0]
        cust_in_noinfo=[]

        f_orgusrdict={}
        f_orgusr="""
        select user_name, ORG from V_STAFF_INFO
        """
        f_org_usr=g.db_session.execute(f_orgusr).fetchall()
        for i in f_org_usr:
            f_orgusrdict[i[0]]=i[1]

        devlop_base=g.db_session.execute("""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_NAME='国际业务跨境基数上调' and HEADER_NAME='国际业务跨境上调基数'
        """).fetchone()

        devlop_base=Decimal(str(devlop_base[0]))


        self.fix_seq_id('ebills_hook','ebills_hook_seq')

        pa_manager="""
        select 
        max(MONTH         )as  MONTH        ,
        max(ORGNO)        as   ORGNO,
        max(CORPNO)       as   CORPNO       ,
        max(EXLCCNT       )as  EXLCCNT      ,
        max(EXLCAMT       )as  EXLCAMT      ,
        max(EXBPCNT       )as  EXBPCNT      ,
        max(EXBPAMT       )as  EXBPAMT      ,
        max(EXAGENTCNT    )as  EXAGENTCNT   ,
        max(EXAGENTAMT    )as  EXAGENTAMT   ,
        max(EXCLEANCNT    )as  EXCLEANCNT   ,
        max(EXCLEANAMT    )as  EXCLEANAMT   ,
        max(EXINREMITCNT  )as  EXINREMITCNT ,
        max(EXINREMITAMT  )as  EXINREMITAMT ,
        max(IMLCCNT       )as  IMLCCNT      ,
        max(IMLCAMT       )as  IMLCAMT      ,
        max(IMICCNT       )as  IMICCNT      ,
        max(IMICAMT       )as  IMICAMT      ,
        max(IMOUTREMITCNT )as  IMOUTREMITCNT,
        max(IMOUTREMTIAMT )as  IMOUTREMTIAMT,
        max(NTINREMITCNT  )as  NTINREMITCNT ,
        max(NTINREMITAMT  )as  NTINREMITAMT ,
        max(NTOUTREMITCNT )as  NTOUTREMITCNT,
        max(NTOUTREMITAMT )as  NTOUTREMITAMT,
        max(NTCLEANCNT    )as  NTCLEANCNT   ,
        max(NTCLEANAMT    )as  NTCLEANAMT   ,
        max(FIINREMITCNT  )as  FIINREMITCNT ,
        max(FIINREMITAMT  )as  FIINREMITAMT ,
        max(FIOUTREMITCNT )as  FIOUTREMITCNT,
        max(FIOUTREMITAMT )as  FIOUTREMITAMT,
        max(CHARGECNT     )as  CHARGECNT    ,
        max(CHARGEAMT     )as  CHARGEAMT    ,
        max(0)             as  LGCNT ,
        max(0)             as  LGAMT,
        max(IMLGCNT       )as  IMLGCNT      ,
        max(IMLGAMT       )as  IMLGAMT , 
        max(ORG_CODE),
        max(ORG_NAME),
        max(SALE_CODE),
        max(SALE_NAME),
        max(CORP_NAME),
        max(CUST_IN_NO),
        max(OPEN_DATE)
        from EBILLS_QRY_SETTLEMENT_CORP
        where MONTH=%s group by CORPNO,ORGNO"""%(month)
        rs = g.db_session.execute(pa_manager)
        for i in rs:
            ebills_all={}
            ebills_all['MONTH']         =i[0]
            ebills_all['CORPNO']         =i[2]
            ebills_all['EXLCCNT']        =i[3]
            ebills_all['EXLCAMT']        =i[4]
            ebills_all['EXBPCNT']        =i[5]
            ebills_all['EXBPAMT']        =i[6]
            ebills_all['EXAGENTCNT']     =i[7]
            ebills_all['EXAGENTAMT']     =i[8]
            ebills_all['EXCLEANCNT']     =i[9]
            ebills_all['EXCLEANAMT']     =i[10]
            ebills_all['EXINREMITCNT']   =i[11]
            ebills_all['EXINREMITAMT']   =i[12]
            ebills_all['IMLCCNT']        =i[13]
            ebills_all['IMLCAMT']        =i[14]
            ebills_all['IMICCNT']        =i[15]
            ebills_all['IMICAMT']        =i[16]
            ebills_all['IMOUTREMITCNT']  =i[17]
            ebills_all['IMOUTREMTIAMT']  =i[18]
            ebills_all['NTINREMITCNT']   =i[19]
            ebills_all['NTINREMITAMT']   =i[20]
            ebills_all['NTOUTREMITCNT']  =i[21]
            ebills_all['NTOUTREMITAMT']  =i[22]
            ebills_all['NTCLEANCNT']     =i[23]
            ebills_all['NTCLEANAMT']     =i[24]
            ebills_all['FIINREMITCNT']   =i[25]
            ebills_all['FIINREMITAMT']   =i[26]
            ebills_all['FIOUTREMITCNT']  =i[27]
            ebills_all['FIOUTREMITAMT']  =i[28]
            ebills_all['CHARGECNT']      =i[29]
            ebills_all['CHARGEAMT']      =i[30]
            ebills_all['LGCNT']          =i[31]
            ebills_all['LGAMT']          =i[32]
            ebills_all['IMLGCNT']        =i[33]
            ebills_all['IMLGAMT']        =i[34]
            ebills_all['ORG_CODE']       =i[35]
            ebills_all['ORG_NAME']       =i[36]
            if i[37]:
                ebills_all['SALE_CODE']=i[37]
                ebills_all['SALE_NAME']=i[38]
            else:
                ebills_all['SALE_CODE']=userinfo.get(i[38].encode('utf-8'))
                ebills_all['SALE_NAME']=i[38]
            ebills_all['CORPNAME']   =i[39]
            ebills_all['CUST_IN_NO'] =i[40]
            ebills_all['OPEN_DATE']=i[41]
            cust_in_noinfo.append(str(ebills_all['CUST_IN_NO']))
            g.db_session.add(EbillsHook(**ebills_all))
        g.db_session.commit()
        SIGHTAMT="""
        merge into 
        (select row_number() over(partition by cust_in_no order by org_code,id) rn,t.* from EBILLS_HOOK t where month=%s) eh 
        using
        (select int(month1) month1,IN_CST_NO,sum(USD_AMOUNT) USD_AMOUNT
        from
        (select   
          to_char(f.LAUNCHDATE,'yyyyMM') month1,f.USD_AMOUNT,f.AMOUNT,f.CURSIGN,f.CORP_NAME,f.IN_CST_NO
        from SNAP_EBILLS_BU_TRANSACTIONINFO f
            inner join  d_ebills_tran_type t on t.id = f.TRAN_TYPE_ID
        where 
            t.immediate_SPFE_TYPE='即期结售汇'
            and amount !=0 
            and to_char(f.LAUNCHDATE,'yyyyMM')='%s' and DATE_ID=%s
            order by LAUNCHDATE,f.IN_CST_NO)
            group by month1,IN_CST_NO) a
        on (eh.cust_in_no=a.IN_CST_NO and eh.month=%s and eh.rn=1)
        when matched then update set eh.SIGHTAMT=a.USD_AMOUNT
        """%(month,month,date_id,month)
        g.db_session.execute(SIGHTAMT)
        g.db_session.commit()

        USANCEAMT="""
        merge into 
        (select row_number() over(partition by cust_in_no order by org_code,id) rn,t.* from EBILLS_HOOK t where month=%s)
        eh 
        using
        (select  int(month1) month1,IN_CST_NO,sum(USD_AMOUNT) USD_AMOUNT
        from
        (select  
            to_char(f.finisheddate,'yyyyMM') month1,f.USD_AMOUNT,f.AMOUNT,f.CURSIGN,f.CORP_NAME,f.IN_CST_NO
        from SNAP_EBILLS_BU_TRANSACTIONINFO f
            inner join  d_ebills_tran_type t on t.id = f.TRAN_TYPE_ID
        where 
            t.FUTURE_SPFE_TYPE='远期结售汇'---用finishdate
            and amount !=0 
            and to_char(f.finisheddate,'yyyyMM')='%s' and DATE_ID=%s
            order by finisheddate,f.IN_CST_NO)
            group by month1,IN_CST_NO)a
        on (eh.cust_in_no=a.IN_CST_NO and eh.month=a.month1 and eh.rn=1)
        when matched then update set eh.USANCEAMT=a.USD_AMOUNT
        """%(month,str(month),date_id)
        g.db_session.execute(USANCEAMT)
        g.db_session.commit()
        CROSSBORDERAMT="""
        merge into 
        (select row_number() over(partition by cust_in_no order by org_code,id) rn,t.* from EBILLS_HOOK t where month=%s)
        eh 
        using
        (select  int(month1) month1 ,IN_CST_NO,sum(USD_AMOUNT)*(1+%s) USD_AMOUNT
        from
        (select  
        to_char(f.LAUNCHDATE,'yyyyMM') month1,f.USD_AMOUNT,f.AMOUNT,f.CURSIGN,f.CORP_NAME,f.IN_CST_NO
        from SNAP_EBILLS_BU_TRANSACTIONINFO f
        inner join  d_ebills_tran_type t on t.id = f.TRAN_TYPE_ID
        where 
        t.FOREIGN_SPFE_TYPE='跨境结售汇'
        and amount !=0 
        and to_char(f.LAUNCHDATE,'yyyyMM')='%s' and DATE_ID=%s
        order by LAUNCHDATE,f.IN_CST_NO)
        group by month1,IN_CST_NO)a
        on (eh.cust_in_no=a.IN_CST_NO and eh.month=a.month1 and eh.rn=1)
        when matched then update set eh.CROSSBORDERAMT=a.USD_AMOUNT
        """%(month,devlop_base,str(month),date_id)
        current_app.logger.debug(CROSSBORDERAMT)
        g.db_session.execute(CROSSBORDERAMT)
        g.db_session.commit()

        self.SIGHTAM_SALE(month,date_id,userinfo,cust_in_noinfo,devlop_base)#结售汇

        for i in self.IMMEDIATE.values():#即期
            b=g.db_session.query(EbillsHook).filter(EbillsHook.MONTH==month,EbillsHook.CUST_IN_NO==i['CUST_IN_NO']).first()
            if b:
                if not b.SIGHTAMT:
                    b.SIGHTAMT=i['SIGHTAMT']
            else:
                g.db_session.add(EbillsHook(**i))
        g.db_session.commit()

        for i in self.FUTURE_SPFE_TYPE.values():#远期
            b=g.db_session.query(EbillsHook).filter(EbillsHook.MONTH==month,EbillsHook.CUST_IN_NO==i['CUST_IN_NO']).first()
            if b:
                if not b.USANCEAMT:
                    b.USANCEAMT=i['USANCEAMT']
            else:
                g.db_session.add(EbillsHook(**i))

        g.db_session.commit()
            
        for i in self.FOREIGN_SPFE_TYPE.values():#跨境
            b=g.db_session.query(EbillsHook).filter(EbillsHook.MONTH==month,EbillsHook.CUST_IN_NO==i['CUST_IN_NO']).first()
            if b:
                if not b.CROSSBORDERAMT:
                    b.CROSSBORDERAMT=i['CROSSBORDERAMT']
            else:
                g.db_session.add(EbillsHook(**i))

        g.db_session.commit()

        year=int(str(month)[:4])
        lastyear=int(str(month)[:4])-1

        """
        下三个为新开有效外汇类型
        """
        this_year="""
        merge into EBILLS_HOOK eh using 
        (select distinct cust_in_no
        from EBILLS_HOOK eh
        where 
            eh.month=%s and OPEN_DATE is not null and left(eh.OPEN_DATE,4)=%s 
            and cust_in_no 
            not in
                (select distinct st.in_cst_no from
                SNAP_EBILLS_BU_TRANSACTIONINFO st
                join 
                (select distinct cust_in_no
                from EBILLS_HOOK eh
                where 
                eh.month=%s and OPEN_DATE is not null and left(eh.OPEN_DATE,4)=%s) a
                on st.in_cst_no=a.cust_in_no 
                where  to_char(st.LAUNCHDATE,'yyyymm')<'%s')) a
        on (eh.cust_in_no =a.cust_in_no and left(eh.cust_in_no,2)='82' and OPEN_DATE is not null and OPEN_DATE>0 and MONTH=%s)
        when matched then update set eh.IS_OPEN_NEW_WH='是' ,eh.THATYEAR_INTERACCT='1'
        """%(month,year,month,year,month,month)
        g.db_session.execute(this_year)
        current_app.logger.debug(this_year)
        current_app.logger.debug('1111111111111111')
        
        g.db_session.commit()
        last_year="""
        merge into EBILLS_HOOK eh using 
        (select distinct cust_in_no
        from EBILLS_HOOK eh
        where 
        eh.month=%s and OPEN_DATE is not null and left(eh.OPEN_DATE,4)=%s ----开户去年的
        and cust_in_no not in
        (select distinct st.in_cst_no from
        SNAP_EBILLS_BU_TRANSACTIONINFO st
        join 
        (select distinct cust_in_no
        from EBILLS_HOOK eh
        where 
        eh.month=%s and OPEN_DATE is not null and left(eh.OPEN_DATE,4)=%s) a ----开户去年的
        on st.in_cst_no=a.cust_in_no 
        where  to_char(st.LAUNCHDATE,'yyyymm')<'%s'))a
        on (eh.cust_in_no =a.cust_in_no and left(eh.cust_in_no,2)='82' and OPEN_DATE is not null and OPEN_DATE>0 and MONTH=%s)
        when matched then update set eh.IS_OPEN_NEW_WH='是' ,eh.LASTYEAR_FIRSTACCT='1'
        """%(month,lastyear,month,lastyear,month,month)
        g.db_session.execute(last_year)
        current_app.logger.debug(last_year)
        current_app.logger.debug('222222222222222222')
        g.db_session.commit()
        oneyear="""
        merge into EBILLS_HOOK eh using 
        (select distinct cust_in_no
        from EBILLS_HOOK eh
        where 
        eh.month=%s and OPEN_DATE is not null and OPEN_DATE>0 and left(eh.OPEN_DATE,4)<%s 
        and cust_in_no not in                   -------开户时间小于去年的
        (select distinct st.in_cst_no from
        SNAP_EBILLS_BU_TRANSACTIONINFO st
        join 
        (select distinct cust_in_no
        from EBILLS_HOOK eh
        where 
        eh.month=%s and OPEN_DATE is not null and OPEN_DATE>0 and left(eh.OPEN_DATE,4)<%s) a
        on st.in_cst_no=a.cust_in_no 
        where  to_char(st.LAUNCHDATE,'yyyymm')>=(to_char(to_date(%s,'yyyymm')-1 year,'yyyymm')) and to_char(st.LAUNCHDATE,'yyyymm')<'%s'))a
        on (eh.cust_in_no =a.cust_in_no and left(eh.cust_in_no,2)='82' and OPEN_DATE is not null and OPEN_DATE>0 and MONTH=%s)
        when matched then update set eh.IS_OPEN_NEW_WH='是' ,eh.ONEYEAR_AGAINACCT='1'
        """%(month,lastyear,month,lastyear,month,month,month)
        current_app.logger.debug(oneyear)
        g.db_session.execute(oneyear)
        current_app.logger.debug('3333333333333')
        g.db_session.commit()

        '''新增个人国际业务'''
        person_sql='''
        select
        F.TRAN_BRANCH_CODE,
        f.ACCT_NO,
        f.CST_NAME,
        sum(USD_AMOUNT) USD_AMOUNT,
        cst_no
        from 
        (
        select F.TRAN_BRANCH_CODE,f.ACCT_NO,d.CST_NAME,f.USD_AMOUNT,f.AMOUNT,d.cst_no from F_JRN_TRANSACTION f
        left join (select row_number() over( partition by ACCOUNT_NO order by ID) rn , f.*
        from D_ACCOUNT f ) d on f.ACCT_NO=d.ACCOUNT_NO
        where sys_tran_code ='410150' and 
        left(DATE_ID,6)='%s' and ACCT_NO like '101%%'and amount!=cny_amount and
        rn=1
        )f group by  F.TRAN_BRANCH_CODE,ACCT_NO,f.CST_NAME,cst_no

        '''%(month)
        person=g.db_session.execute(person_sql).fetchall()

        for i in person:
            person_dict={}
            person_dict['MONTH']=month
            person_dict['SIGHTAMT']=i[3] 
            person_dict['CUST_IN_NO']=i[4] 
            person_dict['CORPNAME']=i[2]
            person_dict['CORPNO']=self.pa_corp_list.get(i[4],"")
            person_dict['ORG_CODE']=i[0]
            person_dict['SALE_CODE']=""
            if person_dict['CORPNO']:
                manager1=person_dict['CORPNO']+'-'+'I'
                manager2=person_dict['CORPNO']+'-'+'A'
                if self.managerid.get(manager2):
                    managerinfo=self.managerid.get(manager2)
                else:
                    managerinfo=self.managerid.get(manager1)
                if managerinfo is not None:
                    managerid=managerinfo.get('MANAGERID')
                    sale_name=self.manager.get(managerid)
                    if sale_name is not None:
                        person_dict["SALE_NAME"]=sale_name.get('MANAGERNAME').decode("gbk").encode("utf-8")
                        if sale_name.get('WORKNO'):
                            person_dict["SALE_CODE"]=sale_name.get('WORKNO')
                        else:
                            person_dict["SALE_CODE"]=userinfo.get(person_dict["SALE_NAME"])

            b=g.db_session.query(EbillsHook).filter(EbillsHook.MONTH==month,EbillsHook.CUST_IN_NO==person_dict['CUST_IN_NO']).first()
            if b:
                if not b.SIGHTAMT:
                    b.SIGHTAMT=person_dict['SIGHTAMT']
            else:
                g.db_session.add(EbillsHook(**person_dict))
        g.db_session.commit()


        """
        下三个转人民币
        """
        self.fix_seq_id('ebills_hook','ebills_hook_seq')

        balance_sql='''
        merge into EBILLS_HOOK eh
        using
        (
        select org_no,org_name,e.cust_in_no,cust_name,sum(nvl(balance,0)) as balance,sale_code,sale_name  from report_sale_rmb_exg e
        where e.date_id=%s
        group by org_no,org_name,e.cust_in_no,cust_name,sale_code,sale_name) a 
        on   ---余额
        (eh.month=%s and eh.org_code=a.org_no and eh.cust_in_no=a.cust_in_no and eh.sale_code=a.sale_code and eh.sale_name=a.sale_name)
        when matched then update set eh.BALANCE=a.balance,eh.org_name=a.org_name,eh.CORPNAME=a.cust_name,eh.sale_code=a.sale_code,eh.sale_name=a.sale_name
        when not matched then insert (eh.month,eh.org_code,eh.balance,eh.org_name,eh.cust_in_no,eh.CORPNAME,eh.sale_code,eh.sale_name) values(%s,a.org_no,a.balance,a.org_name,a.cust_in_no,a.cust_name,a.sale_code,a.sale_name)

        '''%(date_id,month,month)
        g.db_session.execute(balance_sql)#余额
        g.db_session.commit()
        month_avg='''
        merge into EBILLS_HOOK eh
        using
        (
        select d.ym,beg_month_days,org_no,org_name,e.cust_in_no,cust_name,((sum(nvl(balance,0))*1.0)/d.beg_month_days) as avn_month,sale_code,sale_name   from report_sale_rmb_exg e 
        join d_date d on d.id=e.date_id
        where d.id=%s
        group by d.ym,org_no,beg_month_days,org_name,e.cust_in_no,cust_name,sale_code,sale_name) a 
        on   ---月日均
        (eh.month=%s and eh.org_code=a.org_no  and eh.cust_in_no=a.cust_in_no and eh.sale_code=a.sale_code and eh.sale_name=a.sale_name)
        when matched then update set eh.MONTHAMT=a.avn_month,eh.org_name=a.org_name,eh.CORPNAME=a.cust_name,eh.sale_code=a.sale_code,eh.sale_name=a.sale_name
        when not matched then insert (eh.month,eh.org_code,eh.MONTHAMT,eh.org_name,eh.cust_in_no,eh.CORPNAME,eh.sale_code,eh.sale_name) values(%s,a.org_no,a.avn_month,a.org_name,a.cust_in_no,a.cust_name,a.sale_code,a.sale_name)

        '''%(date_id,month,month)
        g.db_session.execute(month_avg)#月日均
        g.db_session.commit()
        year_avg='''
        merge into EBILLS_HOOK eh
        using
        (
        select d.year,beg_year_days,org_no,org_name,e.cust_in_no,cust_name,(sum(nvl(balance,0))*1.0)/d.beg_year_days  as avg_year  ,sale_code,sale_name from report_sale_rmb_exg e 
        join d_date d on d.id=e.date_id
        where d.id=%s
        group by d.year,org_no,beg_year_days,org_name,e.cust_in_no,cust_name ,sale_code,sale_name
        ) a on   ---年日均
        (eh.month=%s and eh.org_code=a.org_no  and eh.cust_in_no=a.cust_in_no and eh.sale_code=a.sale_code and eh.sale_name=a.sale_name)
        when matched then update set eh.DAYAMT=a.avg_year,eh.org_name=a.org_name,eh.CORPNAME=a.cust_name,eh.sale_code=a.sale_code,eh.sale_name=a.sale_name
        when not matched then insert (eh.month,eh.org_code,eh.DAYAMT,eh.org_name,eh.cust_in_no,eh.CORPNAME,eh.sale_code,eh.sale_name) values(%s,a.org_no,a.avg_year,a.org_name,a.cust_in_no,a.cust_name,a.sale_code,a.sale_name)
        '''%(date_id,month,month)
        g.db_session.execute(year_avg)#年日均
        g.db_session.commit()


        """
         更改统一机构名,
        """
        org_name_uion="""
        merge into EBILLS_HOOK eh
        using (select branch_code,branch_name from BRANCH) br
        on(br.branch_code=eh.org_code and eh.month=%s) 
        when matched then update set eh.org_name=br.branch_name
        """%(month)
        g.db_session.execute(org_name_uion)
        g.db_session.commit()
        """
         不是新开外汇的置成否
        """
        update_opennew="""update ebills_hook set IS_OPEN_NEW_WH='否' where MONTH=%s and ( IS_OPEN_NEW_WH!='是' or IS_OPEN_NEW_WH is null)"""%(month)
        g.db_session.execute(update_opennew)
        g.db_session.commit()
        return '计算成功'
        
    def hook_edit_save(self,**kwargs):
        custinfo_ebills =kwargs.get('custinfo')
        for i in custinfo_ebills.keys():
            if i in ['MONTH','ORG_CODE','ORG_NAME','CORPNAME','SALE_CODE','SALE_NAME','ID','CUST_IN_NO','IS_OPEN_NEW_WH',"THATYEAR_INTERACCT","LASTYEAR_FIRSTACCT","ONEYEAR_AGAINACCT","CORPNO"]:
                pass
            else:
                if str(custinfo_ebills[i])=="" or str(custinfo_ebills[i])[0]=='-':
                    raise Exception(u"数据不能为空,或为负值")
                custinfo_ebills[i]=int(Decimal(''.join(str(custinfo_ebills[i]).split(',')))*1000000)
        if custinfo_ebills['IS_OPEN_NEW_WH'] in ['否',u'否','0',u'0']:
            custinfo_ebills['IS_OPEN_NEW_WH']='否'
            custinfo_ebills['THATYEAR_INTERACCT']='0'
            custinfo_ebills['LASTYEAR_FIRSTACCT']='0'
            custinfo_ebills['ONEYEAR_AGAINACCT']='0'

        if custinfo_ebills['IS_OPEN_NEW_WH'] in ['是',u"是"]:
            IS_NEW_OPEN="""
            select month from EBILLS_HOOK where IS_OPEN_NEW_WH='是' and MONTH>(to_char(to_date(%s,'YYYYMM')- 1 year,'YYYYMM')) and MONTH<=%s and cust_in_no='%s'
            """%(int(custinfo_ebills['MONTH']),int(custinfo_ebills['MONTH']),custinfo_ebills['CUST_IN_NO'])
            new_open=g.db_session.execute(IS_NEW_OPEN).fetchone()
            if new_open:
                raise Exception(u"该客户在%s月份已经是新开有效外汇账户"%(new_open[0]))

        g.db_session.query(EbillsHook).filter(EbillsHook.ID==custinfo_ebills['ID']).update(custinfo_ebills)
        return '修改成功'


    def total_cust_info(self,**kwargs):
        branch_code=kwargs.get('ORG_CODE')
        user_name=kwargs.get('SALE_CODE')
        branch_name_sql="select branch_name from branch where BRANCH_CODE='%s'"%(branch_code)
        name_sql="select NAME from V_STAFF_INFO where user_name='%s'"%(user_name)
        if branch_code and user_name:
            branch_name=g.db_session.execute(branch_name_sql).fetchone()
            name=g.db_session.execute(name_sql).fetchone()
            if branch_name and name:
                return({'ORG_NAME':branch_name[0],'SALE_NAME':name[0]})
            else:
                raise Exception(u"无此机构或员工")
        elif branch_code:
            branch_name=g.db_session.execute(branch_name_sql).fetchone()
            if branch_name:
                return({'ORG_NAME':branch_name[0]})
            else:
                raise Exception(u"无此机构名称")
        else:
            name=g.db_session.execute(name_sql).fetchone()
            if name:
                return({'SALE_NAME':name[0]})
            else:
                raise Exception(u"无此员工名称")
            
        


    def total_sum_save(self,**kwargs):
        original_row=kwargs.get('original_row')
        new_row=kwargs.get('new_row')
        add_row=kwargs.get('add_row')
        current_app.logger.debug(original_row)
        current_app.logger.debug(new_row)
        for i in original_row.keys():
            if i in ['MONTH','ID','ORG_CODE','ORG_NAME','CORPNAME','CUST_IN_NO','SALE_CODE','SALE_NAME',"CORPNO","IS_OPEN_NEW_WH","THATYEAR_INTERACCT","LASTYEAR_FIRSTACCT","ONEYEAR_AGAINACCT"]:
                pass
            else:
                original_row[i]=(Decimal(''.join(str(original_row[i]).split(',')))*1000000)
        g.db_session.query(EbillsHook).filter(EbillsHook.ID==original_row['ID']).update(original_row)

        for i in new_row.keys():
            if i in ['MONTH','ID','ORG_CODE','ORG_NAME','CORPNAME','CUST_IN_NO','SALE_CODE','SALE_NAME',"CORPNO","IS_OPEN_NEW_WH","THATYEAR_INTERACCT","LASTYEAR_FIRSTACCT","ONEYEAR_AGAINACCT"]:
                pass
            else:
                new_row[i]=(Decimal(''.join(str(new_row[i]).split(',')))*1000000)
        g.db_session.add(EbillsHook(**new_row))

        for i in add_row.keys():
            if i in ['ORIG_MONTH','ID','ORIG_ORG_CODE','ORIG_ORG_NAME','ORIG_SALE_CODE','ORIG_SALE_NAME','ORIG_CORPNAME','ORIG_CUST_IN_NO',"NEW_ORG_CODE","NEW_ORG_NAME","NEW_SALE_CODE","NEW_SALE_NAME"]:
                pass
            else:
                add_row[i]=(Decimal(''.join(str(add_row[i]).split(',')))*1000000)
        g.db_session.add(EbillsHook_DISINFO(**add_row))


        return '修改成功'







if __name__=='__main__':
    g=Ebills_ManagerService()
    g.managerifno()
