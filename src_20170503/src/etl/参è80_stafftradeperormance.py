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
柜员业务量及绩效
"""
class Stafftradeperormance():
	def __init__(self,etldate=None):
                self.db =util.DBConnect()
                self.etldate=etldate
                self.stretldate =util.tostrdate(self.etldate)
                self.para=util.get_common_parameter(self.db)
                if etldate is not None : self.para['TJRQ']=etldate
	def select_gyywljjx(self):
		sql1=u"""
			select trim(staff_code) yggh,trim(staff_name) as staff_name,trim(staff_sop_code) staff_code,'2' tjzq,'1' as cszd
			from STAFF_RELATION 
			where staff_sop_code is not null and length(trim(STAFF_SOP_CODE))!=0
			with ur
		"""#员工核心号
		
		sql2=u"""
			select trim(sale_code) sale_code ,sum(ZHYWL) fhzhywl,sum(YWl) fhywl
			from t_staff_trade_hz t
			where date_id<=%s and date_id>=(
			case when quarter(to_date(%s,'yyyyMMdd'))='1'  then SUBSTR(%s, 1, 4) || '0101' 
			when quarter(to_date(%s,'yyyyMMdd'))='2' then SUBSTR(%s, 1, 4) || '0401'
			when quarter(to_date(%s,'yyyyMMdd'))='3' then SUBSTR(%s, 1, 4) || '0701'
			else SUBSTR(%s, 1, 4) || '1001' end
)
			and zblx='复核柜员业务量'
			group by sale_code 
			with ur
		"""%(self.para['TJRQ'],self.para['TJRQ'],self.para['TJRQ'],self.para['TJRQ'],self.para['TJRQ'],self.para['TJRQ'],self.para['TJRQ'],self.para['TJRQ'])#复核柜员业务量

		sql3=u"""
			select trim(sale_code) sale_code ,sum(ZHYWL) czzhywl,sum(YWL) czywl
			from t_staff_trade_hz t
			where date_id<=%s and date_id>=(
			case when quarter(to_date(%s,'yyyyMMdd'))='1'  then SUBSTR(%s, 1, 4) || '0101' 
			when quarter(to_date(%s,'yyyyMMdd'))='2' then SUBSTR(%s, 1, 4) || '0401'
			when quarter(to_date(%s,'yyyyMMdd'))='3' then SUBSTR(%s, 1, 4) || '0701'
			else SUBSTR(%s, 1, 4) || '1001' end
)
			and zblx='操作柜员业务量'
			group by sale_code 
			with ur
		"""%(self.para['TJRQ'],self.para['TJRQ'],self.para['TJRQ'],self.para['TJRQ'],self.para['TJRQ'],self.para['TJRQ'],self.para['TJRQ'],self.para['TJRQ'])#操作柜员业务量

		sql4=u"""
            select trim(branch_code) org_code,trim(branch_name)  ORG_NAME,trim(user_name) STAFF_CODE,trim(name)  STAFF_NAME from  V_USER_ORG
		"""#view_rsxxb

		sql5=u"""
			SELECT '1' as cszd, je1,je2 FROM t_jgc_jxkh_cs_qm where PARA_ID=21
		"""#参数
		
		sql6=u"""
			select quarter(to_date(TJRQ,'yyyyMMdd')) KHLX,'1' as cszd from T_COMMON_PARAMETER 
		"""#参数2
		
		sql=u"""
			select FHZHYWL,FHYWL,CZZHYWL,CZYWL,y.YGGH,y.TJZQ,y.CSZD,ORG_CODE as JGBH,ORG_NAME as JGMC,v.STAFF_NAME as YGXM,JE1,JE2,KHLX
			from (%s) as y
			inner join (%s) as v
			on y.YGGH=v.STAFF_CODE
			left join (%s) as f
			on y.STAFF_CODE=f.SALE_CODE
			left join (%s) as c
			on y.STAFF_CODE=c.SALE_CODE
			left join (%s) as c1
			on y.cszd=c1.cszd
			left join (%s) as c2
			on y.cszd=c2.cszd
		"""%(sql1,sql2,sql3,sql4,sql5,sql6)#连接查询

		s_sql=sql.encode('gb2312')
		self.db.cursor.execute(s_sql)
		row=self.db.cursor.fetchone()
		rs_zb=[]
		rs_jx=[]
		TJRQ=self.stretldate
		while row:
			if row[3] is None:
				CZYWL=0
			else:
				CZYWL=int(row[3])
			if row[1] is None:
				FHYWL=0
			else:
				FHYWL=int(row[1])
			if row[0] is None:
                                FHZHYWL=0
                        else:
                                FHZHYWL=int(row[0])
			if row[2] is None:
                                CZZHYWL=0
                        else:
                                CZZHYWL=int(row[2])
			if row[7] is None:
				JGBH='null'
			else:
				JGBH=row[7]
			ywl=CZYWL+FHYWL
			zhywl=FHZHYWL+CZZHYWL
			ywlxj=zhywl*int(row[10])
			if ywlxj>=int(row[11]):
				ywlxj=row[11]
			rs_zb.append((row[4],zhywl,TJRQ,ywl,str(row[12]),row[5],row[9],str(row[7]),row[8]))
			rs_jx.append((row[4],row[5],str(row[7]),row[8],row[9],str(row[12]),ywlxj,TJRQ))
			row=self.db.cursor.fetchone()
		self.insert_update_zb(rs_zb)
		self.insert_update_jx(rs_jx)

	def insert_update_zb(self,rs):
		insert_1=[]
		update_1=[]
		insert_zb_sql=u"""
			insert into T_JGC_JXKH_ZB_QM(YGGH,JE24,TJRQ,JE33,KHLX,TJZQ,YGXM,JGBH,JGMC)
			values(?,?,?,?,?,?,?,?,?)
		"""
		update_zb_sql=u"""
			update T_JGC_JXKH_ZB_QM set JE24=?,JE33=?,YGXM=?,JGMC=? where YGGH=? and TJRQ=? and TJZQ=? and JGBH=? and KHLX=?
		"""
		sql=u"""
			select * from T_JGC_JXKH_ZB_QM where YGGH=? and TJRQ=? and TJZQ=? and JGBH=? and KHLX=?
		"""
		for r in rs:
			self.db.cursor.execute(sql,r[0],r[2],r[5],r[7],r[4])
			row=self.db.cursor.fetchone()	
			if row is None:
				insert_1.append(r)
			else:
				update_1.append((r[1],r[3],r[6],r[8],r[0],r[2],r[5],r[7],r[4]))
		
		if len(insert_1)>0:
                        self.db.cursor.executemany(insert_zb_sql,insert_1)
                        self.db.conn.commit()
                if len(update_1)>0:
                        self.db.cursor.executemany(update_zb_sql,update_1)
                        self.db.conn.commit()
	def insert_update_jx(self,rs):
		insert_1=[]
                update_1=[]
                insert_jx_sql=u"""
                        insert into T_JGC_JXKH_JX_QM(YGGH,TJZQ,JGBH,JGMC,YGXM,KHLX,JE24,TJRQ)
                        values(?,?,?,?,?,?,?,?)
                """#数据插入绩效表
                update_jx_sql=u"""
                        update T_JGC_JXKH_JX_QM set JGMC=?,YGXM=?,JE36=? where YGGH=? and TJZQ=? and TJRQ=? and KHLX=? and JGBH=?
                """
                sql=u"""
                        select * from T_JGC_JXKH_JX_QM where YGGH=? and TJZQ=? and TJRQ=? and KHLX=? and JGBH=?
                """
                for r in rs:
                        self.db.cursor.execute(sql,r[0],r[1],r[7],r[5],r[2])
                        row=self.db.cursor.fetchone()
                        if row is None:
                                insert_1.append(r)
                        else:
                                update_1.append((r[3],r[4],r[6],r[0],r[1],r[7],r[5],r[2]))
		if len(insert_1)>0:
                        self.db.cursor.executemany(insert_jx_sql,insert_1)
                        self.db.conn.commit()
                if len(update_1)>0:
                        self.db.cursor.executemany(update_jx_sql,update_1)
                        self.db.conn.commit()
	def run_gyywljjx(self):
                try:
                        self.select_gyywljjx()
                        self.db.conn.commit()
                finally:
                        self.db.closeDB()
        def run(self):
                self.run_gyywljjx()

if __name__=="__main__":
        arglen=len(sys.argv)
        if arglen  == 2:
                Stafftradeperormance(sys.argv[1]).run()
        else :
                print "please input python gyywljjx.py YYYYMMDD"
