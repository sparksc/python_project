# -*- coding:utf-8 -*- 
from nose.tools import eq_, raises, assert_true
from sqlalchemy.orm import aliased
import unittest
import time,os,random,sys
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
    print filename    
    data = xlrd.open_workbook(filename)
    typ = ""
    if '委托银商' in filename:
        typ = '委托银商'
        sheet = data.sheet_by_index(0)
    elif '助农' in filename:
        typ = '助农'
        sheet = data.sheet_by_index(0)
    elif '自签传统' in filename:
        typ = '自签传统'
        sheet = data.sheet_by_index(0)
    elif '信付通' in filename:
        typ='信付通'
        sheet = data.sheet_by_index(0)
    elif '行内' in filename:
        typ='行内'
        sheet = data.sheet_by_index(0)
    else:
        raise Exception(u'error')

    print filename    
    nrows = sheet.nrows
    cust_sql="""
    INSERT INTO YDW.D_POS(org_no,merchant_name,merchant_no, pos_no, merchant_addr, merchant_contract, merchant_tel, merchant_mob, install_date, typ, status) 
    VALUES(?,?,?,?,?,?,?,?,?,?,?)
    """

    del_sql="""
    DELETE FROM YDW.D_POS WHERE typ = ? 
    """

    delete_hook(del_sql,typ)

    rc=[]
    for r in range(1,nrows):
        row = sheet.row_values(r)

        org_no = str(row[10]).strip()
        merchant_name = str(row[0].strip().encode('UTF-8'))
        merchant_no = str(row[1].strip().encode('UTF-8'))
        pos_no = str(row[2]).encode('UTF-8')
        merchant_addr = str(row[3].strip().encode('UTF-8'))
        merchant_contract = str(row[4].strip().encode('UTF-8'))
        if type(row[5])==type(1.0):
            merchant_tel = str(int(row[5]))
        else:    
            merchant_tel = str(row[5].encode('UTF-8'))
        if type(row[6])==type(1.0):
            merchant_mob = str(int(row[6])).encode('UTF-8')
        else:    
            merchant_mob = str(row[6].encode('UTF-8'))
        if type(row[9])==type(1.0):
            install_date = str(int(row[9]))
        else:    
            install_date = str(row[9])

        if org_no == '':
            print org_no, row
            continue    

        ORG_NO = str(int(org_no)).strip().encode('UTF-8')
        rc.append((ORG_NO, merchant_name,merchant_no, pos_no, merchant_addr, merchant_contract, merchant_tel, merchant_mob,install_date,typ,'正常'))
        print rc
        insert_to_hook(cust_sql,rc)
        rc=[]
    print typ
    print len(rc)
        
def delete_hook(del_sql,typ):
    try :
        db = util.DBConnect()
        db.cursor.execute(del_sql,typ)
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
        run_import(filename)
    else:
        raise Exception("please input python import_pos_info.py [filename]")
