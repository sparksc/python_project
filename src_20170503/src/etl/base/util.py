# -*- coding:utf-8 -*-
#!/bin/python  

import os, time, random  
import DB2  
from datetime import datetime,timedelta
from decimal import *

from etl.base.conf import *
from etl.star.transformdict import *
from etl.base.singleton import singleton
from etl.base.logger import info
import csv
import types


Config().etldate=None
Config().stretldate=None
Config().dimq=None

condecimal = getcontext()

def tostrdate(etldate):
    s=str(etldate)
    return s[0:4]+"-"+s[4:6]+"-"+s[6:8]

def acno_key_dict(date,name):
        addfile=Config().target_data + "/" + str(date) + "/%s_1.txt" %name
        handler = file(addfile, 'rb')
        r={}
        handler_csv=csv.reader(handler)
        rowlen=-1
        for row in handler_csv :
                if rowlen == -1 : rowlen=len(row)
                k = "%s%s%s%s%s"%(row[0],row[1],row[2],row[3],row[4])
                v = str(row[5])
                r[k]=v
        handler.close()
        return r
    
#找到某个字段下标
def get_colname_index(desc,name):
    name=name.upper()# 将小写转换成大写
    idx=0
    for col in desc:
        if col[0] == name : 
            return idx
        idx=idx+1
    return -1
def get_header_index(headers,name):
    name=name.upper()
    idx=0
    for col in headers:
        if col == name : 
            return idx
        idx=idx+1
    return -1

def flag_to_mean(codedict,c,value):
    if value is not None  and isinstance(value,str) == True:
        value1 = value.strip()
    else:
        value1 = value
    d=codedict.get(c)
    if d is None : return  value
    val=d.get(value1)
    if val is None : return  value
    return val.encode('utf-8')

def get_default_nullval(c):
    if c[1] == 12 : rk=u"无".encode('utf-8')
    elif c[1] == 91: rk = '1899-12-31'
    else : rk=0
    return rk
#字段数值处理
def get_default_val(c,rowkey):
    rk=rowkey.get(c[0])
    if rk is None :
        if c[1] == 12 : rk=u"无".encode('utf-8')
        else : rk=0
    return rk
        
def mergerow(conn,cursor,tablename,row,cols=None,commit=True):
    f = isinstance(row,dict)
    if f == False : raise Exception('mergerow', u'mergerow方法只支持数据类型dict')
    #if commit : trans = conn.begin()
    fields = row.keys()
    if "ID" not in fields : raise Exception("mergedb',u'必须包含列名ID")
    keyindex=[ -1 if fields[i] == "ID" else i  for i in range( len(fields) ) ]
    keyindex.remove(-1)
    
    #sv = ",".join([ " %s%s%s %s"%(is_strcol(cols,fields[i]),row[fields[i]],is_strcol(cols,fields[i]),fields[i]) for i in range( len(fields) ) ])
    #uv = ",".join([ "t.%s= %s%s%s "%(fields[i],is_strcol(cols,fields[i]),row[fields[i]],is_strcol(cols,fields[i])) for i in keyindex  ])
    #iv2 = ",".join([ " %s%s%s "% ( is_strcol(cols,fields[i]),row[fields[i]],is_strcol(cols,fields[i])) for i in range( len(fields) ) ])
    
    uv = ",".join([ "t.%s= ? "%( fields[i]) for i in keyindex  ])
    iv1 = ",".join([ " %s"%(fields[i]) for i in range( len(fields) ) ])
    iv2 = ",".join([ " ? "  for i in range( len(fields) ) ])
    data=[ row[fields[i]] for i in range( len(fields) ) ]
    id=row["ID"] 
    uvdata=[ row[fields[i]] for i in keyindex   ]
    uvdata.append(id)

    isql= "  INSERT into %s (%s) values (%s)"%( tablename,iv1,iv2)
    usql= "  update %s  t set  %s where id=?"%( tablename,uv )
    qsql= "  select 1 from %s  t where id=?"%( tablename)
    cursor.execute(qsql,row["ID"])
    qrow = cursor.fetchone() 
    if qrow is None:
        '''
        for i in range( len(fields) ) :
            strlen=0
            val=row[fields[i]]
            if isinstance(val, unicode)  or  isinstance(val, str) :
                strlen=len(val)
        '''
        cursor.execute(isql,data)
    else:
        cursor.execute(usql,uvdata)
    conn.commit()
    
def getConnect(dsn,user,passwd) :
    return  DB2.connect(dsn,user,passwd)

def getUpateSQL(nheader,tbname):         
    updatesql = None
    for k in nheader :
        if updatesql is None :
            updatesql = "update %s t set t.%s=?"%(tbname,k)
        else:
            updatesql = updatesql+ ",   t.%s=?"%(k)
    if updatesql is None :
        raise Exception("%s header is none"%(tbname))
    updatesql = updatesql +" where t.id=?"    
    return updatesql
def getInsertSQL(header,tbname):
    vals=[]
    for r in  header :
        vals.append("?")
    cols=",".join(header)
    vals=",".join(vals)
    insertsql = """ 
        INSERT INTO %s (  %s ) 
        VALUES (%s) 
        """%(tbname,cols,vals)    
 
    return insertsql
        
class DBConnect():
    __connect_num__=0
    def __init__(self,dsn=DSN,user=USER,passwd=PASSWD):
        DBConnect.__connect_num__=DBConnect.__connect_num__+1
        self.conn = getConnect(dsn,user,passwd)
        self.cursor =self.conn.cursor()  
    def closeDB(self):
        try:
            self.cursor.close() 
            self.cursor=None
            self.conn.close() 
            self.conn=None
            DBConnect.__connect_num__=DBConnect.__connect_num__-1
        except  Exception,e:
            pass
        finally:
            pass
        
@singleton
class DBUtilConnect():
    def __init__(self):
        self.conn = getConnect()
        self.cursor =self.conn.cursor()  
    def close(self):
        self.cursor.close() 
        self.conn.close()         
    
