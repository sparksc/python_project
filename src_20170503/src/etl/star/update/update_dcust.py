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
	print "start ",d1
	s_sql ="""
		select d.id,CUNAFLNM, AOIDBRNO,CUIDCSID from ODS.CORE_BCFMCMBI c
		inner join d_cust d on  c.CINOCSNO=d.cust_no and  CUNAFLNM is not null and  AOIDBRNO is not null and  CUIDCSID is not null
	"""
	db.cursor.execute(s_sql)
	d = {}
	row = db.cursor.fetchone()
	while row:
		d[row[0]] = row	
		row = db.cursor.fetchone()
	
	
	u_sql = "update d_cust set CUST_NAME =?,OWNER_ORG_CODE=?,CST_LONG_NO=? where id=?"
	rs = []
	idx = 0
	for row in d.values():
		rs.append ( (row[1],row[2],row[3],row[0] ) )
		idx = idx + 1
                if idx >= 1000 :
			print "1000",datetime.now()-d1
                        db.cursor.executemany ( u_sql , rs )
                        rs = []
			idx = 0
                        db.conn.commit()
	if len(rs) != 0 :
		db.cursor.executemany ( u_sql , rs )
		db.conn.commit()
                rs = []
		
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
