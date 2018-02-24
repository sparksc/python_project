# -*- coding:utf-8 -*-
#!/bin/python  

import os, time, random  
import DB2  
from datetime import datetime,timedelta

from etl.base.conf import *
from etl.base.util import *
from etl.star.transformdict import *
from etl.base.singleton import singleton
from etl.base.logger import *
import etl.base.util as util
from etl.base.logger import info,debug

from etl.star.manage import DimManage


Config().etldate=None
Config().stretldate=None
Config().dimq=None

@singleton        
class DimCreditCard(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_CREDIT_CARD")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

@singleton        
class DimCustContract(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_CUST_CONTRACT")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

@singleton        
class DimKJ(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_CUST_CONTRACT",keylist=["BUSI_TYPE","CARD_NO",'PAY_TYPE'],dim_type={"BUSI_TYPE":"支付宝快捷支付"},sequence_name="D_CUST_CONTRACT_SEQ")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

@singleton        
class DimEPay(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_CUST_CONTRACT",keylist=["BUSI_TYPE","NET_CST_NO","PAY_TYPE","AGREMENT_NO","CARD_NO"],dim_type={"BUSI_TYPE":"丰收e支付"},sequence_name="D_CUST_CONTRACT_SEQ")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

@singleton        
class DimEPay2(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_CUST_CONTRACT",keylist=["BUSI_TYPE","PAY_TYPE","AGREMENT_NO"],dim_type={"BUSI_TYPE":"新丰收e支付"},sequence_name="D_CUST_CONTRACT_SEQ")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

@singleton        
class DimCustStatus(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_CUST_STATUS")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)


@singleton        
class DimCustType(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_CUST_TYPE")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

#"""
#    理财产品维度,弃用
#@singleton        
#class DimPFinProduct(BaseDim):
#    def __init__(self):
#        self.dim=DimConnect("D_P_FINPRODUCT")
#        self.dim.finish()
#    def find_dim_id(self,key):
#        return self.dim.find_dim_id(key)
#"""
#
#"""
#    理财账户维度,弃用
#@singleton        
#class DimFinAcct(BaseDim):
#    def __init__(self):
#        self.dim=DimConnect("D_FINACCT")
#        self.dim.finish()
#    def find_dim_id(self,key):
#        return self.dim.find_dim_id(key)
#"""
#"""


@singleton        
class DimAccountType(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_ACCOUNT_TYPE")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

@singleton        
class DimAccountStatus(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_ACCOUNT_STATUS")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

@singleton        
class DimAccountPrice(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_ACCOUNT_PRICE")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

@singleton        
class DimChannel(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_T_Channel")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)
@singleton        
class DimTime(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_S_TIME")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

@singleton        
class DimAcctTranType(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_ACCT_TRAN_TYPE")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)



@singleton        
class DimOrg(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_ORG",['ID','ORG0_CODE'])
        self.dim.finish()
        self.db = DBConnect()
        sql = u"select sale_code,sale_org from d_sales_temp where dim_date = ?"
        self.sale_org = self.load_dim_bysql(sql,int(str(Config().etldate)[0:4]))
        self.db.closeDB()

    def load_dim_bysql(self,sql,para):
        self.db.cursor.execute(sql,para)  
        row = self.db.cursor.fetchone() 
        d = {}
        while row: 
            d[row[0]] = row[1]
            row = self.db.cursor.fetchone() 
        return d

    def find_dim_id(self,org_code):
        row={'ORG0_CODE':org_code}
        return self.dim.just_find_dim_id(row)
    
    def just_find_dim_id(self,org_code):
        row={'ORG0_CODE':org_code}
        return self.dim.just_find_dim_id(row)
    def find_id_by_code(self,sale_code):
        org_code = self.sale_org.get(sale_code,None)
        row={'ORG0_CODE':org_code}
        return self.dim.just_find_dim_id(row)


@singleton        
class DimSalesTemp(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_SALES_TEMP",['SALE_CODE'])
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.just_find_dim_id(key)
    def just_find_dim_id(self,key):
        return self.dim.just_find_dim_id(key)



@singleton        
class DimAccount():
    def __init__(self):
        self.acctq=None
        self.db = DBConnect()
        self.init_header()
    def init_header(self):
        self.finacctids={}
        self.billacctids={}
        self.depacct = {}
        self.loanacct = {}
        self.maxid=0
        self.accttq = None
        self.header = util.get_table_desc("D_ACCOUNT",self.db)
    def load_dim_bysql(self,sql):
        info("load dim ,sql:%s"%(sql))
        maxid = 0
        self.db.cursor.execute(sql)  
        row = self.db.cursor.fetchone() 
        d = {}
        while row: 
            if maxid < row[0] : maxid = row[0]
            if len(row) > 2 :
                d[ row[1] ] = (row[0],row[2])
            else:
                d[ row[1] ]=row[0]
            row = self.db.cursor.fetchone() 
        return d
    def find_max_id(self,sql):
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        return row[0]

    def start(self):
        self.init_header()
        info("LOAND ids")
        try:
            maxid=0
            self.finacctids = self.load_dim_bysql(u"select id,account_no from d_account where account_class = '理财账户'".encode('utf-8'))
            self.depacct = self.load_dim_bysql(u"select id,account_no,cst_no from d_account  where account_class in('活期分户','定期分户','无')".encode('utf-8'))
            self.loanacct = self.load_dim_bysql(u"select id,account_no from d_account  where  ACCOUNT_CLASS in ('贴现分户','普通贷款','按揭贷款','保函','无')".encode('utf-8'))
            self.billacctids = self.load_dim_bysql(u"select id,account_no from d_account  where  account_class in('承兑汇票账户','无')".encode('utf-8'))
            #maxid = self.find_max_id("select max(id) from d_account")
            maxid = self.find_max_id("select nextval for D_ACCOUNT_SEQ_NEW from sysibm.dual")
            self.maxid = maxid
        finally:
            self.closeDB()
        info("LOAD finish IDS,maxid:%d"%(maxid))
    def setQueue(self,tq):
        self.accttq=tq

    def finish(self):
        pass
    def closeDB(self):
        self.db.closeDB()    

    def __find_id__(self,row,workids):
        if row.get("ACCOUNT_NO") is None :return 0
        kk = row["ACCOUNT_NO"]
        fid = workids.get(kk,None)
        if fid :
            row["ID"]=fid 
            #更新为最后的帐户信息
            if self.accttq is None :
                debug("###Queue is None")
                debug(row)
            else :
                self.accttq.put( ("U",self.header,row,"D_ACCOUNT") )        
            return fid    
        else:
            self.maxid = self.maxid+1
            fid = self.maxid
            row["ID"]=fid 
            self.finacctids[kk]=fid
            if self.accttq is None :
                debug("###Queue is None")
                debug(row)
                return fid    
            else :
                self.accttq.put( ("I",self.header,row,"D_ACCOUNT") )        
                return fid    

    def __find_fin_id__(self,row):
        return self.__find_id__(row,self.finacctids)
    def __find_bill_id__(self,row):
        return self.__find_id__(row,self.billacctids)

    def find_id(self,row,type = '理财'):
        if type == '理财':    
            return self.__find_fin_id__(row)  
        if type == '承兑':
            return self.__find_bill_id__(row)

    def find_id_by_loanno(self,loan_no):
        rs = self.loanacct.get(loan_no,None)
        return rs

    def find_idandcustno_by_depno(self,account_no):
        rs =  self.depacct.get(account_no,None)
        if rs :
            return rs
        elif self.depacct.get(u"无".encode('utf-8')) :
            return (0,'0')
        else:
            d = {}
            d["ID"] = 0
            d["ACCT_TYPE"] = '0'
            d["ACCOUNT_CLASS"] = u"无".encode('utf-8')
            self.depacct[u"无".encode('utf-8')] = (0,u"无".encode('utf-8'))
            if self.accttq is None :
                debug("###Queue is None")
                debug(account_no)
                return (0,u"无".encode('utf-8'))
            else:
                self.accttq.put( ("I",self.header,d,"D_ACCOUNT") )        
                return (0,u"无".encode('utf-8'))    
            
    
@singleton        
class DimCust():
    def __init__(self):
        self.acctq=None
        print "cust"
        self.db = DBConnect()
        self.init_header()
    def init_header(self):
        self.custdict={}
        self.custids={}
        self.custq=None
        self.ids={}
        self.maxid=0
        self.custheader = util.get_table_desc("D_CUST",self.db)
    def load_dim_bysql(self,sql):
        info("load dim ,sql:%s"%(sql))
        maxid = 0
        self.db.cursor.execute(sql)  
        row = self.db.cursor.fetchone() 
        d = {}
        while row: 
            if maxid < row[0] : maxid = row[0]
            if len(row) > 2 :
                d[ row[1] ] = (row[0],row[2])
            else:
                d[ row[1] ]=row[0]
            row = self.db.cursor.fetchone() 
        return ( d, maxid )

    def start(self):
        self.init_header()
        info("LOAND ids")
        maxid=0
        ( self.custids,maxid) = self.load_dim_bysql(" select id,CUST_KEY from D_CUST ")
        self.maxid = maxid
        self.closeDB()
        info("LOAD finish IDS,maxid:%d"%(maxid))
    def setQueue(self,custq):
        self.custq=custq
    def finish(self):
        pass
        
    def closeDB(self):
        self.db.closeDB()    

    def __find_cust_id__(self,row):
        if row.get("CUST_NO") is None :return 0
        kk = "CUST"+row["CUST_NO"]
        row["CUST_KEY"]=kk
        fid = self.custids.get(kk,None)

        if self.custids.get( kk ) is not None :
            row["ID"]=fid 
            #更新为最后的帐户信息
            if self.custq is None :
                debug("###Queue is None")
                debug(row)
            else :
                print 'Update D_CUST'
                self.custq.put( ("U",self.custheader,row,"D_CUST") )        
                pass
            return fid    
        else:
            self.maxid = self.maxid+1
            fid = self.maxid
            row["ID"]=fid 
            self.custids[kk]=fid
            if self.custq is None :
                debug("###Queue is None")
                debug(row)
                return fid    
            else :
                self.custq.put( ("I",self.custheader,row,"D_CUST") )        
                return fid    
    def find_cust_id(self,row,newflag=True):
        return  self.__find_cust_id__(row)  
    
    def find_dim_id_by_custno(self,cust_no):
        return self.custids.get("CUST"+cust_no,None)
        
def dims_start():
    DimCust().start()
    DimAccount().start()

def dims_finish():
    DimCust().finish()    
    DimAccount().finish()
    DimCust().closeDB()    
    DimAccount().closeDB()

#def load_dims(quenu1,quenu2,quenu3):
def load_dims(quenu1):
    DimCust().setQueue(quenu1) 
    DimCustType().setQueue(quenu1) 
    DimCustStatus().setQueue(quenu1) 
    DimCustContract().setQueue(quenu1) 
    DimEPay().setQueue(quenu1) 
    DimEPay2().setQueue(quenu1) 
    DimKJ().setQueue(quenu1) 
    #DimPFinProduct().setQueue(quenu1) 
    #DimFinAcct().setQueue(quenu1) 
    DimAccount().setQueue(quenu1) 
    DimManage().setQueue(quenu1) 
    DimAccountType().setQueue(quenu1) 
    DimAccountStatus().setQueue(quenu1) 
    DimAccountPrice().setQueue(quenu1) 
    #DimTime().setQueue(quenu1) 
    DimChannel().setQueue(quenu1) 
    DimAcctTranType().setQueue(quenu1) 
    
    DimOrg()
    DimSalesTemp()    

@singleton        
class DimBuTransaction(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_EBILLS_BU_TRANSACTIONINFO",keylist=["TXNSERIALNO"],sequence_name="D_EBILLS_BU_TRANSACTIONINFO_SEQ")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

@singleton        
class DimEbillsTranType(BaseDim):
    def __init__(self):
        self.dim=DimConnect("d_ebills_tran_type",sequence_name="d_ebills_tran_type_seq")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

@singleton        
class DimTransAction(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_TRANSACTION",keylist=["JRNL_NO"],sequence_name="D_TRANSACTION_SEQ")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

@singleton        
class DimTransActionType(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_TRANSACTION_TYPE",sequence_name="D_TRANSACTION_TYPE_SEQ")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

class DimAccountBase():
    '''
    原有的DimAccount实现的不好，暂不修改，增加该对象
    drop table D_ACCOUNT2
    go
    CREATE TABLE YDW.D_ACCOUNT2  (
    ID          BIGINT NOT NULL,
    ACCOUNT_NO  VARCHAR(32) NOT NULL,
    CONTRACT_NO VARCHAR(32) NOT NULL,
    DUEBILL_SEQ INTEGER NOT NULL,
    CCY         VARCHAR(3) NOT NULL DEFAULT '000',
    CST_NAME    VARCHAR(160) ,
    ACCOUNT_NAME    VARCHAR(160) ,
    CASH_TP     VARCHAR(32),
    card_no varchar(32),
    ACCOUNT_CLASS varchar(32),
    open_date_id bigint,
    close_date_id bigint,
    due_date_id bigint,
    SUBJ_NO varchar(32),
    RIMARY KEY(ID)
    ) IN DMS_DIM
    go
    insert into D_ACCOUNT2
    select g.id,g.account_no,g.CONTRACT_NO,g.DUEBILL_SEQ,g.CCY,a.CST_NAME,a.CST_NAME ACCOUNT_NAME,g.CASH_TP,a.CARD_NO,a.ACCOUNT_CLASS,a.OPEN_DATE_ID,a.CLOSE_DATE_ID,a.DUE_DATE_ID,a.SUBJ_NO  from D_ACCOUNT a,d_account_gid g where g.id=a.id
    '''
    def __init__(self, dim_name = "d_account2", cols=None):
        self.dim_name = dim_name
        self.cols = cols
        pass
        #self.init_header()

    def init_header(self):
        self.db = DBConnect()
        self.acctq=None
        if self.cols is not None:
            self.header = self.cols
        else:
            self.header = util.get_table_desc(self.dim_name, self.db)

    def load_dim_bysql(self,sql):
        info("load dim ,sql:%s"%(sql))
        self.db.cursor.execute(sql)  
        row = self.db.cursor.fetchone() 
        d = {}
        while row: 
            d[ row[1] ] = row[0]
            row = self.db.cursor.fetchone() 
        return d

    def start(self):
        self.init_header()
        info("LOAND ids")
        try:
            sql = """
            insert into D_ACCOUNT2
            select 
                g.id,g.account_no,g.CONTRACT_NO,g.DUEBILL_SEQ,g.CCY,a.CST_NAME,a.CST_NAME ACCOUNT_NAME,
                g.CASH_TP,a.CARD_NO,a.ACCOUNT_CLASS,a.OPEN_DATE_ID,a.CLOSE_DATE_ID,a.DUE_DATE_ID,a.SUBJ_NO ,a.cst_no
                ,'否' as is_fc_flag
            from 
                D_ACCOUNT a,d_account_gid g 
            where 
                g.id=a.id
                and not exists ( select 1 from D_ACCOUNT2 a2 where a2.id = a.id )
            """
            if self.dim_name.upper()  == 'D_ACCOUNT2':
                self.db.cursor.execute(sql)  
                self.db.conn.commit()
                sql = u"select id,account_no||'-'||CCY||'-'||CASH_TP from %s"%( self.dim_name )
                sql = sql.encode('utf-8')
            else:
                sql = """
                    merge into d_account a 
                        using d_account_gid g
                        on a.id= g.id
                        when matched then update set a.cash_tp=g.cash_tp
                """
                #self.db.cursor.execute(sql)  
                #self.db.conn.commit()

                sql = u"select id,account_no||'-'||CCY||'-'||CASH_TP from %s"%(self.dim_name)
                sql = sql.encode('utf-8')
            print sql
            self.accts = self.load_dim_bysql( sql )
        finally:
            pass

    def setQueue(self,tq):
        self.acctq = tq

    def finish(self):
        self.closeDB()

    def closeDB(self):
        self.db.closeDB()    

    def find_dim_id(self, row, auto_update=True):
        if row.get("ACCOUNT_NO") is None :return 0
        key = [ row["ACCOUNT_NO"], row.get("CCY","CNY"),row.get("CASH_TP","1") ]
        kk = "-".join( key )

        gid = DimAccountGid().find_dim_id(row["ACCOUNT_NO"],row["CCY"],row["CASH_TP"])
        fid = self.accts.get( kk )
        self.accts[kk] = gid

        if fid is not None and fid != gid :
            raise Exception("%s id error?"%( row.get("ACCOUNT_NO") ) )
        if fid is not None:
            if auto_update:
                row["ID"]  = gid
                self.acctq.put( ("U", self.header, row, self.dim_name) )        
        else:
            row["ID"]  = gid
            self.acctq.put( ("I", self.header, row, self.dim_name) )
        return gid

    def find_dim_id_by_child_account(self, row, auto_update=True):
        if row.get("ACCOUNT_NO") is None :return 0
        nrow = {k:row[k] for k in row}
        seq = nrow["ACCOUNT_SEQ"] 
        if nrow["CASH_TP"] == "现钞":
            nrow["CASH_TP"] = '1'
        else:
            nrow["CASH_TP"] = '2'
        nrow["CASH_TP"] = nrow["CASH_TP"] + "-" + str( seq )
        nrow["ACCOUNT_CLASS"] = "定期子账户"
        return self.find_dim_id(nrow, auto_update)


    def find_dim_id_by_ccrd(self, row, auto_update=True):
        if row.get("ACCOUNT_NO") is None :return 0
        nrow = {k:row[k] for k in row}
        nrow["CASH_TP"] = '1'
        nrow["ACCOUNT_NO"] = nrow["ACCOUNT_NO"].replace(".","").strip()
        nrow["CCY"] = 'CNY'
        nrow["ACCOUNT_CLASS"] = '贷记卡分户'
        if nrow.get("ACCOUNT_NAME") is not None:
            nrow["ACCOUNT_NAME"] = nrow["ACCOUNT_NAME"].decode("gbk").encode("utf8").strip()
        if nrow.get("CST_NAME") is not None:
            nrow["CST_NAME"] = nrow["CST_NAME"].decode("gbk").encode("utf8").strip()
            if nrow.get("ACCOUNT_NAME") is None:
                nrow["ACCOUNT_NAME"] = nrow["CST_NAME"]
        return self.find_dim_id(nrow, auto_update)


@singleton        
class DimAccount2():
    def __init__(self):
        self.dimbase = DimAccountBase("d_account2")
    def init_header(self):
        self.dimbase.init_header()
    def start(self):
        self.dimbase.start()
    def setQueue(self,tq):
        self.dimbase.setQueue(tq)
    def finish(self):
        self.dimbase.finish()
    def closeDB(self):
        self.dimbase.closeDB()
    def find_dim_id(self, row, auto_update=True):
        return self.dimbase.find_dim_id(row, auto_update)
    def find_dim_id_by_child_account(self, row, auto_update=True):
        return self.dimbase.find_dim_id_by_child_account(row, auto_update)
    def find_dim_id_by_ccrd(self, row, auto_update=True):
        return self.dimbase.find_dim_id_by_ccrd(row, auto_update)

@singleton        
class DimAccountNew(DimAccountBase):
    def __init__(self):
        self.dimbase = DimAccountBase("d_account")
    def init_header(self):
        self.dimbase.init_header()
    def start(self):
        self.dimbase.start()
    def setQueue(self,tq):
        self.dimbase.setQueue(tq)
    def finish(self):
        self.dimbase.finish()
    def closeDB(self):
        self.dimbase.closeDB()
    def find_dim_id(self, row, auto_update=True):
        return self.dimbase.find_dim_id(row, auto_update)
    def find_dim_id_by_child_account(self, row, auto_update=True):
        return self.dimbase.find_dim_id_by_child_account(row, auto_update)
    def find_dim_id_by_ccrd(self, row, auto_update=True):
        return self.dimbase.find_dim_id_by_ccrd(row, auto_update)

@singleton        
class DimAccountGid(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_ACCOUNT_GID",keylist=["ACCOUNT_NO","CCY","CASH_TP"],sequence_name="D_ACCOUNT_SEQ")
        self.dim.finish()

    def find_dim_id(self, account_no, ccy="CNY", cash_tp='1', etldate=18991231):
        key = {"ACCOUNT_NO":account_no,"CCY":ccy,"CASH_TP":cash_tp,"ETL_DATE":etldate}
        return self.dim.find_dim_id(key)

@singleton        
class DimAccountTypeExtend(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_ACCOUNT_TYPE_EXTEND",sequence_name="D_ACCOUNT_TYPE_EXTEND_SEQ")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

@singleton        
class DimOrgStat(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_ORG_STAT",keylist=["ORG_CODE","SUM_ORG"],sequence_name="D_ORG_STAT_SEQ")
        self.dim.finish()

    def find_dim_id(self, org_code):
        key = {"ORG_CODE":org_code,"SUM_ORG":org_code}
        return self.dim.find_dim_id(key)

    def find_dim_id2(self, org_code, sum_org):
        key = {"ORG_CODE":org_code,"SUM_ORG":sum_org}
        return self.dim.find_dim_id(key)

@singleton        
class DimStarPrice(BaseDim):
    def __init__(self):
        self.dim=DimConnect("D_STAR_PRICE",sequence_name="D_STAR_PRICE_SEQ")
        self.dim.finish()
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)