class DbInsert(DBConnect):
    def __init__(self):
        DBConnect.__init__(self)
        self.flag = 2
    def queue2db(self,data):
        if len(data) == 2:
            if self.flag!=2: 
                self.flag = 2
                self.commit()
            self.insert_onedata(data)
        else:
            self.flag = 3
            self.update_dim(data)
    def commit(self):
        self.conn.commit()
    def insert_onedata(self,data):
        #print "2323",data[0],data[1]
        try :
            #print data[0],data[1]
            self.cursor.execute(data[0],data[1])  
        except Exception , e :
            print "insert_dim.sql=",data[0]
            print "insert_dim.value=",data[1]
            raise e

    def get_dbheader(self,row,dbheader):
        header = row.keys()
        db= []
        for k in dbheader :
            if isinstance(k, unicode) or isinstance(k, str ):
                k1=k
            else:
                k1=k[0]
            db.append( k1 )
        header=[]
        for k in row.keys():
            if k in db : header.append( k )
        return header
                
    def update_dim(self,data):
        if data[0] == 'U' :
            row=data[2]
            header = self.get_dbheader(row,data[1])
            tbname=data[3]
            
            if "ID" in header : header.remove("ID")            
            nheader=[]
            nrow=[]
            for k in header :
                val = row.get(k)
                if val is None :continue
                nheader.append(k)
                nrow.append( val )
            nrow.append( row["ID"] )
            usql=getUpateSQL(nheader,tbname)
            try:
                self.cursor.execute(usql,nrow)  
                #self.conn.commit()
            except  Exception,e:
                print "update_dim.sql=",usql
                print "update_dim.value=",nrow
                for i in range( len(nheader)):
                    val =nrow[i]
                    if isinstance(val, unicode) or isinstance(val, str ):
                        print nheader[i],val,type(val),len(val)
                    else:
                        print nheader[i],val,type(val)
                raise e
            
        else:
            #header=data[1]
            row=data[2]
            header = self.get_dbheader(row,data[1])
            tbname=data[3]
            
            nheader=[]
            nrow=[]
            for k in data[1] :
                    val = row.get(k[0])
                    if val is None : 
                        val  = get_default_nullval(k)
                    nheader.append(k[0])
                    nrow.append( val )
        
            isql=getInsertSQL(nheader,tbname)
            if(tbname=='D_CUST_TYPE'):
                print isql
                print nrow
                
            try:
                self.cursor.execute(isql,nrow) 
            except  Exception,e:
                print "insert_onedata.sql=",isql
                print "insert_onedata.value=",",".join( [ str(x) for x in nrow ] )
                for i in range( len(nheader)):
                    val =nrow[i]
                    if isinstance(val, unicode) or isinstance(val, str ):
                        print nheader[i],val,type(val),len(val),"index=",i
                    else:
                        print nheader[i],val,type(val),"index=",i
                raise e
def queue2db(q):
    db=DbInsert()
    idx =0 
    while True:
        if not q.empty() :
            value = q.get(True)
            if value is  None :
                db.commit()
                break
            db.queue2db(value)
            idx = idx + 1
            if idx >= 1000 :
                #print "comint"
                db.commit()
                idx=0
        else:
            time.sleep(0.001)
    db.commit()
    db.closeDB()

 
            
def daycalc(etldate,days):
    if etldate == 0:
        return 0
    s=str(etldate)
    d1=datetime(int(s[0:4]),int(s[4:6]),int(s[6:8])) + timedelta(days)
    s=str(d1.strftime('%Y%m%d'))
    return s            

def cust_in_fo(etldate):
    db = DBConnect()
    sql="""
    select cst_no,OPEN_DATE_ID
    from
        (select cst_no,OPEN_DATE_ID from D_ACCOUNT where CCY!='CNY' and  OPEN_DATE_ID <=? group by CST_NO,OPEN_DATE_ID)
    order by OPEN_DATE_ID desc
    """
    db.cursor.execute(sql,etldate)
    row = db.cursor.fetchone()
    d = {}
    while row: 
        if str(row[0]) not in d:
            d[str(row[0])] = int(row[1])#客户内码开户时间
        row = db.cursor.fetchone()
    db.closeDB()
    return d

