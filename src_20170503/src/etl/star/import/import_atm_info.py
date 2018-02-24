# -*- coding:utf-8 -*- 
from nose.tools import eq_, raises, assert_true
from sqlalchemy.orm import aliased
import unittest
import time,os,random,sys
import DB2
from decimal import Decimal

import etl.base.util as util

import xlrd

from openpyxl import Workbook,load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter
from openpyxl.styles import colors
from openpyxl.styles import Font,Color
import datetime

def run_import(filename,org_no=None,subtype=None):
    data = xlrd.open_workbook(filename)
    if 'ATM' in filename:
        filename='ATM'
        sheet = data.sheet_by_index(1)
    else:
        raise Exception(u'error')

    print filename    
    nrows = sheet.nrows
    cust_sql="""
    INSERT INTO YDW.D_ATM(org_no,atm_no,typ,sub_typ,addr,status) 
    VALUES(?,?,?,?,?,?)
    """

    del_sql="""
    DELETE FROM YDW.D_ATM WHERE typ in ('存取','取') 
    """

    #delete_hook(del_sql)

    rc=[]
    for r in range(1,nrows):
        row = sheet.row_values(r)
        ORG_NO = str(int(row[0])).strip()
        ATM_NO = str(row[2].strip().encode('UTF-8'))
        TYP = str(row[3].strip().encode('UTF-8'))
        SUB_TYP = str(row[4].strip().encode('UTF-8'))
        ADDR = str(row[5].strip().encode('UTF-8'))
        TO_ORG_NO = str(row[6]).strip()

        if TO_ORG_NO=='':
            #print ORG_NO, row
            continue    
        #print r,'---',len(ORG_NO),len(ATM_NO),len(TYP),len(SUB_TYP),len(ADDR)
        rc.append((ORG_NO, ATM_NO,TYP,SUB_TYP,ADDR,'正常'))
    insert_to_hook(cust_sql,rc)    
    print len(rc)
        
def delete_hook(del_sql):
    try :
        db = util.DBConnect()
        db.cursor.execute(del_sql)
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
        print "end:", str(datetime.datetime.now())
    else:
        raise Exception("please input python import_atm_info.py [filename]")
