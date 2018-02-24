# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from utils import config
"""
   贷款合同有效合同数报表 
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE','NOTE','ACCT_NO']
        filterstr,vlist = self.make_eq_filterstr()
        print filterstr,vlist
        sql ="""
        SELECT F.DATE_ID,O.ORG0_CODE,O.ORG0_NAME,M.SALE_CODE,M.SALE_NAME,DI.CUST_LONG_NO,DI.CUST_NO,DI.CUST_NAME,
            RIGHT(D.SUB_TYPE,3) AS 产品代码,
            RIGHT(D.SUB_TYPE,3)  AS 产品名称,
            (CASE WHEN LENGTH(DI.CUST_CREDIT_ADDRESS)>LENGTH(DI.CUST_ADDRESS) THEN '信贷地址为:'||DI.CUST_CREDIT_ADDRESS 
                  WHEN DI.CUST_ADDRESS IS NOT NULL THEN '核心地址为:'||DI.CUST_ADDRESS
                  WHEN DI.CUST_CREDIT_ADDRESS IS NOT NULL THEN '信贷地址为:'||DI.CUST_CREDIT_ADDRESS  
                  ELSE '暂无地址信息' END ) AS 地址,
            DI.TEL_CORE,
            D.ACCT_NO AS 合同号,
            ( CASE WHEN D.EMAIL='100' THEN '信用' WHEN D.EMAIL='210' THEN '普通保证' WHEN D.EMAIL='220' THEN '联保' 
                   WHEN D.EMAIL='300' THEN '抵押' WHEN D.EMAIL='411' THEN '系统内存单质押' WHEN D.EMAIL='412' THEN '系统外存单质押' 
                   WHEN D.EMAIL='421' THEN '系统内股金质押' WHEN D.EMAIL='422' THEN '系统外股金质押' WHEN D.EMAIL='490' THEN '其他质押' 
                   WHEN D.EMAIL='532'THEN '抵押＋保证' WHEN D.EMAIL='542' THEN '质押＋保证' WHEN D.EMAIL='599' THEN '组合担保' 
                   WHEN D.EMAIL='999' THEN '全部' 
                   ELSE D.EMAIL END )AS 担保方式,
            DECIMAL(D.CARD_NO) AS 贷款合同金额, 
            DECIMAL(NVL(BD.BALANCE/ 100.00,0)) AS 贷款余额,
            F.STATUS AS 合同状态,D.OPEN_DATE,D.CLOSE_DATE 
        FROM F_CONTRACT_STATUS F
            JOIN D_CUST_CONTRACT D ON F.CONTRACT_ID=D.ID
            JOIN D_ORG O ON D.OPEN_BRANCH_NO=O.ORG0_CODE
            JOIN D_MANAGE DM ON F.MANAGE_ID = DM.ID
            JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID
            JOIN D_CUST_INFO DI ON DI.CUST_NO=D.CST_NO
            LEFT JOIN (
                SELECT D.CONTRACT_NO, SUM(FF.BALANCE) BALANCE 
                FROM F_BALANCE FF 
                    JOIN D_LOAN_ACCOUNT D ON FF.ACCOUNT_ID = D.ID 
                    WHERE FF.DATE_ID = ? AND FF.ACCT_TYPE = '4' AND FF.BALANCE > 0 
                    GROUP BY  D.CONTRACT_NO) BD ON BD.CONTRACT_NO = D.ACCT_NO
         WHERE D.BUSI_TYPE = '贷款合同' AND F.STATUS IN ('发放','暂停','有效')  AND D.CLOSE_DATE>=DATE_ID %s 
         ORDER BY O.ORG0_CODE ,M.SALE_CODE ASC WITH UR
            """%(filterstr)
        print sql
        print vlist 
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i[0:14])
            for j in i[14:16]:
                if j is None:j=0
                j=self.trans_dec(j)
                t.append(j)
            t.append(i[16])
            t.append(i[17])
            t.append(i[18])
            t[9] = self.get_pro_name(t[9])
            rowlist.append(t)
        return self.translate(rowlist,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and O.ORG0_CODE in(%s) "%(vvv)
                elif k == 'DATE_ID':
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
                    vlist.insert(0,v)
                elif k == 'SALE_CODE':
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
                elif k == 'NOTE':
                    filterstr = filterstr+" AND (DI.CUST_ADDRESS LIKE ("+" '%'|| "+"?"+"||'%') OR DI.CUST_CREDIT_ADDRESS LIKE (" +"'%'||" +"?"+"||'%')) "
                    vlist.append(v)
                    vlist.append(v)
                elif k == 'ACCT_NO':
                    vvv = self.dealfilterlist(v)
                    if vvv == '\'two_card\'':
                        filterstr = filterstr+" AND D.SUB_TYPE IN ('51118','51154','51155','51156')"
                    elif vvv == '\'un_two_card\'':
                        filterstr = filterstr+" AND D.SUB_TYPE NOT IN ('51118','51154','51155','51156')"
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'m.SALE_CODE','O.ORG0_CODE', None))
        return filterstr,vlist

    def get_pro_name(self,pro_num):
        pro_dict = {
            '118':u'丰收创业贷款卡',
            '155':u'丰收消费贷',
            '154':u'丰收小额贷',
            '156':u'''丰收卡"先贷后用"循环贷''',
            '1A1':u'个人住房自建房贷款',
            '1A2':u'个人住房公积金贷款',
            '1A3':u'个人住房组合贷款',
            '1A4':u'个人住房改造贷款',
            '1A5':u'个人住房直客式贷款',
            '1A6':u'个人住房商业按揭贷款',
            '1B1':u'个人汽车消费直客式贷款',
            '1B2':u'个人汽车消费按揭贷款',
            '1C1':u'国家助学贷款',
            '1C2':u'商业助学贷款',
            '1C3':u'生源地助学贷款',
            '1D1':u'个人大额耐用消费品贷款',
            '1D2':u'个人生活扶贫贷款',
            '1D3':u'个人其他消费贷款',
            '1D4':u'养老保险专项贷款',
            '1E1':u'个人商用房直客式贷款',
            '1E2':u'个人商用房按揭贷款',
            '1F1':u'个人商用汽车直客式贷款',
            '1F2':u'个人商用汽车按揭贷款',
            '1F3':u'个人商用船舶贷款',
            '1F4':u'个人其他商用交通工具贷款',
            '1G1':u'个人生产经营贷款',
            '1G2':u'粮农贷（对私）',
            '1G3':u'税银贷（个人）'
        }
        if str(pro_num) in pro_dict.keys():
            pro_name = pro_dict[str(pro_num)]
        else:
            pro_name = pro_num
        return pro_name

    def column_header(self):
        return ['统计时间','机构号','机构名','客户经理号','客户经理名','客户号','客户内码','客户名','产品代码','产品名称','联系地址','联系方式','合同号','担保方式','贷款合同金额','贷款余额','合同状态','开始日期','结束日期']
    def trans_dec(self,num):
        tmp = Decimal(num)
        tmp = '{:,}'.format(tmp)
        return tmp

    @property
    def page_size(self):
        return 15
