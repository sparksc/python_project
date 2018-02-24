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
from etl.star.model.odsfile import BIFDBRIR,BIFDPDIR,BFFMDQCL,BIFMAIRT,BIFDBRIR,BDFMHQBQ,BDFMHQAP,BDFMHQFN, BDFMHQEM,BIFMACIR,BDFMHQAC,load_hq_interest
from etl.star.model.odsmerge import  mergeallfile
from etl.star.model.interestutil import *
from account_aggrement import  calc_aggrentment_account
from etl.star.ftpprice import  find_price_id, query_para_price

from decimal import *
condecimal = getcontext()


FIRSTDATE = 20151220
def query_row(etldate, dh='A',org_no=None, db=None, account_id  = None):
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
        if account_id  is not None :
            sql = sql + " where f.account_id  = ?   and f.date_id = ? "
            db.cursor.execute(sql, (account_id,int(etldate)) )
        else:
            sql = sql + " where f.date_id = ? "
            if dh  == 'A':
                pass
            elif dh == 'D':
                sql = sql + " and f.account_class  in ('D','C') "
            elif dh == 'H':
                sql = sql + " and f.account_class  in ('H') "
            else:
                raise Exception("not support dh typeL:%s"%dh)
            #if org_no is not None:
            #    sql = sql + " and s.org_code = '%s'"%( org_no )
            print sql 
            #sql = sql + " with ur "
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

def load_close_accounts(etldate):
    bq = BDFMHQBQ(etldate)
    def cjkey(row):
        key = [ row[0].strip(), row[1].strip(), row[2].strip()]
        k = "-".join( key )
        return k
    return bq.loadfile2dict2([0,1,2], cjkey)

def load_loser_new_account(etldate):
    ap = BDFMHQAP(etldate)
    return ap.loadfile2dict2([1])

def load_dq_draw(etldate):
    fn = BDFMHQFN(etldate)
    def cjkey(row):
        return row[0].strip()
    return fn.loadfile2dict2([0],cjkey)

def get_losernew_account(row, aps):
    ap = aps.get(row["ACCOUNT_NO"])
    if ap is None : return None
    r = None
    for nr in  ap:
        if nr["ACTION"] == 'D':continue
        if nr["RCSTRS1B"] == '9':continue
        r = nr
    return r 

def get_close_account(row, close_accounts):
    if row["CASH_TYPE"] =='现钞':
        key =  row["ACCOUNT_NO"]+"-" + row["CCY"] + "-1"
    else:
        key =  row["ACCOUNT_NO"]+"-" + row["CCY"] + "-2"
           
    #查找当天开销户信息
    close_account1 = close_accounts.get( key )
    #701账户会有多记录，本程序只处理定期，活期，不会包括701（股金账户)
    if close_account1 is None: 
        #raise Exception(1) 
        return None

    ccount = 0
    c = None
    for crow  in  close_account1:
        if crow["ACTION"] == 'D':continue
        ccount = ccount + 1
        c =  crow
    if ccount > 1:
        raise Exception("找到多条销户记录%s"%(key))
    return c

def load_tran_dep(etldate):
    em = BDFMHQEM(etldate,"ADD")
    def cjkey(row):
        key = [row[6].strip(), row[7].strip()]
        k = "-".join( key )
        if row[19] == 'D': return "-1"
        if row[1] == '1': return "-1" #只取定转活数据
        if int(str(row[0]).replace("-",""))  != etldate : return "-1" #只取当日数据
        return k
    return em.loadfile2dict2([6,7], cjkey)


def load_rate_base(etldate):
    acir = BIFMACIR(etldate,"ALL")
    def cjkey(row):
        key = [row[5].strip(), row[4].strip(), row[6].strip()]
        k = "-".join( key )
        if row[30] == '9': return "-1"
        if row[35] == 'D': return "-1"
        return k
    return acir.loadfile2dict2([5,4,6],cjkey)


def find_account_rate(ak, etldate, aggr_rate):
    rate1 = aggr_rate.get(ak)
    if rate1 is None :
        return None
    rate = None
    if rate1 is not None:
        for xr in rate1:
            rb = int(xr["M1__DATE"].replace("-",""))
            re = int(xr["M1LSDATE"].replace("-",""))
            if re == 18991231 : re = 30001231
            if etldate>= rb and etldate <= re:
                d1 = Decimal(xr["M1__RATE"])*10000000
                d2 = Decimal(xr["M1__RTIO"])*10000000
                if int(d1) == 0 and int(d2) == 0 : return None
                #TODO 目前只有定期有值，温岭只有1条记录
                return int(d1)

