# -*- coding:UTF-8 -*-
#!/bin/python
import etl.base.util as util
from basereport import BaseReport
from etl.performance.util import common
import DB2
import sys

"""
	例子
"""
class Demo(BaseReport):
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
		d = {}
		sql = u"select  trim(org0_code) JGBH,org0_NAME from D_ORG"
		self.db.cursor.execute(sql)
		rows = self.db.cursor.fetchall()
		for row in rows:
			item={}
			item["JGBH"]=row[0]
			item["JGMC"] = row[1]
			item["TJRQ"] = self.stretldate
			d[row[0]] = item
		return d
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

if __name__=="__main__":
	arglen=len(sys.argv)
	if arglen  == 2:
		Demo(sys.argv[1]).run()
	else :
		print "please input python %s.py YYYYMMDD "% sys.argv[0]
