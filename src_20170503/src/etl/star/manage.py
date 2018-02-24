# -*- coding:utf-8 -*-
#!/bin/python  

import os, time, random  
import DB2  
from datetime import datetime,timedelta

from etl.base.conf import *
import etl.base.util as util
from etl.star.transformdict import *
from etl.base.singleton import singleton
from etl.base.logger import info,debug


@singleton        
class DimManage():
    def __init__(self):
        self.refresh_cash()

    def refresh_cash(self):
        self.dim=util.DimConnect("D_MANAGE")
        self.desc=None
        self.init()
        self.dim.finish()

    def init(self):
        self.load_dep_relation()
        self.load_fin_relation()
        self.load_loan_relation()
        self.load_ebank_relation()
        self.load_ebank_relation2()
        self.load_credit_relation()
        self.load_stock_relation()
        self.load_adb_relation()
        self.load_org_info()#机构上下级
    
    def get_rela_dict(self,sql,para=None):
        cursor=self.dim.cursor
        if para:
            cursor.execute(sql,para)
        else:
            cursor.execute(sql)
        d={}
        row = cursor.fetchone()
        while row:
            xrow=d.get( str(row[0]) )
            if xrow is None : xrow=[]
            if row not in xrow:
                xrow.append(row)
                d[str(row[0])]=xrow
            row = cursor.fetchone()
        #print len(d)    
        return d

    def load_org_info(self):
        cursor=self.dim.cursor
        sql = """
        SELECT ORG0_CODE, ORG0_NAME, ORG1_CODE, ORG1_NAME, ORG2_CODE, ORG2_NAME, ORG3_CODE, ORG3_NAME
            FROM YDW.D_ORG
            where START_DATE<=? and END_DATE>=?"""
        etldate=int(Config().etldate)
        cursor.execute(sql,etldate,etldate)
        d = {}
        row = cursor.fetchone()
        while row:
            d[str(row[0])]=row
            row = cursor.fetchone()

        self.orgs = d

    #存款关系    
    def load_dep_relation(self):
        #存款客户号关系
        sql="select org_no||'!'||cust_in_no,manager_no,typ||hook_type type,percentage from cust_hook where STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and typ = '存款'"
        self.ckcust_managers=self.get_rela_dict(sql)

        #存款账号关系
        sql="""
            select org_no||'!'||account_no,manager_no,typ||hook_type type,percentage 
            from ACCOUNT_HOOK 
            where STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and typ = '存款'
              and start_date <=%d
              ---and end_date >= %d ---暂时不检查结束日期
        """%(Config().etldate,Config().etldate)
        print sql
        self.ckacct_managers=self.get_rela_dict(sql)

    #贷款关系    
    def load_loan_relation(self):
        #贷款客户号关系
        sql="select org_no||'!'||cust_in_no,manager_no,typ||hook_type type,percentage from cust_hook where STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and typ = '贷款'"
        self.dkcust_managers=self.get_rela_dict(sql)

        #贷款账号关系
        sql="select org_no||'!'||account_no,manager_no,typ||hook_type type,percentage from ACCOUNT_HOOK where STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and typ = '贷款'"
        self.dkacct_managers=self.get_rela_dict(sql)

    #理财关系    
    def load_fin_relation(self):
        #理财客户号关系
        sql="select org_no||'!'||cust_in_no,manager_no,typ||hook_type type,percentage from cust_hook where STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and typ = '理财'"
        self.fincust_managers=self.get_rela_dict(sql)

        #理财账号关系
        sql="select '!'||account_no,manager_no,typ||hook_type type,percentage from ACCOUNT_HOOK where STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and typ = '理财'"
        self.finacct_managers=self.get_rela_dict(sql)
        #print len(self.finacct_managers)

    #电子银行关系    
    def load_ebank_relation(self):
        #贷款客户号关系
        sql="select org_no||'!'||cust_in_no||'!'||sub_typ,manager_no,typ||hook_type type,percentage from cust_hook where STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and typ = '电子银行'"
        self.ebankcust_managers=self.get_rela_dict(sql)

    #电子银行关系,不考虑类型
    def load_ebank_relation2(self):
        #贷款客户号关系
        sql="select org_no||'!'||cust_in_no,manager_no,typ||hook_type type,percentage from cust_hook where STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and typ = '电子银行'"
        self.ebankcust_managers2=self.get_rela_dict(sql)

    #信用卡关系    
    def load_credit_relation(self):
        sql="select '!'||account_no,manager_no,typ||hook_type type,percentage from account_hook where STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and typ = '信用卡'"
        self.creditcust_managers=self.get_rela_dict(sql)

    #第三方存管关系    
    def load_stock_relation(self):
        #贷款客户号关系
        sql="select org_no||'!'||cust_in_no,manager_no,typ||hook_type type,percentage from cust_hook where STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and typ = '第三方存管'"
        self.stockcust_managers=self.get_rela_dict(sql)

    #i代理保险存管关系    
    def load_adb_relation(self):
        #贷款客户号关系
        sql="select org_no||'!'||cust_in_no,manager_no,typ||hook_type type,percentage from cust_hook where STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and typ = '代理保险'"
        self.adbcust_managers=self.get_rela_dict(sql)

    def setQueue(self,queue):
        self.dim.queue=queue
    
    #得到存款客户的key
    def find_dep_cust_key(self,org_no,cust_in_no):
        d =  self.find_cdk_key(org_no,"%s!%s"%(org_no,cust_in_no),self.ckcust_managers)
        if d["GROUP_KEY"] == "无":
            d["MANAGE_TYPE"] = "机构管理"
            return self.dim.find_dim_id(d),False
        else:
            d["MANAGE_TYPE"] = "存款客户管理"
            return self.dim.find_dim_id(d),True

    #得到存款账户的key
    def find_dep_acct_key(self,org_no,acct_no):
        d =  self.find_cdk_key(org_no,acct_no,self.ckacct_managers)
        if d["GROUP_KEY"] == "无":
            d["MANAGE_TYPE"] = "机构管理"
            return self.dim.find_dim_id(d),False
        else:
            #print d['GROUP_KEY']
            d["MANAGE_TYPE"] = "存款账户管理"
            return self.dim.find_dim_id(d),True

    #得到理财账户的key
    def find_fin_acct_key(self,org_no,acct_no):
        d =  self.find_cdk_key(org_no,acct_no,self.finacct_managers)
        if d["GROUP_KEY"] == "无":
            d["MANAGE_TYPE"] = "机构管理"
            return self.dim.find_dim_id(d),False
        else:
            d["MANAGE_TYPE"] = "理财客户管理"
            return self.dim.find_dim_id(d),True

    #得到贷款客户的key
    def find_loan_cust_key(self,org_no,cust_in_no):
        d =  self.find_cdk_key(org_no,cust_in_no,self.dkcust_managers)
        if d["GROUP_KEY"] == "无":
            d["MANAGE_TYPE"] = "机构管理"
            return self.dim.find_dim_id(d),False
        else:
            d["MANAGE_TYPE"] = "贷款客户管理"
            return self.dim.find_dim_id(d),True

    #得到承兑汇票客户的key
    def find_acpt_cust_key(self,org_no,cust_in_no):
        d =  self.find_cdk_key(org_no,cust_in_no,self.dkcust_managers)
        if d["GROUP_KEY"] == "无":
            d["MANAGE_TYPE"] = "机构管理"
            return self.dim.find_dim_id(d),False
        else:
            d["MANAGE_TYPE"] = "贷款客户管理"
            return self.dim.find_dim_id(d),True

    #得到贷款账户的key
    def find_loan_acct_key(self,org_no,acct_no):
        d =  self.find_cdk_key(org_no,acct_no,self.dkacct_managers)
        if d["GROUP_KEY"] == "无":
            d["MANAGE_TYPE"] = "机构管理"
            return self.dim.find_dim_id(d),False
        else:
            d["MANAGE_TYPE"] = "贷款账户管理"
            return self.dim.find_dim_id(d),True
    
    #得到合约的key
    def find_contract_cust_key(self,org_no,cust_in_no,subtype):
        #print org_no,cust_in_no,subtype
        d = self.find_cdk_key(org_no,cust_in_no+'!'+subtype,self.ebankcust_managers)
        if d["GROUP_KEY"] == "无":
            d["MANAGE_TYPE"] = "机构管理"
            return self.dim.find_dim_id(d),False
        else:
            d["MANAGE_TYPE"] = "电子银行客户管理"
            return self.dim.find_dim_id(d),True

    #得到合约的key,不考虑子类型，认为所有电子银行在一个网点只能认给一个人
    def find_contract_cust_key2(self,org_no,cust_in_no):
        d = self.find_cdk_key(org_no,cust_in_no,self.ebankcust_managers2)
        #print org_no,cust_in_no,d["GROUP_KEY"]
        if d["GROUP_KEY"] == "无":
            d["MANAGE_TYPE"] = "机构管理"
            return self.dim.find_dim_id(d),False
        else:
            d["MANAGE_TYPE"] = "电子银行客户管理"
            return self.dim.find_dim_id(d),True

    #得到信用卡的key
    def find_credit_account_key(self,org_no,account_no):
        d = self.find_cdk_key(org_no,account_no,self.creditcust_managers)
        if d["GROUP_KEY"] == "无":
            d["MANAGE_TYPE"] = "机构管理"
            return self.dim.find_dim_id(d),False
        else:
            #print d['GROUP_KEY']
            d["MANAGE_TYPE"] = "信用卡客户管理"
            return self.dim.find_dim_id(d),True

    #得到第三方存管的key
    def find_stock_cust_key(self,org_no,cust_in_no):
        d = self.find_cdk_key(org_no,cust_in_no,self.stockcust_managers)
        if d["GROUP_KEY"] == "无":
            d["MANAGE_TYPE"] = "机构管理"
            return self.dim.find_dim_id(d),False
        else:
            #print d['GROUP_KEY']
            d["MANAGE_TYPE"] = "信用卡客户管理"
            return self.dim.find_dim_id(d),True

    #得到安贷宝的key
    def find_adb_cust_key(self,org_no,cust_in_no):
        d = self.find_cdk_key(org_no,cust_in_no,self.adbcust_managers)
        if d["GROUP_KEY"] == "无":
            d["MANAGE_TYPE"] = "机构管理"
            return self.dim.find_dim_id(d),False
        else:
            #print d['GROUP_KEY']
            d["MANAGE_TYPE"] = "安贷宝客户管理"
            return self.dim.find_dim_id(d),True

    #得到存贷款的key
    def find_cdk_key(self,org_no,number_no,d_managers):
        keys=None
        etldate=int(Config().etldate)
        if number_no is None:number_no = '0'
        ono=org_no
        for i in d_managers:
            #print d_managers.get(i)[0][0][0]
            if d_managers.get(i)[0][0][0]=='!':
                ono=''
            break    
        #org_no=''#存款,理财,信用卡按账号认定
        acs=d_managers.get(ono+'!'+number_no)
        #print acs,org_no+'!'+number_no
        org_list = self.orgs.get(str(org_no),[org_no,org_no,org_no,org_no,org_no,org_no])
        d ={}
        d["FIRST_BRANCH_CODE"] = org_list[4] 
        d["FIRST_BRANCH_NAME"] = org_list[5]
        d["SECOND_BRANCH_CODE"] = org_list[2] 
        d["SECOND_BRANCH_NAME"] = org_list[3]
        d["THIRD_BRANCH_CODE"] = org_list[0] 
        d["THIRD_BRANCH_NAME"] = org_list[1]
        d["DIM_DATE"] = int(str(Config().etldate)[:4])
        d["MANAGE_FACTOR"] = 100
        if acs:
            #print acs
            org_str = "%s!%s!%s"%(org_list[0],org_list[2],org_list[4])
            for r in acs:
                d["MANAGE_FACTOR"] = d["MANAGE_FACTOR"] - r[3]
                if keys is None:
                    keys = "%s!%s!%s!%s"%(r[1],r[2],str(r[3]),org_str)
                else:
                    keys = "%s;%s"%(keys,"%s!%s!%s!%s"%(r[1],r[2],str(r[3]),org_str))
        if keys is None:
            d['GROUP_KEY'] = '无' 
            return d
        else:
            d['GROUP_KEY'] = keys
            #print keys
            return d

    def is_nullstr(self,val):
        if val is None or len(val.strip()) == 0 : return True
        return False


if __name__=='__main__':
    Config().etldate=20150101
    DimManage().find_dep_cust_key("966150","81078216836")
    #print DimManage().find_interbus_manage_key('100135988717','A').decode("gb2312")
    #print DimManage().find_interbus_manage_key('100092965866','I').decode("gb2312")
