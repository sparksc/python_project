# -*- coding:utf-8 -*-
#!/bin/python  

import os, time, random,sys
import DB2
from datetime import datetime,timedelta
from decimal import *
import  etl.star.util  as util
from etl.star.conf import *
from etl.star.transformdict import *
from etl.star.singleton import singleton
from etl.star.logger import info


"""
导入机构信息
"""
class Import_org():
	def __init__(self,etldate):
		self.db = util.DBConnect()
		self.strdate = str(etldate[0:4])+"-"+str(etldate[4:6])+"-"+str(etldate[6:8])



	def run(self):
		try:
			self.delete_jg()
			self.import2csjg()
			self.import2branch()
			self.db.conn.commit()
		finally:
			self.db.closeDB()

	def delete_jg(self):
		sql="""
		delete from hunan.USER_BRANCH
		"""
		self.db.cursor.execute(sql)
		self.db.conn.commit()
		sql="""
		delete from hunan.branch
		"""
		self.db.cursor.execute(sql)
		self.db.conn.commit()
		sql="""
		delete from hunan.t_cs_jg
		"""
		self.db.cursor.execute(sql)
		self.db.conn.commit()
		

	def import2csjg(self):
		sql = u"""
                        select jgm,jgmc,sxlh from ods.jgxxb_his where jgm like '189403%%' and  jglx='0' and  tjrq='%s'
                """%(self.strdate,)
                print sql
                self.db.cursor.execute(sql)
                row = self.db.cursor.fetchone()
                rs=[]
                while row:
                        if row[0]=='1894030000':
                                rs.append((self.strdate,row[0],row[1],None,'1','0',None,None,None))
                        else :

                                rs.append((self.strdate,row[0],row[1],'1894030000','2','0',None,None,None))
                        row = self.db.cursor.fetchone()

                sql2 = u"""
                        insert into  hunan.t_cs_jg  (drrq,jgbh,jgmc,sjjg,jgjb,jgzt,cjrq,zxrq,jgbs) values (?,?,?,?,?,?,?,?,?)
                """
                print sql2


                self.db.cursor.executemany(sql2,rs)
                self.db.conn.commit()



	def import2branch(self):
		sql = u"""
			select jgm,jgmc,sxlh from ods.jgxxb_his where jgm like '189403%%' and jglx='0' and  tjrq='%s'
		"""%(self.strdate,)
		print sql
		self.db.cursor.execute(sql)
		row=self.db.cursor.fetchone()
		rs=[]
		while row :
			rs.append((row[0],row[1]))
			row=self.db.cursor.fetchone()
		rs1=[]
		for r in rs :
			sql0="""
			select (NEXTVAL  for HUNAN.ROLE_ID) from sysibm.sysdummy1
			"""
			self.db.cursor.execute(sql0)
			role_id = self.db.cursor.fetchone()[0]
			sql="""
			insert into role (role_id,type_code) values(%s,'branch')
			"""%(role_id)
			self.db.cursor.execute(sql)
			self.db.conn.commit()


			rs1.append((role_id,r[0],r[1]))
		
		sql2 = u"""
			insert into  hunan.branch  (role_id,branch_code,branch_name) values (?,?,?)
		"""
		print sql2 
		self.db.cursor.executemany(sql2,rs1)
		self.db.conn.commit()	
		






if __name__=='__main__':
	if len(sys.argv)==2:
		Import_org(sys.argv[1]).run()
	else:
		print "please input python init_org.py YYYYMMDD"		