def hq_interest(etldate, dh):
    if dh == 'H' or dh == 'A':
        (hqinterests,hqsum) = load_hq_interest(etldate)
    else:
        (hqinterests,hqsum) = ( {},{})
    db = DBConnect()
    try:
        db.cursor.execute("delete from f_hq_interest f where date_id= ?",(etldate))
        db.conn.commit()
        isql = """
            insert into f_hq_interest values( ?,?,?,?,?,?,?)
        """
        db.cursor.executemany(isql, hqinterests)
        db.conn.commit()
    finally:
        db.closeDB()
    return (hqinterests,hqsum)

fact_keys =["PAY_INTEREST","PLAN_INTEREST","CONTRACT_RATE","EXECUTE_RATE","INTEREST_MONTH","INTEREST_DAY"]
factsql = """
        update F_ACCOUNT_BALANCE
        set 
            pay_interest=?
            ,plan_interest=?
            ,contract_rate = ?
            ,execute_rate = ?
            ,interest_month = ?
            ,interest_day = ?
            ,price_id = ?
        where id = ?
    """

def put_fact_data2(sm, row, last_row, prices):
    if last_row is None: return None
    price_id = find_price_id(sm, prices, row)
    data = [last_row[k] for k in fact_keys]
    data.append( price_id )
    data.append( row["ID"] )
    if row["CST_NO"] == '83000044582': data[1] = 0 
    sm.put_fact_data( (factsql, data) )

def put_fact_data(sm, rt, row, last_row, prices):
    price_id = find_price_id(sm, prices, row)
    if rt is None:
        if last_row is None: return None
        data = [last_row[k] for k in fact_keys]
        data.append( price_id )
        data.append( row["ID"] )
        if row["CST_NO"] == '83000044582': data[1] = 0 
        sm.put_fact_data( (factsql, data) )
    else:
        if len(rt) == 2: 
            raise Exception("not support")
        else:
            data = [rt[x] for x in range(6)]
            if row["CST_NO"] == '83000044582': data[1] = 0 
            data.append( price_id )
            data.append( row["ID"] )
            if last_row is not None:
                data[0] = last_row["PAY_INTEREST"] + data[0]
            sm.put_fact_data( (factsql, data) )

def get_price_args(row, last_row, hqsum, hq_agg_rates, aggr_rate, close_accounts, last_close_accounts, tran_deps):
    ak = row["ACCOUNT_NO"] + "-" + row["CCY"] + "-" + row["CASH_TP"].split("-")[0]
    account_no = row["ACCOUNT_NO"]

    hqinterest = hqsum.get(ak)
    hq_agg_rate = hq_agg_rates.get(ak)

    agg_rate = find_account_rate(ak, etldate, aggr_rate)
    close_account = get_close_account(row, close_accounts)
    if close_account is None:
        close_account = get_close_account(row, last_close_accounts)

    td0 = None
    if row["ACCOUNT_CLASS"] == 'C':
        tp = row["CASH_TP"].split("-")[1]
        seq = row["ACCOUNT_NO"] + "-" + tp
        td = tran_deps.get( seq )
        if td is not None and len(td) > 1 :
            raise Exception("转存登记薄有重复数据%s"(account_no))
        if td is not None:
            td0 = td[0]
    return close_account , td0, agg_rate, hqinterest, hq_agg_rate

def starun(etldate, dh):
    last_day = int(daycalc(etldate,-1))
    #if etldate != 20151220:
    #    mergeallfile(etldate)


    pr = BIFDPDIR(etldate)
    dqcl = BFFMDQCL(etldate)
    dqcldict = dqcl.loadfile2dict()
    close_accounts = load_close_accounts(etldate)
    #当日销户，下发数据在昨日下发的销户登记薄中
    last_close_accounts = load_close_accounts(last_day)
    lnew = load_loser_new_account(etldate)
    tran_deps = load_tran_dep(etldate)
    aggr_rate = load_rate_base(etldate)
    (hqinterests, hqsum) = hq_interest(etldate, dh)
    hq_agg_rates = calc_aggrentment_account(etldate, hqsum)
    
    '''
    db = util.DBConnect()
    sql = """
            select distinct  s.org_code from d_org_stat s
    """
    db.cursor.execute(sql)
    row = db.cursor.fetchone()
    
    orgs = []
    orgs_all = []
    while row: 
        orgs.append( row[0] )
        if len(orgs) >= 10:
            orgs_all.append( [ o for o in orgs ] )
            orgs =[]
        row = db.cursor.fetchone()
    orgs_all.append( [ o for o in orgs ] )
    db.closeDB()
    pws = []
    for orgs in orgs_all:
        for org_no in orgs:
            print org_no
            pw1 = Process(target= account_price_by_org, args=(etldate, dh, org_no, hqsum, hq_agg_rates, aggr_rate, close_accounts, last_close_accounts, lnew, pr, dqcl, dqcldict,tran_deps))
            pw1.start()
            pws.append( pw1 )
        for p in pws:
            p.join()

    '''
    account_price_by_org(etldate, dh, None, hqsum, hq_agg_rates, aggr_rate, close_accounts, last_close_accounts, lnew, pr, dqcl, dqcldict, tran_deps)

