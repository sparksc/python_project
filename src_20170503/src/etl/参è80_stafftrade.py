# -*- coding:utf-8 -*-
#!/bin/python  
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random  
from datetime import datetime,timedelta
from decimal import *
import DB2  

from etl.star.logger import info,debug,error
import etl.star.util as util
from etl.star.conf import Config
	



class Stafftrade():
	def __init__(self,etldate=None):
		self.db =util.DBConnect()
		self.etldate=etldate
		self.stretldate =util.tostrdate(self.etldate) 
		self.para=util.get_common_parameter(self.db)
		if etldate is not None : self.para['TJRQ']=etldate

	"""
	柜员业务量
	"""
	def gyywl(self,temp_rs):
		rs=[]
		for r in temp_rs :
			d={}
			d['SALE_CODE']=r[0]
			d['TRAN_CODE']=r[1]
			d['TRAN_NUM']=r[2]
			d['CS']=r[3]
			d['ZBLX']=r[4]
			d['DATE_ID']=r[5]
			d['ZHYWL']=r[3]*r[2]  
			rs.append(d)
		#分组求和
		d={}
		for r in rs :
			key=str(r['SALE_CODE'])+'|'+str(r['ZBLX'])+'|'+str(r['DATE_ID'])
			if d.get(key) is None :
				d[key]={'YWL':r['TRAN_NUM'],'ZHYWL':r['ZHYWL']}
			else :
				d[key]['YWL']=d[key]['YWL']+r['TRAN_NUM']
				d[key]['ZHYWL']=d[key]['ZHYWL']+r['ZHYWL']
		res=[]
		for r in d :
			dic={}	
			dic['SALE_CODE']=r.split('|')[0]
			dic['ZBLX']=r.split('|')[1]
			dic['DATE_ID']=r.split('|')[2]
			dic['YWL']=d[r]['YWL']
			dic['ZHYWL']=d[r]['ZHYWL']
			res.append(dic)		
		self.update_insert_jx(res)#复核柜员业务量入库
		
	
			


	"""
	数据库更新或插入
	"""
	def update_insert_jx(self,rs):
		update_l=[]
		insert_l=[]
		sql=u"""
		select * from T_STAFF_TRADE_HZ where SALE_CODE=? and ZBLX=? and DATE_ID=? 
		"""
		for r in rs :
			self.db.cursor.execute(sql,(r['SALE_CODE'],r['ZBLX'],int(r['DATE_ID'])))
			row = self.db.cursor.fetchone()
			if row is None :
				insert_l.append((r['YWL'],r['ZHYWL'],r['SALE_CODE'],r['ZBLX'],int(r['DATE_ID'])))

			else :
				update_l.append((r['YWL'],r['ZHYWL'],r['SALE_CODE'],r['ZBLX'],int(r['DATE_ID'])))
			
		if len(insert_l)>0:
			self.insert_jx_db(insert_l)
		if len(update_l)>0:
			self.update_jx_db(update_l)	


	def insert_jx_db(self,r):
		sql=u"""
		insert into T_STAFF_TRADE_HZ (YWL,ZHYWL,SALE_CODE,ZBLX,DATE_ID) values(?,?,?,?,?)
		"""
		self.db.cursor.executemany(sql,r)
		self.db.conn.commit()
	def update_jx_db(self,r):
		sql=u"""
		update T_STAFF_TRADE_HZ set YWL=?,ZHYWL=?  where SALE_CODE =? and ZBLX=? and DATE_ID=?
		"""			
		self.db.cursor.executemany(sql,r)
		self.db.conn.commit()		
	







	def get_fh_ywl(self):
		sql=u"""
		select trim(sale_code) sale_code ,TRAN_CODE,sum(tran_num) tran_num,nvl(j.JE1,0) cs,'复核柜员业务量' ZBLX ,%s date_id
from m_staff_tran t
left join t_jgc_cs j on t.tran_code = j.dxbh and cslx='6'
where  manage_type='柜员操作' and relaction_type='复核柜员' and date_id = %s
group by sale_code,tran_CODE,j.JE1
order by sale_code
		"""%(self.para['TJRQ'],self.para['TJRQ'])#使用ydw测试
		rs = util.get_select_row(self.db,sql.encode('gb2312'))	
		if rs is None :
			error('复核柜员业务量为0')
			exit()
		return rs

	def get_cz_ywl(self):
		sql=u"""
		select trim(sale_code) sale_code ,TRAN_CODE,sum(tran_num) tran_num,nvl(j.JE1,0) cs,'操作柜员业务量' ZBLX ,%s date_id
from m_staff_tran t
left join t_jgc_cs j on t.tran_code = j.dxbh and cslx='6'
where   relaction_type='操作柜员' and date_id = %s
group by sale_code,tran_CODE,j.JE1
order by sale_code
		"""%(self.para['TJRQ'],self.para['TJRQ'])#使用ydw测试
		rs = util.get_select_row(self.db,sql.encode('gb2312'))	
		if rs is None :
			error('操作柜员业务量为0')
			exit()
		return rs




	def run_gyywl(self):
		try :
			rs=self.get_fh_ywl()
			self.gyywl(rs)#复核柜员业务量
			rs=self.get_cz_ywl()
			self.gyywl(rs)#操作柜员业务量	
			self.db.conn.commit()

		finally :
			self.db.closeDB()
	
	def run(self):
		self.run_gyywl()
	




"""
柜员业务量(操作柜员和复核柜员)
"""
if __name__ == "__main__":
	arglen=len(sys.argv)
	if arglen  == 2:
		Stafftrade(sys.argv[1]).run()
	else :
		print "please input python gyywl.py YYYYMMDD "




