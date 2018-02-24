# -*- coding:utf-8 -*-
#!/bin/python  
import os,sys
import os, time, random  
from datetime import datetime,timedelta
from decimal import *
import DB2  

import etl.base.util as util
from etl.performance.util import common

	 
condecimal = getcontext()


class Zjc2Ifs():
	def __init__(self):
		self.col = {'table':"BPAPP.IFS_SALE_ACCT_RELA",'cols':['ID','TYPE','SALE_ID','SALE_CODE','ACCT_ID','START_DT','END_DT','PERCENT','SALE_ROLE','MANUAL','ORG_CODE','FLAG'],'insert_cols':['DATE_ID'],'update_cols':['UP_DATE_ID','REL_UP_DATE'],'key':['ID']}
		#self.db = util.DBConnect()
		pass

	def run(self):
		try :
			self.db = util.DBConnect()
			print "ck_start"
			self.transfer_ck()
			print "dk_start"
			self.transfer_dk()
			self.after_transfer()
			self.db.conn.commit()
		finally :
			self.close()
	def get_rela(self,sql):
		self.db.cursor.execute(sql)
		return  self.db.cursor.fetchall()
	
	def after_transfer(self):
		ck_sql = """update t_zjc_gsgx_ck set newflag ='1' where newflag!='1' """
		self.db.cursor.execute(ck_sql)
		
		dk_sql = """update t_zjc_gsgx_dk set newflag ='1' where newflag!='1' """
		self.db.cursor.execute(dk_sql)
	
		self.db.conn.commit()
	
	"存款归属_转换"
	def transfer_ck(self):
		sql = u"""
			select PARA_ID,JGBH,DRRQ,DXBH,GLDXBH,GLJE1,GLRQ1,GLRQ2,CK_TYPE,(case when CK_TYPE = '派生' then '7' else '1' end),'是','01'
			from t_zjc_gsgx_ck
			where newflag = '0'
		""".encode('gb2312')
		dep_rela = self.get_rela(sql)
		print "rela len ",len(dep_rela)
		rs=[]
		for row in dep_rela:
			data = {}
			tr_dict = {'ID':0,'ORG_CODE':1,'DATE_ID':2,'UP_DATE_ID':2,'REL_UP_DATE':2,'ACCT_ID':3,'SALE_CODE':4,'SALE_ID':4,
				'PERCENT':5,'START_DT':6,'END_DT':7,'SALE_ROLE':8,'TYPE':9,'MANUAL':10,'FLAG':11}
			for k,v in tr_dict.items():
				data[k] = row[v]
			data['SALE_ID'] = int(data['SALE_ID'])
			rs.append(data)
		if len(rs)>0:
			common.insert_update(self.db,rs,self.col)
		
	"贷款归属_数据转换"
	def transfer_dk(self):
		sql = u"""
			select PARA_ID,JGBH,DRRQ,DXBH,GLDXBH,GLJE1,GLRQ1,GLRQ2,'管户','3','是','01'
			from t_zjc_gsgx_dk
			where newflag = '0'
		""".encode('gb2312')
		dk_rela = self.get_rela(sql)
		print "rela len ",len(dk_rela)
		rs=[]
		for row in dk_rela:
			data = {}
			tr_dict = {'ID':0,'ORG_CODE':1,'DATE_ID':2,'UP_DATE_ID':2,'REL_UP_DATE':2,'ACCT_ID':3,'SALE_CODE':4,'SALE_ID':4,
				'PERCENT':5,'START_DT':6,'END_DT':7,'SALE_ROLE':8,'TYPE':9,'MANUAL':10,'FLAG':11}
			for k,v in tr_dict.items():
				data[k] = row[v]
			data['SALE_ID'] = int(data['SALE_ID'])
			rs.append(data)
		if len(rs)>0:
			common.insert_update(self.db,rs,self.col)


	def close(self):
		self.db.conn.commit()
		self.db.closeDB()
if __name__=='__main__':
	Zjc2Ifs().run()
