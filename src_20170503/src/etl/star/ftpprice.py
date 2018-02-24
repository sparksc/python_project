# -*- coding:utf-8 -*-
#!/bin/python  

from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random,sys 
from datetime import datetime,timedelta

from etl.base.conf import *
import etl.base.util as util

from etl.star.dim import DimStarPrice
from etl.star.model.loanlist import BICUXLOAN

from etl.star.transformdict import *
from etl.base.singleton import singleton
     
from etl.star.starbase import StarManage, StarBase
from etl.base.logger import info


from decimal import *
condecimal = getcontext()


FIRSTDATE = 20151220

def find_price_id(sm, prices, row):
    vf = "有效"
    busi_code = row["BUSI_CODE"]
    product = row["PRODUCT"]
    term = row["TERM"]
    if busi_code == '17' and product == '101':    
        p = prices["一天丶7天"]
    elif busi_code == '27' and product == '701':    
        p = prices["一天丶7天"]
    elif row["ACCOUNT_CLASS"] == 'H':
        p = prices["活期"]
    else:
        if term  == 3:
            p = prices["三个月"]
        elif term  == 6:
            p = prices["半年"]
        elif term  == 12:
            p = prices["一年"]
        elif term  == 24:
            p = prices["二年"]
        elif term  == 36:
            p = prices["三年"]
        elif term  == 60:
            p = prices["五年"]
        else:
            p = 0
            vf = "无效"
    price = {"FTP_PRICE":int(Decimal(p)*10000000), "VALIDATE_FLAG":vf}
    return DimStarPrice().find_dim_id( price )

def find_loan_price_id(sm, prices, row):
    tp = row["GUA_TP_NAME"]
    vf = "有效"
    if tp in  ["抵押","其他质押","系统内存单质押"]:
        #pn = "抵质押"
        p = prices[tp]
    elif tp in  ["联保","普通保证","信用","组合担保"]:
        #pn = "保证、信用"
        #p = prices[pn]
        p = prices[tp]
    else:
        p = 0
        vf = "无效"
    price = {"FTP_PRICE":int(Decimal(p)*10000000), "VALIDATE_FLAG":vf}
    return DimStarPrice().find_dim_id( price )
        
def query_para_price(etldate):
    db = util.DBConnect()
    year = str(etldate)[0:4]
    try:
        sql = """
        SELECT  H.HEADER_NAME,A.DETAIL_VALUE FROM T_PARA_DETAIL A 
         JOIN T_PARA_HEADER H ON H.ID=A.PARA_HEADER_ID
         WHERE A.PARA_ROW_ID =
            (
                SELECT distinct D.PARA_ROW_ID FROM T_PARA_TYPE Y JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=Y.ID JOIN T_PARA_DETAIL D ON H.ID=D.PARA_HEADER_ID
                WHERE Y.TYPE_NAME='存款定价' AND D.DETAIL_VALUE= ?
        )   
        """
        db.cursor.execute(sql, year)
        row = db.cursor.fetchone()
        prices = {}
        while row: 
            prices[ row[0] ] = row[1]
            row = db.cursor.fetchone()
        return prices
    finally:
        db.closeDB()

def query_loan_para_price(etldate):
    #return {"抵质押":4,"保证、信用":6}
    db = util.DBConnect()
    year = str(etldate)[0:4]
    try:
        sql = """
        SELECT  H.HEADER_NAME,A.DETAIL_VALUE FROM T_PARA_DETAIL A 
         JOIN T_PARA_HEADER H ON H.ID=A.PARA_HEADER_ID
         WHERE A.PARA_ROW_ID =
            (
                SELECT distinct D.PARA_ROW_ID FROM T_PARA_TYPE Y JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=Y.ID JOIN T_PARA_DETAIL D ON H.ID=D.PARA_HEADER_ID
                WHERE Y.TYPE_NAME='贷款定价' AND D.DETAIL_VALUE= ?
        )
        """
        print sql,year
        db.cursor.execute(sql, year)
        row = db.cursor.fetchone()
        prices = {}
        while row: 
            prices[ row[0] ] = row[1]
            row = db.cursor.fetchone()
        return prices
    finally:
        db.closeDB()

def update_dep_price(etldate):
    prices = query_para_price(etldate)
    db = util.DBConnect()
    try:
        sql2 = """
        select  f.id,t.TERM,f.ACCOUNT_CLASS,t.PRODUCT,t.BUSI_CODE from f_account_balance_back f
        inner join d_account_type_extend t on t.id = f.ACCOUNT_TYPE_ID
        where f.DATE_ID = ?
          --  and f.id in ( 2001759406,2000009510, 2000009514, 2000009531, 2000009533, 2000009657, 2000009662, 2000009684, 2000009688, 2000010144, 2000010146
            --    ,2001951568, 2001859317, 2001859334, 2001859336, 2001859339, 2001859637, 2001859930, 2001859935, 2001860038, 2001860136
            --    ,2001910408
           -- )
        """
        usql= """
            update f_account_balance_back f
                set f.price_id = ?
                where f.id = ?
        """
        db.cursor.execute(sql2, etldate )
        row = db.cursor.fetchone()
        datas = []

        sm = StarManage(2,[ DimStarPrice() ])
        sm.start_dim_process()
        sm.start_fact_process()
        sm.setDimQueue()
        sm.start()
        desc = db.cursor.description    
        ld = len(desc)
        while row: 
            data = {}
            for x in range(ld):
                data[ desc[x][0] ] = row[x]
            dim_id = find_price_id(sm, prices, data)
            datas.append( (dim_id,row[0]) )
            row = db.cursor.fetchone()
        sm.finish()
        db.cursor.executemany(usql, datas )
        db.conn.commit()
    finally:
        db.closeDB()


def load_loan_price_view(etldate):
    db = util.DBConnect()
    try:
        db.cursor.execute("delete from GAS_BI_CUX_LOAN_CHECK_DTL_V where date_id = ?",(etldate))
        db.conn.commit()
    finally:
        db.closeDB()

    '''
    导入总账系统下发的贷款视图
    '''
    prices = query_loan_para_price(etldate)
    db = util.DBConnect()
    try:
        sql2 = """
        SELECT  A.ACCOUNT_NO,F.MANAGE_ID,t.GUA_TP_NAME,f.year_pdt FROM F_BALANCE F 
        inner join d_account_type t on t.id = f.ACCOUNT_TYPE_ID
        INNER JOIN D_ACCOUNT A ON A.ID = F.ACCOUNT_ID WHERE F.DATE_ID=? AND F.ACCT_TYPE='4'
        """

        db.cursor.execute(sql2, etldate )
        row = db.cursor.fetchone()
        datas = {}
        desc = db.cursor.description    
        ld = len(desc)
        sm = StarManage(2,[ DimStarPrice() ])
        sm.start_dim_process()
        sm.start_fact_process()
        sm.setDimQueue()
        sm.start()
        while row: 
            data = { desc[x][0] : row[x] for x in range(ld) }
            
            dim_id = find_loan_price_id(sm, prices, data)
            datas[ row[0] ] = (row[1],dim_id,row[3])
            row = db.cursor.fetchone()
        loan = BICUXLOAN()
        loan.manages = datas
        StarBase().files2fact2(loan, sm)
        sm.finish()
    finally:
        db.closeDB()



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
            #update_dep_price(etldate)
            load_loan_price_view(etldate)
            etldate=int(util.daycalc(etldate,1))
