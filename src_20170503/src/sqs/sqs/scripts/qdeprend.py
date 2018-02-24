# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
存款待认定
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CUST_NO','ORG_NO','NOTE','CST_TYP','YD','LD','hide']
        filterstr,vlist,filterstr2,vlist2,filterstr3,vlist3 = self.make_eq_filterstr()
        sql1 =u"""
                select c.id, c.org_no,o.branch_name, CASE WHEN left(c.cust_in_no,2)='81' THEN '对私' WHEN left(c.cust_in_no,2)='82' THEN '对公' END S_SIGN,
                c.cust_no,i.cust_name,c.percentage,nvl(balance/100.00,0) bal,nvl(add_avg_balance/100.00,0) pdt,c.note, c.cust_in_no
                from cust_hook c
                join branch o on o.branch_code=c.org_no
                join d_cust_info i on i.cust_no=c.cust_in_no
                where c.typ='存款' and c.status='待手工' %s
                order by c.id desc
               """%(filterstr)
        print sql1
        row1 = self.engine.execute(sql1,vlist).fetchall()

        row = list(row1)
        for i in range(0,len(row)):
            row[i] = list(row[i])
            row[i][6] =self.trans_dec('%.2f' % row[i][6])
            row[i][7] =self.trans_dec('%.2f' % row[i][7])
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr,filterstr2,filterstr3 ="","",""
        vlist,vlist2,vlist3 = [],[],[]
        for k,v in self.args.items():
            if k == 'login_teller_no':
                if self.deal_teller_query_auth(v) == True:
                    filterstr = filterstr+" and c.manager_no = '%s'"%v
            elif k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False :
                    filterstr = filterstr+" and c.org_no in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'ORG_NO':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and c.org_no in ( %s ) "%(vvv)
                elif k == 'CUST_NO':
                    filterstr = filterstr + " and c.cust_no  = ?"
                    vlist.append(v)
                elif k == 'NOTE':
                    filterstr = filterstr + " and c.note like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                elif k == 'LD':
                    filterstr = filterstr + " and balance >= ? "
                    vlist.append(float(v)*1000000)
                elif k == 'YD':
                    filterstr = filterstr + " and add_avg_balance >= ? "
                    vlist.append(float(v)*1000000)
                elif k == 'hide':
                    filterstr = filterstr + 'and c.hide = ?'
                    vlist.append(v.strip())
                elif k == 'CST_TYP':
                    if v == u'对公':
                        filterstr = filterstr + " and  left(c.cust_in_no,2)='82' "
                    elif v == u'对私':
                        filterstr = filterstr + " and  left(c.cust_in_no,2)='81' "
                
        return filterstr,vlist,filterstr2,vlist2,filterstr3,vlist3
    def column_header(self):
        return ["序号", "机构号","机构名","公私类型","客户号","客户名","占比(%)","余额(元)","当前日均(元)","地址信息","操作"]

    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        tmp = '{:,}'.format(tmp)
        return tmp
    @property
    def page_size(self):
        return 10
