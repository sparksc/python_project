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
    if '委托银商' in filename:
        filename='委托银商'
        sheet = data.sheet_by_index(0)
    elif '助农' in filename:
        filename='助农'
        sheet = data.sheet_by_index(0)
    elif '自签传统' in filename:
        filename='自签传统'
        sheet = data.sheet_by_index(0)
    elif '信付通' in filename:
        filename='信付通'
        sheet = data.sheet_by_index(0)
    elif '行内' in filename:
        filename='行内'
        sheet = data.sheet_by_index(0)
    print filename    
    cust_sql="""
    INSERT INTO YDW.CUST_HOOK(CUST_NO,CUST_IN_NO,MANAGER_NO,ORG_NO,PERCENTAGE,HOOK_TYPE,START_DATE,END_DATE,STATUS,ETL_DATE,SRC,TYP,SUB_TYP,NOTE) 
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    del_cust_sql="""
    DELETE FROM YDW.CUST_HOOK WHERE ID = ?
    """
    cust_hishook=util.get_custhook('POS')
    print len(cust_hishook)
    rc=[]
    ra=[]
    indexdict={
        '委托银商':['cust',1,11,10,3,2],
        '自签传统':['cust',1,11,10,3,2],
        '助农':    ['cust',1,11,10,3,2],
        '行内':    ['cust',1,11,10,3,2],
        '信付通':  ['cust',1,11,10,3,2],
    }
    custdict=util.get_cust_info()
    #accountdict=util.get_dep_account(20160630,org_no)
    #if accountdict.get('81000000000'):accountdict.pop('81000000000')
    accountdictlist={}
    staffdict=util.get_staff_branch()
    nrows = sheet.nrows
    for r in range(1,nrows):
        #print r
        row = sheet.row_values(r)
        CUST_IN_NO=    row[indexdict[filename][1]]
        MANAGER_NO=    str(row[indexdict[filename][2]]).strip()
        ORG_NO    =    str(row[indexdict[filename][3]]).strip()
        #print CUST_IN_NO,MANAGER_NO,ORG_NO
        if MANAGER_NO=='' or ORG_NO=='':
            #print row
            continue    
        CUST_IN_NO=str(int(float(CUST_IN_NO))).strip()
        MANAGER_NO=str(int(float(MANAGER_NO))).strip()
        ORG_NO    =str(int(float(ORG_NO    ))).strip()
        if MANAGER_NO[0:3]!='966' or len(ORG_NO)!=6 or ORG_NO[0:3]!='966' or len(MANAGER_NO)!=7:
            print MANAGER_NO,ORG_NO,'~~~~~~~~~~~~~' 
            continue
        staffinfo=staffdict.get(MANAGER_NO,None)   
        if staffinfo is None:
            print MANAGER_NO,'!!!!!!!!!!!!!!'
            continue
        if staffinfo[1]=='非客户经理' and staffinfo[0][:-1]!=ORG_NO[:-1]:
            print ORG_NO,staffdict.get(MANAGER_NO)
            print '!!!!!',row
            continue
        if staffinfo[1]=='客户经理' and staffinfo[0]!=ORG_NO:
            print ORG_NO,staffdict.get(MANAGER_NO)
            print '!!!!!',row
            continue
        CUST_NO=CUST_IN_NO
        CUST_IN_NO=str(row[indexdict[filename][-1]]).strip()
        #print CUST_IN_NO
        chh=cust_hishook.get(CUST_IN_NO+ORG_NO)    
        if chh:
            delete_hook(del_cust_sql,int(cust_hishook.get(CUST_IN_NO+ORG_NO)[-1]))
        HOOK_TYPE='管户'
        START_DATE=20150101
        END_DATE=20991231
        STATUS='正常'
        ETL_DATE=20160630
        SRC='存量导入'
        TYP='POS'
        SUB_TYP=filename
        NOTE=str(row[indexdict[filename][4]].encode('UTF-8'))
        PERCENTAGE=100
        rc.append((CUST_NO,CUST_IN_NO,MANAGER_NO,ORG_NO,PERCENTAGE,HOOK_TYPE,START_DATE,END_DATE,STATUS,ETL_DATE,SRC,TYP,SUB_TYP,NOTE))
    insert_to_hook(cust_sql,rc)    
    print len(rc)
        
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
            if 'POS' in filepath:
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
