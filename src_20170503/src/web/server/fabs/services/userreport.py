# -*- coding:utf-8 -*-
from flask import json,g,current_app
import sys
import time
import inspect
import hashlib
import datetime
import decimal
import string
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all
from ..database.sqlal import simple_session
from ..model import REPORT_MANAGER_DEP,REPORT_MANAGER_LOAN,REPORT_MANAGER_OTHER,REPORT_MANAGER_CREDITCARD,Branch,GroupHis,UserGroup,GroupType,Group,EbillsHook,EBANK_REPLACE_NUM
from .service import BaseService
from ..database import simple_session
from ..base import utils
import logging
from datetime import timedelta,datetime
import datetime as thisdatetime
import calendar

class UserReport(BaseService):
    def __init__(self):
        self.session = simple_session()

    def dep_balance(self,*kwargs):
        '''得到客户经理存款日均余额'''
        rowlist=[]
        for i in range(0,len(kwargs[0][0])): 
            year=int(kwargs[0][0][i][2]) #传入变成元组
            DATE_ID=self.get_month_end(year,12) #取当年年末时间
            SALE_CODE=str(kwargs[0][0][i][1])
            bal_sql = self.session.query(func.nvl(REPORT_MANAGER_DEP.THIS_AVG,0)).filter(REPORT_MANAGER_DEP.DATE_ID == DATE_ID,REPORT_MANAGER_DEP.SALE_CODE==SALE_CODE).all()

            bal=0
            row=()
            for a in bal_sql:
                if len(a)==1:
                    bal= bal+int(a[0])
            row=(str((float(bal/10000000000.00))),SALE_CODE,str(year))
            rowlist.append(row)

        bal = rowlist
        #logging.debug(bal)
        return bal

    def manage_dep_avg_bal(self,year,orgcode,salecode):
        """客户经理日均存款余额""" #年日均TBD
        year=int(year)
        month=1
        avg_pdt=0
        while month <= 12:
            starday=self.get_month_end(year,month)
            #logging.debug(starday)
            bal_sql=self.session.query(REPORT_MANAGER_DEP).filter(REPORT_MANAGER_DEP.DATE_ID==starday,REPORT_MANAGER_DEP.ORG_CODE==orgcode,REPORT_MANAGER_DEP.SALE_CODE==salecode).all()
            for a in bal_sql:
                if getattr(a,'MONTH_AVG') is not None:
                    avg_pdt=avg_pdt+getattr(a,'MONTH_AVG')
                else:
                    continue
                    avg_pdt=avg_pdt
                #logging.debug("this is avg_pdt:"+str(avg_pdt))
            month = month+1
        year_avg_pdt=avg_pdt/12
        #logging.debug(year_avg_pdt)
        return year_avg_pdt

    def manage_loan_avg_bal(self,*kwargs):
        """客户经理年度日均贷款余额"""
        rowlist=[]
        for i in range(0,len(kwargs[0][0])): 
            year=int(kwargs[0][0][i][2]) #传入变成元组
            DATE_ID=self.get_month_end(year,12) #取当年年末时间
            SALE_CODE=str(kwargs[0][0][i][1])
            bal_sql = self.session.query(func.nvl(REPORT_MANAGER_LOAN.PRI_THIS_AVG,0),func.nvl(REPORT_MANAGER_LOAN.PUB_THIS_AVG,0)).filter(REPORT_MANAGER_LOAN.DATE_ID == DATE_ID,REPORT_MANAGER_LOAN.SALE_CODE==SALE_CODE).all()
            bal=0
            row=()
            #logging.debug(bal_sql)
            for a in bal_sql:
                if  len(a)==2:
                    bal= bal+int(a[0])+ int(a[1])
            row=(str((float(bal/10000000000.00))),SALE_CODE,str(year))
            rowlist.append(row)

        bal = rowlist
        #logging.debug(bal)
        return bal

    def manage_loan_num(self,*kwargs):
        """客户经理管贷户数（户）"""
        rowlist=[]
        for i in range(0,len(kwargs[0][0])): 
            year=int(kwargs[0][0][i][2]) #传入变成元组
            DATE_ID=self.get_month_end(year,12) #取当年年末时间
            SALE_CODE=str(kwargs[0][0][i][1])
            bal_sql = self.session.query(func.nvl(REPORT_MANAGER_LOAN.PRI_NUM,0),func.nvl(REPORT_MANAGER_LOAN.PUB_NUM,0)).filter(REPORT_MANAGER_LOAN.DATE_ID == DATE_ID,REPORT_MANAGER_LOAN.SALE_CODE==SALE_CODE).all()
            bal=0
            row=()
            for a in bal_sql:
                if  len(a)==2:
                    bal= bal+int(a[0])+int(a[1])*12 #管贷户数企业户1户按12户换算
            row=(str(bal),SALE_CODE,str(year))
            rowlist.append(row)

        bal = rowlist
        #logging.debug(bal)
        return bal


    def manage_avg_dep_loan_percent(self,*kwargs):
        """客户经理贷款户日均存贷挂钩率(%) 日均存款/日均贷款 *100%"""
        listall=kwargs[0]
        loan=self.manage_loan_avg_bal(listall)
        #logging.debug(loan)
        rowlist=[]
        for i in range(0,len(kwargs[0][0])):
            year=int(kwargs[0][0][i][2]) #传入变成元组
            DATE_ID=self.get_month_end(year,12) #取当年年末时间
            SALE_CODE = kwargs[0][0][i][1]
            dep=self.session.query(func.nvl(REPORT_MANAGER_LOAN.DSGGRJ,0),func.nvl(REPORT_MANAGER_LOAN.DGGGRJ,0)).filter(REPORT_MANAGER_LOAN.DATE_ID==DATE_ID,REPORT_MANAGER_LOAN.SALE_CODE==SALE_CODE).all()
            #logging.debug((dep[0][0]+dep[0][1])/10000000000.00)
            #logging.debug(dep)
            if float(loan[i][0]) !=0.0:
                percent= (float((dep[0][0]+dep[0][1])/10000000000.00) / float(loan[i][0])) *100
            else:
                percent=100.0
            row=()
            row=(str(round(float(percent),2)),loan[i][1],loan[i][2])
            rowlist.append(row)
        #logging.debug(rowlist)
        return rowlist 

    def manage_bad_bal_percent(self,*kwargs):
        """客户经理四级不良率（%）"""
        rowlist=[]
        for i in range(0,len(kwargs[0][0])): 
            year=int(kwargs[0][0][i][2]) #传入变成元组
            DATE_ID=self.get_month_end(year,12) #取当年年末时间
            SALE_CODE=str(kwargs[0][0][i][1])
            bal_sql = self.session.query(func.nvl(REPORT_MANAGER_LOAN.DSZRYE,0),func.nvl(REPORT_MANAGER_LOAN.DGZRYE,0),func.nvl(REPORT_MANAGER_LOAN.DSZRYE1,0),func.nvl(REPORT_MANAGER_LOAN.DGZRYE1,0)).filter(REPORT_MANAGER_LOAN.DATE_ID == DATE_ID,REPORT_MANAGER_LOAN.SALE_CODE==SALE_CODE).all()
            #logging.debug(bal_sql)
            dsye=dgye=dsye1=dgye1=0
            row=()
            for a in bal_sql:
                if len(a)==4:
                    dsye=dsye+a[0]
                    dgye=dgye+a[1]
                    dsye1=dsye1+a[2]
                    dgye1=dgye1+a[3]
            if (float(dsye1)+float(dgye1)+float(dsye)+float(dgye)) == 0:
                percent=0
            else:
                percent= round( (float(dsye1)+float(dgye1)) / ( float(dsye1)+float(dgye1)+float(dsye)+float(dgye)  ) ,4)
            percent = str(round((float(percent)*100),2))
            bal_bal = str(round(float((dsye1 + dgye1)/1000000.00),2))
            row=((percent,bal_bal),str(SALE_CODE),str(year))
            rowlist.append(row)
        #logging.debug(rowlist)
        return rowlist 

    def dep_avg_all(self,year,orgcode,branch = False):
        """年度日均存款总量"""
        year=int(year)
        orgcode = self.org_list(orgcode,branch)
        month=12
        avg_pdt=0
        while month <= 12:
            starday=self.get_month_end(year,month)
            bal_sql=self.session.query(func.nvl(REPORT_MANAGER_DEP.THIS_AVG,0)).filter(REPORT_MANAGER_DEP.DATE_ID==starday,REPORT_MANAGER_DEP.ORG_CODE.in_(orgcode)).all()
            for a in bal_sql:
                if len(a)==1:
                    avg_pdt=avg_pdt+a[0]
            month = month+1
        year_avg_pdt=long(avg_pdt)
        #logging.debug(year_avg_pdt)
        return year_avg_pdt

    def loan_avg_all(self,year,orgcode,branch = False):
        """年度日均贷款总量"""
        year=int(year)
        orgcode = self.org_list(orgcode,branch)
        month=12
        avg_pdt=0
        while month <= 12:
            starday=self.get_month_end(year,month)
            bal_sql=self.session.query(func.nvl(REPORT_MANAGER_LOAN.PRI_THIS_AVG,0),func.nvl(REPORT_MANAGER_LOAN.PUB_THIS_AVG,0)).filter(REPORT_MANAGER_LOAN.DATE_ID==starday,REPORT_MANAGER_LOAN.ORG_CODE.in_(orgcode)).all()
            for a in bal_sql:
                if len(a)==2:
                    avg_pdt=avg_pdt+int(a[0])+int(a[1])
            month = month+1
        year_avg_pdt=long(avg_pdt)
        #logging.debug(year_avg_pdt)
        return year_avg_pdt

    def ebank_num(self,year,orgcode,branch = False):
        """电子银行开户数"""
        year=int(year)
        orgcode = self.org_list(orgcode,branch)
        month=12
        mb=0
        cb=0
        pb=0
        while month <= 12:
            starday=self.get_month_end(year,month)
            bal_sql=self.session.query(func.nvl(REPORT_MANAGER_OTHER.MB_LAST_NUM,0),func.nvl(REPORT_MANAGER_OTHER.CB_LAST_NUM,0),func.nvl(REPORT_MANAGER_OTHER.PB_LAST_NUM,0)).filter(REPORT_MANAGER_OTHER.DATE_ID==starday,REPORT_MANAGER_OTHER.ORG_CODE.in_(orgcode)).all()
            for a in bal_sql:
                if len(a)==3:
                    mb=mb+a[0]
                    cb=cb+a[1]
                    pb=pb+a[2]
            month = month+1
        all_num=int(mb)+int(cb)+int(pb)
        #logging.debug(all_num)
        return all_num
 
    def loan_num(self,year,orgcode,branch = False):
        """贷款户数"""
        year=int(year)
        orgcode = self.org_list(orgcode,branch)
        month=12
        pr=0
        pu=0
        while month <= 12:
            starday=self.get_month_end(year,month)
            bal_sql=self.session.query(func.nvl(REPORT_MANAGER_LOAN.PRI_NUM,0),func.nvl(REPORT_MANAGER_LOAN.PUB_NUM,0)).filter(REPORT_MANAGER_LOAN.DATE_ID==starday,REPORT_MANAGER_LOAN.ORG_CODE.in_(orgcode)).all()
            for a in bal_sql:
                if len(a)==2:
                    pr=pr+a[0]
                    pu=pu+a[1]
            month = month+1
        all_num=int(pr)+int(pu)
        #logging.debug(all_num)
        return all_num
 
    def bad_bal_percent(self,year,orgcode,branch = False):
        """四级不良率（%）"""
        year=int(year)
        orgcode = self.org_list(orgcode,branch)
        month=12   #是不是只取年末就可以 TBD
        dsye=0
        dgye=0
        dsye1=0
        dgye1=0
        while month <= 12:
            starday=self.get_month_end(year,month)
            bal_sql=self.session.query(func.nvl(REPORT_MANAGER_LOAN.DSZRYE,0),func.nvl(REPORT_MANAGER_LOAN.DGZRYE,0),func.nvl(REPORT_MANAGER_LOAN.DSZRYE1,0),func.nvl(REPORT_MANAGER_LOAN.DGZRYE1,0)).filter(REPORT_MANAGER_LOAN.DATE_ID==starday,REPORT_MANAGER_LOAN.ORG_CODE.in_(orgcode)).all()
            for a in bal_sql:
                if len(a)==4:
                    dsye=dsye+a[0]
                    dgye=dgye+a[1]
                    dsye1=dsye1+a[2]
                    dgye1=dgye1+a[3]
            month = month+1
        if (long(dsye)+long(dgye)) == 0.0:
            percent=0
        else:
            percent= round( ((float(dsye1)+float(dgye1)) / ( float(dsye)+float(dgye)))*100.00   ,4)
        logging.debug(percent)
        logging.debug(float(dsye)+float(dgye))
        logging.debug(float(dsye1)+float(dgye1))
        return percent 
 
    def card_num(self,year,orgcode,branch = False):
        """贷记卡发卡量（张）"""
        year=int(year)
        orgcode = self.org_list(orgcode,branch)
        #logging.debug(orgcode)
        month=12    #是不是只取年末 TBD
        num=0
        while month <= 12:
            starday=self.get_month_end(year,month)
            bal_sql=self.session.query(func.nvl(REPORT_MANAGER_CREDITCARD.THIS_NUM,0)).filter(REPORT_MANAGER_CREDITCARD.DATE_ID==starday,REPORT_MANAGER_CREDITCARD.ORG_CODE.in_(orgcode)).all()
            for a in bal_sql:
                if len(a)==1:
                    num=num+a[0]
            month = month+1
        all_num=int(num)
        #logging.debug(all_num)
        return all_num
    
    def avg_dep_percent(self,year,orgcode,branch = False):
        """网点存款挂钩日均"""
        year=int(year)
        orgcode = self.org_list(orgcode,branch)
        month=12    #是不是只取年末 TBD
        num=0
        while month <= 12:
            starday=self.get_month_end(year,month)
            bal_sql=self.session.query(func.nvl(REPORT_MANAGER_LOAN.DSGGRJ,0),func.nvl(REPORT_MANAGER_LOAN.DGGGRJ,0)).filter(REPORT_MANAGER_LOAN.DATE_ID==starday,REPORT_MANAGER_LOAN.ORG_CODE.in_(orgcode)).all()
            for a in bal_sql:
                if len(a)==2:
                    num=num+a[0]+a[1]
            month = month+1
        all_num=long(num)
        #logging.debug(all_num)
        return all_num
 
    def avg_dep_loan_percent(self,year,orgcode,branch = False):
        """支行贷款户日均存贷挂钩率(%) 日均存款/日均贷款 *100%"""
        dep=self.avg_dep_percent(year,orgcode,branch)
        loan=self.loan_avg_all(year,orgcode,branch)
        if loan >0:
            percent= round(float(dep) / float(loan) *100  ,4)
        else:
            percent=0.0
        #logging.debug(percent)
        #logging.debug(dep)
        #logging.debug(loan)
        return percent

    def teller_num(self,year):
        """柜员等级 业务量"""
        sql_t=u"""
        SELECT "柜员交易业务量29"."柜员号"  SALE_CODE, --"柜员号"
          FLOAT(SUM( CASE  WHEN "柜员交易业务量29"."交易码" IN('00413091','413091' ) ---批量代发工资
          THEN CASE  WHEN "柜员交易业务量29"."柜员实际业务量" <= 4500 
          THEN "柜员交易业务量29"."柜员考核业务量" * 0.15 WHEN 4500 < "柜员交易业务量29"."柜员实际业务量" 
          AND "柜员交易业务量29"."柜员实际业务量" <= 7500 THEN ("柜员交易业务量29"."柜员考核业务量" - 4500) * 0.1 + 675 
          WHEN 7500 < "柜员交易业务量29"."柜员实际业务量" AND "柜员交易业务量29"."柜员实际业务量" < 18000 
          THEN ("柜员交易业务量29"."柜员考核业务量" - 7500) * 0.05 + 975 ELSE ("柜员交易业务量29"."柜员考核业务量" - 18000) * 0 + 1500 END  ELSE "柜员交易业务量29"."柜员考核业务量" END))  TELLER_EXAM_NUM   --"柜员考核业务量"
          FROM 
          (SELECT SUBSTR(M_TELLER_TRAN.DATE_ID, 1, 4) "年份" , M_TELLER_TRAN.TEL_TRAN_CODE "交易码" , M_ORG_DATE_FLAT.CHILD_ORG_CODE "机构号" , M_ORG_DATE_FLAT.CHILD_ORG_NAME "机构名称" ,
                  M_TELLER_TRAN.TRAN_TELLER_CODE "柜员号" , M_TELLER_TRAN.SALE_NAME "柜员姓名" , SUM(M_TELLER_TRAN.CNT) "柜员实际业务量" , SUM(M_TELLER_TRAN.TRADE_CNT) "柜员考核业务量"
                  FROM
                  M_TELLER_TRAN M_TELLER_TRAN, M_ORG_DATE_FLAT M_ORG_DATE_FLAT
                  WHERE  
                  M_TELLER_TRAN.DATE_ID>='%s'||'0101' AND  
                  M_TELLER_TRAN.DATE_ID<='%s'||'1231'
                  AND M_ORG_DATE_FLAT.ORG_CODE = '966000'
                  AND M_TELLER_TRAN.TRAN_BRANCH_CODE = M_ORG_DATE_FLAT.CHILD_ORG_CODE
                  AND M_TELLER_TRAN.YM = M_ORG_DATE_FLAT.DATE_ID 
                  GROUP BY
                  SUBSTR(M_TELLER_TRAN.DATE_ID, 1, 4),
                  M_TELLER_TRAN.TEL_TRAN_CODE,M_ORG_DATE_FLAT.CHILD_ORG_CODE,M_ORG_DATE_FLAT.CHILD_ORG_NAME,
                  M_TELLER_TRAN.TRAN_TELLER_CODE,M_TELLER_TRAN.SALE_NAME) "柜员交易业务量29"
          GROUP BY
          "柜员交易业务量29"."柜员号" 
        """%(year,year)
        connection = self.session.bind.raw_connection()
        cursor = connection.cursor()
        cursor.execute(sql_t)
        r = cursor.fetchone()
        #r=self.session.execute(sql_t).fetchone()
        dict_t = {}
        while r:
            dict_t[str(r[0])] = list(r)
            r = cursor.fetchone()
        #logging.debug(dict_t)
        return dict_t 

    def ebank_percent(self,year,orgcode,branch = False):
        """网点 电子银行替代率"""
        year=int(year)
        orgcode = self.org_list(orgcode,branch)
        month=01    #是不是只取年末 TBD
        num=0
        ebank = term = 0.0
        while month <= 12:
            starday=str(self.get_month_end(year,month))
            doller=self.session.query(func.nvl(EBANK_REPLACE_NUM.ATM_TOTAL,0)+func.nvl(EBANK_REPLACE_NUM.EBANK_TOTAL,0)+func.nvl(EBANK_REPLACE_NUM.CELLPHONE_BANK,0)+func.nvl(EBANK_REPLACE_NUM.AUTO_BANK,0),func.nvl(EBANK_REPLACE_NUM.TERM_NUM,0)).filter(EBANK_REPLACE_NUM.DATE==starday,EBANK_REPLACE_NUM.BRANCH_CODE.in_(orgcode)).all()
            for a in doller:
                ebank = ebank + a[0]
                term  = term  + a[1]
            month = month+1
        percent = str(round(ebank / (ebank + term) ,3))
        #logging.debug(percent)
        return percent

    def international_num(self,year,orgcode,branch = False):
        """支行 国际结算量"""
        year=int(year)
        orgcode = self.org_list(orgcode,branch)
        month=01    #是不是只取年末 TBD
        num=0
        while month <= 12:
            starday=str(self.get_month_end(year,month))[0:6]
            doller=self.session.query(func.nvl(EbillsHook.IMLCAMT,0),func.nvl(EbillsHook.IMICAMT,0),func.nvl(EbillsHook.IMOUTREMTIAMT,0),func.nvl(EbillsHook.EXBPAMT,0),func.nvl(EbillsHook.EXAGENTAMT,0),func.nvl(EbillsHook.EXINREMITAMT,0),func.nvl(EbillsHook.FIINREMITAMT,0),func.nvl(EbillsHook.FIOUTREMITAMT,0)).filter(EbillsHook.MONTH==starday,EbillsHook.ORG_CODE.in_(orgcode)).all()
            for a in doller:
                for i in range(0,len(a)):
                    num = num + a[i]
            month = month+1

        num = str(round(float(num) / 10000000.00 ,2))
        #logging.debug(num)
        return num 

    def org_ranking(self,year):
        """支行（部）业务总量排名"""
        sql_t=u"""
        SELECT TRIM(B.BRANCH1_CODE),SUM(A.TELLER_EXAM_NUM) FROM (
        SELECT "柜员交易业务量29"."机构号" ORG_CODE, --"机构号"
          FLOAT(SUM( CASE  WHEN "柜员交易业务量29"."交易码" IN('00413091','413091' ) ---批量代发工资
          THEN CASE  WHEN "柜员交易业务量29"."柜员实际业务量" <= 4500 
          THEN "柜员交易业务量29"."柜员考核业务量" * 0.15 WHEN 4500 < "柜员交易业务量29"."柜员实际业务量" 
          AND "柜员交易业务量29"."柜员实际业务量" <= 7500 THEN ("柜员交易业务量29"."柜员考核业务量" - 4500) * 0.1 + 675 
          WHEN 7500 < "柜员交易业务量29"."柜员实际业务量" AND "柜员交易业务量29"."柜员实际业务量" < 18000 
          THEN ("柜员交易业务量29"."柜员考核业务量" - 7500) * 0.05 + 975 ELSE ("柜员交易业务量29"."柜员考核业务量" - 18000) * 0 + 1500 END  ELSE "柜员交易业务量29"."柜员考核业务量" END))  TELLER_EXAM_NUM   --"柜员考核业务量"
          FROM 
          (SELECT SUBSTR(M_TELLER_TRAN.DATE_ID, 1, 4) "年份" , M_TELLER_TRAN.TEL_TRAN_CODE "交易码" , M_ORG_DATE_FLAT.CHILD_ORG_CODE "机构号" , M_ORG_DATE_FLAT.CHILD_ORG_NAME "机构名称" ,
                  M_TELLER_TRAN.TRAN_TELLER_CODE "柜员号" , M_TELLER_TRAN.SALE_NAME "柜员姓名" , SUM(M_TELLER_TRAN.CNT) "柜员实际业务量" , SUM(M_TELLER_TRAN.TRADE_CNT) "柜员考核业务量"
                  FROM
                  M_TELLER_TRAN M_TELLER_TRAN, M_ORG_DATE_FLAT M_ORG_DATE_FLAT
                  WHERE  
                  M_TELLER_TRAN.DATE_ID>='%s'||'0101' AND  
                  M_TELLER_TRAN.DATE_ID<='%s'||'1231'
                  AND M_ORG_DATE_FLAT.ORG_CODE = '966000'
                  AND M_TELLER_TRAN.TRAN_BRANCH_CODE = M_ORG_DATE_FLAT.CHILD_ORG_CODE
                  AND M_TELLER_TRAN.YM = M_ORG_DATE_FLAT.DATE_ID 
                  GROUP BY
                  SUBSTR(M_TELLER_TRAN.DATE_ID, 1, 4),
                  M_TELLER_TRAN.TEL_TRAN_CODE,M_ORG_DATE_FLAT.CHILD_ORG_CODE,M_ORG_DATE_FLAT.CHILD_ORG_NAME,
                  M_TELLER_TRAN.TRAN_TELLER_CODE,M_TELLER_TRAN.SALE_NAME) "柜员交易业务量29"
          GROUP BY
          "柜员交易业务量29"."机构号" ) A
          JOIN V_BRANCH_INFO B ON A.ORG_CODE=B.BRANCH0_CODE
          GROUP BY B.BRANCH1_CODE
           ORDER BY 2 DESC
        """%(year,year)
        connection = self.session.bind.raw_connection()
        cursor = connection.cursor()
        cursor.execute(sql_t)
        r = cursor.fetchall()
        #r=self.session.execute(sql_t).fetchone()
        dict_t = {}
        #logging.debug(len(r))
        for i in range(0,len(r)):
            dict_t[str(r[i][0])] = i+1
        #logging.debug(dict_t)
        return dict_t 

    def org_ranking_branch(self,year):
        """支行（部）业务总量排名    到网点"""
        sql_t=u"""
        SELECT "柜员交易业务量29"."机构号" ORG_CODE, --"机构号"
          FLOAT(SUM( CASE  WHEN "柜员交易业务量29"."交易码" IN('00413091','413091' ) ---批量代发工资
          THEN CASE  WHEN "柜员交易业务量29"."柜员实际业务量" <= 4500 
          THEN "柜员交易业务量29"."柜员考核业务量" * 0.15 WHEN 4500 < "柜员交易业务量29"."柜员实际业务量" 
          AND "柜员交易业务量29"."柜员实际业务量" <= 7500 THEN ("柜员交易业务量29"."柜员考核业务量" - 4500) * 0.1 + 675 
          WHEN 7500 < "柜员交易业务量29"."柜员实际业务量" AND "柜员交易业务量29"."柜员实际业务量" < 18000 
          THEN ("柜员交易业务量29"."柜员考核业务量" - 7500) * 0.05 + 975 ELSE ("柜员交易业务量29"."柜员考核业务量" - 18000) * 0 + 1500 END  ELSE "柜员交易业务量29"."柜员考核业务量" END))  TELLER_EXAM_NUM   --"柜员考核业务量"
          FROM 
          (SELECT SUBSTR(M_TELLER_TRAN.DATE_ID, 1, 4) "年份" , M_TELLER_TRAN.TEL_TRAN_CODE "交易码" , M_ORG_DATE_FLAT.CHILD_ORG_CODE "机构号" , M_ORG_DATE_FLAT.CHILD_ORG_NAME "机构名称" ,
                  M_TELLER_TRAN.TRAN_TELLER_CODE "柜员号" , M_TELLER_TRAN.SALE_NAME "柜员姓名" , SUM(M_TELLER_TRAN.CNT) "柜员实际业务量" , SUM(M_TELLER_TRAN.TRADE_CNT) "柜员考核业务量"
                  FROM
                  M_TELLER_TRAN M_TELLER_TRAN, M_ORG_DATE_FLAT M_ORG_DATE_FLAT
                  WHERE  
                  M_TELLER_TRAN.DATE_ID>='%s'||'0101' AND  
                  M_TELLER_TRAN.DATE_ID<='%s'||'1231'
                  AND M_ORG_DATE_FLAT.ORG_CODE = '966000'
                  AND M_TELLER_TRAN.TRAN_BRANCH_CODE = M_ORG_DATE_FLAT.CHILD_ORG_CODE
                  AND M_TELLER_TRAN.YM = M_ORG_DATE_FLAT.DATE_ID 
                  GROUP BY
                  SUBSTR(M_TELLER_TRAN.DATE_ID, 1, 4),
                  M_TELLER_TRAN.TEL_TRAN_CODE,M_ORG_DATE_FLAT.CHILD_ORG_CODE,M_ORG_DATE_FLAT.CHILD_ORG_NAME,
                  M_TELLER_TRAN.TRAN_TELLER_CODE,M_TELLER_TRAN.SALE_NAME) "柜员交易业务量29"
          GROUP BY
           "柜员交易业务量29"."机构号" 
           ORDER BY 2 DESC
        """%(year,year)
        connection = self.session.bind.raw_connection()
        cursor = connection.cursor()
        cursor.execute(sql_t)
        r = cursor.fetchall()
        #r=self.session.execute(sql_t).fetchone()
        dict_t = {}
        logging.debug(len(r))
        for i in range(0,len(r)):
            dict_t[str(r[i][0])] = i+1
        #logging.debug(dict_t)
        return dict_t 


    def org_num(self,orgcode):
        """支行网点数"""
        parent_id = self.session.query(Branch.parent_id).filter(Branch.branch_code == orgcode).all()
        branch_all = self.session.query(Branch.branch_code).filter(Branch.parent_id == parent_id[0][0]).all() 
        num=len(branch_all)
        #logging.debug(num)
        return num

    def org_list(self,orgcode,branch = False):
        """支行网点列表"""
        if orgcode is not None:
            if orgcode[0] == 'M':
                orgcode = orgcode[1:]
            if branch == True:
                parent_id = self.session.query(Branch.parent_id).filter(Branch.branch_code == orgcode).all()
                branch_all = self.session.query(Branch.branch_code).filter(Branch.parent_id == parent_id[0][0]).all() 
                org_list = []
                for i in range(0,len(branch_all)):
                    org_list.append(str(branch_all[i][0]))
                org_list = tuple(org_list)
            else :
                org_list = ("('" + str(orgcode) + "')")
                org_list = ( str(orgcode) ,)
        else:
            return u'机构号错误'
        #logging.debug(org_list)
        return org_list 
    def branch_org(self,branch):
        """根据网店得到支行"""
        if branch is not None:
            if branch[0] == 'M':
                branch = branch[1:]
            parent_id = self.session.query(Branch.parent_id).filter(Branch.branch_code == branch).all()
            org = self.session.query(Branch.branch_code).filter(Branch.parent_id == parent_id[0][0],Branch.branch_level=='支行营业部').all()
            #logging.debug(org[0][0])
            return org[0][0]
        else:
            return branch

    #时间加减
    def daycalc(self,etldate,days):
        if etldate == 0:
            return 0
        s=str(etldate)
        d1=datetime(int(s[0:4]),int(s[4:6]),int(s[6:8])) + timedelta(days)
        s=str(d1.strftime('%Y%m%d'))
        return s
    #计算天数
    def days(self,stardate,enddate):
        l=str(stardate)
        e=str(enddate)
        ld=thisdatetime.date(int(l[0:4]),int(l[4:6]),int(l[6:8]))
        ed=thisdatetime.date(int(e[0:4]),int(e[4:6]),int(e[6:8]))
        daynu=(ed-ld).days+1
        return daynu
    #得到每月月末
    def get_month_end(self,year,month):
        weak,endday=calendar.monthrange(year,month)
        month=str(month).zfill(2)
        day=str(year)+str(month)+str(endday)
        return day
    #取得当年年份,年初,去年年份,去年年末
    def get_year_day(self):
        localtime = time.strftime('%Y%m%d',time.localtime(time.time()))
        local_year = localtime[0:4]
        local_satrday = str(local_year) + '0101'
        last_endday = str(self.daycalc(local_satrday,-1))
        last_year = last_endday[0:4]
        #logging.debug(local_year+"*"+local_satrday+"*"+last_endday+"*"+last_year)
        return local_year,last_year,local_satrday,last_endday

    """
    更改员工等级信息
    """
    def check_update_his(self,last_month,month,sale_code,level):
        last_month=int(last_month)#年末20161231
        month=int(month)#年初20170101
        year_end=g.db_session.execute("select year_end from d_date where id=%s"%(last_month)).fetchone()
        if str(year_end[0]).strip()!='Y':
            raise Exception(u"计算时间未到年末")
        if month!=int(self.daycalc(last_month,1)):
            raise Exception(u"等级计算未到年初")
    
        lately_time="""
        select max(end_date) from GROUP_HIS where sale_code='%s' 
        """%(sale_code)
        max_end_date=g.db_session.execute(lately_time).fetchone()
        #current_app.logger.debug(max_end_date)
        #if len(max_end_date):
        if max_end_date[0] :
            max_finish_date=int(max_end_date[0])
            if max_finish_date>=last_month:
                raise Exception(u"该员工在已有历史信息(日期%d)超出上年末的日期"%(max_finish_date))
        else:
            max_finish_date=0#还没有历史产生
        
        his_dict={}
        leve_lastly_date="""
        select * from 
        (select 
        max(ug.STARTDATE) , --0
        fu.USER_NAME,--1
        fu.NAME, --2
        max(case when gt.TYPE_NAME='人员性质' and g.group_name is not null then g.group_name end) aa, --3
        fu.ID_NUMBER , --4
        b.BRANCH_NAME , ---机构名5 
        max(case when gt.TYPE_NAME='部门' then g.group_name end),--6
        max(case when gt.TYPE_NAME='职务' then g.group_name end),--7
        max(case when gt.TYPE_NAME='等级' then g.group_name end),--8
        max(case when gt.TYPE_NAME='客户经理类别' then g.group_name end),--9
        fu.IS_SAFE,--10
        fu.WORK_STATUS,--11
        fu.is_test,--12
        fu.is_virtual,--13
        fu.EDU,--14
        fu.IS_HEADMAN, ---柜组长 15
        fu.ROLE_ID, --16user_id
        max(case when gt.TYPE_NAME='等级' then ug.id end) --17user_group的id
        from F_USER fu
        left join USER_BRANCH ub on ub.USER_ID=fu.ROLE_ID
        left join BRANCH b on b.ROLE_ID=ub.BRANCH_ID
        left join USER_GROUP ug on ug.USER_ID=fu.ROLE_ID 
        left join "GROUP" g on g.ID=ug.GROUP_ID
        left join GROUP_TYPE gt on gt.TYPE_CODE=g.GROUP_TYPE_CODE
        where 1=1  and is_virtual='否' and gt.type_code!='5000' and fu.USER_NAME='%s'
        group by ug.startdate,fu.USER_NAME, fu.NAME,fu.ID_NUMBER,b.BRANCH_NAME, fu.IS_SAFE,fu.WORK_STATUS,fu.is_test,fu.is_virtual,fu.EDU,fu.IS_HEADMAN,fu.ROLE_ID) 
        where aa is not null
        """%(sale_code)
        leve_date=g.db_session.execute(leve_lastly_date).fetchone()
        #current_app.logger.debug(leve_date)
        if leve_date:
            max_leve_date=int(leve_date[0])
            user_id=leve_date[16]
            user_group_id=leve_date[17]
            if max_leve_date>=month:
                e = "员工"+str(sale_code)+"信息已有员工信息(日期"+str(max_leve_date)+")超出所更改的年末等级"
                raise Exception(e)
            
            if max_finish_date:
                max_finish_date=self.daycalc(max_finish_date,1)#传进来开始时间
            else:
                max_finish_date=str(max_leve_date)

            if str(max_finish_date)[6:8]!='01':
                e = "员工"+str(sale_code)+"信息开始日期不是月初"
                raise Exception(e)
            if int(max_finish_date)>last_month:
                raise Exception(u"月末不能小于月初")
                
            his_dict={
            "start_date":max_finish_date,
            "end_date":str(last_month),
            "sale_code":leve_date[1],
            "org_code":leve_date[5],
            "group_his":leve_date[6],
            "position_his":leve_date[7],
            "SALE_NAME":leve_date[2],
            "PROPERTY":leve_date[3],
            "POSITION_TYPE":leve_date[9],
            "SALE_FALG":leve_date[10],
            "WORKSTATUS":leve_date[11],
            "IS_VIRIUAL":leve_date[13],
            "IS_TEST":leve_date[12],
            "DEG_LEVEL":leve_date[8]
            }
    
            g.db_session.add(GroupHis(**his_dict))        
        else:
            e = "员工"+str(sale_code)+"信息不存在,或没有任职时间"
            raise Exception(e)

        data={}
        data['user_id']=user_id
        data['startdate']=str(month)
        p=g.db_session.query(Group).join(GroupType,GroupType.type_code==Group.group_type_code).filter(GroupType.type_name==u'等级').filter(Group.group_name==level).first()
        xxx=g.db_session.query(Group).join(GroupType,GroupType.type_code==Group.group_type_code).filter(GroupType.type_name==u'等级').filter(Group.group_name==level).statement
        #current_app.logger.debug(xxx)
        if p:
            data['group_id']=p.id #等级group的id
            if user_group_id:
                g.db_session.query(UserGroup).filter(UserGroup.id==user_group_id).update(data)
            else:
                g.db_session.add(UserGroup(**data))
        else:
            raise Exception(u"无此等级")
                
        g.db_session.query(UserGroup).filter(UserGroup.user_id==user_id).update({"startdate":str(month)})
            
        return u'计算成功'   

    #修改机构等级
    def update_org_grade(self,org_code,level,branch = False):
        if branch == False:
            org_code = org_code
        else :
            org_code = str('M') + str(org_code)

        #查询branch_id
        b_id = g.db_session.query(Branch.role_id).filter(Branch.branch_code==org_code).first()

        if b_id:
            g.db_session.query(Branch).filter(Branch.role_id == b_id[0]).update({Branch.deg_level:level})
            return u"等级修改成功"
        else:
            return u"等级修改失败"
