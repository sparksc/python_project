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
    filename='信用卡'
    print filename    
    sheet = data.sheet_by_index(0)
    nrows = sheet.nrows
    account_sql="""
    INSERT INTO YDW.ACCOUNT_HOOK(ACCOUNT_NO,CARD_NO,MANAGER_NO,ORG_NO,PERCENTAGE,HOOK_TYPE,START_DATE,END_DATE,STATUS,ETL_DATE,SRC,TYP,SUB_TYP,NOTE,FOLLOW_CUST,CUST_IN_NO) 
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    del_account_sql="""
    DELETE FROM YDW.ACCOUNT_HOOK WHERE ACCOUNT_NO = ?
    """
    account_hishook=util.get_accounthook('信用卡')
    print len(account_hishook)
    ra=[]
    ru=[]
    rd=[]
    indexdict={
        '信用卡':['account',2,14,11,0],
    }
    custdict=util.get_cust_info()
    staffdict=util.get_staff_branch()
    for r in range(1,nrows):
        #print r
        row = sheet.row_values(r)
        CUST_IN_NO=str(row[indexdict[filename][1]]).strip()
        MANAGER_NO=row[indexdict[filename][2]]
        ORG_NO    =str(int(row[indexdict[filename][3]]))
        ACCOUNT_NO=str(row[indexdict[filename][4]]).strip()
        #print CUST_IN_NO,MANAGER_NO,ORG_NO
        if MANAGER_NO=='' or ORG_NO=='':
            #print row
            continue    
        CUST_IN_NO=str(int(float(CUST_IN_NO))).strip()
        MANAGER_NO=str(int(MANAGER_NO)).strip()
        ORG_NO    =str(int(ORG_NO    )).strip()
        if MANAGER_NO[0:3]!='966' or len(ORG_NO)!=6 or ORG_NO[0:3]!='966':
            print MANAGER_NO,ORG_NO,'~~~~~~~' 
            continue
        if len(MANAGER_NO)==6:
            print row
            continue
        staffinfo=staffdict.get(MANAGER_NO)   
        if staffinfo[1]=='非客户经理' and staffinfo[0][:-1]!=ORG_NO[:-1]:
            print ORG_NO,staffdict.get(MANAGER_NO)
            print '!!!!!',row
            continue
        if staffinfo[1]=='客户经理' and staffinfo[0]!=ORG_NO:
            print ORG_NO,staffdict.get(MANAGER_NO)
            print '!!!!!',row
            continue
        rd.append(ACCOUNT_NO)
        HOOK_TYPE='管户'
        PERCENTAGE=100    
        START_DATE=20150101
        END_DATE=20991231
        STATUS='正常'
        ETL_DATE=20160630
        SRC='存量导入'
        TYP='信用卡'
        SUB_TYP='信用卡'
        info=custdict.get(CUST_IN_NO,('0','核心地址为:暂无','信贷地址为:暂无'))
        if info[0]=='0':
            NOTE='地址暂无'
        if info[2] is None:
            NOTE='核心地址为:'+str(info[1])
        else:    
            NOTE='信贷地址为:'+str(info[2])
        FOLLOW_CUST='账号优先'
        CARD_NO=ACCOUNT_NO
        ra.append((ACCOUNT_NO,CARD_NO,MANAGER_NO,ORG_NO,PERCENTAGE,HOOK_TYPE,START_DATE,END_DATE,STATUS,ETL_DATE,SRC,TYP,SUB_TYP,NOTE,FOLLOW_CUST,CUST_IN_NO))
    print len(rd), str(datetime.datetime.now())
    insert_to_hook(del_account_sql,rd)    
    print len(ra), str(datetime.datetime.now())
    insert_to_hook(account_sql,ra)    
        
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
        filelist=[x for x in os.listdir(filename) if os.path.splitext(x)[1].find('xls')]
        print "begin:", str(datetime.datetime.now())
        for filepath in filelist:
            if 'svn' in filepath:continue
            print filepath
            run_import(filename+filepath)
        uhb.del_dup()
        print "end:", str(datetime.datetime.now())
    elif arglen==3:
        filename=sys.argv[1]
        orgcode=sys.argv[2]
        print filename,orgcode
        print "begin:", str(datetime.datetime.now())
        run_import(filename,orgcode)
        print "end:", str(datetime.datetime.now())
    else:
        print "please input python import_hook.py [filename] [hooktype]"
