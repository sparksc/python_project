# -*- coding:utf-8 -*-
#!/bin/python  

from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random,sys 
from datetime import datetime,timedelta
from decimal import *
import DB2  

from etl.base.conf import *
import etl.base.util as util
from etl.star.dim import *
from etl.star.transformdict import *
from etl.base.singleton import singleton
     
from etl.base.logger import info


condecimal = getcontext()
import hashlib


def tomd5(row, jumpattr):
    md5 = hashlib.md5()
    for i in range(len(row)):
        if i in jumpattr: continue
        k = row[i]
        if k is None: k=""
        if isinstance(k, unicode) or isinstance(k, str ):
            md5.update( k )
        else:
            md5.update( str(k) )
    return md5.hexdigest()

def find_idx(desc):
    idxs = find_add_attr(desc,["ID"])
    if len(idxs) == 0:
        raise Exception("只支持有ID的表的拉链存储")
    return idxs[0]

def find_add_attr(desc,cols, jumpattr = [] ):
    idx = []
    for x in range(len(desc)):
        if desc[x][0] in cols or desc[x][0] in jumpattr:
            idx.append(x)
    return idx

def get_insert_values( table, desc): 
    x1 = []
    x2 = []
    for x in desc:
        if x[0]  == 'RN': continue
        x1.append( x[0] )
        x2.append( "?" )
    return  """
        insert into %s_ADD ( %s ) values ( %s )
    """%( table, ",".join( x1 ), ",".join( x2 ) )

def table_add(etldate, table, jumpattr = [] ):
    db = DBConnect()
    try:
        db.cursor.execute("delete from %s_add  where add_date=?"%(table),etldate)
        db.conn.commit()

        db.cursor.execute("select * from ( select f.* , ROW_NUMBER() OVER (PARTITION BY  ID  ORDER BY ADD_DATE desc) RN  from %s_add f ) where rn=1 "%(table))
        desc = db.cursor.description    
        cursor = db.cursor
        insertsql = get_insert_values( table, desc)
        idx = find_idx(desc)
        addattr = find_add_attr(desc, ["ADD_DATE","ACTION","RN"],jumpattr)


        row = cursor.fetchone()
        d = {}
        while row:
            d[row[idx]] = [tomd5(row, addattr),row]
            row = cursor.fetchone()


        db.cursor.execute("select * from %s"%(table))
        desc = db.cursor.description    
        idx = find_idx(desc)
        addattr = find_add_attr(desc, ["ADD_DATE","ACTION","RN"],jumpattr)

        rsts = []
        cursor = db.cursor
        row = cursor.fetchone()
        while row:
            flag = False
            nr = list(row)
            k = row[idx]
            if d.has_key(k):
                old = d.pop(k)[0]
                md5 = tomd5(row,addattr)
                if old != md5:
                    nr.append( "U" )
                    nr.append( etldate )
                    rsts.append( nr )
            else:
                nr.append( "A" )
                nr.append( etldate )
                rsts.append( nr )
            row = cursor.fetchone()
        for k in d:
            row = list(d[k][1])[0:-1]
            row[-2] ='D'
            row[-1] = etldate
            rsts.append( row )
        """
        for r in rsts:
            print r
            print insertsql
            print len(r)
            db.cursor.execute(insertsql, r)
        """
        db.cursor.executemany(insertsql, rsts)
        db.conn.commit()
    finally:
        db.closeDB()

def hook_back(etldate):
    table_add(etldate,"ACCOUNT_HOOK",["EXIST_AVG_BALANCE","ADD_AVG_BALANCE","NOTE","ETL_DATE","BALANCE",])
    table_add(etldate,"CUST_HOOK"   ,["EXIST_AVG_BALANCE","ADD_AVG_BALANCE","HIDE","NOTE","ETL_DATE","BALANCE",])

if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen != 2:
        print "please input python %s yyyyyMMdd "%(sys.argv[0])
    else:
        startdate=sys.argv[1]
        etldate=int(startdate)
        hook_back(etldate)
