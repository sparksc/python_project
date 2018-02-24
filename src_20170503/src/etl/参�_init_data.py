
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
			#self.import_org_pos_rel()
			self.import_org_pos_staff_rel()
		finally:
			self.db.closeDB()
	def import_org_pos_staff_rel(self):
		sql=u"""
select (select org_pos_id from ORG_POS_REL where ORG_ID=o.ORG_ID and POSITION_ID=(case when sr.IS_KHJL='0' then '1053' else '1050' end )) as org_pos_id , g.JGM, s.staff_id, sr.IS_KHJL from staff  s inner join staff_relation sr on sr.STAFF_CODE=s.STAFF_CODE
inner join ods.GYXXB_HIS g on g.GYH=s.STAFF_CODE and g.TJRQ='%s' 
inner join ORGANIZATION o on o.ORG_CODE=g.JGM
		"""%self.strdate

		self.db.cursor.execute(sql)
		row = self.db.cursor.fetchone()
		rs = []
		while row :
			rs.append((int(row[0]),int(row[2]),None,None,self.strdate,None,self.strdate))	
			row = self.db.cursor.fetchone()
		sql2 = u"""
		insert into hunan.org_pos_staff_rel (org_pos_id,staff_id,is_main_position,created_by,date_created,updated_by,date_updated) values(?,?,?,?,?,?,?)
		"""
	
		print sql2
		print rs
		self.db.cursor.executemany(sql2,rs)
		self.db.conn.commit()
			




	def import_org_pos_rel(self):
		sql=u"""
		select org_id,org_code from organization

		"""

		self.db.cursor.execute(sql)
		row = self.db.cursor.fetchone()
		rs = []
		while row :
			rs.append((int(row[0]),1050,None,self.strdate,None,self.strdate))	
			row = self.db.cursor.fetchone()
		sql2 = u"""
		insert into hunan.org_pos_rel (org_id,position_id,created_by,date_created,updated_by,date_updated) values(?,?,?,?,?,?)
		"""
	
		print sql2
		print rs
		self.db.cursor.executemany(sql2,rs)
		self.db.conn.commit()
		

		

if __name__ == '__main__':
	if len(sys.argv)==2:
		Staff(sys.argv[1]).run()

	else :
		print 'please input init_staff YYYYMMDD'