def account_price_by_org(etldate, dh, org_no, hqsum, hq_agg_rates, aggr_rate, close_accounts, last_close_accounts, lnew, pr, dqcl, dqcldict, tran_deps):
    prices = query_para_price(etldate)
    last_day = int(daycalc(etldate,-1))
    
    if org_no is None:
        sm = StarManage(2,[])
    else:
        sm = StarManage(10,[])
    sm.start_dim_process()
    sm.start_fact_process()
    sm.setDimQueue()
    sm.start()
    rows = query_row(etldate,dh, org_no)
    last_rows = { row["ACCOUNT_ID"]: row for row in  query_row(last_day,dh,org_no) }
    db = util.DBConnect()
    for row in rows:
        if row["INTEREST_TYPE"] == '不计息': 
            continue
        if row["TERM"] == 96 and row["START_INTEREST"] >20020220:
            continue
        if row["CLOSE_DATE"] == etldate and last_row is None and row["ACCOUNT_CLASS"] == 'D':
            #当天销户，昨日没有，说明是当日新开即销户,无需计息
            continue
        if row["START_INTEREST"] == 18991231:
            row["START_INTEREST"] = row["OPEN_DATE"]
        last_row = last_rows.get( row["ACCOUNT_ID"])
        '''
        if last_row is None and row["OPEN_DATE"] != etldate and etldate != FIRSTDATE:
            lds = [ r for r in query_row(last_day, dh, org_no, db,row["ACCOUNT_ID"] ) ]
            if len(lds) > 0 : last_row = lds[0]
        '''
        if ( row["OPEN_DATE"] == row["CLOSE_DATE"] and row["OPEN_DATE"] !=18991231 ):#or row["START_INTEREST"] == row["CLOSE_DATE"]:
            put_fact_data2(sm, row, last_row, prices)
        else:
            ak = row["ACCOUNT_NO"] + "-" + row["CCY"] + "-" + row["CASH_TP"].split("-")[0]
            nrt = hq_agg_rates.get(ak)
            if nrt is None:
                close_account , td0, agg_rate, hqinterest, hq_agg_rate = get_price_args(row, last_row, hqsum, hq_agg_rates, aggr_rate, close_accounts, last_close_accounts, tran_deps)
                la = get_losernew_account(row, lnew)
                laflag = True if la is not None and la["AP09LSTP"] == '1' else False
                td = TimeDepositInterest(etldate, row, last_row, pr, dqcl, dqcldict, close_account, laflag, td0, agg_rate, hqinterest, hq_agg_rate)
                rt = td.calc_interest()
            else:
                rt = nrt
            ak = row["ACCOUNT_NO"] + "-" + row["CCY"] + "-" + row["CASH_TP"].split("-")[0]
            put_fact_data(sm, rt, row, last_row, prices)
    sm.finish()
    db.closeDB()

def str2intdate(dt):
    dts = dt.split("-")
    if len(dt) == 8 : return int(dt)
    xd = dt.replace("-","").strip()
    if len(xd) == 8 :
        return int(xd)
    if int(dts[1]) < 10:
        dts[1] = "0"+int(dts[1])
    if int(dts[2]) < 10:
        dts[2] = "0"+int(dts[2])
    return int("".join(dts))

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


if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen != 4:
        print "please input python %s yyyyyMMdd yyyyMMdd D/H/A(定期/活期/全部"%(sys.argv[0])
    else:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        etldate=int(startdate)
        while etldate<=int(enddate):    
            #print etldate
            #hq_agg_rates = update_agg_account(etldate)
            #print hq_agg_rates
            print '*****start calculate interest %d*****'%(etldate)
            Config().etldate =etldate
            Config().stretldate=util.tostrdate(etldate)        
            starun(etldate,sys.argv[3])
            etldate=int(daycalc(etldate,1))
