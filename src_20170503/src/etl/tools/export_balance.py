# -*- coding:utf-8 -*- 
from nose.tools import eq_, raises, assert_true
from sqlalchemy.orm import aliased
import unittest
import time,os,random,sys
import DB2
from decimal import Decimal

import etl.base.util as util

import xlrd,xlwt

from openpyxl import Workbook,load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter
from openpyxl.styles import colors
from openpyxl.styles import Font,Color
import datetime

def run_export(etldate):
        f=open('test.txt','w')
        data=query_detail(etldate)
        xx=len(data)
        for i in range(0,xx):
            for x in data[i]:
                f.write(str(x)+',')
            f.write('\n')
def query_detail(etldate):
    try :
        db = util.DBConnect()
        q_sql="""
        select a.ACCOUNT_NO,a.CST_NAME,a.ACCOUNT_CLASS,f.BALANCE from F_BALANCE f
        join D_ACCOUNT a on f.ACCOUNT_ID=a.ID
        where f.DATE_ID = ? and f.ACCT_TYPE in (1,4,8) 
        """
        db.cursor.execute(q_sql,etldate)
        row=db.cursor.fetchall()
        print len(row)
        return row
    finally :
        db.closeDB()


if __name__=='__main__':
    arglen=len(sys.argv)
    print "begin:", str(datetime.datetime.now())
    if arglen ==2:
        etldate=int(sys.argv[1])
        run_export(etldate)
    else:
        print "please input python %s yyyyMMdd"%sys.argv[0]
    print "end:", str(datetime.datetime.now())
