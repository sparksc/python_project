# -*- coding:utf-8 -*-
#!/bin/python  

from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random,sys 
from datetime import datetime,timedelta
from pprint import pprint

from etl.base.conf import *
import etl.base.util as util
from etl.star.dim import *
from etl.star.transformdict import *
from etl.base.singleton import singleton
             
from etl.base.logger import info

from etl.star.model.deposit_lczq import Deposit_lczq
from etl.star.model.odsfile import BFFTDQAC,BDFMHQBQ,BDFMHQAP
from etl.star.model.odsmerge_lczq import mergeallfile
from etl.star.model.interestutil import *

from decimal import *
condecimal = getcontext()

FIRSTDATE = 20151220

def query_row(etldate, db=None, account_no = None,start_date =None):
    new = False
    if db is None:
        new = True
        db = util.DBConnect()
    try:
        sql = """
            select e.*,f.*,a.account_no,a.CASH_TP
            from F_ACCOUNT_BALANCE_BACK f
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
            sql = sql + """
                and e.busi_code='14' and e.product = '102'
            """
            #print sql 
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
        if new: 
            db.closeDB()

def calc_lczq_account(startdate, etldate, hqsum = {}):

    mergeallfile(etldate)
    last_day = int(daycalc(etldate,-1))
    next_day = int(daycalc(etldate,1))
    
    pr = BIFDPDIR(etldate)
    f = BFFTDQAC(etldate, "ALL")
    d = f.loadfile2dict2([0,7])

    db = util.DBConnect()
    msg = {}
    rows = query_row(etldate)
    last_rows = { row["ACCOUNT_ID"]: row for row in  query_row(last_day)}
    rows = [ row for row in rows ]
    for row in rows:
        last_row = last_rows.get( row["ACCOUNT_ID"] )
        ak = row["ACCOUNT_NO"] + "-" + row["CCY"]   
        acs = d.get(ak)
        dq_pdt = 0
        hq_pdt = 0

        cd = int(row["CLOSE_DATE"])
        if cd != 18991231 and cd >= etldate:
            f = False
        elif cd == 18991231:
            f = False
        elif etldate == startdate:
            f = False
        else:
            f = True
        print f
        if f: #取上一日数据，不计算
            if last_row is not None:
                rt = (last_row["PAY_INTEREST"], last_row["PLAN_INTEREST"], last_row["CONTRACT_RATE"], last_row["EXECUTE_RATE"], 0, 0, 0, 0)
            else:
                rt = (0, 0, 0, 0, 0, 0, 0, 0)
        else:
            acs.sort(key=lambda x: int(x["AC03DATE"].replace("-","")))
            b1 = row["OPEN_DATE"]
            over_flag = False
            for ac in acs:
                if ac["AC09CDFG"] == '1':
                    continue
                st = int(ac["AC03DATE"].replace("-",""))
                if row["DUE_DATE"] > etldate:
                    days = sum_days(st, next_day)
                    dq_pdt = dq_pdt + days * Decimal(ac["AC10AMT"])*100
                elif row["DUE_DATE"] == etldate:
                    days = sum_days(st, etldate)
                    dq_pdt = dq_pdt + days * Decimal(ac["AC10AMT"])*100
                    if row["CLOSE_DATE"]  == etldate:
                       pass 
                    else:
                        hq_pdt = hq_pdt + Decimal(ac["AC10AMT"])*100
                else:

                    days = sum_days(st, row["DUE_DATE"])
                    dq_pdt = dq_pdt + days * Decimal(ac["AC10AMT"])*100

                    days2 = sum_days(row["DUE_DATE"],next_day)
                    hq_pdt = hq_pdt + days2 * Decimal(ac["AC10AMT"])*100
                if st > b1:
                    #b1的下一月
                    nb = get_next_month_end(b1)
                    nb2 = int(str(get_next_month_end(nb))[4:6])
                    nb = int(str(nb)[4:6])
                    cm = str(st)[4:6]
                    if cm == nb or cm  == nb2: #下月有存  或 下下个月有补存 （假定核心会控制，不满足补存标志，不会允许客户存入)
                        pass
                    else:
                        over_flag = True
                b1 = st
            if etldate>=row["DUE_DATE"]:
                #判断最后一次存入日期是否大于等于到期日期的上月月初，如果是，则没有违约，否则违约
                pre = int(str(get_pre_month_end(row["DUE_DATE"]))[0:6]+"01")
                if b1 >= pre:
                    pass
                else:
                    over_flag = True
            else:
                nb = get_next_month_end(b1)
                nb2 = get_next_month_end(nb)
                if etldate > nb2:
                    over_flag = True
            lczq = Deposit_lczq(etldate, row, last_row, pr, dq_pdt, hq_pdt, over_flag)
            rt = lczq.product_14101_interest()
        if rt is not None:
            msg[ row["ID"]] = rt
    return msg

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
            print "*************RunTime: %s*************"%(etldate)
            pprint(calc_lczq_account(startdate, etldate))
            #starun(etldate,sys.argv[3])
            etldate=int(daycalc(etldate,1))
