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

class Networkdeposit():
	def __init__(self,etldate=None):
		self.db =util.DBConnect()
		self.etldate=etldate
		self.stretldate =util.tostrdate(self.etldate) 
		self.para=util.get_common_parameter(self.db)
		if etldate is not None : self.para['TJRQ']=etldate

	"""
	网点存款指标与薪酬
	"""
	def wdck(self):
		staff_rs = self.get_staff_rs()	
		if staff_rs is None :
			error('staff is None')
			return

		ck_sd_rj=self.get_ck_sd_rj()
		if ck_sd_rj is None : ck_sd_rj =[(1,1)]	
		ck_cl_rj=self.get_ck_cl_rj()
		if ck_cl_rj is None : ck_cl_rj =[(1,1)]
		gy_rs = self.get_gy_rs()
		if gy_rs is None : gy_rs =[('1','1')]
		rs=[]
		for r in staff_rs:
			d={}
			d['JGBH']=r[0]
			d['JGMC']=r[1]
			d['YGGH']=r[2]
			d['YGXM']=r[3]
			d['CSZD']=r[4]
			rs.append(d)

		for r in rs:	
			for col1 in ck_sd_rj :
				if r['JGBH']==col1[0]:
					r['WD_CK_SD_RJ']=col1[1]
					r['ZLDAYS']=col1[2]
					break
				else :
					r['WD_CK_SD_RJ']=0
					r['ZLDAYS']=0
			for col2 in ck_cl_rj :
				if r['JGBH']==col2[0]:
					r['WD_CK_CL_RJ']=col2[1]
					break
				else :
					r['WD_CK_CL_RJ']=0
			for col3 in gy_rs :
				if r['JGBH']==col3[0]:
					r["YGRS"]=col3[1]
					break
				else :
					r["YGRS"]=0
		for r in rs:
			r['TJZQ']='1'
			r['KHLX']=str(self.para['TJRQ'])[0:4]
			r['TJRQ']=self.stretldate
			r['WD_CK_ZL_RJ']=r['WD_CK_SD_RJ']-r['WD_CK_CL_RJ']
			if r['WD_CK_CL_RJ']==0: r['WD_CK_CL_RJ']=1#机构存款存量为0怎么办
			r['SSBL']=r['WD_CK_ZL_RJ']/r['WD_CK_CL_RJ']
			r['ZBTS']=r['ZLDAYS']/int(self.para['JNTS'])
			r['CK_CL_RJ_tmp']=r['WD_CK_CL_RJ']/10000
			
		#计算人均
		rs=self.js_rj(rs)
		self.update_insert_zb(rs)#插入更新指标
		(cs1,cs2,cs3,cs4,cs5) = self.get_cs()#获得参数
		#jion 参数
		for r in rs :
			r['ZL_XX_1']=cs1[0][0]
			r['ZL_SX1']=cs1[0][1]
			r['ZL_CS11']=cs1[0][2]
			r['ZL_CS12']=cs1[0][3]	
			r['ZL_XX_2']=cs2[0][0]
			r['ZL_SX2']=cs2[0][1]
			r['ZL_CS21']=cs2[0][2]
			r['ZL_CS22']=cs2[0][3]
			r['CK_XJ_XX1']=cs3[0][0]
			r['CK_XJ_SX1']=cs3[0][1]
			r['CK_XJ_CS1']=cs3[0][2]
			r['CK_XJ_XX2']=cs4[0][0]
			r['CK_XJ_SX2']=cs4[0][1]
			r['CK_XJ_CS2']=cs4[0][2]	
		#绩效计算
		rs=self.jx_js(rs)
		#与CS5 join	
		for r in rs :
			for col in cs5:
				if r['WDCLJZ']>=col[0] and r['WDCLJZ']<col[1]:
					r['JE1']=col[2]
					r['WDCLJX']=col[2]
					break
				else :
					r['JE1']=0
					r['WDCLJX']=0 
		#薪酬入库	
		self.update_insert_jx(rs)

	def update_insert_jx(self,rs):
		update_l=[]
		insert_l=[]
		sql=u"""
		select * from T_JGC_JXKH_JX_QM where YGGH=? and TJRQ=? and TJZQ=? and JGBH=? and KHLX=?
		"""
		for r in rs :
			self.db.cursor.execute(sql,(r['YGGH'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX']))
			row = self.db.cursor.fetchone()
			if row is None :
				insert_l.append((r['YGGH'],r['TJZQ'],r['WDZLJX'],r['WDCLJX'],r['TJRQ'],r['YGXM'],r['JGBH'],r['JGMC'],r['KHLX']))
			else :
				update_l.append((r['WDZLJX'],r['WDCLJX'],r['YGXM'],r['JGMC'],r['YGGH'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX']))
		if len(insert_l)>0:
			self.insert_jx_db(insert_l)
		if len(update_l)>0:
			self.update_jx_db(update_l)	


	def insert_jx_db(self,r):
		sql=u"""
		insert into T_JGC_JXKH_JX_QM (YGGH,TJZQ,JE26,JE25,TJRQ,YGXM,JGBH,JGMC,KHLX) values(?,?,?,?,?,?,?,?,?)
		"""
		self.db.cursor.executemany(sql,r)
		self.db.conn.commit()
	def update_jx_db(self,r):
		sql=u"""
		update T_JGC_JXKH_JX_QM set JE26=?,JE25=? ,YGXM=?,JGMC=? where YGGH=? and TJRQ=? and TJZQ=? and JGBH=? and KHLX=?
		"""			
		self.db.cursor.executemany(sql,r)
		self.db.conn.commit()		


	"""
	绩效计算
	"""
	def jx_js(self,rs):
		for r in rs: 
			wdcljz = 0
			wdzljx = 0  
			if r['SSBL'] >= 0:#有增量部分
				wdcljz = r['CK_CL_RJ_tmp']
				if r['SSBL']<r['ZL_SX1']:
					wdzljx = r['ZL_CS11']*(r['WD_CK_ZL_RJ']/10000/r['YGRS'])
				if r['SSBL']>=r['ZL_XX_2']:
					wdzljx = r['ZL_CS11']*r['ZL_XX_2']*(r['WD_CK_CL_RJ']/r['10000']/r['YGRS'])+r['ZL_CS11']*(r['SSBL']-r['ZL_XX_2'])*(r['WD_CK_CL_RJ']/10000/r['YGRS'])
			else :#无增量部分
				if r['SSBL']+r['CK_XJ_XX1']>0:
					wdcljz = r['CK_CL_RJ_tmp']
				elif r['SSBL']+r['CK_XJ_SX1']>0:
					wdcljz = r['CK_CL_RJ_tmp']*(1+r['SSBL']*r['CK_XJ_CS1'])
				elif r['SSBL']+r['CK_XJ_XX2']>0 :
					wdcljz =r['CK_CL_RJ_tmp']*(1+r['SSBL']*r['CK_XJ_CS2'])
				else :
					wdcljz = -1
			r['WDCLJZ']=wdcljz
			r['WDZLJX']=wdzljx	
		return rs

	def get_cs(self):
		sql1=u"""
		SELECT A.XX,A.SX,A.JE1,A.JE2,'1' as CSZD FROM t_jgc_jxkh_cs_qm A where  para_id = 27
		"""
		cs1=util.get_select_row(self.db,sql1)
		sql2=u"""
		SELECT A.XX,A.SX,A.JE1,A.JE2,'1' as CSZD FROM t_jgc_jxkh_cs_qm A where  para_id = 28
		"""
		cs2=util.get_select_row(self.db,sql2)
		
		sql3=u"""
		SELECT A.XX,A.SX,A.JE1,'1' as CSZD FROM t_jgc_jxkh_cs_qm A where para_id = 51
		"""
		cs3=util.get_select_row(self.db,sql3)
		sql4=u"""
		SELECT A.XX CK_XJ_XX2,A.SX CK_XJ_SX2,A.JE1 CK_XJ_CS2 ,'1' as CSZD FROM t_jgc_jxkh_cs_qm A where para_id = 52
		"""
		cs4=util.get_select_row(self.db,sql4)
	
		sql5=u"""
		SELECT A.XX,A.SX,A.JE1 FROM t_jgc_jxkh_cs_qm A where cslx = 12
		"""
		cs5=util.get_select_row(self.db,sql5)

		if cs1 is None or cs2 is None or cs3 is None or cs4 is None or cs5 is None:
			error('get cs error')
			exit()

		return (cs1,cs2,cs3,cs4,cs5)
			

	def update_insert_zb(self,rs):
		sql=u"""
		select *  from T_JGC_JXKH_ZB_QM where YGGH=? and TJRQ=?
		and TJZQ=? and JGBH=? and KHLX=?
		"""	
		update_l=[]
		insert_l=[]
			
		for r in rs:
			self.db.cursor.execute(sql,(r['YGGH'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX']))
			row=self.db.cursor.fetchone()
			if row is None :
				insert_l.append((r['JGBH'],r['JGMC'],r['YGGH'],r['YGXM'],r['CK_ZL_RJ_RJ'],r['CK_CL_RJ_RJ'],r['TJZQ'],r['KHLX'],r['TJRQ'],r['CK_SD_RJ_RJ']))

			else :
				update_l.append((r['JGMC'],r['YGXM'],r['CK_ZL_RJ_RJ'],r['CK_CL_RJ_RJ'],r['CK_SD_RJ_RJ'],r['YGGH'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX']))
		if len(insert_l)>0:
			self.insert_zb_db(insert_l)

		if len(update_l)>0:
			self.update_zb_db(update_l)
			

	def insert_zb_db(self,rs):
		sql=u"""
		insert into T_JGC_JXKH_ZB_QM (JGBH,JGMC,YGGH,YGXM,JE26,JE25,TJZQ,KHLX,TJRQ,JE36) values (?,?,?,?,?,?,?,?,?,?)
		"""	
		self.db.cursor.executemany(sql,rs)
		self.db.conn.commit()

	def update_zb_db(self,rs):
		sql=u"""
		update T_JGC_JXKH_ZB_QM set JGMC=? ,YGXM=?, JE26=?,JE25=?,JE36=? where YGGH=? and TJRQ=? and TJZQ=? and JGBH=? and KHLX=?
		"""
		self.db.cursor.executemany(sql,rs)
		self.db.conn.commit()

	


	def js_rj(self,rs):
		for r in rs :
			r['CK_CL_RJ_RJ']=r['WD_CK_CL_RJ']/r['YGRS']
			r['CK_SD_RJ_RJ']=r['WD_CK_SD_RJ']/r['YGRS']
			r['CK_ZL_RJ_RJ']=r['CK_SD_RJ_RJ']-r['CK_CL_RJ_RJ']
		return rs



	"""
	柜员人数
	"""
	def get_gy_rs(self):
		sql=u"""
        select o.branch_code, count(1) ygrs
        from V_USER_GROUP g
        inner join V_USER_ORG o on  g.user_name = o.user_name
        where group_id in (27)
        group by o.branch_code
        order by 1
		"""
		rs = util.get_select_row(self.db,sql)
		return rs
		


	"""
	机构存款时点日均	
	"""	
	def get_ck_sd_rj(self):
		sql="""
			SELECT trim(ORG_CODE) JGBH ,JE1/JE2 as  wd_ck_sd_rj,je2
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='%s' 
		"""%(self.para['TJRQ'],u'机构存款年积数'.encode('gb2312'))
		rs = util.get_select_row(self.db,sql)
		return rs	
	"""
	机构存量存量日均
	"""
	def get_ck_cl_rj(self):
		sql="""
		SELECT 
		trim(ORG_CODE) JGBH ,JE1/JE2 as  wd_ck_cl_rj
		FROM t_jgc_jgzb T
		WHERE T.DATE_ID=%s AND ZBLX='%s' 
		"""%(self.para['JZZZRQ'],u'机构存款年积数'.encode('gb2312'))

		rs = util.get_select_row(self.db,sql)
		return rs


	"""
	获取柜员信息	
	"""	
	def get_staff_rs(self):
		sql=u"""
        select trim(o.branch_code) JGBH,trim(o.branch_name) JGMC,trim(o.user_name) YGGH,trim(o.name) YGXM ,'1' as CSZD
        from V_USER_GROUP g
        inner join V_USER_ORG o on  g.user_name = o.user_name
        where group_id in (27)
        order by 1
		"""#TODOposition_code要改
		rs = util.get_select_row(self.db,sql)
		return rs

	def run_wdck(self):
		try :
			self.wdck()#网点存款指标与薪酬
			self.db.conn.commit()
		finally :
			self.db.closeDB()
	
	def run(self):
		self.run_wdck()

	
"""
网点存款指标与薪酬
"""
if __name__ == "__main__":
	arglen=len(sys.argv)
	if arglen  == 2:
		Networkdeposit(sys.argv[1]).run()
	else :
		print "please input python wdck.py YYYYMMDD "




