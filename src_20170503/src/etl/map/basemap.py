# -*- coding:UTF-8 -*-
#!/bin/python
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random
from datetime import datetime,timedelta
from decimal import *

import etl.base.util as util
from etl.base.conf import Config
from etl.map.util import common
import DB2


"""
	基类
"""
class BaseReport():
	def __init__(self,etldate):
		self.db =util.DBConnect()
		self.etldate=etldate
		self.stretldate =util.tostrdate(self.etldate)
		self.para=util.get_etl_date(etldate)
		self.data_func()

	
	def renone(self):
		return []
	
	def _simple_data(self,data,func):
		parafun = data.get("paralist",self.renone)
		if hasattr(parafun,'__call__'):
			drs = func(data["sql"],parafun())
		else:
			drs = func(data["sql"],parafun)
		for code,value in drs.items():
			if self.datadict.has_key(code):self.datadict[code][data["name"]] = value

	"""
		处理过程
		需要子类去实现
	"""
	def handle(self):
		pass	

	"""
		初始化数据集合,需要声明col和初始化数据集合中的key
		需要子类去实现
		此处为一个例子
		col说明:
			table:需要插入的表名,
			cols:需要插入的字段,
			key:比较时使用的字段,
	"""
	def init_dict(self):
		print "请实现init_data,此处仅是一个例子,具体还需要自行实现"
		self.col = {'table':'T_JGC_JG_ZB_QM','cols':['JGBH','JGMC','TJRQ'],'key':['JGBH','TJRQ']} 
		return {}
		d = {}
		sql = u"select  trim(branch_code) JGBH,branch_NAME from BRANCH"
		self.db.cursor.execute(sql)
		rows = self.db.cursor.fetchall()
		for row in rows:
			item={}
			item["JGBH"]=row[0]
			item["JGMC"] = row[1]
			d[row[0]] = item
		return {}
	"""
		指标配置
		需要子类去实现
		必备属性:
			name:在数据源中的名字
			func:查询数据源的函数,可自行扩展+实现
		扩展属性:
			sql:查询用到的sql,现在主要供simple_data使用
			paralist:sql执行中使用的参数,可以是函数，或者list
		其他，可自行扩展
			
	"""	
	def data_func(self):
		print "请实现data,此处仅是一个例子,具体还需要自行实现"
		pass
		self.datalist = [
		{   
			"name":"CKYE",
                	"func":self.simple_data,
                	"sql":"""
				select '31',sum(f.balance)*0.01 je1
				from f_balance f
				where date_id=?
			""",
			"paralist":self.get_tjrq,
		},
		]
	"""
		简单查询
	"""
	def simple_data(self,sql,paralist):
		self.db.cursor.execute(sql.encode('gb2312'),paralist)
		rows = self.db.cursor.fetchall() 
		rsdict = {}
		for row in rows:
			rsdict[row[0]] = row[1]
		return rsdict

		
	def get_tjrq(self):
		return self.para["DATE"]

	def data2rs(self):
		return self.datadict.values()	

	def get_data(self):
		self.datadict = self.init_dict()
		for data in self.datalist:
			func = data.get('func',None)
			if func and func.func_name == 'simple_data':
				self._simple_data(data,func)
			elif func:
				func()
			else:
				print "请定义处理函数"
		self.handle()
				
		"""
		此时的数据格式
		self.datadict = {
			"3409371":{'JGBH':'3409371','JGMC':'121212','TJRQ':'2016-12-12'},
			"3409372":{'JGBH':'3409372','JGMC':'1213','TJRQ':'2016-12-12'},
			"3409373":{'JGBH':'3409373','JGMC':'1213','TJRQ':'2016-12-12'},
		}
		"""
		rs = self.data2rs()
		#rs = common.list2dict(data,col)
		"""
		rs = [
			"3409371":{'JGBH':'3409371','JGMC':'121212','TJRQ':'2016-12-12'},
			"3409372":{'JGBH':'3409372','JGMC':'1213','TJRQ':'2016-12-12'},
			"3409373":{'JGBH':'3409373','JGMC':'1213','TJRQ':'2016-12-12'},
		]
		"""
		common.insert_update(self.db,rs,self.col)
	
	def run(self):
		try :
			self.get_data()
			self.db.conn.commit()
		finally :
			self.db.closeDB()
if __name__=="__main__":
	arglen=len(sys.argv)
	if arglen  == 2:
		BaseReport(sys.argv[1]).run()
	else :
		print "please input python %s.py YYYYMMDD "% sys.argv[0]
