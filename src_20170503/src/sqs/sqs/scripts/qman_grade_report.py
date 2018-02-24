# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['org_no', 'kyear', 'user_name','grade']
        filterstr,vlist = self.make_eq_filterstr()
        sql = u"""
        SELECT KYEAR,ORG,BRANCH_NAME,USER_NAME,NAME,AVE_DBAL,AVE_DBAL_SCORE,AVE_DBAL_WEIGHT,AVE_DBAL_WSCORE,AVE_DLOAN,AVE_DLOAN_SCORE,AVE_DLOAN_WEIGHT,AVE_DLOAN_WSCORE,LOAN_NUM,LOAN_NUM_SCORE,LOAN_NUM_WEIGHT,LOAN_NUM_WSCORE,DAVE_LOAN,DAVE_LOAN_SCORE,DAVE_LOAN_WEIGHT,DAVE_LOAN_WSCORE,FGRAD_BAD,FGRAD_BAD_SCORE,FGRAD_BAD_WEIGHT,FGRAD_BAD_WSCORE,EDU,EDU_SCORE,EDU_WEIGHT,EDU_WSCORE,LOAN_EXP,LOAN_EXP_SCORE,LOAN_EXP_WEIGHT,LOAN_EXP_WSCORE,EXTRA_SCORE,ILLEGAL_SCORE,TOTAL_SCORE,SYS_GRADE,ADJ_GRADE,GRADE,ID FROM (
         SELECT A.*,ROW_NUMBER()OVER(PARTITION BY A.KYEAR,A.USER_NAME ORDER BY A.KYEAR,A.USER_NAME ) B FROM (
          SELECT MS.KYEAR,V.ORG, V.BRANCH_NAME, MS.USER_NAME, FU.NAME, MS.AVE_DBAL, MS.AVE_DBAL_SCORE, MS.AVE_DBAL_WEIGHT, MS.AVE_DBAL_WSCORE, MS.AVE_DLOAN, MS.AVE_DLOAN_SCORE, MS.AVE_DLOAN_WEIGHT, MS.AVE_DLOAN_WSCORE, MS.LOAN_NUM, MS.LOAN_NUM_SCORE, MS.LOAN_NUM_WEIGHT, MS.LOAN_NUM_WSCORE, MS.DAVE_LOAN, MS.DAVE_LOAN_SCORE, MS.DAVE_LOAN_WEIGHT, MS.DAVE_LOAN_WSCORE, MS.FGRAD_BAD, MS.FGRAD_BAD_SCORE, MS.FGRAD_BAD_WEIGHT, MS.FGRAD_BAD_WSCORE, FU.EDU, MS.EDU_SCORE, MS.EDU_WEIGHT, MS.EDU_WSCORE, MS.LOAN_EXP, MS.LOAN_EXP_SCORE, MS.LOAN_EXP_WEIGHT, MS.LOAN_EXP_WSCORE, MS.EXTRA_SCORE, MS.ILLEGAL_SCORE, MS.TOTAL_SCORE, MS.SYS_GRADE, MS.ADJ_GRADE, MS.GRADE, MS.ID FROM MAN_SCORE MS 
          JOIN F_USER FU ON FU.USER_NAME = MS.USER_NAME
          JOIN MAN_GRADE MG ON MG.USER_NAME = MS.USER_NAME
          JOIN V_STAFF_INFO V ON V.USER_NAME=MS.USER_NAME
          WHERE 1=1 %s ORDER BY MS.KYEAR DESC,MS.ID
         )  A 
        ) C WHERE C.B=1  ORDER BY C.KYEAR DESC,C.ID
        """%(filterstr)

        print sql
        row = self.engine.execute(sql, vlist).fetchall()
        needtrans = {}
        return self.translate(row, needtrans)

    def make_eq_filterstr(self):
        filterstr = ""
        vlist = []
        for k, v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org_no':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr + "and V.ORG in(%s)"%(vvv)
                else:
                    filterstr = filterstr + "and MS.%s = ?"%k
                    vlist.append(v)
        
        filterstr = "%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'ms.user_name','org_no',None))
       
        return filterstr, vlist
    def column_header(self):
        return [
            [{'name':'统计年份','h':2},{'name':'机构编号','h':2},{'name':'机构名称','h':2},{'name':'员工编号','h':2},{'name':'员工姓名','h':2},{'name':'日均存款余额（亿元）','w':4},{'name':'日均贷款余额（亿元）','w':4},{'name':'管贷户数（户）','w':4},{'name':'贷款户日均存贷挂钩率（%）','w':4},{'name':'四级不良贷款控制（%）','w':4},{'name':'文化程度','w':4},{'name':'信贷工作经验（年）','w':4},{'name':'附加分','h':2},{'name':'违规积分附扣分','h':2},{'name':'综合得分','h':2},{'name':'系统测算等级','h':2},{'name':'调整后等级','h':2},{'name':'等级','h':2},{'name':'操作','h':2}],
            [{'name':'实绩','h':1},{'name':'分值','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'分值','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'分值','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'分值','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩(四级不良率/四级不良金额(万元))','h':1},{'name':'分值','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'分值','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1},{'name':'实绩','h':1},{'name':'分值','h':1},{'name':'权重(%)','h':1},{'name':'得分','h':1}]
        ]

    @property
    def page_size(self):
        return 10

