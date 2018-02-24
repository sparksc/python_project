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


class Ifs2Zjc():
	def __init__(self):
		self.ck_col = {'table':"T_ZJC_GSGX_CK",'cols':['JGBH','DRRQ','DXBH','DXXH','GLDXBH','FJDXBH','GLJE1','GLRQ1','GLRQ2','PARA_ID','CK_TYPE','NEWFLAG'],'key':['PARA_ID']}
		self.dk_col = {'table':"T_ZJC_GSGX_DK",'cols':['JGBH','DRRQ','DXBH','DXXH','GLDXBH','FJDXBH','GLJE1','GLRQ1','GLRQ2','PARA_ID','NEWFLAG'],'key':['PARA_ID']}
		#self.db = util.DBConnect()
		pass

	def run(self):
		try :
			self.db = util.DBConnect()
			print "ck_start"
			self.transfer_ck()
			print "dk_start"
			self.transfer_dk()
			self.db.conn.commit()
		finally :
			self.close()
	def get_ifs_rela(self,sql):
		self.db.cursor.execute(sql)
		return  self.db.cursor.fetchall()
	
	"存款归属_数据转换"
	def transfer_ck(self):
		sql = u"""
			select org_code,date_id,acct_id,'0',sale_code,acct_id,percent,start_dt,end_dt,id,sale_role,'1'
			from bpapp.IFS_SALE_ACCT_RELA where type in (1,7) 
			and flag!='00'
		""".encode('gb2312')
		ifs_dep_rela = self.get_ifs_rela(sql)
		print "rela len ",len(ifs_dep_rela)
		rs=[]
		for row in ifs_dep_rela:
			data = {}
			idx =0
			for it in self.ck_col['cols']:
				data[it] = row[idx]
				if data[it] == None:
					print row
					data[it] = '--'
				idx = idx+1
			rs.append(data)
		if len(rs)>0:
			common.insert_update(self.db,rs,self.ck_col,"I")
		
	"贷款归属_数据转换"
	def transfer_dk(self):
		sql = u"""
			select org_code,date_id,acct_id,'0',sale_code,acct_id,percent,start_dt,end_dt,id,'1'
			from bpapp.IFS_SALE_ACCT_RELA where type in (3) and sale_role = '管户' 
			and flag!='00'
		""".encode('gb2312')
		ifs_rela = self.get_ifs_rela(sql)
		print "rela len ",len(ifs_rela)
		rs=[]
		for row in ifs_rela:
			data = {}
			idx =0
			for it in self.dk_col['cols']:
				data[it] = row[idx]
				if data[it] == None:
					data[it] = '--'
				idx = idx+1
			rs.append(data)
		if len(rs)>0:
			common.insert_update(self.db,rs,self.dk_col,"I")


	def close(self):
		self.db.conn.commit()
		self.db.closeDB()
if __name__=='__main__':
	Ifs2Zjc().run()
