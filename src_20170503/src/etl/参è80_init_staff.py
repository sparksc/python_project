
import os, time, random,sys
import DB2
from datetime import datetime,timedelta
from decimal import *
import  etl.star.util  as util
from etl.star.conf import *
from etl.star.transformdict import *
from etl.star.singleton import singleton
from etl.star.logger import info



class Staff():
	def __init__(self,etldate):
		self.db = util.DBConnect()
		self.strdate = str(etldate[0:4])+"-"+str(etldate[4:6])+"-"+str(etldate[6:8])


	def run(self):
		try:
			self.delete_staff()
			self.import_staff()
		
		finally:
			self.db.closeDB()

	def delete_staff(self):
		
		self.db.cursor.execute("delete from password")
		self.db.cursor.execute("delete from user_group")
		self.db.cursor.execute("delete from factor")
		self.db.cursor.execute("delete from user_session")
		self.db.cursor.execute("delete from AUTHENTICATION")
		self.db.cursor.execute("delete from f_user")
		self.db.conn.commit()
		

	def import_staff(self):
		sql=u"""
		select gyh,xm,jgm,LXDH from ods.gyxxb_his  where tjrq='%s'  and jgm in (select  branch_code  from branch)
		"""%self.strdate

		self.db.cursor.execute(sql)
		row = self.db.cursor.fetchone()
		rs = []
		while row :
			rs.append((row[0],row[1],row[2]))
			row=self.db.cursor.fetchone()
		rs1=[]
		for r in rs :
			sql0="""
			select (NEXTVAL  for HUNAN.ROLE_ID) from sysibm.sysdummy1
			"""
			self.db.cursor.execute(sql0)
			role_id = self.db.cursor.fetchone()[0]
			sql="""
			insert into role (role_id,type_code) values(%s,'f_user')
			"""%(role_id)
			self.db.cursor.execute(sql)
			self.db.conn.commit()
			rs1.append((role_id,str(r[0]),str(r[1])))
		
		sql2 = u"""
			insert into  hunan.f_user  (role_id,user_name,name) values (?,?,?)
		"""
		print sql2 
		self.db.cursor.executemany(sql2,rs1)
		self.db.conn.commit()	
		sql="""
		select role_id  from f_user 
		"""
		self.db.cursor.execute(sql)
		row = self.db.cursor.fetchone()
		rs=[]	
		sql1 ="""
			insert into factor (factor_id ,factor_type,user_id) values(nextval for factor_id , 'password',?)
		"""

		while row :
			rs.append((row[0]))
			row=self.db.cursor.fetchone()
		self.db.cursor.executemany(sql1,rs)
		self.db.conn.commit()
	
		sql="""
		select factor_id from factor 
		"""
		self.db.cursor.execute(sql)
		row=self.db.cursor.fetchone()
		rs=[]
		sql1="""
		insert into password  (factor_id,algorithm,credential)values(?,'MD5','qwe123') 
		"""
		while row :
			rs.append((row[0]))
			row=self.db.cursor.fetchone()
		self.db.cursor.executemany(sql1,rs)	
		self.db.conn.commit()
		

if __name__ == '__main__':
	if len(sys.argv)==2:
		Staff(sys.argv[1]).run()

	else :
		print 'please input init_staff YYYYMMDD'

