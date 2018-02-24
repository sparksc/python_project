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
        SELECT  D_RATE, ORG_NO, ORG_NAME, RALE_NO, RALE_NAME, GUST_NO, GUST_NAME, PERSON_LOAN_NAME, PERSON_ASSUER_NAME, COP_PRESENT_NAME, HEAD_PHOTO, FINGER_PRINT, ID_CARD, MARRIAGE,ID
        FROM LOAN_PERSOM_INPUT
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
        return ["统计日期","机构号","机构名称","员工号","员工名称","客户号","客户名称","个人借款","个人担保人","代理人","头像","指纹","身份证件","户口簿","操作"]

    @property
    def page_size(self):    
        return 15
