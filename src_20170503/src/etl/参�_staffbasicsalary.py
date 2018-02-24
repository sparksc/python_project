# -*- coding:UTF-8 -*-
#!/bin/python
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random
from datetime import datetime,timedelta
from decimal import *
import DB2

import etl.star.util as util
from etl.star.conf import Config

"""
员工基本薪酬
"""
class Staffbasicsalary():
	def __init__(self,etldate=None):
		self.db =util.DBConnect()
                self.etldate=etldate
                self.stretldate =util.tostrdate(self.etldate)
                self.para=util.get_common_parameter(self.db)
                if etldate is not None : self.para['TJRQ']=etldate
	def select_view_rsxxb(self):
        	v_sql=u"""
             	select trim(branch_code) ORG_CODE,trim(branch_name) ORG_NAME,trim(user_name) STAFF_CODE,trim(name) STAFF_NAME,'1' as CSZD from v_user_org
        	"""
		return v_sql
	
	def select_staff_relation(self):
		s_sql=u"""
			SELECT trim(STAFF_CODE) as STAFF_CODE, trim(XL) as XL, trim(ZC) as ZC, trim(RHNX) as RHNX, trim(GZNX) as GZNX,GWXS,trim(GWZJ) as GWZJ FROM STAFF_RELATION
			ORDER BY STAFF_CODE ASC
		"""
	        return s_sql
	
	def select_xueli(self):
		x_sql=u"""
			SELECT trim(dxbh) as DXBH,je1 as XL_JT FROM t_jgc_jxkh_cs_jbxc WHERE sjlx='1'
			ORDER BY DXBH ASC
		"""
	        return x_sql
	
	def select_zhichen(self):
		z_sql=u"""
			SELECT trim(dxbh) as DXBH,je1 as ZC_JT FROM t_jgc_jxkh_cs_jbxc WHERE sjlx='2'
			ORDER BY DXBH ASC
		"""
	        return z_sql
	
	def select_gongling(self):
		g_sql=u"""
			SELECT '1' as DXBH,je1 as GL_JT FROM t_jgc_jxkh_cs_jbxc WHERE sjlx='5'
			ORDER BY DXBH ASC
		"""
	        return g_sql
	
	def select_baseshbz(self):
		b_sql=u"""
			SELECT '1' as DXBH,je1 as JBSHBZ FROM t_jgc_jxkh_cs_jbxc WHERE sjlx='6'
			ORDER BY DXBH ASC
		"""
	        return b_sql
	
	def select_gangweilevel(self):
		gl_sql=u"""
			SELECT '1' as CSZD,DXBH,je1 as GW_JT FROM t_jgc_jxkh_cs_jbxc WHERE sjlx='8'
			ORDER BY DXBH ASC
		"""
	        return gl_sql
	
	def select_ygjbxc(self):
		v_sql=self.select_view_rsxxb()
		s_sql=self.select_staff_relation()
		x_sql=self.select_xueli()
		z_sql=self.select_zhichen()
		g_sql=self.select_gongling()
		b_sql=self.select_baseshbz()
		gl_sql=self.select_gangweilevel()
		sql=u"""
			select v.ORG_CODE,v.ORG_NAME,v.STAFF_CODE,v.STAFF_NAME,%s,s.XL,s.ZC,s.RHNX,s.GZNX,s.GWXS,s.GWZJ,a.XL_JT,b.ZC_JT,c.GL_JT,d.JBSHBZ,e.GW_JT
	                from (%s) as v inner join (%s) as s
			on v.STAFF_CODE=s.STAFF_CODE
			inner join (%s) as a
			on S.XL=A.DXBH
			inner join (%s) as b
			on s.ZC=b.DXBH
			inner join (%s) as c
			on v.CSZD=c.DXBH
			inner join (%s) as d
			on v.CSZD=d.DXBH
			inner join (%s) as e
			on v.CSZD=e.CSZD and s.GWZJ=e.DXBH
		"""%(self.para['TJRQ'],v_sql,s_sql,x_sql,z_sql,g_sql,b_sql,gl_sql)
		self.insert_update_ygjbxc(sql)
	def shujuchuli(self,s_sql):
		self.db.cursor.execute(s_sql)
	        row=self.db.cursor.fetchone()
	        rs=[]
	        while row:
	                if row[8] >0:
	                        gl=int(row[8])
	                        if row[13]*gl >0:
	                                JE9=int(row[13])*gl
	                else:
	                        gl=0
	                        JE9=0
	                JE2=int(row[11])+int(row[12])+int(row[13])*gl
	                if not JE2 > 0:
	                        JE2=0
	                if row[11] >0:
	                        JE6=row[11]
	                else:
	                        JE6=0
	                if row[12]>0:
	                        JE7=row[12]
	                else:
	                        JE7=0
			JGJB='3'
	                JE1=int(row[14])
	                JE4=int(row[15])
	                JE5=JE1+JE2+JE4
	                rs.append((str(row[4]),JGJB,row[0],row[1],row[2],row[3],JE1,JE2,int(row[15]),int(JE5),int(JE6),int(JE7),int(JE9)))
	                row=self.db.cursor.fetchone()
		return rs
	def insert_update_ygjbxc(self,s_sql):
		rs=self.shujuchuli(s_sql)
		insert_1=[]
		update_1=[]
		sql=u"""
			select * from T_JGC_JXKH_YG_JCXC where TJRQ=? and JGJB=? and JGBH=? and YGGH=?
		"""
		for r in rs:
			self.db.cursor.execute(sql,r[0],r[1],r[2],r[4])
			row=self.db.cursor.fetchone()
			if row is None:
				insert_1.append(r)
			else:
				update_1.append((r[3],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[0],r[1],r[2],r[4]))
		if len(insert_1)>0:
			self.insert_ygjbxc(insert_1)
		if len(update_1)>0:
			self.update_ygjbxc(update_1)
	def insert_ygjbxc(self,rs):
		insert_sql="""
			insert into T_JGC_JXKH_YG_JCXC(TJRQ,JGJB,JGBH,JGMC,YGGH,YGXM,JE1,JE2,JE4,JE5,JE6,JE7,JE9)
			VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
		"""
		self.db.cursor.executemany(insert_sql,rs)
		self.db.conn.commit()
		
	def update_ygjbxc(self,rs):
		update_sql=u"""
			update T_JGC_JXKH_YG_JCXC set JGMC=?,YGXM=?,JE1=?,JE2=?,JE4=?,JE5=?,JE6=?,JE7=?,JE9=?  where TJRQ=? and JGJB=? and JGBH=? and YGGH=?
	
		"""
		self.db.cursor.executemany(update_sql,rs)
		self.db.conn.commit()
	
	def run_ygjbxc(self):
		try:
			self.select_ygjbxc()
			self.db.conn.commit()
		finally:
			self.db.closeDB()
	
	def run(self):
		self.run_ygjbxc()
if __name__=='__main__':
        arglen=len(sys.argv)
        if arglen  == 2:
                Staffbasicsalary(sys.argv[1]).run()
        else :
                print "please input python ygjbxc.py YYYYMMDD"
