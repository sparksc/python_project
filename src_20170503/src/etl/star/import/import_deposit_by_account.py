# -*- coding:utf-8 -*- 
from nose.tools import eq_, raises, assert_true
from sqlalchemy.orm import aliased
import unittest
import time,os,random,sys
import DB2
from decimal import Decimal

import etl.base.util as util
import etl.star.update.update_hook_balance as uhb
import xlrd

from openpyxl import Workbook,load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter
from openpyxl.styles import colors
from openpyxl.styles import Font,Color
import datetime

def run_import(filename,org_no=None,subtype=None):
    #if subtype==None:subtype=hooktype
    data = xlrd.open_workbook(filename)
    filename='账号'
    print filename
    sheet = data.sheet_by_index(0)
    nrows = sheet.nrows
    cust_sql="""
    INSERT INTO YDW.CUST_HOOK(CUST_NO,CUST_IN_NO,MANAGER_NO,ORG_NO,PERCENTAGE,HOOK_TYPE,START_DATE,END_DATE,STATUS,ETL_DATE,SRC,TYP,SUB_TYP,NOTE) 
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    account_sql="""
    INSERT INTO YDW.ACCOUNT_HOOK(ACCOUNT_NO,CARD_NO,MANAGER_NO,ORG_NO,PERCENTAGE,HOOK_TYPE,START_DATE,END_DATE,STATUS,ETL_DATE,SRC,TYP,SUB_TYP,NOTE,FOLLOW_CUST,CUST_IN_NO) 
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    del_account_sql="""
    delete from ACCOUNT_HOOK where ACCOUNT_NO=?
    """
    account_hishook=util.get_accounthook('存款')
    print len(account_hishook)
    rc=[]
    ra=[]
    rd=[]
    indexdict={
        '账号':['account',1,3,0,5,-1],
    }
    custdict=util.get_cust_info()
    staffdict=util.get_staff_branch()
    carddict,accountdict=util.get_cust_no_by_card_account_no()
    for r in range(1,nrows):
        #print r
        row = sheet.row_values(r)
        ACCOUNT_NO=str(row[indexdict[filename][1]]).strip()
        MANAGER_NO=    row[indexdict[filename][2]]
        ORG_NO    =    row[indexdict[filename][3]]
        #print CUST_IN_NO,MANAGER_NO,ORG_NO
        if MANAGER_NO=='' or ORG_NO=='':
            print row
            continue    
        ACCOUNT_NO=str(int(ACCOUNT_NO)).strip()
        MANAGER_NO=str(int(MANAGER_NO)).strip()
        ORG_NO    =str(int(ORG_NO    )).strip()
        if MANAGER_NO[0:3]!='966' or len(ORG_NO)!=6 or ORG_NO[0:3]!='966':
            print MANAGER_NO,ORG_NO,'~~~~~~~~' 
            continue
        staffinfo=staffdict.get(MANAGER_NO)   
        if staffinfo is None:
            print MANAGER_NO,'!!!!!!'
            continue
        if staffinfo[1]=='非客户经理' and staffinfo[0][:-1]!=ORG_NO[:-1]:
            print ORG_NO,staffdict.get(MANAGER_NO)
            print '!!!!!',row
            continue
        if staffinfo[1]=='客户经理' and staffinfo[0]!=ORG_NO:
            print ORG_NO,staffdict.get(MANAGER_NO)
            print '!!!!!',row
            continue
        HOOK_TYPE='管户'
        PERCENTAGE=int(float(row[indexdict[filename][4]]))
        START_DATE=20150101
        END_DATE  =20991231
        STATUS='正常'
        ETL_DATE=20160630
        SRC='存量导入'
        TYP='存款'
        SUB_TYP='存款'
        NOTE='核心地址为:暂无'+'信贷地址为:暂无'
        FOLLOW_CUST='账号优先'
        if ACCOUNT_NO in accountdict:
            CARD_NO=accountdict.get(ACCOUNT_NO)[0]
            CUST_IN_NO=accountdict.get(ACCOUNT_NO)[1]
        if ACCOUNT_NO in carddict:
            CARD_NO=ACCOUNT_NO
            ACCOUNT_NO=carddict.get(CARD_NO)[0]
            CUST_IN_NO=carddict.get(CARD_NO)[1]
        info=custdict.get(CUST_IN_NO,('0','核心地址为:暂无','信贷地址为:暂无'))
        if info[0]=='0':
            NOTE='地址暂无'
        if info[2] is None:
            NOTE='核心地址为:'+str(info[1])
        else:    
            NOTE='信贷地址为:'+str(info[2])
        rd.append(ACCOUNT_NO)
        ra.append((ACCOUNT_NO,CARD_NO,MANAGER_NO,ORG_NO,PERCENTAGE,HOOK_TYPE,START_DATE,END_DATE,STATUS,ETL_DATE,SRC,TYP,SUB_TYP,NOTE,FOLLOW_CUST,CUST_IN_NO))
    insert_to_hook(del_account_sql,rd)    
    insert_to_hook(account_sql,ra)    
    print len(rd),len(ra)
        
def delete_hook(del_sql,hook_id):
    try :
        db = util.DBConnect()
        db.cursor.execute(del_sql,hook_id)
        db.conn.commit()
    finally :
        db.closeDB()

def insert_to_hook(insert_sql,listdata):
    try :
        db = util.DBConnect()
        db.cursor.executemany(insert_sql,listdata)
        db.conn.commit()
    finally :
        db.closeDB()


if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen==2:
        filename=sys.argv[1]
        print filename
        print "begin:", str(datetime.datetime.now())
        run_import(filename)
        uhb.del_dup()
        print "end:", str(datetime.datetime.now())
    elif arglen==3:
        filename=sys.argv[1]
        hooktype=sys.argv[2]
        print filename,hooktype
        print "begin:", str(datetime.datetime.now())
        run_import(filename,hooktype)
        print "end:", str(datetime.datetime.now())
    else:
        print "please input python import_hook.py [filename] [hooktype]"
