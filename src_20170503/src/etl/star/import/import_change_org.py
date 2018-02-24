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
    #if subtype==None:subtype=hooktype
    data = xlrd.open_workbook(filename)
    sheet = data.sheet_by_index(0)
    nrows = sheet.nrows
    u_sql="""
    UPDATE F_BALANCE SET ORG_ID=22001 WHERE CST_NO= ? AND DATE_ID=20160630 AND ACCT_TYPE=4 AND ORG_ID=20212
    """
    rr=[]
    for r in range(1,nrows):
        row = sheet.row_values(r)
        #print str(row[0])
        rr.append(str(row[0]))
    update_org_id(u_sql,rr)
        
        
def update_org_id(insert_sql,listdata):
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
    elif arglen==3:
        filename=sys.argv[1]
        hooktype=sys.argv[2]
        print filename,hooktype
        print "begin:", str(datetime.datetime.now())
        run_import(filename,hooktype)
        print "end:", str(datetime.datetime.now())
    elif arglen==4:
        filename=sys.argv[1]
        hooktype=sys.argv[2]
        subtype=sys.argv[3]
        print filename,hooktype,subtype
        print "begin:", str(datetime.datetime.now())
        run_import(filename,hooktype,subtype)
        print "end:", str(datetime.datetime.now())
    else:
        print "please input python import_hook.py [filename] [hooktype]"
