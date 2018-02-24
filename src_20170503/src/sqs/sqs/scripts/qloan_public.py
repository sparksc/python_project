# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
对私电子档案录入
"""

class Query(ObjectQuery):
  
    def prepare_object(self):
        filterlist1 = ['date','BRANCH_CODE','user_name']
        global ny 
        filterstr,vlist = self.make_eq_filterstr(filterlist1)
        sql1="""
        SELECT D_RATE, ORG_NO, ORG_NAME, RALE_NO, RALE_NAME, GUST_NO, GUST_NAME, PUBLIC_LOAN_NAME, PUBLIC_ASSUER_NAME, YYZZ, ZZDMZ, SWDJZ, KHXKZ, JGXYDMZ,ID
        FROM LOAN_PUBLIC_INPUT
        where 1=1 %s
        """%(filterstr)
        row = self.engine.execute(sql1,vlist).fetchall()
        needtrans={}

        return self.translate(row,needtrans)
        
    def make_eq_filterstr(self,filterlist):
        filterstr =""
        vlist = []
        global ymday
        for k,v in self.args.items():
            if(k=='date'):
                ymday=v
            if v and k in filterlist:
                if(k=='BRANCH_CODE'):
                    filterstr = filterstr+" and org_no = ? "
                    vlist.append(v)
                if(k=='user_name'):
                    filterstr = filterstr+" and rale_no = ? "
                    vlist.append(v)
        if(len(ymday)==8):
            for k in filterlist:
                if(k=='date'):
                    v=int(ymday)
                    filterstr = filterstr+" and d_rate = ? "
                    vlist.append(v)
            
        return filterstr,vlist


    def column_header(self):
        return ["统计日期","机构号","机构名称","员工号","员工名称","客户号","客户名称","对公借款人","对公担保人","营业执照","组织代码证","税务登记证","开户许可证","机构信用代码证","操作"]

    @property
    def page_size(self):    
        return 15
