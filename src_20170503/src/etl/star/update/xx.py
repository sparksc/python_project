# -*- coding:utf-8 -*-
#!/bin/python  
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random  
from datetime import datetime,timedelta
from decimal import *
import DB2  

import etl.base.util as util
from etl.base.conf import Config
	 
condecimal = getcontext()
"""
"""
def update(db):
	d1 = datetime.now()
	
	u_sql = "update T_SJPB_KHJL_JXZB set TJNF = ?,TJYF = ?,JGBH = ?,JGMC = ?,YGBH = ?,YGMC = ?,PRI_LOAN_STOCK_NUM = ? where TJNF = ? and TJYF = ? and JGBH = ? and YGBH = ?"
        db.cursor.executemany(u_sql , [[2013, 12, '999190', '999190', '9990399', '\xeb\xf8\xd7\xd4\xc7\xbf            ', None, 2013, 12, '999190', '9990399'],[2013, 12, '999190', '999190', '9990399', '\xeb\xf8\xd7\xd4\xc7\xbf            ', None, 2013, 12, '999190', '9990399']])
        db.conn.commit()
		
def update_dcust():
	try :
		db = util.DBConnect()
		update(db)
		db.conn.commit()
	finally :
		db.closeDB()

if __name__=='__main__':
	update_dcust()
	#update_dxxh_no()
