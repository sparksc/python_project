# -*- coding:utf-8 -*-
#!/bin/python  
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random  
from datetime import datetime,timedelta
from decimal import *
import DB2  

import etl.star.util as util
from etl.star.conf import Config
import etl.performance.measureutil as mutil
	


def delete_liushi(db,etldate):
	strdate = str(etldate)[0:4]+"-" +str(etldate)[4:6]+"-"+str(etldate)[6:8]
	d_sql = u"""
		delete from T_JGC_JXKH_LIUSHI where tjrq=?;
	""" 
	db.cursor.execute( d_sql,strdate)
        db.conn.commit()

def insert2db(db,rs):
	insert_sql = u"""
		insert into T_JGC_JXKH_LIUSHI(TJRQ,SJLX,ZH,KH,KHH,HM,JGBH,BZ,RQYE,YGGH,YGXM,JYJE,SQYE)
		values(?,?,?,?,?,?,?,?,?,?,?,?,?)
	"""
        db.cursor.executemany (insert_sql, rs )
        db.conn.commit()


def get_dk_dict(db,date):
	sql = u"""
		SELECT DISTINCT a.PARA_ID,f.balance,trim(da.CUST_SEQ),TRIM(a.dxmc) dxmc,trim(a.dxmc),trim(d.BRANCH_CODE) JGBH,da.ccy,trim(d.user_name),trim(b.STAFF_NAME),TRIM(a.DXBH) DXBH ,trim(da.pe_flag)
        FROM
                t_zjc_gsgx_dk a 
                inner JOIN STAFF_RELATION b 
                ON a.GLDXBH=b.STAFF_CMS_CODE 
                inner JOIN D_ACCOUNT da 
                ON a.DXBH=da.ACCOUNT_NO  and a.dxxh = da.debit_no and da.account_classify = 'L'
                inner join f_balance f on f.account_id = da.id and f.date_id =? and f.balance <>0 and f.account_classify = 'L'
                inner JOIN v_user_org d 
                ON b.STAFF_CODE=d.USER_NAME
        WHERE
                (da.close_date>? or da.close_date=0)
	"""
	db.cursor.execute(sql,date,date)
	row = db.cursor.fetchone()
	data = {}
	while row :
		data[row[0]] = row
		row = db.cursor.fetchone() 
	return data

def insertdata(row,balance,etldate,sjlx,sqye):
	bzdict = {'01':'CNY'}#我这没用
	strdate = str(etldate)[0:4]+"-" +str(etldate)[4:6]+"-"+str(etldate)[6:8]
	if sjlx == '1': #数据类型
		kh = row[10]#卡号
	else: 
		kh ='--'
	khh = row[2]#客户号
	hm = row[3]#客户名
	jgbh = row[5]#机构号
	if bzdict.has_key(row[6]):
		bz = bzdict[row[6]]
	else:
		bz = row[6]#币种
	rqye = row[1]*0.01#当日余额
	yggh = row[7]#员工
	ygxm = row[8]#员工姓名
	zh = row[9]#账户
	jyje = balance*0.01#交易金额
	return (strdate,sjlx,zh,kh,khh,hm,jgbh,bz,rqye,yggh,ygxm,jyje,sqye)
	
	
def get_ck_dict(db,date):
	sql = u"""
		SELECT a.para_id,f.BALANCE,trim(B.CUST_SEQ),TRIM(a.dxmc) dxmc,trim(C.NAME),trim(c.org_code) jgbh,B.CCY,trim(A.GLDXBH),trim(c.NAME),trim(A.DXBH),trim(B.CARD_NO),trim(b.pe_flag)
		FROM T_ZJC_GSGX_CK A 
		inner join D_ACCOUNT B on  A.DXBH=B.ACCOUNT_NO AND A.DXXH=B.ACCOUNT_SBSQ 
		inner join f_balance f on f.account_id = b.id and f.date_id =?  and f.balance <>0
	 	inner join d_account_type t on f.account_type_id=t.id	
		inner JOIN v_user_org c ON a.GLDXBH=c.USER_NAME
		where (B.close_date>20151001 or B.close_date=0) and t.first_subj_code in ('2001','2002','2003','2004','2005','2006','2007','2011','2014','2017')
	"""

	db.cursor.execute(sql,date)
	row = db.cursor.fetchone()
	data = {}
	while row :
		data[row[0]] = row
		row = db.cursor.fetchone() 
	return data

def get_large_loss_cs(db):
	sql =u"""
	 select SJLX, JYJE
  	 from T_JGC_JXKH_CS_LIUSHI
	"""
	db.cursor.execute(sql)
	row = db.cursor.fetchone()
	data = {}
	while row :
		data[row[0]] = row[1]
		row = db.cursor.fetchone() 
	return data

"""
大额存款流失
""" 
def large_ck_loss(db,etldate):
	print etldate
	tdata = get_ck_dict(db,etldate)#今日
	ydate=int(util.daycalc(etldate,-1))#昨日
	ydata = get_ck_dict(db,ydate)
	cs = get_large_loss_cs(db)	
	balance = 0
	rs =[]
	for item in tdata:
		if not ydata.has_key(item):
			balance = 0
		else:
			balance = ydata[item][1]#昨日余额
		row = tdata[item]
		sqye = balance*0.01#昨日余额
		bal = balance-row[1]#昨日余额-今日余额
		balance =  abs(balance-row[1])
		if row[11] == '1' and balance>cs['1']*100:#对私
			rs.append(insertdata(row,bal,etldate,'1',sqye))
		if row[11] == '2' and balance>cs['2']*100:#对公
			rs.append(insertdata(row,bal,etldate,'1',sqye))
  	if len(rs)>0:
		insert2db(db,rs)
	rs = []
			
		
"""
大额贷款流失
""" 
def large_dk_loss(db,etldate):
	tdata = get_dk_dict(db,etldate)
	ydate=int(util.daycalc(etldate,-1))
	ydata = get_dk_dict(db,ydate)
	cs = get_large_loss_cs(db)	
	balance = 0
	rs =[]
	for item in tdata:
		if not ydata.has_key(item):
			balance = 0
		else:
			balance = ydata[item][1]
		row = tdata[item]
		sqye = balance*0.01
		bal = balance-row[1]
		balance = abs(balance-row[1])
		if row[10] == '1' and balance>cs['4']*100:#单位贷款
			rs.append(insertdata(row,bal,etldate,'2',sqye))
		if row[10] == '2' and balance>cs['3']*100:#私人贷款
			rs.append(insertdata(row,bal,etldate,'2',sqye))
  	if len(rs)>0:
		insert2db(db,rs)
	rs = []
				
	
def large_loss(etldate):
	try :
		db = util.DBConnect()
		delete_liushi(db,etldate)
		large_ck_loss(db,etldate)
		large_dk_loss(db,etldate)
		db.conn.commit()
	finally :
		db.closeDB()
def days(startdate,enddate):
	etldate=int(startdate)
	enddate=int(enddate)
	while etldate <= enddate:
		large_loss(etldate)
		etldate=int(util.daycalc(etldate,1))
	

if __name__=='__main__':
	arglen=len(sys.argv)
	if arglen  == 3:
		days(sys.argv[1],sys.argv[2])
	else :
		print "please input python large_loss.py YYYYMMDD YYYYMMDD "