def delete_fcustview(etldate,enddate,atype=None):
    db = DBConnect()
    info("lock tableF_C_CUSTVIEW")
    lock="lock table  F_C_CUSTVIEW in exclusive   mode"
    #db.cursor.execute(lock)
    info("delete F_C_CUSTVIEW")
    if atype is None :
        db.cursor.execute("DELETE from  F_C_CUSTVIEW where date_id>=? and date_id<=? ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_financialsale(etldate,enddate,atype=None):
    db = DBConnect()
    if atype is None :
        db.cursor.execute("DELETE from F_balance  where date_id>=? and date_id<=? and acct_type = '8' ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_contract(etldate,enddate,atype=None):
    db = DBConnect()
    if atype is None :
        db.cursor.execute("delete from F_CONTRACT_STATUS f where CONTRACT_ID in (select s.CONTRACT_ID from F_CONTRACT_STATUS s  join D_CUST_CONTRACT c on s.CONTRACT_ID=c.ID  where c.BUSI_TYPE in ('丰收e支付','新丰收e支付','贷款合同','自助终端','ATM','POS') and s.DATE_ID>= ? and s.DATE_ID<= ? ) and f.date_id >= ? and f.date_id <= ?",(etldate,enddate, etldate,enddate))
    else:
        db.cursor.execute("delete from F_CONTRACT_STATUS f where CONTRACT_ID in (select s.CONTRACT_ID from F_CONTRACT_STATUS s  join D_CUST_CONTRACT c on s.CONTRACT_ID=c.ID  where c.BUSI_TYPE= ? and s.DATE_ID>= ? and s.DATE_ID<= ? ) and f.date_id >= ? and f.date_id <= ?",(atype,etldate,enddate,etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_creditbad(etldate,enddate,atype=None):
    db = DBConnect()
    if atype is None :
        db.cursor.execute("DELETE FROM YDW.F_CREDIT_BAD WHERE date_id>=? and date_id<=? ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_creditbad2(etldate,enddate,atype=None):
    db = DBConnect()
    if atype is None :
        db.cursor.execute("DELETE FROM YDW.F_CREDIT_BAD_20161031 WHERE date_id>=? and date_id<=? ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_creditmpur(etldate,enddate,atype=None):
    db = DBConnect()
    if atype is None :
        db.cursor.execute("DELETE FROM YDW.F_CREDIT_MPUR_20161031 WHERE date_id>=? and date_id<=? ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_fbillacount(etldate,enddate,atype=None):
    db = DBConnect()
    if atype is None :
        db.cursor.execute("DELETE from F_balance  where date_id>=? and date_id<=? and acct_type = '7' ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_blta(etldate,enddate):
    db = DBConnect()
    info("lock table FF_CORE_BLTA03LC")
    db.cursor.execute("DELETE FROM FF_CORE_BLTA03LC WHERE WORKDATE>=? and WORKDATE<=?",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_blfm(etldate,enddate):
    db = DBConnect()
    info("lock table F_CORE_BLFMCNAF")
    db.cursor.execute("DELETE FROM F_CORE_BLFMCNAF WHERE WORKDATE>=? and WORKDATE<=?",(etldate,enddate))
    db.conn.commit()
    db.closeDB()
def delete_blfmmtrn(etldate,enddate):
    db = DBConnect()
    info("lock table F_CORE_BLFMMTRN")
    db.cursor.execute("DELETE FROM F_CORE_BLFMMTRN WHERE WORKDATE>=? and WORKDATE<=?",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_gasaccount(etldate,enddate):
    db = DBConnect()
    info("lock table GAS_BIDW_BUSINESS_COND_DO3_APP")
    #db.cursor.execute(lock)
    db.cursor.execute("DELETE from GAS_BIDW_BUSINESS_COND_DO3_APP where DATE_ID>=? and DATE_ID<=? ",(etldate,enddate))
    db.cursor.execute("DELETE FROM GAS_BIDW_ORG_LV6_DA WHERE DATE_ID>=? and DATE_ID<=?",(etldate,enddate))

    db.cursor.execute("DELETE FROM GAS_BIDW_BUSINESS_COND_DO6_APP WHERE DATE_ID>=? and DATE_ID<=?",(etldate,enddate))
    db.cursor.execute("DELETE FROM GAS_BIDW_ACCOUNT_KJ_DA WHERE DATE_ID>=? and DATE_ID<=?",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_pos_insert(etldate,enddate):
    db = DBConnect()
    info("lock table FARM_MON_LIVING")
    #db.cursor.execute(lock)
    db.cursor.execute("DELETE FROM FARM_MON_LIVING WHERE WORK_DATE>=? and WORK_DATE<=? ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_ebills_qry_settlement_corp(etldate,enddate):
    db = DBConnect()
    info("lock table ebills_qry_settlement_corp")
    #db.cursor.execute(lock)
    db.cursor.execute("DELETE FROM  ebills_qry_settlement_corp  WHERE WORKDATE>=? and WORKDATE<=? ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_core_bhfmcmrd(etldate,enddate):
    db = DBConnect()
    info("lock table CORE_BHFMCMRD")
    #db.cursor.execute(lock)
    db.cursor.execute("DELETE FROM  CORE_BHFMCMRD  WHERE WORKDATE>=? and WORKDATE<=? ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_CORE_BHFMCMRM_DIRECT(etldate,enddate):
    db = DBConnect()
    info("lock table CORE_BHFMCMRM_DIRECT")
    #db.cursor.execute(lock)
    db.cursor.execute("DELETE FROM  CORE_BHFMCMRM_DIRECT  WHERE WORKDATE>=? and WORKDATE<=? ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()


def delete_ebills_pa_managercorpinfo(etldate,enddate):
    db = DBConnect()
    info("lock table ebills_pa_managercorpinfo")
    #db.cursor.execute(lock)
    db.cursor.execute("DELETE FROM  ebills_pa_managercorpinfo  WHERE WORKDATE>=? and WORKDATE<=? ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_ebills_pa_managerinfo(etldate,enddate):
    db = DBConnect()
    info("lock table ebills_pa_managercorpinfo")
    #db.cursor.execute(lock)
    db.cursor.execute("DELETE FROM  ebills_pa_managerinfo  WHERE WORKDATE>=? and WORKDATE<=? ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_ebills_pa_corp(etldate,enddate):
    db = DBConnect()
    info("lock table ebills_pa_managercorpinfo")
    #db.cursor.execute(lock)
    db.cursor.execute("DELETE FROM  ebills_pa_corp  WHERE WORKDATE>=? and WORKDATE<=? ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_ebills_pa_org(etldate,enddate):
    db = DBConnect()
    info("lock table ebills_pa_managercorpinfo")
    #db.cursor.execute(lock)
    db.cursor.execute("DELETE FROM  ebills_pa_org  WHERE WORKDATE>=? and WORKDATE<=? ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_new_ebills_bu_transactioninfo(etldate,enddate):
    db = DBConnect()
    info("lock table ebills_pa_managercorpinfo")
    #db.cursor.execute(lock)
    db.cursor.execute("DELETE FROM  new_ebills_bu_transactioninfo  WHERE WORKDATE>=? and WORKDATE<=? ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_atm_insert(etldate,enddate):
    db = DBConnect()
    info("lock table FARM_MON_LIVING")
    #db.cursor.execute(lock)
    db.cursor.execute("DELETE FROM T_BSMP_JRNL WHERE WORKDATE>=? and WORKDATE<=?",(etldate,enddate))
    db.conn.commit()
    db.closeDB()


def delete_qry_settlementmanager(etldate,enddate):
    db = DBConnect()
    info("lock table QRY_SETTLEMENTMANGER")
    #db.cursor.execute(lock)
    db.cursor.execute("DELETE FROM EBILLS_QRY_SETTLEMENT_MANAGER WHERE WORKDATE>=? and WORKDATE<=?",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_ebills_pa_quotePricearv(etldate,enddate):
    db = DBConnect()
    info("lock table ebills_pa_quotePricearv")
    #db.cursor.execute(lock)
    db.cursor.execute("DELETE FROM EBILLS_PA_QUOTEPRICEARV WHERE WORKDATE>=? and WORKDATE<=?",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def delete_accounthook(etldate,enddate,atype=None):
    raise Exception("not support ")
    db = DBConnect()
    info("lock table account_hook")
    db.cursor.execute("DELETE from ACCOUNT_HOOK where ETL_DATE>=? and ETL_DATE<=? and TYP=? and SRC='批量'",(etldate,enddate,atype))
    db.conn.commit()
    db.closeDB()
def delete_accounthook_by_id(hook_id):
    raise Exception("not support ")
    db = DBConnect()
    info("delete from ACCOUNT_HOOK with id = " + str(hook_id))
    db.cursor.execute("DELETE from ACCOUNT_HOOK where id = ?",(hook_id))
    db.conn.commit()
    db.closeDB()
def delete_accounthook_by_account_no(account_no):
    db = DBConnect()
    info("delete from ACCOUNT_HOOK with account_no = " + str(account_no))
    db.cursor.execute("DELETE from ACCOUNT_HOOK where ACCOUNT_NO = ?",(account_no))
    db.conn.commit()
    db.closeDB()

def delete_custhook_by_ebank_cb(cust_in_no):
    db = DBConnect()
    info("delete from cust_in_no_hook with cust_in_no= " + str(cust_in_no))
    db.cursor.execute("DELETE from CUST_HOOK where CUST_IN_NO= ? AND SUB_TYP='企业网上银行'",(cust_in_no))
    db.conn.commit()
    db.closeDB()


def delete_custhook(etldate,enddate,atype=None):
    db = DBConnect()
    info("lock table cust_hook")
    db.cursor.execute("DELETE from CUST_HOOK where ETL_DATE>=? and ETL_DATE<=? and TYP=? and SRC='批量'",(etldate,enddate,atype))
    db.conn.commit()
    db.closeDB()

def get_accounthook(atype):
    db = DBConnect()
    try:
        sql ="""
        SELECT ACCOUNT_NO, MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, NOTE,ID
        FROM YDW.ACCOUNT_HOOK
        where HOOK_TYPE='管户' and TYP= ? and status not in ('待手工','录入待审批') 
        """
        db.cursor.execute(sql, atype)
        row = db.cursor.fetchone()
        d = {}
        while row: 
            d[str(row[0])] = list(row)#账号不用关心机构
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()
def get_accounthook_pass(atype):
    db = DBConnect()
    try:
        sql ="""
        SELECT ACCOUNT_NO, MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, NOTE,ID, CUST_IN_NO
        FROM YDW.ACCOUNT_HOOK
        where TYP = ? 
        """
        db.cursor.execute(sql, atype)
        row = db.cursor.fetchone()
        d = {}
        while row: 
            d[str(row[0])] = list(row)#账号不用关心机构
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()

def get_custhook(atype):
    db = DBConnect()
    try:
        sql ="""
        SELECT CUST_IN_NO, MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, NOTE,CUST_NO,ID,BATCH_ID
        FROM YDW.CUST_HOOK
        where HOOK_TYPE='管户' and TYP= ? and status not in ('待手工','录入待审批') 
        """
        db.cursor.execute(sql,atype)
        row = db.cursor.fetchone()
        d = {}
        while row: 
            d[str(row[0]+row[2])] = list(row)
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()
def get_custhook_with_percentage(atype):
    db = DBConnect()
    try:
        sql ="""
        SELECT CUST_IN_NO, MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, NOTE,CUST_NO,ID,BATCH_ID
        FROM YDW.CUST_HOOK
        where TYP= ?
        """
        db.cursor.execute(sql,atype)
        row = db.cursor.fetchone()
        d = {}
        while row: 
            dd = {}
            dd[str(row[1])] = list(row)
            ckey = str(row[0]+row[2])
            if ckey in d:
                d[str(row[0]+row[2])] = d[str(row[0]+row[2])].append(dd)
            else:
                d[str(row[0]+row[2])] = list(dd)
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()

def get_custhook_ebank(atype):
    db = DBConnect()
    try:
        sql ="""
        SELECT CUST_IN_NO, MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, NOTE,CUST_NO,ID,BATCH_ID
        FROM YDW.CUST_HOOK
        where HOOK_TYPE='管户' and TYP= ? and status not in ('待手工','录入待审批') 
        """
        db.cursor.execute(sql,atype)
        row = db.cursor.fetchone()
        d = {}
        while row: 
            d[str(row[0])] = list(row)
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()

def get_ebank_org(sub_typ):
    db = DBConnect()
    try:
        sql ="""
        SELECT CUST_NET_NO
        FROM YDW.EBANK_ORG
        where TYP= '电子银行' and sub_typ = ?
        """
        db.cursor.execute(sql, sub_typ)
        row = db.cursor.fetchone()
        d = {}
        while row: 
            d[str(row[0])] = 1
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()


def get_CORE_BLFMCNAF_his(data):
    db = DBConnect()
    try:
        sql ="""
            select AFAAAC15,AFBKDATE,AFAABRNO,AFASAMT,AFBIIAM2,AFBVIAM2,AFBJIAM2,AFBWIAM2,AFBXIAM2 from F_CORE_BLFMCNAF where AFBKDATE< ? order by AFBKDATE desc
        """
        db.cursor.execute(sql,data)
        row = db.cursor.fetchone()
        d={}
        while row: 
            if str(row[0]) not in d:
                d[str(row[0])]=list(row)
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()  

def get_ebills_qry_settlement_manager_his(data):
    db = DBConnect()
    try:
        sql ="""
            select ORGNO,MANAGERID,nvl(EXLCAMT,0),nvl(EXBPAMT,0),nvl(EXAGENTAMT,0),nvl(EXCLEANAMT,0),nvl(EXINREMITAMT,0),nvl(IMLCAMT,0),nvl(IMICAMT,0),nvl(IMOUTREMTIAMT,0),nvl(NTINREMITAMT,0),nvl(NTOUTREMITAMT,0),nvl(NTCLEANAMT,0),nvl(FIINREMITAMT,0),nvl(FIOUTREMITAMT,0),nvl(CHARGEAMT,0),nvl(IMLGAMT,0) from EBILLS_QRY_SETTLEMENT_MANAGER where month= ? and workdate < ? order by workdate desc
        """
        db.cursor.execute(sql,(int(str(data)[:6]),int(str(data))))
        row = db.cursor.fetchone()
        d={}
        while row: 
            if str(row[0]+row[1]) not in d:
                d[str(row[0])+row[1]]=list(row)
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()  



def get_custhook_pass(atype):
    db = DBConnect()
    try:
        sql ="""
        SELECT CUST_IN_NO, MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, NOTE,CUST_NO,ID
        FROM YDW.CUST_HOOK
        where HOOK_TYPE='管户' and TYP= ? and status in ('待手工','录入待审批') 
        """
        db.cursor.execute(sql,atype)
        row = db.cursor.fetchone()
        d = {}
        while row: 
            d[str(row[0]+row[2])] = list(row)
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()

def get_ebankhook():
    db = DBConnect()
    try:
        sql ="""
        SELECT CUST_IN_NO, MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, NOTE,CUST_NO,ID,SUB_TYP,BATCH_ID
        FROM YDW.CUST_HOOK
        where HOOK_TYPE='管户' and TYP= '电子银行' and status<>'待手工' and status<>'待分配'
        """
        db.cursor.execute(sql)
        row = db.cursor.fetchone()
        d = {}
        while row: 
            if str(row[0]+row[2]) not in d:
                d[str(row[0]+row[2])] = [row[1]]        #内码+机构号
            #d[str(row[0]+row[2])].append(row[-1])
            d[str(row[0]+row[2])].append(row[7])
            d[str(row[0]+row[2])].append(row[-1])
            #if row[-1] == None:
            #    d[str(row[0]+row[2])].append(0)
            #else:
            #    d[str(row[0]+row[2])].append(row[-1])
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()

def get_ebankhook_typ():
    db = DBConnect()
    try:
        sql ="""
        SELECT CUST_IN_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, NOTE,CUST_NO,ID,SUB_TYP,BATCH_ID
        FROM YDW.CUST_HOOK
        where TYP= '电子银行'
        """
        db.cursor.execute(sql)
        row = db.cursor.fetchone()
        d = {}
        while row: 
            d[str(row[0]+row[1])]=1         #按照要求内码+机构
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()

"""
适用于通过net_no去重的
"""
def get_ebankhook_typ_by_net_no( sub_typ ):
    db = DBConnect()
    try:
        sql ="""
        SELECT CUST_NET_NO, ORG_NO
        FROM YDW.CUST_HOOK
        where TYP= '电子银行' and sub_typ = ?
        """
        db.cursor.execute(sql, sub_typ)
        row = db.cursor.fetchone()
        d = {}
        while row: 
            d[str(row[0])]=1         #适用于ETC、手机银行和网上银行去除
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()

def get_etchook():
    db = DBConnect()
    try:
        sql ="""
        SELECT CUST_IN_NO, MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, NOTE,CUST_NO,ID,SUB_TYP
        FROM YDW.CUST_HOOK
        where HOOK_TYPE='管户' and SUB_TYP= 'ETC' and status<>'待手工' 
        """
        db.cursor.execute(sql)
        row = db.cursor.fetchone()
        d = {}
        while row: 
            d[str(row[0])]=1
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()

def get_cust_in_no_by_net(para):
    db = DBConnect()
    try:
        sql ="""select CUST_IN_NO from D_CUST_NET_NO where CUST_NET_NO = ?"""
        db.cursor.execute(sql,para)
        row = db.cursor.fetchone()
        if row:
            return row[0]
        else:
            return 0
    finally:
        db.closeDB()

def get_cust_in_no(para):
    db = DBConnect()
    try:
        sql ="""select CUST_NO from D_CUST_INFO where CUST_LONG_NO = ?"""
        db.cursor.execute(sql,para)
        row = db.cursor.fetchone()
        if row:
            return row[0]
        else:
            return 0
    finally:
        db.closeDB()
def get_cust_in_no2(para):
    db = DBConnect()
    try:
        sql ="""select CUST_LONG_NO from D_CUST_INFO where CUST_NO = ?"""
        db.cursor.execute(sql,para)
        row = db.cursor.fetchone()
        if row:
            return row[0]
        else:
            return 0
    finally:
        db.closeDB()

def get_cust_in_no_by_creditcard_no(para):
    db = DBConnect()
    try:
        sql ="""select CST_NO from D_CREDIT_CARD where CARD_NO= ? """
        db.cursor.execute(sql,para)
        row = db.cursor.fetchone()
        if row:
            return row[0]
        else:
            return 0
    finally:
        db.closeDB()

def get_cust_in_no_by_debitcard_no(para):
    db = DBConnect()
    try:
        sql ="""select CST_NO from D_DEBIT_CARD where CARD_NO= ? """
        db.cursor.execute(sql,para)
        row = db.cursor.fetchone()
        if row:
            return row[0]
        else:
            return 0
    finally:
        db.closeDB()

def get_d_cust_info():
    db = DBConnect()
    try:
        sql ="""select CUST_NO,CUST_LONG_NO,CUST_ADDRESS,CUST_CREDIT_ADDRESS from D_CUST_INFO"""
        db.cursor.execute(sql)
        datadict={}
        row = db.cursor.fetchone()
        while row:
            datadict[row[0]]=row
            row = db.cursor.fetchone()
        return datadict
    finally:
        db.closeDB()

def get_d_cust_info2():
    db = DBConnect()
    try:
        sql ="""select CUST_LONG_NO,CUST_NO, CUST_ADDRESS,CUST_CREDIT_ADDRESS from D_CUST_INFO"""
        db.cursor.execute(sql)
        datadict={}
        row = db.cursor.fetchone()
        while row:
            datadict[row[0]]=row
            row = db.cursor.fetchone()
        return datadict
    finally:
        db.closeDB()

def get_cust_no(para):
    db = DBConnect()
    try:
        sql ="""select CUST_LONG_NO from D_CUST_INFO where CUST_NO = ?"""
        db.cursor.execute(sql,para)
        row = db.cursor.fetchone()
        if row:
            return row[0]
        else:
            return 0
    finally:
        db.closeDB()

def get_cust_no_by_idcard(para):
    db = DBConnect()
    try:
        sql ="""select CUST_NO from D_CUST_INFO where CUST_IDCARDNUM = ?"""
        db.cursor.execute(sql,para)
        row = db.cursor.fetchone()
        if row:
            return row[0]
        else:
            return 0
    finally:
        db.closeDB()

def get_cust_address(custno):
    db = DBConnect()
    try:
        sql ="""select CUST_ADDRESS,CUST_CREDIT_ADDRESS from D_CUST_INFO where CUST_NO = ?"""
        db.cursor.execute(sql,str(custno))
        row = db.cursor.fetchone()
        if row:
            return row
        else:    
            return ('无','无')
    finally:
        db.closeDB()
        
def get_next_seq_id(c,seqname):
    try:
        sqll="""select nextval for %s from sysibm.dual"""%seqname
        c.execute(sqll)
        return  c.fetchone()[0]
    finally:
        pass


def fix_seq_id(tabname,seqname):
    db = DBConnect()
    try:
        sql ="""select max(id) from %s"""%tabname
        db.cursor.execute(sql)
        maxid = db.cursor.fetchone()
        sqll="""select nextval for %s from sysibm.dual"""%seqname
        db.cursor.execute(sqll)
        idd = db.cursor.fetchone()
        while idd[0]<=maxid[0]:
            db.cursor.execute(sqll)
            idd = db.cursor.fetchone()    
    finally:
        db.closeDB()

def get_cust_info():
    db = DBConnect()
    try:
        sql ="""select CUST_NO,CUST_LONG_NO,CUST_ADDRESS,CUST_CREDIT_ADDRESS from D_CUST_INFO """
        db.cursor.execute(sql)
        row = db.cursor.fetchone()
        custdict={}
        while row:
            custdict[row[0]]=(row[1],row[2],row[3])
            row = db.cursor.fetchone()
        return custdict
    finally:
        db.closeDB()

def get_dep_account(etldate,orgcode):
    db = DBConnect()
    try:
        sql ="""
        select f.CST_NO,d.ACCOUNT_NO,c.CARD_NO,t.ACCOUNT_CLASS from F_BALANCE f
        join D_ACCOUNT d on f.ACCOUNT_ID=d.ID
        join D_ACCOUNT_TYPE t on f.ACCOUNT_TYPE_ID=t.ID
        join D_MANAGE m on f.MANAGE_ID=m.ID
        left join D_DEBIT_CARD c on d.ACCOUNT_NO=c.ACCOUNT_NO and c.CLOSE_DATE > ? and c.START_USING_DATE<= ?
        where f.DATE_ID = ? and f.ACCT_TYPE=1 and m.THIRD_BRANCH_CODE= ?
        """
        db.cursor.execute(sql,etldate,etldate,etldate,orgcode)
        row = db.cursor.fetchone()
        accountdict={}
        while row:
            if accountdict.get(row[0],None) is None:
                accountdict[row[0]]=[]
            accountdict[row[0]].append((row[1],row[2],row[3]))
            row = db.cursor.fetchone()
        return accountdict    
    finally:
        db.closeDB()

def get_cust_no_by_card_account_no():
    db = DBConnect()
    try:
        accountdict={}
        carddict={}
        sql ="""
        select CARD_NO,ACCOUNT_NO,CST_NO from D_DEBIT_CARD 
        """
        db.cursor.execute(sql)
        row = db.cursor.fetchone()
        while row:
            carddict[row[0]]=(row[1],row[2])
            row = db.cursor.fetchone()
        sql ="""
        select ACCOUNT_NO,CARD_NO,CST_NO from D_ACCOUNT 
        """
        db.cursor.execute(sql)
        row = db.cursor.fetchone()
        while row:
            accountdict[row[0]]=(row[1],row[2])
            row = db.cursor.fetchone()
        return carddict,accountdict    
    finally:
        db.closeDB()

def get_fin_account(etldate,orgcode):
    db = DBConnect()
    try:
        sql ="""
        SELECT f.CST_NO,a.ACCOUNT_NO FROM F_BALANCE F                                  
        JOIN D_ACCOUNT A ON F.ACCOUNT_ID=A.ID                
        JOIN D_ORG O ON F.ORG_ID=O.ID
        WHERE F.DATE_ID = ? AND F.ACCT_TYPE=8 AND O.ORG0_CODE = ?
        """
        db.cursor.execute(sql,etldate,orgcode)
        row = db.cursor.fetchone()
        accountdict={}
        while row:
            if accountdict.get(row[0],None) is None:
                accountdict[row[0]]=[]
            accountdict[row[0]].append((row[1]))
            row = db.cursor.fetchone()
        return accountdict    
    finally:
        db.closeDB()
def get_staff_branch():
    db = DBConnect()
    try:
        sql ="""
        select USER_NAME,BRANCH_CODE,GROUP_NAME from F_USER f
        join USER_BRANCH ub on f.ROLE_ID=ub.USER_ID
        join BRANCH b on ub.BRANCH_ID=b.ROLE_ID
        join USER_GROUP ug on f.ROLE_ID=ug.USER_ID
        join "GROUP" g on g.ID=ug.GROUP_ID and g.GROUP_TYPE_CODE='2000'
        """
        db.cursor.execute(sql)
        row = db.cursor.fetchone()
        staffdict={}
        while row:
            staffdict[row[0]]=(row[1],row[2])
            row = db.cursor.fetchone()
        return staffdict    
    finally:
        db.closeDB()
def get_ebank_busi_type(orgcode,custno):
    db = DBConnect()
    try:
        sql ="""
        select distinct c.BUSI_TYPE from F_CONTRACT_STATUS f
        join D_CUST_CONTRACT c on f.CONTRACT_ID=c.ID
        where DATE_ID=20160630 and c.OPEN_BRANCH_NO= ? and c.CST_NO= ?
        """
        db.cursor.execute(sql,orgcode,custno)
        row = db.cursor.fetchall()
        return row    
    finally:
        db.closeDB()
def get_open_org(acctno):
    db = DBConnect()
    try:
        if acctno[0:2]=='62':
            sql ="""select OPEN_BRANCH_CODE from D_DEBIT_CARD c
            join D_ACCOUNT a on c.ACCOUNT_NO=a.ACCOUNT_NO where CARD_NO = ?"""
            db.cursor.execute(sql,acctno)
            row = db.cursor.fetchone()
        else:
            sql ="""select OPEN_BRANCH_CODE from D_ACCOUNT where ACCOUNT_NO = ?"""
            db.cursor.execute(sql,acctno)
            row = db.cursor.fetchone()
        if row:
            return row[0]
        else:
            return 0
    finally:
        db.closeDB()

def get_daily(date):
    db = DBConnect()
    try:
        sql ="""
            select f.CST_NO,o.ORG0_CODE,sum(f.YEAR_PDT) /d.BEG_YEAR_DAYS,sum(f.BALANCE) from F_BALANCE f                       
            join D_ORG o on f.ORG_ID=o.ID                                   
            join D_DATE d on f.DATE_ID=d.ID
            where f.DATE_ID = ?  and f.ACCT_TYPE=1                           
            group by d.BEG_YEAR_DAYS,f.CST_NO,o.ORG0_CODE
        """
        db.cursor.execute(sql,date)#
        row = db.cursor.fetchone()
        datadict={}
        while row:
            datadict[(row[0],row[1])]=(row[2],row[3])
            row = db.cursor.fetchone()
        return datadict    
    finally:
        db.closeDB()

def get_managerorg(etldate,salecode):
    db = DBConnect()
    try:
        sql ="""select SALE_ORG from D_SALES_TEMP where SALE_CODE = ?"""
        db.cursor.execute(sql,salecode)
        row = db.cursor.fetchone()
        if row:
            return row[0]
        else:
            return 0
    finally:
        db.closeDB()

def is_nullstr(val):
        if val is None or isinstance(val, unicode) or isinstance(val, str ):
                if val is None or len( val.strip() ) == 0 : return True
                return False
        else :
                return False


class NumTransform():
    @classmethod
    def valtransfor3(self, name, row, format):
        try:
            val = row.get(name) 
            val=NumTransform.valtransfor(name, val, format, row)
            return val
        except  Exception,e:
            print name,val,e

    @classmethod
    def valtransfor2(self,name,val,format):
        try:
            val=NumTransform.valtransfor(name,val,format)
            if val is not None : return val
        except  Exception,e:
            print name,val,e

    @classmethod
    def valtransfor(self,name,val,format, row=None):
        if format is None :
            if isinstance(val, unicode) or isinstance(val, str ):return val.strip()
            return val
        if format == "*7" :
            if is_nullstr(val) : return 0
            return int(Decimal(val)*10000000)
        elif format == "*2" :
            if is_nullstr(val) : return 0
            if isinstance(val, str) :
                return int(Decimal(val)*100)
            else:
                return int(val*100)
        elif format == "int" :
            if is_nullstr(val) : return 0
            return int(Decimal(val))
        elif format == "YYYYMMDD" or format == "YYYYMMDDHHMMSS":
            if is_nullstr(val) : return 0
            if val!=None:
                if isinstance(val, float ):
                    return int(val)
                if isinstance(val, str ) and len(val)==0:
                    return 0
                if isinstance(val, int ) :
                    return  val
                if format == "YYYYMMDDHHMMSS":
                    return str(Decimal(val.replace("-","").strip().replace(".","").replace(":","").replace(" ","")))
                return int(Decimal(val.replace("-","").strip()))
            
            else:
                return 0
        else:
            if type(format) == types.FunctionType:
                val = format(name, val, row)
            elif str(type(format)) == "<type 'instancemethod'>":
                val = format(name, val, row)
        if isinstance(val, unicode) or isinstance(val, str ) :
            return val.strip()
        else:
            return val

class DimConnect(DBConnect):
    def __init__(self,table,cols=None,keylist=None,dim_type=None,sequence_name =None):
        DBConnect.__init__(self)
        self.maxid=0;
        self.table=table
        self.keylist = keylist
        self.cols=cols
        self.table=table
        self.dim_type=dim_type
        self.sequence_name=sequence_name
        self.cursor.execute("select * from %s where 1!=1  "%(table) ) 
        self.desc=self.cursor.description
        self.header=[ r[0] for r in self.desc ]#获得其他维表的字段名
        self.load_dim()
        self.queue=None
        self.xc = None 
    def __dbrowtokey__(self,row):
        #如果没指定要组装成key的字段则其他维表中除了id的字段全部组装成key
        idx=0
        key=None
        for c in self.desc:
            if self.cols is not None and c[0] not in self.cols:  continue 
            if self.keylist is not None and c[0] not in self.keylist:  continue 
            if c[0] == "ID" :  continue  
            val = row.get( c[0] )
            if val is None :
                val = get_default_nullval( c )
            if isinstance(val, unicode) :
                val=val.strip()
            elif isinstance(val, str) : 
                val=val.strip()
            else :
                val=str(val)
            if key is None : 
                key = val 
            else:
                key=key+"|"+val
        return key
        
    def load_dim(self):
        sql="select * from %s"%(self.table)
        if self.dim_type is not None :
            w = ' WHERE 1=1 '
            for k in self.dim_type :
                #w = w + k  + " and '" + self.dim_type[k] + "' "
                w = w   + " and "+k+" ='" + self.dim_type[k] + "' "
            sql = sql + w 
        d={}
        self.cursor.execute(sql)  
        row = self.cursor.fetchone() #得到维表的字段值的一行
        rg=range(len(self.desc))
        while row: 
            r={}            
            for i in rg :
                k = self.desc[i][0]
                r[ k ] = row[i]
            id = r["ID"]
            key=self.__dbrowtokey__( r )
            d[key]=id#将key和id的值形成字典
            if id > self.maxid : self.maxid=id #得到最大的id值
            row = self.cursor.fetchone() 
        self.dims=d
            
    def find_dim_id(self,row):
        rowkey = self.__dbrowtokey__(row)#得到rowkey
        fid=self.dims.get(rowkey) #得到key所在的id
        if self.table == 'D_CUST_CONTRACT':
            #print "find_dim_id,",rowkey,fid
            pass
        if fid is not None : return fid
        if self.sequence_name is not None :
            fid = get_next_seq_id(self.cursor,self.sequence_name)
        else : 
            fid=self.maxid+1
        self.maxid=fid#更新maxid
        self.dims[rowkey]=fid#更新i
        #hd = self.header if self.cols is None else self.cols
        row["ID"]=fid
        #qdata=('I',hd,row,self.table)
        qdata=('I',self.desc,row,self.table)
        self.put_data(qdata)
        return fid
    def just_find_dim_id(self,row):
        rowkey = self.__dbrowtokey__(row)#得到rowkey
        fid=self.dims.get(rowkey,None) #得到key所在的id
        return fid
            
    def put_data(self,data) :
        if self.queue is None :
            pass
            #print "### queue is none### ",data
        else :
            self.queue.put(data)
    def find_id(self,k):
        return self.dims.get(k)
    def putkey(self,key,id):
        self.dims[key]=id        
    def finish(self):
        #如果有sequence，则不关闭数据库
        if self.sequence_name is None :
            self.closeDB()            

class BaseDim():
    def __init__(self):
        pass
    def setQueue(self,queue):
        self.dim.queue=queue        
    def finish(self):
        pass
    def find_dim_id(self,key):
        return self.dim.find_dim_id(key)

def get_table_desc(table,db1=None):
    if db1 is None :
        db = DBConnect()
    else:
        db = db1
    sql = "select * from %s where 1!=1  "%(table)
    db.cursor.execute(sql)
    account_desc=db.cursor.description    
    if db1 is None : db.closeDB()
    return account_desc

def year_begin(etldate):
    s=str(etldate)
    return s[0:4]+"0101"

def year_days(etldate):
    s=str(etldate)
    d1=datetime(int(s[0:4]),int(s[4:6]),int(s[6:8])) - datetime(int(s[0:4]),1,1)
    return  d1.days + 1
def date_diff_days(d1,d2):
    s=str(d1)
    s2=str(d2)
    d=datetime(int(s2[0:4]),int(s2[4:6]),int(s2[6:8])) - datetime(int(s[0:4]),int(s[4:6]),int(s[6:8])) 
    return  d.days + 1
def get_etl_date(etldate):
    ld=daycalc(etldate,-1)
    lds=tostrdate(ld)
    tds=tostrdate(etldate)
    s = str(etldate)
    yb = s[0:4]+"0101"  
    ye = s[0:4]+"1231"
    yr=str(int(s[0:4]) - 1)
    syb = yr + "0101"  
    sym = yr + "1231"  
    jnts = date_diff_days(yb,ye)

    data = {}
    data['DATE'] = int(etldate)
    data['YB'] = int(yb)
    data['YE'] = int(ye)
    data['LYB'] = int(syb)
    data['LYE'] = int(sym)
    return  data

#[creditcard.py]中获取该卡客户号
def get_card_cust_in_no(idcardnum):
    db = DBConnect()
    try:
        sql ="""select CST_NO from D_CREDIT_CARD where ACCOUNT_NO=?"""
        db.cursor.execute(sql,idcardnum)
        row = db.cursor.fetchone()
        if row:
            return row[0]
        else:
            return 0
    finally:
        db.closeDB()

#[creditcard.py]中获取该卡帐号
def get_card_account_no(idcardnum):
    db = DBConnect()
    try:
        sql ="""select CARD_NO from D_CREDIT_CARD where ACCOUNT_NO=?"""
        db.cursor.execute(sql,idcardnum)
        row = db.cursor.fetchone()
        if row:
            return row[0]
        else:
            return 0
    finally:
        db.closeDB()

def delete_fcacctjrnl(etldate,enddate):
    db = DBConnect()
    info("lock table F_C_ACCTJRNL")
    #db.cursor.execute(lock)
    db.cursor.execute("DELETE from F_T_LOAN_JRNL where date_id>=? and date_id<=? ",(etldate,enddate))
    db.conn.commit()
    db.closeDB()

def update_account_hook_new_cust_in_no(new_cust_in_no, old_cust_in_no):
    db = DBConnect()
    db.cursor.execute("UPDATE YDW.ACCOUNT_HOOK SET CUST_IN_NO = ? WHERE CUST_IN_NO = ? ",(new_cust_in_no, old_cust_in_no))
    db.conn.commit()
    db.closeDB()

def get_branch_typ():
    db = DBConnect()
    try:
        sql ="""
            select b.BRANCH_CODE, b.BRANCH_NAME, count(*) from branch b
            join branch c on b.PARENT_ID = c.PARENT_ID
            where b.BRANCH_CODE != '966000' and b.BRANCH_LEVEL != '支行'
            group by b.BRANCH_CODE, b.BRANCH_NAME
        """
        db.cursor.execute(sql)
        row = db.cursor.fetchone()
        d = {}
        while row: 
            d[str(row[0])] =  int(row[2])        #机构号,所在网点数量
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()

def get_parent_hook():
    db = DBConnect()
    try:
        sql ="""
        SELECT 
            CUST_IN_NO, MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, END_DATE, STATUS, SRC, TYP, NOTE
            ,ACCOUNT_NO
        FROM 
            YDW.PARENT_HOOK
        where 
            TYP = '汇集户' and STATUS in ('正常')
        """
        db.cursor.execute(sql,)
        row = db.cursor.fetchone()
        d = []
        while row: 
            #d[str(row[1])] = list(row)
            nr = [str(row[1]),str(row[3]),row]
            key = row[10].strip()
            nrs = d.get(key)
            if nrs is None:
                nrs = []
            nrs.append( nr )
            d[ key ]  = nrs
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()

def deal_parent_acct(account_no,org_no,etldate):
    db = DBConnect()
    db.cursor.execute("UPDATE PARENT_HOOK SET STATUS = '失效', END_DATE = ?, ETLDATE = ? WHERE ACCOUNT_NO = ? AND ORG_NO != ? AND STATUS = '正常' AND ETL_DATE < ?",(etldate,etldate,account_no,org_no,etldate))
    db.conn.commit()
    db.closeDB()
