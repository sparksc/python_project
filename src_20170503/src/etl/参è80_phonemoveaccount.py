# -*- coding:utf-8 -*-
#!/bin/python 
import os,sys
import os, time, random
from datetime import datetime,timedelta
from decimal import *
from etl.star.conf import Config
import DB2

import etl.star.util as util
def get_android_mx_data(db,etldate):
	mx_sql = """
	select d.CONTRACT_KEY,count(1) from F_TRANSACTION C 
	inner join d_contract d  on d.id = c.contract_id
	inner join D_TRAN_TYPE dt on C.TRAN_TYPE_ID = dt.id and dt.tran_status =1 and dt.TRAN_CODE IN ('021001','021003','021004','021005') and dt.CHANNEL = '1002' 
	and C.DATE_ID = ? and C.TRAN_CLASSIFY = 'A'
	group by d.CONTRACT_KEY
	"""
	db.cursor.execute(mx_sql,etldate)
	row = db.cursor.fetchone()
	d={}
	while row:
		d[row[0].strip()] = row[1]
		row = db.cursor.fetchone()
	return d
def get_iphone_mx_data(db,etldate):
	mx_sql = """
	SELECT d.CONTRACT_KEY,count(1) from  F_TRANSACTION c
	inner join d_contract d  on d.id = c.contract_id
	inner join D_TRAN_TYPE dt on dt.id = c.tran_type_id 
	and  c.date_id = ? and C.TRAN_CLASSIFY = 'H'
	group by d.CONTRACT_KEY
	"""
	db.cursor.execute(mx_sql,etldate)
	row = db.cursor.fetchone()
	d={}
	while row:
		d[row[0].strip()] = row[1]
		row = db.cursor.fetchone()
	return d

def get_phone_num(db,etldate,classify):
	if classify == 'A':
		fh_num_sql = u"""
		select sum(android_num) phone_sum,ORG_CODE
		from M_EBANK_INFO
		where date_id = ? and contract_classify = 'A' and open_date <= ?  and (close_date >= ? or close_date=0) 
		and contract_status = '正常'
		group by ORG_CODE
		with ur	
		"""
	elif classify == 'I':
		fh_num_sql = u"""
		select sum(apple_num) phone_sum,ORG_CODE
		from M_EBANK_INFO
		where date_id = ? and contract_classify = 'I' and open_date <= ?  and (close_date >= ? or close_date=0) 
		and contract_status = '正常'
		group by ORG_CODE
		with ur	
		"""
	db.cursor.execute(fh_num_sql.encode('gb2312'),etldate,etldate,etldate)
	row = db.cursor.fetchone()
	d = {}
	while row :
		d[row[1].strip()] = int(row[0])			
		row = db.cursor.fetchone()
	return d

def get_cust_trantime(db,etldate,classify):
	lastdate = int(str(etldate)[0:4] + '0101')	
	sel_sql = """
	select sum(TRANTIME),ORG_CODE,CONTRACT_KEY from T_JGC_AZ_DHS where DATE_ID <= ? and DATE_ID >=? and CONTRACT_CLASSIFY = ? group by ORG_CODE,CONTRACT_KEY
	"""
	db.cursor.execute(sel_sql,etldate,lastdate,classify)
	row = db.cursor.fetchone()
	d={}
	while row:
		d[row[2]] = row
		row = db.cursor.fetchone()
	return d	
def insert_dhs(db,etldate,classify):
	db1 =  util.DBConnect()
	fh_sql = """
	select  A.ORG_CODE,A.CUST_NO 
	from  D_CONTRACT A 
	where A.CONTRACT_KEY = ?
	"""
	del_sql = """
	delete from T_JGC_AZ_DHS where DATE_ID = ? and CONTRACT_CLASSIFY = ?
	"""
	insert_sql ="""
	insert into T_JGC_AZ_DHS(DATE_ID,CUST_NO,ORG_CODE,CONTRACT_KEY,TRANTIME,CONTRACT_CLASSIFY) 
	values(?,?,?,?,?,?)
	"""
	if classify =='A':
		mx_data = get_android_mx_data(db,etldate)
	elif classify =='I':
		mx_data = get_iphone_mx_data(db,etldate)
	else:
		pass
	db1.cursor.execute(del_sql,etldate,classify)
	for key,data in mx_data.items():
		db.cursor.execute(fh_sql,key)
		row = db.cursor.fetchone()
		db1.cursor.execute(insert_sql,etldate,row[1].strip(),row[0].strip(),key,data,classify)
	db1.conn.commit()
	db1.closeDB()

