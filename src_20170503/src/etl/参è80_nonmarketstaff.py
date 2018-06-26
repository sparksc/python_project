# -*- coding:UTF-8 -*-
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

"""
非营销人员绩效薪酬
"""
class Nonmarketstaff():
	def __init__(self,etldate=None):
                self.db =util.DBConnect()
                self.etldate=etldate
                self.stretldate =util.tostrdate(self.etldate)
                self.para=util.get_common_parameter(self.db)
                if etldate is not None : self.para['TJRQ']=etldate
	def select_fyxryjxxc(self):
		sql1=u"""
			select trim(o.user_name) YGGH,trim(o.branch_code) JGBH,trim(o.branch_name) JGMC,'1' AS CSZD,trim(o.user_name) YGXM,days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1 ZLDAYS,days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1 CLDAYS
            from V_USER_GROUP g
            inner join V_USER_ORG o on  g.user_name = o.user_name
            where group_id  not in (1)
            order by 1
            with ur
		"""%(self.para['TJRQ'],self.para['TJQSRQ'],self.para['JZZZRQ'],self.para['JZQSRQ'])#非营销人员
		sql2=u"""
			select trim(sale_code) YGGH,sum(balance)  CK_CL_JS
			from m_jgc_khzb
			where date_id>=%s and  date_id<=%s and  relaction_type in('存款管理','派生存款','存款管理分配')
			group by sale_code
			order by 1
			with ur
		"""%(int(self.para['JZQSRQ']),int(self.para['JZZZRQ']))#存款存量积数
		sql3=u"""
			select trim(sale_code) yggh,sum(balance) ck_sd_js
			from m_jgc_khzb
			where date_id>=%s and  date_id<=%s and relaction_type in('存款管理','派生存款','存款管理分配')
			group by sale_code
			order by 1
			with ur
		"""%(int(self.para['TJQSRQ']),int(self.para['TJRQ']))#员工时点存款积数
		sql4=u"""
			select '1' as CSZD,a.JE2 from T_JGC_JXKH_CS_QM as a
			where PARA_ID=39
		"""#参数
		sql5=u"""
			SELECT trim(ORG_CODE) as JGBH ,JE1/JE2 as  wd_ck_cl_rj
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='机构存款年积数' 
		"""%(int(self.para['JZZZRQ']))#网点存量日均
		sql6=u"""
			SELECT trim(ORG_CODE) as JGBH ,JE1/JE2 as  wd_ck_sd_rj
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='机构存款年积数' 
		"""%(int(self.para['TJRQ']))#网点时点日均
		sql=u"""
                        select CK_CL_JS,CK_SD_JS,JE2,WD_CK_CL_RJ,WD_CK_SD_RJ,CLDAYS,ZLDAYS,f.JGBH,JGMC,f.YGGH,YGXM
                        from (%s) as f left join (%s) as ck
                        on f.YGGH=ck.YGGH
                        left join (%s) as yg
                        on f.YGGH=yg.YGGH
                        left join (%s) as cs
                        on f.CSZD=cs.CSZD
                        left join (%s) as wc
                        on f.JGBH=wc.JGBH
                        left join (%s) as ws
                        on f.JGBH=ws.JGBH and wc.JGBH=ws.JGBH
                """%(sql1,sql2,sql3,sql4,sql5,sql6)#连接查询
		s_sql=sql.encode('gb2312')
		self.db.cursor.execute(s_sql)
		row=self.db.cursor.fetchone()
		rs_zb=[]
		rs_jx=[]
		TJZQ='1'
		TJDT=str(self.para['TJRQ'])
		KHLX=str(TJDT[0:4])
		TJRQ=str(TJDT[0:4])+'-'+str(TJDT[4:6])+'-'+str(TJDT[6:8])
		while row:
			if row[0] is None:
				error(u"存款存量为空")
				CK_CL_RJ=0
			else:
				CK_CL_RJ=int(row[0])/int(row[5])
			if KHLX=='2016':
				CK_CL_RJ=0
			if row[1] is None:
                                error(u"员工时点存款积数为空")
                                CK_SD_RJ=0
                        else:
                                CK_SD_RJ=int(row[1])/int(row[6])
			CK_ZL_RJ=int(CK_CL_RJ)-int(CK_SD_RJ)
			if row[4] is None:
				WD_CK_CL_RJ=0
			else:
				WD_CK_CL_RJ=row[4]
			if row[5] is None:
				WD_CK_SD_RJ=0
			else:
				WD_CK_SD_RJ=row[5]
			WD_CK_ZL_RJ=WD_CK_SD_RJ-WD_CK_CL_RJ
			ck_zl_rj_tmp=CK_ZL_RJ
			JE2=int(row[2])
			FYXCKXC=0
			if CK_ZL_RJ!=0:
				FYXCKXC=(ck_zl_rj_tmp*JE2*0.0001)*int(row[6])/int(self.para['JNTS'])#以万为单位计算
			rs_zb.append((row[7],row[8],row[9],row[10],CK_SD_RJ,CK_CL_RJ,TJRQ,CK_ZL_RJ,TJZQ,KHLX))
			rs_jx.append((row[7],row[8],row[9],row[10],TJRQ,FYXCKXC,TJZQ,KHLX))
			row=self.db.cursor.fetchone()
		self.insert_update_zb(rs_zb)
		self.insert_update_jx(rs_jx)
	
	def insert_update_zb(self,rs):
		insert_1=[]
		update_1=[]
		insert_zb_sql=u"""
			insert into T_JGC_JXKH_ZB_QM(JGBH,JGMC,YGGH,YGXM,JE37,JE38,TJRQ,JE39,TJZQ,KHLX)
			values(?,?,?,?,?,?,?,?,?,?)
		"""#数据插入指标表
		update_zb_sql=u"""
			update T_JGC_JXKH_ZB_QM set JGMC=?,YGXM=?,JE37=?,JE38=?,JE39=?  where TJRQ=? and TJZQ=? and KHLX=? and YGGH=? and JGBH=?
		"""
		sql=u"""
			select * from T_JGC_JXKH_ZB_QM where TJRQ=? and TJZQ=? and KHLX=? and YGGH=? and JGBH=?
		"""
		for r in rs:
			self.db.cursor.execute(sql,r[6],r[8],r[9],r[2],r[0])
			row=self.db.cursor.fetchone()
			if row is None:
				insert_1.append(r)
			else:
				update_1.append((r[1],r[3],r[4],r[5],r[7],r[6],r[8],r[9],r[2],r[0]))
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
			insert into T_JGC_JXKH_JX_QM(JGBH,JGMC,YGGH,YGXM,TJRQ,JE36,TJZQ,KHLX)
			values(?,?,?,?,?,?,?,?)
		"""#数据插入绩效表
		update_jx_sql=u"""
			update T_JGC_JXKH_JX_QM set JGMC=?,YGXM=?,JE36=? where TJRQ=? and TJZQ=? and KHLX=? and YGGH=? and JGBH=?
		"""
		sql=u"""
			select * from T_JGC_JXKH_JX_QM where TJRQ=? and TJZQ=? and KHLX=? and YGGH=? and JGBH=?
		"""
		for r in rs:
                        self.db.cursor.execute(sql,r[4],r[6],r[7],r[2],r[0])
                        row=self.db.cursor.fetchone()
                        if row is None:
                                insert_1.append(r)
                        else:
				if r[5] is None:
					print r[5]
                                update_1.append((r[1],r[3],r[5],r[4],r[6],r[7],r[2],r[0]))
                if len(insert_1)>0:
                        self.db.cursor.executemany(insert_jx_sql,insert_1)
                        self.db.conn.commit()
                if len(update_1)>0:
                        self.db.cursor.executemany(update_jx_sql,update_1)
                        self.db.conn.commit()

	def run_fyxryjxxc(self):
		try:
			self.select_fyxryjxxc()
			self.db.conn.commit()
		finally:
			self.db.closeDB()
	def run(self):
		self.run_fyxryjxxc()

if __name__=="__main__":
	arglen=len(sys.argv)
        if arglen  == 2:
                Nonmarketstaff(sys.argv[1]).run()
        else :
                print "please input python fyxryjxxc.py YYYYMMDD"
