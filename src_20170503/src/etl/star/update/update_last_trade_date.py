# -*- coding:utf-8 -*-
#!/bin/python  
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random  
from datetime import datetime,timedelta
from decimal import *
import DB2  
import csv

import etl.base.util as util
from etl.base.conf import Config
	 
condecimal = getcontext()
"""
	更新F_CONTRACT_STATUS表上的LAST_TRADE_DATE字段，用于判断是否活跃
"""
def update(db,etldate,trantype,filename):
	d1 = datetime.now()
	print str(etldate)+" "+trantype+" start",d1

	targetfile = Config().data_path+"/%s/ADD/%s_%s_ADD_%s.del"%(etldate,filename,etldate,Config().branch_code)
	targethandler = file(targetfile, 'r')
	targethandler_csv=csv.reader(targethandler)
	update_data=[]
	for row in targethandler_csv:
		#u_sql = u"update F_CONTRACT_STATUS set LAST_TRADE_DATE= %s where contract_id=(select ID from D_CUST_CONTRACT where net_cst_no= %s and busi_type='%s') and date_id = %s"%(etldate,row[2],trantype,etldate)
		#db.cursor.execute(u_sql.encode('utf-8'))
		#print row int(row[0][0:8])
		update_data.append((etldate,row[2],str(trantype.encode('utf-8')),etldate))

	uu_sql = u"update F_CONTRACT_STATUS set LAST_TRADE_DATE= ? where contract_id=(select ID from D_CUST_CONTRACT where net_cst_no= ? and busi_type= ? ) and date_id = ?".encode('utf-8')
	db.cursor.executemany(uu_sql,update_data)
	d2 = datetime.now()
	print str(etldate)+" "+trantype+" end",d2-d1
		
def update_ltd(startdate,enddate):
	try :
		db = util.DBConnect()
		etldate=startdate
		while int(etldate) <= int(enddate):
			m_sql ="""
			merge into F_CONTRACT_STATUS f1 
			using F_CONTRACT_STATUS f2 on f1.contract_id = f2.contract_id and f2.date_id= ? and f1.date_id= ?
			when matched then update set f1.last_trade_date=f2.last_trade_date
			"""
			db.cursor.execute(m_sql,int(util.daycalc(etldate,-1)),etldate)
	
			update(db,etldate,u'手机银行',u'IBS_MB_PB_TRANFLOW')
			update(db,etldate,u'企业网上银行',u'IBS_CB_TRANFLOW')
			update(db,etldate,u'个人网上银行',u'IBS_PB_TRANFLOW')
			etldate=int(util.daycalc(etldate,1))
		db.conn.commit()
	finally :
		db.closeDB()

if __name__=='__main__':
	update_ltd(20141201,20141231)
