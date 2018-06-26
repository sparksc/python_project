
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
			self.delete()
			self.import_staff()
		
		finally:
			self.db.closeDB()

	def delete(self):
		self.db.cursor.execute("delete from staff_relation")
		self.db.cursor.execute("delete from user_group")
		self.db.conn.commit()

	def import_staff(self):
		sql=u"""
SELECT
	g.xm,
	g.GYH ,
	g.JGM ,
     trim(char(cast(c.USER_ID as decimal(19,0)))),
    case when c.USER_ID is null then 0
    else 1  end is_khjl,
    case when c.USER_ID is not null then 0
    else 1  end is_zhgy , 
	u.role_id as user_id,
	b.role_id as branch_id
 
FROM
	ods.gyxxb_his G 
		LEFT JOIN ods.CZYMX_HIS C 
		ON G.XM=c.USER_CN AND
		G.JGM=c.ORG and
	C.TJRQ='2016-02-15' AND
	C.ORG LIKE '189403%%'
	inner join f_user u on u.user_name=G.gyh
	inner join branch b on b.branch_code=G.jgm
WHERE
	G.tjrq='%s' AND
	G.jgm IN (	SELECT
					branch_code 
				FROM
					branch) order by GYH



		"""%self.strdate

		self.db.cursor.execute(sql)
		row = self.db.cursor.fetchone()
		rs = []
		rs2=[]
		rs3=[]
		while row :
			rs.append((str(row[1]),str(row[1]),row[3],str(row[4]),str(row[5]),'0','0'))	
			rs2.append((row[6],row[7]))
			s=''
			if row[4]==1 :
				s='1'
			else :
				s='27'
			rs3.append((row[6],int(s)))
			row = self.db.cursor.fetchone()
		sql2 = u"""
		insert into hunan.staff_relation (staff_code , staff_sop_code,staff_cms_code,is_khjl,is_zhgy,is_kjzg,is_zhhz) values(?,?,?,?,?,?,?)
		"""
		print sql2
		sql3="""
		insert into hunan.user_branch(id,user_id,branch_id)values(nextval for user_branch_id_seq,?,?)
		"""
		print sql3
	
		sql4="""
		insert into hunan.user_group (id,user_id,group_id) values(nextval for user_group_id_seq,?,?)

		"""
		print sql4
		self.db.cursor.executemany(sql2,rs)
		self.db.conn.commit()
		self.db.cursor.executemany(sql3,rs2)
		self.db.conn.commit()
		
		print rs3
		self.db.cursor.executemany(sql4,rs3)
		self.db.conn.commit()

if __name__ == '__main__':
	if len(sys.argv)==2:
		Staff(sys.argv[1]).run()

	else :
		print 'please input init_staff YYYYMMDD'