def clac_rate(db,etldate,classify):
	insert_dhs(db,etldate,classify)
	cust_trantime = get_cust_trantime(db,etldate,classify)
	d_org = {}
	for key,value in cust_trantime.items():
		if int(value[0]) >= 4:
			rs = d_org.get(value[1].strip())
			if rs is None:
				d_org[value[1].strip()] = 0 
			d_org[value[1].strip()] = d_org[value[1].strip()] + 1
	return d_org

def delete_jgzb(db,etldate,name):
	deletesql = u"""
	delete from t_jgc_jgzb where date_id = ? and zblx = ?
	"""
	db.cursor.execute(deletesql.encode('gb2312'),etldate,name)
	db.conn.commit()
	
def android_move_account_rate(db,etldate):	
	db1 =  util.DBConnect()
	insql = u"""
	insert into t_jgc_jgzb(date_id,org_code,zblx,je1,je2) values(?,?,?,?,?)	
	"""
	delete_jgzb(db,etldate,u'安卓手机动户率'.encode('gb2312'))
	phone_live_num = clac_rate(db,etldate,'A')
	phone_num = get_phone_num(db,etldate,'A')
	for key,value in phone_live_num.items():
		org_code = key
		je1 = value*1.0 /phone_num.get(org_code)
		db1.cursor.execute(insql.encode('gb2312'),etldate,org_code,u'安卓手机动户率'.encode('gb2312'),je1,0.0)
	db1.conn.commit()
	db1.closeDB()

def iphone_move_account_rate(db,etldate):	
	db1 =  util.DBConnect()
	insql = u"""
	insert into t_jgc_jgzb(date_id,org_code,zblx,je1,je2) values(?,?,?,?,?)	
	"""
	delete_jgzb(db,etldate,u'苹果手机动户率'.encode('gb2312'))
	phone_live_num = clac_rate(db,etldate,'I')
	phone_num = get_phone_num(db,etldate,'I')
	for key,value in phone_live_num.items():
		org_code = key
		je1 = value*1.0 /phone_num.get(org_code)
		db1.cursor.execute(insql.encode('gb2312'),etldate,org_code,u'苹果手机动户率'.encode('gb2312'),je1,0.0)
	db1.conn.commit()
	db1.closeDB()
def all_move_account_rate(db,etldate):	
	db1 =  util.DBConnect()
	sel_sql = """
	select distinct org_code from M_EBANK_INFO
	"""
	db.cursor.execute(sel_sql)
	org_code = []
	row = db.cursor.fetchone()
	while row:
		org_code.append(row[0].strip())
		row = db.cursor.fetchone()
	insql = u"""
	insert into t_jgc_jgzb(date_id,org_code,zblx,je1,je2) values(?,?,?,?,?)	
	"""
	delete_jgzb(db,etldate,u'苹果手机动户率'.encode('gb2312'))
	iphone_live_num = clac_rate(db,etldate,'I')
	iphone_num = get_phone_num(db,etldate,'I')
	android_phone_live_num = clac_rate(db,etldate,'A')
	android_phone_num = get_phone_num(db,etldate,'A')
	all_phone_live_num = {}
	all_phone_num = {}
	for key in org_code:
		all_phone_num[key] = iphone_num.get(key,0) + android_phone_num.get(key,0)
		all_phone_live_num[key] = iphone_live_num.get(key,0) + android_phone_live_num.get(key,0) 
	for key,value in all_phone_live_num.items():
		org_code = key
		je1 = value*1.0 /all_phone_num.get(org_code)
		db1.cursor.execute(insql.encode('gb2312'),etldate,org_code,u'总手机动户率'.encode('gb2312'),je1,0.0)
	db1.conn.commit()
	db1.closeDB()

def phone_move_account_rate(etldate):
	try:
		db =  util.DBConnect()
		android_move_account_rate(db,etldate)
		iphone_move_account_rate(db,etldate)
		all_move_account_rate(db,etldate)
	finally:
		db.closeDB()
if __name__=='__main__':
	etldate = 20160115
	while etldate <= 20160201:
		print etldate
		phone_move_account_rate(etldate)
		etldate = int(util.daycalc(etldate,1))
