# -*- coding:UTF-8 -*-
#!/bin/python
import etl.base.util as util
from basereport import BaseReport
from etl.performance.util import common
import DB2
import sys

"""
    客户经理绩效指标报表
"""
class Demo(BaseReport):
    """
        处理过程
        需要子类去实现
    """
    def handle(self):
        for data in self.datadict:
            if 'PRI_LOAN_STOCK_NUM' not in self.datadict[data]:
                self.datadict[data]['PRI_LOAN_STOCK_NUM']=0
            if 'PRI_LOAN_INCRE_NUM' not in self.datadict[data]:
                self.datadict[data]['PRI_LOAN_INCRE_NUM']=0
            self.datadict[data]['PRI_LOAN_INCRE_NUM']-=self.datadict[data]['PRI_LOAN_STOCK_NUM']
            #print self.datadict[data]
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
        self.col = {'table':'T_SJPB_KHJL_JXZB','cols':['TJNF','TJYF','JGBH','JGMC','YGBH','YGMC','PRI_LOAN_STOCK_NUM','PRI_LOAN_INCRE_NUM'],'key':['TJNF','TJYF','JGBH','YGBH']} 
        d = {}
        sql = u"select distinct SALE_CODE,SALE_NAME,SALE_ORG,o.ORG0_NAME from D_SALES_TEMP s join D_ORG o on s.SALE_ORG=o.ORG0_CODE where DIM_DATE= ?".encode('gb2312')
        self.db.cursor.execute(sql,int(self.etldate[0:4]))
        rows = self.db.cursor.fetchall()
        for row in rows:
            item={}
            item["TJNF"]=int(self.etldate[0:4])
            item["TJYF"]=int(self.etldate[4:6])
            item["YGBH"] = row[0]
            item["YGMC"] = row[1]
            item["JGBH"] = row[2]
            item['JGMC'] = row[3]
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
            "name":"PRI_LOAN_STOCK_NUM",
                    "func":self.simple_data,
                    "sql":u"select st.SALE_CODE,int(sum(s.is_loan)) from f_c_custview f inner join  d_cust_type t on f.cust_type_id = t.id  and t.CUST_TYPE = '对私' inner join  d_cust_status s on f.cust_status_id = s.id inner join d_sales_temp st on st.id = f.sales_temp_id where f.date_id = ? group by st.sale_code",
            "paralist":util.get_etl_date(self.etldate).get('LYE'),
        },
        {
            "name":"PRI_LOAN_INCRE_NUM",
                    "func":self.simple_data,
                    "sql":u"select st.SALE_CODE,int(sum(s.is_loan)) from f_c_custview f inner join  d_cust_type t on f.cust_type_id = t.id  and t.CUST_TYPE = '对私' inner join  d_cust_status s on f.cust_status_id = s.id inner join d_sales_temp st on st.id = f.sales_temp_id where f.date_id = ? group by st.sale_code",
            "paralist":util.get_etl_date(self.etldate).get('DATE'),
        },
        ]

if __name__=="__main__":
    arglen=len(sys.argv)
    if arglen  == 2:
        Demo(sys.argv[1]).run()
    else :
        print "please input python %s.py YYYYMMDD "% sys.argv[0]
