
# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
pos录入
"""

class Query(ObjectQuery):

    def prepare_object(self):

        self.filterlist = ['ORG_NO','MER_NO','MERCHANT_NAME','POS_NO','TYP','STATUS']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
        select org_no,merchant_name,merchant_no,pos_no,merchant_addr,merchant_contract,merchant_tel,merchant_mob,install_date,typ,status,end_date,id 
        from D_POS where 1=1 %s order by install_date desc,id
        """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'ORG_NO':
                    filterstr = filterstr + " and org_no=?"
                    vlist.append(v.strip())
                elif k == 'MER_NO':
                    filterstr = filterstr + " and merchant_no=?"
                    vlist.append(v.strip())
                elif k=='MERCHANT_NAME':
                    filterstr = filterstr + " and MERCHANT_NAME like "+"'%'||"+"?"+"||'%'"
                    vlist.append(v.strip())
                elif k=='POS_NO':
                    filterstr = filterstr + " and POS_NO=?"
                    vlist.append(v.strip())
                elif k=='TYP':
                    filterstr = filterstr + " and TYP=?"
                    vlist.append(v.strip())  
                elif k=='STATUS':
                    filterstr = filterstr + " and STATUS=?"
                    vlist.append(v.strip())
        return filterstr,vlist
    def column_header(self):
        return ["机构号","商户名称","商户编号","终端号","商户地址","联系人","联系电话","手机号码","安装日期","类型","状态","销户时间"]

    @property
    def page_size(self):
        return 10
