# -*- coding:utf-8 -*-
#!/bin/python  
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random  
from datetime import datetime,timedelta
from decimal import *
import DB2  
from  etl.star.logger  import info , debug , error
import etl.star.util as util
from etl.star.conf import Config



class Performancesummary():
	def __init__(self,etldate=None):
		self.db =util.DBConnect()
		self.etldate=etldate
		self.stretldate =util.tostrdate(self.etldate) 
		self.para=util.get_common_parameter(self.db)
		if etldate is not None : self.para['TJRQ']=etldate

	"""
	薪酬汇总
	"""
	def xchz(self):
		xc_rs=self.get_xc_rs()
		res=[]
		for r in xc_rs:
			d={}
			d['TJRQ']=r[0]
			d['TJZQ']=r[1]
			d['YGGH']=r[2]
			d['JGBH']=r[3]
			d['JGMC']=r[4]
			d['JE1']=r[5]	
			d['JE2']=r[6]
			d['JE6']=r[7]
			d['JE8']=r[8]
			d['JE13']=r[9]
			d['JE14']=r[10]
			d['JE15']=r[11]
			d['JE16']=r[12]
			d['JE17']=r[13]
			d['JE18']=r[14]
			d['JE19']=r[15]
			d['JE20']=r[16]
			d['JE21']=r[17]
			d['JE22']=r[18]
			d['JE23']=r[19]
			d['JE11']=r[20]
			d['KHLX']=r[21]
			res.append(d)
		for r in res: #汇总计算
			pass
			"""
			r['GRWY']=r['JE13']+r['JE14']
			r['SJYH']=r['JE14']+r['JE16']
			r['QYWY']=r['JE17']+r['JE18']
			r['POS']=r['JE20']+r['JE21']
			r['ZJYW']=r['GRWY']+r['SJYH']+r['QYWY']+r['POS']+r['JE19']
			r['XCZE']=r['JE1']+r['JE2']+r['JE6']+r['JE8']+r['JE11']+r['ZJYW']
			#改名赋值
			r['JE34']=r['XCZE']
			r['JE9']=r['GRWY']
			r['JE10']=r['SJYH']
			r['JE12']=r['QYWY']
			r['JE32']=r['POS']
			r['JE33']=r['ZJYW']
			"""	

		#self.update_insert_jx(res)#更新薪酬或插入

	def update_insert_jx(self,rs):
		update_l=[]
		insert_l=[]
		sql=u"""
		select * from T_JGC_JXKH_JX_QM where YGGH=? and TJRQ=? and TJZQ=? and JGBH=? and KHLX=?
		"""
		for r in rs :
			self.db.cursor.execute(sql,(r['YGGH'],r['TJRQ'],r['TJZQ'],r['JGBH'],str(r['KHLX'])))
			row = self.db.cursor.fetchone()
			if row is None :
				insert_l.append((r['TJRQ'],r['YGGH'],r['JE34'],r['JE9'],r['JE10'],r['JE12'],r['JE32'],r['JE33'],r['TJZQ'],r['JGBH']))

			else :
				update_l.append((r['JE34'],r['JE9'],r['JE10'],r['JE12'],r['JE32'],r['JE33'],r['TJRQ'],r['YGGH'],r['TJZQ'],r['JGBH'],r['KHLX']))
		if len(insert_l)>0:
			self.insert_jx_db(insert_l)
		if len(update_l)>0:
			self.update_jx_db(update_l)	


	def insert_jx_db(self,r):
		sql=u"""
		insert into T_JGC_JXKH_JX_QM (TJRQ,YGGH,JE34,JE9,JE10,JE12,JE32,JE33,TJZQ,JGBH) values(?,?,?,?,?,?,?,?,?,?)
		"""
		self.db.cursor.executemany(sql,r)
		self.db.conn.commit()
	def update_jx_db(self,r):
		sql=u"""
		update T_JGC_JXKH_JX_QM set JE34=?,JE9=? ,JE10=?,JE12=? ,JE32=?,JE33=?  where YGGH=? and TJRQ=? and TJZQ=? and JGBH=? and KHLX=?
		"""			
		self.db.cursor.executemany(sql,r)
		self.db.conn.commit()		
	





	"""
	获取薪酬数据
	"""
	def get_xc_rs(self):
		sql=u"""
		select tjrq,tjzq,YGGH,YGXM,JGBH,JGMC,je1,je2,je6,je8,je13,je14,je15,je16,je17,je18,je19,je20,je21,je22,je23,je11,khlx
from T_JGC_JXKH_JX_QM 
where tjrq ='%s' order by YGGH asc , JGBH asc
		"""%(self.stretldate)
		rs = util.get_select_row(self.db,sql)
		if rs is None :
			error(u'薪酬汇总无数据')
			exit()
		return rs




	def run_xchz(self):
		try :
			self.xchz()#薪酬汇总
			self.db.conn.commit()

		finally :
			self.db.closeDB()
	
	def run(self):
		self.run_xchz()
	






"""
薪酬汇总
"""
if __name__ == "__main__":
	arglen=len(sys.argv)
	if arglen  == 2:
		Performancesummary(sys.argv[1]).run()
	else :
		print "please input python Performancesummary.py YYYYMMDD "




