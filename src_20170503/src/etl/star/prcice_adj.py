# -*- coding:utf-8 -*-
#!/bin/python  

from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random,sys 
from datetime import datetime,timedelta

from etl.base.conf import *
import etl.base.util as util
from etl.star.dim import *
from etl.star.transformdict import *
from etl.base.singleton import singleton
     
from etl.base.logger import info

from etl.star.starbase import StarManage, StarBase

from etl.star.model.dqab import DQAB
from etl.star.model.depositinterest import TimeDepositInterest
from etl.star.model.odsfile import BIFDBRIR,BIFDPDIR,BFFMDQCL,BIFMAIRT,BIFDBRIR,BDFMHQBQ,BDFMHQAP,BDFMHQFN, BDFMHQEM,BIFMACIR,BDFMHQAC,load_hq_interest,BGFMFBAL
from etl.star.model.odsmerge import  mergeallfile
from etl.star.model.interestutil import *

from decimal import *
condecimal = getcontext()
getcontext().prec = 12


FIRSTDATE = 20151220

def load_inner_inte(etldate, yd, name = '个人定期存款利息支出',ccy="CNY"):
    acir = BGFMFBAL(etldate,"ALL")
    d = acir.loadfile2dict()
    nd = {}
    for k in d:
        row = d[k]
        n = row["FGCAFLNM"].decode("gbk").encode("utf8").strip()
        if str(etldate)[4:8] == '1231':
            bal = int(Decimal(row["FGCACMBL"])*100/Decimal(yd))
        else:
            bal = int(Decimal(row["FGCEIBAL"])*100)
        org = row["FGCBBRNO"].strip()
        if org == '966000':continue
        if row["FGCARS1B"].strip() == '9': continue
        #if row["FGCARS1B"].strip() == '9': continue
        if n  == name and row["FGCACCYC"].strip() == ccy:
            if nd.get(org) is not None:
                raise Exception("利息账户重复:%s"%(row["FGCAAC20"]))
            nd[org] = bal
    return nd

def query_row(db, etldate, org_code, ccy, first_subj):
    year = int( str(etldate)[0:4] ) - 1
    ly = int(str(year)+"1231")
    sql = """
        select 
            (case when f.ACCOUNT_class='D' and  t.INTEREST_TYPE='不计息' then  0 else  f.PAY_INTEREST+f.PLAN_INTEREST-nvl(f2.PAY_INTEREST,0)-nvl(f2.PLAN_INTEREST,0)  end ) as   interest       
            ,f.id
       from
            F_ACCOUNT_BALANCE_back f
       inner join d_org_stat s on  s.id = f.ORG_ID
       inner join d_account_type_extend t on t.id = f.ACCOUNT_TYPE_ID
       inner join D_AC_MAP da on t.SUBJ_NO=da.AC_CODE
        left join F_ACCOUNT_BALANCE_back f2 on f2.ACCOUNT_ID=f.ACCOUNT_ID and f2.DATE_ID = ? 
         where f.DATE_ID = ? 
          and t.CCY = ?
          and s.ORG_CODE = ?
          and da.SUBJ_NO in ('20010101','20020101','20020102','20030101','20030102','20040101','20040105','20040106','20050201','20060101','20140106', '20140109', '20140199', '20140201', '20140204', '20140206') 
            and da.subj_no like '2004%'
    """
    print sql,ly, etldate, ccy, org_code
    db.cursor.execute( sql, (ly, etldate, ccy, org_code) )
    datas = []
    row = db.cursor.fetchone()
    sum1 = 0 
    while row: 
        sum1 = sum1 + row[0] 
        datas.append( list(row) )
        row = db.cursor.fetchone()
    return sum1,datas

def adj_interst(etldate, ccy="CNY", name="个人定期存款利息支出",first_subj= '2004'):
    if is_month_end(etldate) == False: return ;

    db = DBConnect()
    sql = "select year_days from d_date where id = ?"
    db.cursor.execute(sql, etldate)
    yd = db.cursor.fetchone()[0]

    inners = load_inner_inte(etldate, yd, name, ccy)
    usql = """
        update F_ACCOUNT_BALANCE_back f
            set f.ADJ_INTEREST = ?
        where f.id = ?
    """
    try:

        for k in inners:
            bal = inners[k]
            sum1,datas = query_row(db, etldate, k, ccy, first_subj)
            if sum1  == 0 : continue
            p = Decimal((bal - sum1))/Decimal(sum1)
            #print k,bal,bal-sum1,p
            a = 0
            for row in datas:
                adj = int(row[0]*p)
                #print k,row[0], row[1], adj
                a = a + adj
                row[0] = adj
            db.cursor.executemany(usql,datas)
            db.conn.commit()
    finally:
        db.closeDB()

if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen != 3:
        print "please input python %s yyyyyMMdd yyyyMMdd "%(sys.argv[0])
    else:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        etldate=int(startdate)
        while etldate<=int(enddate):    
            Config().etldate =etldate
            Config().stretldate=util.tostrdate(etldate)        
            adj_interst(etldate)
            etldate=int(daycalc(etldate,1))
