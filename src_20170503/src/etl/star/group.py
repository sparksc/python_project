# -*- coding:utf-8 -*-
#!/bin/python  

import os, time, random  
import DB2  
from datetime import datetime,timedelta

from etl.base.conf import *
import etl.base.util as util
from etl.base.util import BaseDim,DimConnect
from etl.star.transformdict import *
from etl.base.singleton import singleton
from etl.base.logger import info,debug


@singleton        
class DimGroup(BaseDim):
    def __init__(self):
        self.dim = DimConnect("D_GROUP",sequence_name="D_GROUP_SEQ")
        self.dim.finish()
        self.load_dep_relation()

    def get_rela_dict(self, sql, para=None):
        cursor = self.dim.cursor
        if para:
            cursor.execute(sql,para)
        else:
            cursor.execute(sql)
        d={}
        row = cursor.fetchone()
        while row:
            xrow=d.get( str(row[0]) )
            if xrow is None : xrow=[]
            if row not in xrow:
                xrow.append(row)
                d[str(row[0])]=xrow
            row = cursor.fetchone()
        return d

    def load_dep_relation(self):
        sql="""
            select 
                org_no||'-'||cust_in_no
                ,manager_no
                ,typ||hook_type type
                ,sum(percentage)
            from cust_hook 
            where 
                STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and typ = '存款'
              and start_date <=%d
              and end_date >= %d
              group by org_no||'-'||cust_in_no,manager_no, typ||hook_type
            order by 1,2
        """%(Config().etldate,Config().etldate)
        print sql
        self.ckcust_managers = self.get_rela_dict(sql)

        sql="""
            select 
                org_no||'-'||account_no
                ,manager_no
                ,typ||hook_type type
                ,sum(percentage) percentage
            from ACCOUNT_HOOK 
            where 
                STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and typ = '存款'
              and start_date <=%d
              and end_date >= %d
             group by    org_no||'-'||account_no,manager_no, typ||hook_type
            order by 1,2
        """%(Config().etldate,Config().etldate)
        print sql
        self.ckacct_managers = self.get_rela_dict(sql)


    def find_dim_id_by_dep_account_no(self, org_no, account_no, cst_no):
        accts = self.ckacct_managers.get( org_no +"-" + account_no )
        if accts is None:
            accts = self.ckcust_managers.get( org_no + "-" + cst_no )

        group_key = None
        group_type = "机构管理"
        rest_assign = 100
        group_key = None
        if accts is not None:
            for k in accts:
                group_type = "客户经理管理"
                rest_assign = rest_assign - k[3] 
                ks = [ str(k[x+1]) for x in range(3)]
                if group_key is None:
                    group_key = "-".join( ks )
                else:
                    group_key = group_key + ";"  + "-".join( ks )
            if rest_assign < 0 :
                raise Exception("挂钩比例有错，%s-%s"%( account_no,org_no ))
        if group_key is None : 
            group_key ="%s-机构管理-%d"%(org_no, rest_assign)
        dimkey = { "GROUP_KEY":group_key,"REST_ASSIGN":rest_assign,"GROUP_TYPE":group_type}
        return self.dim.find_dim_id(dimkey)

def group_split():
    pass
    db = util.DBConnect()
    try:
        cursor = db.cursor
        cursor.execute( "select * from d_group")
        row = cursor.fetchone()
        datas = []
        delsql = "delete from d_group_relation "
        insersql = """
            insert into d_group_relation( group_id,sale_code,sale_role,GROUP_TYPE,percent)
                values ( ?,?,?,?,? )
        """
        while row:
            group_type = row[1]
            group_key = row[3]
            if group_key == "无":
                data =[row[0],"无","机构管理",group_type,row[2]]
                datas.append( data )
            else:
                gks = group_key.split(";")
                for gk in gks:
                    keys = gk.split("-")
                    data = [ row[0], keys[0],keys[1],group_type,int(keys[2]) ]
                    datas.append( data )
            row = cursor.fetchone()
        cursor.execute(delsql)
        cursor.execute(delsql)
        cursor.executemany(insersql, datas)
        db.conn.commit()
    finally :
        db.closeDB()

if __name__=='__main__':
    group_split()
