# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
客户经理存款佣金报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['tjrq','jgbh','yggh']
        filterstr,vlist = self.make_eq_filterstr()
   

        sql ="""
            SELECT  A.TJRQ,A.JGBH,B.BRANCH_NAME as JGMC,A.YGGH,A.YGXM,A.JE1,A.JE2,(A.je1+A.je2) as hj,A.JE4,A.JE5,A.JE6,A.JE7,A.JE8,A.JE9,(A.je1+A.je2-A.je4-A.je5-A.je6-A.je7-A.je8-A.je9) as sf,A.PARA_ID
            FROM T_JGC_SFXC A 
            INNER JOIN BRANCH B
            ON A.JGBH=B.BRANCH_CODE 
       
            where 1=1 %s
        """%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)


    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ? "%k
                vlist.append(v)
        return filterstr,vlist

    def column_header(self):
        return ["操作nidaye","统计日期","机构编号","机构名称","员工工号","员工姓名","基本工资","预发绩效工资","月工资合计","住房公积金","养老金","医疗保险","失业保险","企业年金","个人所得税","实发工资"]
    
    
    @property
    def page_size(self):
        return 8
