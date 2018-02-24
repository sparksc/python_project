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

from etl.star.model.odsfile import BIFMAIRT,BIFDBRIR,BDFMHQBQ,BDFMHQAP
from etl.star.model.odsmerge import  mergeallfile
from etl.star.model.interestutil import *

from decimal import *
condecimal = getcontext()


FIRSTDATE = 20151220

def get_pre_interest_date(etldate):
    md = int(str(etldate)[4:8])
    year = int(str(etldate)[0:4])
    if md <=320:
        pre = str(year-1) + "1221"
        return int(pre)
    elif md>=321 and md <=620:
        pre = str(year) + "0321"
        return int(pre)
    elif md>=621 and md <=920:
        pre = str(year) + "0621"
        return int(pre)
    elif md>=921 and md <=1220:
        pre = str(year) + "0921"
        return int(pre)
    else:
        pre = str(year) + "1221"
        return pre

def query_row(etldate, db=None, account_no = None,start_date =None):
    new = False
    if db is None:
        new = True
        db = util.DBConnect()
    try:
        sql = """
            select e.*,f.*,a.account_no,a.CASH_TP
            from F_ACCOUNT_BALANCE f
            inner join d_account_type_extend e on e.id=f.ACCOUNT_TYPE_ID
            inner join d_account_gid a on a.id=f.account_id
            inner join d_org_stat s on s.id = f.ORG_ID
        """
        if account_no is not None :
            sql = sql + " where a.account_no = '%s' "%( account_no )
            sql = sql + " and f.date_id >= ? "
            sql = sql + " and f.date_id <= ? "
            #print sql
            db.cursor.execute(sql, int(start_date), int(etldate) )
        else:
            sql = sql + " where f.date_id = ? "
            print sql 
            db.cursor.execute(sql, etldate)
        row = db.cursor.fetchone()
        desc = db.cursor.description    
        ld = len(desc)
        d = {}
        while row: 
            data = {} 
            for x in range(ld):
                data[ desc[x][0] ] = row[x]
            if data["AUTO_DEP"] == '自动转存' and data["PRODUCT"] =='301' and data["BUSI_CODE"] == '13' and data["DUE_DATE"] == 18991231:
                st = data["START_INTEREST"]
                if st == 18991231 : st = data["OPEN_DATE"]
                data["DUE_DATE"] = add_month_date(st,data["TERM"])

            if data["AUTO_DEP"] == '自动转存' and data["PRODUCT"] =='101' and data["BUSI_CODE"] == '17' and data["DUE_DATE"] == 18991231:
                st = data["START_INTEREST"]
                if st == 18991231 : st = data["OPEN_DATE"]
                data["DUE_DATE"] = add_month_date(st,data["TERM"])
            yield data
            row = db.cursor.fetchone()
    finally:
        if new: db.closeDB()

def calc_aggrentment_account(etldate, hqsum = {}):

    last_day = int(daycalc(etldate,-1))
    f = BIFMAIRT(etldate)
    d = f.loadfile2dict2([4])

    predate = get_pre_interest_date(etldate)
    db = util.DBConnect()
    agg_rates = {}
    fd = BIFDBRIR(etldate)
    for k in d:
        #查找账号信息

        rates = d[k]
        rows = query_row(etldate, db, k, etldate)
        rows = [ r for r in rows ]
        last_rows = query_row(last_day, db, k, last_day)
        last_rows = [ r for r in last_rows ]

        if rows is None or len(rows) == 0: continue
        row = rows[0]
        last_row = None
        if len(last_rows) > 9:
            last_row = last_row[0]
        flag = True
        pay_interest = 0
        if flag :
            balance = row["BALANCE"]
            mb =  0
            nr = []
            ak = None
            for r in rates:
                ak =  k + "-" + r["M2__CCYC"].strip() + "-" + r["M2__CHSX"].strip()
                r["M2__AMNT"] = int(Decimal(r["M2__AMNT"])*100)
                nr.append(r)
            pay_interest = hqsum.get(ak)
            nr.sort(key=lambda x:x["M2__AMNT"])
            plan_interest = 0
            for r in nr:
                if balance<=0: break
                amt = r["M2__AMNT"]
                if r["M2__BIRC"].strip() == '':
                    rate = int( Decimal(Decimal(r["M2__RATE"])) * 10000000 )
                else:
                    baserate = fd.find_rate(r["M2__BIRC"].strip(), row["CCY"], etldate)
                    f1 = Decimal(r["M2__RATE"])
                    f2 = Decimal(r["M2__RTIO"])*10000000
                    rate = int(Decimal(baserate[2])*(1+f1)+f2)
                if r["M2__AMNT"] > balance:
                    amt = balance
                p = sum_interest_by_days(1, amt , rate)
                plan_interest = plan_interest + p
                balance = balance - r["M2__AMNT"]
            if last_row is not None:
                plan_interest = plan_interest + last_row["PLAN_INTEREST"]
            if pay_interest is None: pay_interest = 0
            rr = (pay_interest, plan_interest, rate,rate, 0, 0, 0, 0)
            print k,rr,row["BALANCE"]
            if ak is None : continue
            agg_rates[ak] = rr
    db.closeDB()
    return agg_rates

def starun(etldate):
    pass
        
if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen != 3:
        print "please input python %s yyyyMMdd yyyyMMdd"%(sys.argv[0])
    else:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        etldate=int(startdate)
        while etldate<=int(enddate):    
            Config().etldate =etldate
            Config().stretldate=util.tostrdate(etldate)        
            calc_aggrentment_account(etldate) 
            #starun(etldate,sys.argv[3])
            etldate=int(daycalc(etldate,1))
