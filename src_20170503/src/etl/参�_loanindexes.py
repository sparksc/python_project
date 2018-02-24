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
	



class Loanindexes():
	def __init__(self,etldate=None):
		self.db =util.DBConnect()
		self.etldate=etldate
		self.stretldate =util.tostrdate(self.etldate) 
		self.para=util.get_common_parameter(self.db)
		if etldate is not None : self.para['TJRQ']=etldate


	def dkzbjj(self):
		rs=self.get_manage()#获取信贷员工信息
		if rs is None :
			info('manage is none')
			return 
		five_loan_rs_sd = self.get_five_loan_sd()#获取当前五级不良	
		if five_loan_rs_sd is None : five_loan_rs_sd=[('1','1')]
		five_loan_rs_cl = self.get_five_loan_cl()#获取上年五级不良
		if five_loan_rs_cl  is None :five_loan_rs_cl =[('1','1')]
		dk_gh_rj_rs = self.get_dk_gh_rj()#日均贷款管户数
		if dk_gh_rj_rs is None :dk_gh_rj_rs =[('1','1')]
		gh_xc_rs = self.get_gh_xc()#管户数薪酬
		if gh_xc_rs is None : gh_xc_rs =[('1','1')]
		dk_sd_js_rs =self.get_dk_sd_js()#贷款时点积数
		if dk_sd_js_rs is None : dk_sd_js_rs =[('1','1')]	
		
		dk_rs=[]
		for r in rs :
			d={}
			d['YGNM']=r[0]
			d['JGBH']=r[1]
			d['JGMC']=r[2]
			d['YGGH']=r[3]
			d['YGXM']=r[4]
			d['JE2']=r[5]	
			d['CSZD']=r[6]				
			dk_rs.append(d)
		
		for col in dk_rs:
			for r1 in five_loan_rs_sd :
				if col['YGGH']==r1[0]:
					col['WJBL_SD']=r1[1]
					break
				else :
					col['WJBL_SD']=0
			for r2 in five_loan_rs_cl :
				if col['YGGH']==r2[0]:
					col['WJBL_CL']=r2[1]
					break
				else :
					col['WJBL_CL']=0
			for r3 in dk_gh_rj_rs:
				if col['YGGH']==r3[0]:
					col['NEW_HS0']=r3[1]
					col['NEW_HS50']=r3[2]
					col['OLD_HS0']=r3[3]
					col['OLD_HS50']=r3[4]	
					break
				else:
					col['NEW_HS0']=0
					col['NEW_HS50']=0
					col['OLD_HS0']=0
					col['OLD_HS50']=0	

			for r4 in gh_xc_rs:
				if col['YGGH']==r4[0]:
					col['HS0_XC']=r4[1]
					col['HS50_XC']=r4[2]
					break
				else :
					col['HS0_XC']=0
					col['HS50_XC']=0
			for r5 in dk_sd_js_rs :
				if col['YGGH']==r5[0]:
					col['DK_SD_JS']=r5[1]
					break
				else :
					col['DK_SD_JS']=0
		
		for col in dk_rs :
			col['TJZQ']='1'
			col['KHLX']=str(self.para['TJRQ'])[0:4]
			col['TJRQ'] =self.stretldate
			zldays =col['JE2']*1.0
			col['ZBTS'] = zldays/int(self.para['JNTS'])
			col['WJBL_SDYE'] = col['WJBL_SD']
			col['WJBL_CLYE'] = col['WJBL_CL']
			col['WJBL_ZLYE'] = col['WJBL_CL']-col['WJBL_SD']

			col['DK_SD_RJ'] = col['DK_SD_JS']/col['JE2']
			col['DK_SD_RJ_XX'] = col['DK_SD_RJ']*0.0001

			

		self.update_insert_zb(dk_rs)#指标入库
		bl_cs=self.get_bl_cs()
		if bl_cs is None :
			info('bl_cs is None')
			return
	
		for r in dk_rs:
			r['BL_SX']=bl_cs[0][1]
			r['BL_XX']=bl_cs[0][2]


		dk_sr_cs = self.get_dk_sr_cs()
		if dk_sr_cs is None : 
			info('dk_sr_cs is None')
			return
	

		for r in dk_rs :
			for  cs in  dk_sr_cs :	
				if r['DK_SD_RJ_XX']>= cs[1] and r['DK_SD_RJ_XX']<cs[2]:
					r['JE1']=cs[3]
					break
				else :
					r['JE1']=0

		#计价
		for r in dk_rs:
			bl_jx=0
			if r['WJBL_SDYE']>r['BL_SX'] :
				bl_jx = r['BL_SX']*r['ZBTS']
			dk_sj_jx = r['JE1']*10000*r['ZBTS']	
			
			r['BL_JX']=bl_jx
			r['DK_SJ_JX']=dk_sj_jx

		self.update_insert_jx(dk_rs)
		


	def update_insert_jx(self,rs):
		update_l=[]
		insert_l=[]
		sql=u"""
		select * from T_JGC_JXKH_JX_QM where YGGH=? and TJRQ=? and TJZQ=? and JGBH=? and KHLX=?
		"""
		for r in rs :
			self.db.cursor.execute(sql,(r['YGNM'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX']))
			row = self.db.cursor.fetchone()
			if row is None :
				insert_l.append((r['YGNM'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX'],r['HS0_XC'],r['HS50_XC'],r['BL_JX'],r['DK_SJ_JX']))

			else :
				update_l.append((r['HS0_XC'],r['HS50_XC'],r['BL_JX'],r['DK_SJ_JX'],r['YGNM'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX']))

		

			
		if len(insert_l)>0:
			self.insert_jx_db(insert_l)
		if len(update_l)>0:
			self.update_jx_db(update_l)	


	def insert_jx_db(self,r):
		sql=u"""
		insert into T_JGC_JXKH_JX_QM (YGGH,TJRQ,TJZQ,JGBH,KHLX,JE7,JE8,JE11,JE4) values(?,?,?,?,?,?,?,?,?)
		"""
		self.db.cursor.executemany(sql,r)
		self.db.conn.commit()
	def update_jx_db(self,r):
		sql=u"""
		update T_JGC_JXKH_JX_QM set JE7=?,JE8=? ,JE11=?,JE4=? where YGGH=? and TJRQ=? and TJZQ=? and JGBH=? and KHLX=?
		"""			
		self.db.cursor.executemany(sql,r)
		self.db.conn.commit()		
	


			

	def get_dk_sr_cs(self):
		sql=u"""
		SELECT '1' AS CSZD,A.XX,A.SX,A.JE1 FROM T_JGC_JXKH_CS_QM A WHERE cslx=11
		"""	
		rs = util.get_select_row(self.db,sql)
		return rs


	def get_bl_cs(self):
		sql=u"""
		SELECT '1' AS CSZD,A.SX,A.JE1 FROM T_JGC_JXKH_CS_QM A WHERE PARA_ID=20
		"""	
		rs = util.get_select_row(self.db,sql)
		return rs
		



	def update_insert_zb(self,dk_rs):
		sql=u"""
		select *  from T_JGC_JXKH_ZB_QM where YGGH=? and TJRQ=?
		and TJZQ=? and JGBH=? and KHLX=?
		"""	
		update_l=[]
		insert_l=[]
			
		for r in dk_rs:
			self.db.cursor.execute(sql,(r['YGNM'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX']))
			row=self.db.cursor.fetchone()
			if row is None :
				insert_l.append((r['OLD_HS0'],r['NEW_HS0'],r['OLD_HS50'],r['NEW_HS50'],r['JGMC'],r['YGXM'],r['WJBL_SDYE'],r['WJBL_CLYE'],r['WJBL_ZLYE'],r['DK_SD_RJ'],r['YGNM'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX']))

			else :
				update_l.append((r['OLD_HS0'],r['NEW_HS0'],r['OLD_HS50'],r['NEW_HS50'],r['JGMC'],r['YGXM'],r['WJBL_SDYE'],r['WJBL_CLYE'],r['WJBL_ZLYE'],r['DK_SD_RJ'],r['YGNM'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX'] ))
		if len(insert_l)>0:
			self.insert_zb_db(insert_l)

		if len(update_l)>0:
			self.update_zb_db(update_l)
			

	def insert_zb_db(self,rs):
		sql=u"""
		insert into T_JGC_JXKH_ZB_QM (JE7,JE8,JE9,JE10,JGMC,YGXM,JE11,JE34,JE12,JE44,YGGH,TJRQ,TJZQ,JGBH,KHLX) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
		"""	
		self.db.cursor.executemany(sql,rs)
		self.db.conn.commit()

	def update_zb_db(self,rs):
		sql=u"""
		update T_JGC_JXKH_ZB_QM set JE7=?,JE8=?,JE9=?,JE10=?,JGMC=?,YGXM=?,JE11=?,JE34=?,JE12=?,JE44=? where YGGH=? and TJRQ=? and TJZQ=? and JGBH=? and KHLX=?
		"""
		self.db.cursor.executemany(sql,rs)
		self.db.conn.commit()





	def get_dk_sd_js(self):
		sql=u"""
		select trim(sale_code) YGGH,sum(balance)*0.01 dk_sd_js
		from m_jgc_khzb
		where  date_id>=%s and  date_id<=%s and account_classify in ('L') 
		group by sale_code
		"""%(self.para['TJQSRQ'],self.para['TJRQ'])

		rs = util.get_select_row(self.db,sql)
		return rs


	def get_gh_xc(self):
		sql="""
		select  trim(sale_code) yggh, sum(JXXC) hs0_XC,sum(JXXC2) hs50_XC
		from T_TMP_KHJL_DKHS
		where data_id <= %s and sjlx ='%s' and data_id >= %s
		group by sale_code
		order by 1
		"""%(self.para['TJRQ'],u'日均贷款管户数'.encode('gb2312'),self.para['TJQSRQ'])
		rs = util.get_select_row(self.db,sql)
		return rs


	def get_dk_gh_rj(self):
		sql="""
		select  trim(sale_code) yggh, new_hs0,new_hs50,old_hs0,old_hs50
		from T_TMP_KHJL_DKHS
		where data_id = %s and sjlx ='%s'
		order by 1
		"""%(self.para['TJRQ'],u'日均贷款管户数'.encode('gb2312'))
		rs = util.get_select_row(self.db,sql)
		return rs

	def get_five_loan_cl(self):
		sql="""
		select trim(sale_code) YGGH, sum(balance)*0.01 wjbl_cl
		from m_staff_loan 
		where date_id = %s and loan_five in (%s)
		group by sale_code
		order by 1
		"""%(self.para['JZZZRQ'],u"'次级','可疑','损失'".encode('gb2312'))
			
		rs = util.get_select_row(self.db,sql)
		return rs

		
	def get_five_loan_sd(self):
		sql="""
		select trim(sale_code) YGGH, sum(balance)*0.01 wjbl_sd 
		from m_staff_loan 
		where date_id = %s and loan_five in (%s)
		group by sale_code
		order by 1
		"""%(self.para['TJRQ'],u"'次级','可疑','损失'".encode('gb2312'))
			
		rs = util.get_select_row(self.db,sql)
		return rs



	def get_manage(self):
		sql=u'''
		select m(o.user_name) ygnm,trim(o.branch_code) JGBH,trim(o.branch_name) JGMC,trim(s.STAFF_CMS_CODE) yggh ,trim(o.name) ygxm,days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1 je2,'1' as cszd
        inner join V_USER_ORG o on  g.user_name = o.user_name
        inner join STAFF_RELATION s on s.STAFF_CODE = o.user_name
        where group_id   in (1)
        with ur
		'''%(self.para['TJRQ'],self.para['TJQSRQ'])
		rs = util.get_select_row(self.db,sql)
		return rs


	 
	def run_dkzbjj(self):
		try :
			self.dkzbjj()	
			self.db.conn.commit()

		finally :
			self.db.closeDB()
	
	def run(self):
		self.run_dkzbjj()
	













"""
贷款指标计价
"""
if __name__ == "__main__":
	arglen=len(sys.argv)
	if arglen  == 2:
		Loanindexes(sys.argv[1]).run()
	else :
		print "please input python dkzbjj.py YYYYMMDD "




