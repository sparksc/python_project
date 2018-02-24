# -*- coding:utf-8 -*-
#!/bin/python  
import sys
import csv 
import os, time, random  
from datetime import datetime,timedelta
from decimal import *
import DB2  

from etl.base.conf import DSN,PASSWD,USER
import etl.base.util as util
from etl.performance.util import common
from etl.base.oradbconn import session
	 
condecimal = getcontext()


class Ora2Db():
	def __init__(self):
		self.tmppath = """/tmp/xinchang/"""
		if not os.path.exists(self.tmppath):
			os.mkdir(self.tmppath)
		#self.db = util.DBConnect()
		pass

	def run(self,etldate):
		try :
			self.db = util.DBConnect()
			
			cols = [{
				'table':'T_JGC_HMT_CKMX',
				'cols':['TJRQ','SJLX','JYRQ','ZH','HM','JGBH','DQRQ','KMBH','TZRQ','QX','CPLX','RQYE','LL','LXSR_YS','LXSRLJ_YS','FTP','FTP_TZ','LCSR','LCSR_NLJ','SCLX','SCLX_LJ'],
				'filter':['TJRQ'],
				'merge':{'YJFX':'RISK_AMOUNT'}},
				{
				'table':'T_JGC_HMT_DKMX',
				'cols':['TJRQ','SJLX','JYRQ','ZH','HM','JGBH','DQRQ','KMBH','KHRQ','QX','CPLX','RQYE','LL','LXZC_YF','LXZCLJ_YF','FTP','FTP_TZ','LCSR','LCSR_NLJ','SCLX','SCLX_LJ'], 
				'filter':['TJRQ'],
				'merge':{'YJFX':'RISK_AMOUNT'}},
			]
			"""
			for col in cols:
				self.transfer(col,{'TJRQ':util.tostrdate(etldate)})
			"""
			self.load_data(cols)

			for col in cols:
				self.mergeinto(col)
			
			self.truncate_data(cols)
			self.db.conn.commit()
		finally :
			self.close()
	"""清除中间表"""
	def truncate_data(self,cols):
		for name in cols:
			sql ="""
			truncate table %s immediate
			"""%name['table']
			self.db.cursor.execute(sql)
			self.db.conn.commit()
		
			
	"""更新f_balcance 的字段"""
	def mergeinto(self,col,etldate):
		upsql = ""
		for k,v in col['merge']:
			upsql = upsql +",f.%s=int(t.%s*100)"%(k,v)
	
		sql = u"""
			merge into F_BALANCE f
			using  d_account a on f.account_id = a.id 
			innner join  %s t on t.DXBH=a.account_no and f.date_id = ? 
			when matched then update set %s
		"""%(col['table'],upsql)
		self.db.cursor.execute(sql,etldate)
			
			
		
		
	"""通过load加入db2数据库,为了效率,未测试"""
	def load_data(self,tables):
		file = self.tmppath + "load.sql"
		if os.path.exists(file) : os.remove(file)
		newfile= open(file, 'w')
		newfile.write(" connect to %s user %s using %s ;"%(DSN,USER,PASSWD))
		for table in tables:
			file2 = self.tmppath +"%s.del"%table['table']

			if not os.path.exists(self.tmppath+"log"):
				os.mkdir(self.tmppath+"log")
			logfile2  = self.tmppath +"log/%s.log"%table['table']
			load="\n load client from %s of del MESSAGES %s insert into %s;"%(file2,logfile2, table['table'])
			newfile.write(load)
		newfile.write("\n terminate;")
		newfile.close()

		runbatfile = self.tmppath + "load.sh"
		if os.path.exists(runbatfile) : os.remove(runbatfile)
		runbat= open(runbatfile, 'w')
		runbat.write("\n db2 -tvf %s"%(file))
		runbat.write("\n exit")
		runbat.close()
		os.system(" sh  "+runbatfile) 
	
		for table in tables:
			file2 = self.tmppath +"%s.del"%table
			if os.path.exists(file2) : os.remove(file2)


	def get_sel_sql(self,col):
                cols = u""
                pars = u""
                for it in col['cols']:
                        cols = cols + ',' + it
		for it in col['filter']:
			pars = pars +'and %s = :%s'%(it,it)
                sql = u"""
                        select %s
			from %s
                        where 1 = 1 %s 
                """%(cols[1:],col['table'],pars)
                return sql

	
	
	"取oracle数据，写成文本"	
	def transfer(self,cols,cond):
		filepath = self.tmppath+"%s.del"%cols['table']

		outfile = file(filepath, 'w')
		outfile_csv=csv.writer(outfile)
		sql = self.get_sel_sql(cols).encode('gb2312')
		result = session.execute(sql,cond) 
		rowdata = result.fetchall()
		for row in rowdata:
			#ls = self.trans(row)
			outfile_csv.writerow(row)
		outfile.close()
		return cols['table']
	"数据列格式装换"	
	def trans(self,row):
		rs = []
		for it in row:
			if isinstance(it,float):
				rs.append(int(it*100))
			else:
				rs.append(it)
		return tuple(rs)

	def close(self):
		self.db.conn.commit()
		self.db.closeDB()
if __name__=='__main__':
	Ora2Db().run(20141203)
