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
    if '核销' in filename:
        filename='核销'
    else:
        filename='贷款'
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
    u_sql="""
    update F_BALANCE set ORG_ID=(select ID from D_ORG where ORG0_CODE= ? ) where ACCOUNT_ID=(select ID from D_LOAN_ACCOUNT where ACCOUNT_NO= ? ) and DATE_ID=20160630
    """
    del_cust_sql="""
    delete from CUST_HOOK where TYP in ('贷款','存款') and ORG_NO= ? and CUST_IN_NO=?
    """
    del_account_sql="""
    delete from ACCOUNT_HOOK where ACCOUNT_NO=?
    """
    rc=[]
    ra=[]
    ru=[]
    rcd=[]
    rad=[]
    indexdict={
        '贷款':['cust',1,12,6,-1,-1,40],
        '核销':['cust',1,38,37,5,-1,0],
    }
    custdict=util.get_cust_info()
    accountdictlist={}
    staffdict=util.get_staff_branch()
    for r in range(1,nrows):
        row = sheet.row_values(r)
        CUST_IN_NO=str(row[indexdict[filename][1]])
        MANAGER_NO=    row[indexdict[filename][2]]
        ORG_NO    =    row[indexdict[filename][3]]
        if MANAGER_NO=='' or ORG_NO=='':
            print row
            continue    
        CUST_IN_NO=str(int(float(CUST_IN_NO)))
        MANAGER_NO=str(int(MANAGER_NO)).strip()
        ORG_NO    =str(int(ORG_NO    )).strip()
        if MANAGER_NO[0:3]!='966' or len(ORG_NO)!=6 or ORG_NO[0:3]!='966' or len(MANAGER_NO)!=7:
            print row
            continue
        #print CUST_IN_NO,MANAGER_NO,ORG_NO
        staffinfo=staffdict.get(MANAGER_NO)   
        if staffinfo[1]=='非客户经理' and staffinfo[0][:-1]!=ORG_NO[:-1]:
            print ORG_NO,staffdict.get(MANAGER_NO)
            print '!!!!!',row
            continue
        if staffinfo[1]=='客户经理' and staffinfo[0]!=ORG_NO:
            print ORG_NO,staffdict.get(MANAGER_NO)
            print '!!!!!',row
            continue
        PERCENTAGE=100    
        HOOK_TYPE='管户'
        START_DATE=20150101
        END_DATE=20991231
        STATUS='正常'
        ETL_DATE=20160630
        SRC='存量导入'
        TYP='贷款'
        SUB_TYP='贷款'
        info=custdict.get(CUST_IN_NO,('0','核心地址为:暂无','信贷地址为:暂无'))
        CUST_NO=info[0]
        if CUST_NO=='0':CUST_NO=str(row[2].strip())
        if info[0]=='0':
            NOTE='地址暂无'
        if info[2] is None:
            NOTE='核心地址为:'+str(info[1])
        else:    
            NOTE='信贷地址为:'+str(info[2])
        if ORG_NO not in accountdictlist:
            print ORG_NO
            accountdictlist[ORG_NO]=util.get_dep_account(20160630,ORG_NO)
            if accountdictlist[ORG_NO].get('81000000000'):
                accountdictlist[ORG_NO].pop('81000000000')
        accountlist=accountdictlist[ORG_NO].get(CUST_IN_NO,[])
        rcd.append((ORG_NO,CUST_IN_NO))
        if filename=='核销':
            #print len(row),indexdict[filename][-1]
            ORG_NO1=str(int(row[indexdict[filename][-1]])).strip()
            if ORG_NO!=ORG_NO1:
                print ORG_NO1,ORG_NO,str(row[indexdict[filename][4]]),r
                #ORG_NO=ORG_NO1
                ru.append((ORG_NO,str(row[indexdict[filename][4]]).strip()))
                if ORG_NO not in accountdictlist:
                    print ORG_NO
                    accountdictlist[ORG_NO]=util.get_dep_account(20160630,ORG_NO)
                    if accountdictlist[ORG_NO].get('81000000000'):
                        accountdictlist[ORG_NO].pop('81000000000')
                accountlist=accountdictlist[ORG_NO].get(CUST_IN_NO,[])
        rc.append((CUST_NO,CUST_IN_NO,MANAGER_NO,ORG_NO,PERCENTAGE,HOOK_TYPE,START_DATE,END_DATE,STATUS,ETL_DATE,SRC,TYP,SUB_TYP,NOTE))
        TYP=SUB_TYP='存款'
        rc.append((CUST_NO,CUST_IN_NO,MANAGER_NO,ORG_NO,PERCENTAGE,HOOK_TYPE,START_DATE,END_DATE,STATUS,ETL_DATE,SRC,TYP,SUB_TYP,NOTE))
        for i in accountlist:
            ACCOUNT_NO = i[0]
            CARD_NO    = i[1]
            if CARD_NO is None:CARD_NO=ACCOUNT_NO
            SUB_TYP    = i[2]
            FOLLOW_CUST='客户号优先'
            rad.append(ACCOUNT_NO)
            ra.append((ACCOUNT_NO,CARD_NO,MANAGER_NO,ORG_NO,PERCENTAGE,HOOK_TYPE,START_DATE,END_DATE,STATUS,ETL_DATE,SRC,TYP,SUB_TYP,NOTE,FOLLOW_CUST,CUST_IN_NO))
        #print rs[-1]    
    insert_to_hook(del_cust_sql,rcd)
    insert_to_hook(del_account_sql,rad)
    insert_to_hook(u_sql,ru)
    insert_to_hook(cust_sql,rc)    
    insert_to_hook(account_sql,ra)    
    print len(rcd),len(rad),len(rc),len(ra),len(ru)
        
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
    #elif arglen==4:
        #filename=sys.argv[1]
        #hooktype=sys.argv[2]
        #subtype=sys.argv[3]
        #print filename,hooktype,subtype
        #print "begin:", str(datetime.datetime.now())
        #run_import(filename,hooktype,subtype)
        #print "end:", str(datetime.datetime.now())
    else:
        print "please input python import_loan.py [filename] "
