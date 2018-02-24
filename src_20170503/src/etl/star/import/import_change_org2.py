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
    update F_BALANCE set ORG_ID=(select ID from D_ORG where ORG0_CODE=?) where ACCOUNT_ID=(
    select ACCOUNT_ID from F_BALANCE f
    join D_ACCOUNT a on f.ACCOUNT_ID=a.ID and a.ACCOUNT_NO =?
    where f.DATE_ID=20160630 and f.ACCT_TYPE=1 ) and DATE_ID=20160630 and ACCT_TYPE=1 
    """
    rr=[]
    for r in range(1,nrows):
        row = sheet.row_values(r)
        account_no = row[0].encode('UTF-8')
        now = str(int(row[3])).encode('UTF-8')
        print account_no,now
        update_org_id(u_sql,now,account_no)
        
        
def update_org_id(insert_sql,now,account_no):
    db = util.DBConnect()
    try :
        db.cursor.execute(insert_sql,now,account_no)
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
