# -*- coding: utf-8 -*-

import datetime,xlrd
from flask import json, g,current_app
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all

from .service import BaseService
from ..base import utils
from ..model import BranchGrade,Branch,UserBranch,User,UserGroup,T_Para_Detail,T_Para_Type,T_Para_Header,Group,Hand_Maintain,Bank_ProfitEarning_Input
import datetime
from userreport import UserReport


ur = UserReport()
local_year,last_year,local_satrday,last_endday = ur.get_year_day()
class Branch_grade_reportService():
    """ Target Service  """

    def update(self, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            adj_grade = kwargs.get('adj_grade')

            g.db_session.query(BranchGrade).filter(BranchGrade.id == item_id).update({BranchGrade.adj_grade:adj_grade,BranchGrade.grade:adj_grade})
            return u'修改成功！'
        except Exception,e:
            return u'修改失败！'
            
    def get_grade_param(self, **kwargs):
        type_name = kwargs.get('type_name')
        min_header_keys = kwargs.get('min_header_key')
        max_header_keys = kwargs.get('max_header_key')
        real_datas = kwargs.get('real_data')              # 实绩
        header_name = kwargs.get('header_name')          # 分值
        kscore = []

        for k in range(0,len(real_datas)):
            fscore = []
            for n in range(0,len(min_header_keys)):
                min_header_key = min_header_keys[n]
                max_header_key = max_header_keys[n]
                real_data = real_datas[k][n]
                
                min_param = g.db_session.query(T_Para_Detail.detail_value).\
                        join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
                        join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
                        filter(T_Para_Type.type_name == type_name).\
                        filter(T_Para_Header.header_key == min_header_key).\
                        order_by(T_Para_Detail.para_row_id).all()
                max_param = g.db_session.query(T_Para_Detail.detail_value).\
                        join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
                        join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
                        filter(T_Para_Type.type_name == type_name).\
                        filter(T_Para_Header.header_key == max_header_key).\
                        order_by(T_Para_Detail.para_row_id).all()
                score = g.db_session.query(T_Para_Detail.detail_value).\
                    join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
                    join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
                    filter(T_Para_Type.type_name == type_name).\
                    filter(T_Para_Header.header_name == header_name).\
                    order_by(T_Para_Detail.para_row_id).all()
                #current_app.logger.debug(str(min_param)+"****"+str(len(min_param))+"****"+str(score))

                if min_header_key in ['min_ave_profit_year','min_ave_dloan','min_ave_dloan_year','min_income_year','min_inter_set','min_ebank_account_num','min_credit_card_num','min_loan_num','min_ebank_sub_rate','min_branch_ave_hook']:
                    if float(real_data) > float(min_param[0][0]):
                        fscore.append(score[0][0])
                    for i in range(1,len(min_param)):
                        if float(real_data) > float(min_param[i][0]) and float(real_data) <= float(max_param[i][0]):
                            fscore.append(score[i][0])
                    if float(real_data) > float(min_param[len(score)-1][0]):
                        fscore.append(score[len(min_param)-1][0])
                    if float(real_data) <= 0:
                        fscore.append(score[len(min_param)-1][0])
                elif min_header_key in ['min_FOR_GRAD_BAD_rate']:
                    for i in range(1,len(min_param)):
                        if float(real_data) > float(min_param[i][0]) and float(real_data) <= float(max_param[i][0]):
                            fscore.append(score[i][0])
                    if float(real_data) > float(min_param[len(score)-1][0]):
                        fscore.append(score[len(min_param)-1][0])
                    if float(real_data) <= 0:
                        fscore.append(score[1][0])
                else:
                    if float(real_data) > float(min_param[0][0]):
                        fscore.append(score[0][0])
                    for i in range(1,len(min_param)):
                        if float(real_data) > float(min_param[i][0]) and float(real_data) <= float(max_param[i][0]):
                            fscore.append(score[i][0])
            kscore.append(fscore)
        return kscore
            
    def get_score(self, **kwargs):
        real_data = g.db_session.query(Bank_ProfitEarning_Input.year_profit,Hand_Maintain.org_count,Bank_ProfitEarning_Input.org_code,Bank_ProfitEarning_Input.syear).outerjoin(Hand_Maintain,and_(Hand_Maintain.syear==Bank_ProfitEarning_Input.syear,Hand_Maintain.org_code==Bank_ProfitEarning_Input.org_code)).filter(Bank_ProfitEarning_Input.syear==last_year).order_by(Bank_ProfitEarning_Input.org_code).all()
        for i in range(0,len(real_data)):
            if real_data[i][1] == None:
                e = u"请补录支行(部): " + str(real_data[i][2]) + u" 在" + str(real_data[i][3]) + u"年的人数"
                return e
        #计算年度人均利润(万元)
        for i in range(0,len(real_data)):
            temp = ()
            avg_profit = str(round(float(real_data[i][0]) / float(real_data[i][1]) , 2) )
            temp = (avg_profit,real_data[i][2],real_data[i][3])
            real_data[i] = temp
        fscore = []
        min_header_key = ['min_ave_profit_year']
        max_header_key = ['max_ave_profit_year']
        para1 = {'type_name':'支行（部）业务经营管理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'等级值'}
        score = self.get_grade_param(**para1)
        para2 = {'type_name':'支行（部）业务经营管理等级指标权重参数','header_key':'branch_weight'}
        weight = self.get_weight(**para2)
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[3][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            org_no = real_data[n][1]
            org = g.db_session.query(BranchGrade.org_no).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).first()
            if org:
                g.db_session.query(BranchGrade).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).update({BranchGrade.ave_profit_year_score:score[n][0],BranchGrade.ave_profit_year_wscore:str(float(fscore[n])),BranchGrade.ave_profit_year_weight:weight[3][0],BranchGrade.ave_profit_year:real_data[n][0]})
            elif not org:
                g.db_session.add(BranchGrade(org_no=real_data[n][1], ave_profit_year_score=score[n][0], ave_profit_year_wscore=str(float(fscore[n])), ave_profit_year_weight=weight[3][0], kyear=real_data[n][2],ave_profit_year=real_data[n][0]))

        #计算等级
        self.calculate_all_grade(real_data)

        #计算综合分
        allscore=g.db_session.query(BranchGrade.ave_dbal_year_wscore,BranchGrade.ave_dloan_wscore,BranchGrade.ave_dloan_year_wscore,BranchGrade.ave_profit_year_wscore,BranchGrade.income_year_wscore,BranchGrade.inter_set_wscore,BranchGrade.ebank_account_num_wscore,BranchGrade.credit_card_num_wscore,BranchGrade.loan_num_wscore,BranchGrade.ebank_sub_rate_wscore,BranchGrade.branch_ave_hook_wscore,BranchGrade.for_grad_bad_rate_wscore,BranchGrade.org_no,BranchGrade.kyear).filter(BranchGrade.kyear == last_year).all() 
        for n in range(0,len(allscore)):
            org_no = allscore[n][12]
            total_score=0
            lens = len(allscore)
            for i in range(0,12):
                if not allscore[n][i] is None :
                    total_score=total_score + float(allscore[n][i])
            para0 = {'score':total_score,'lens':lens}
            kgrade = self.get_grade(**para0)
            g.db_session.query(BranchGrade).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==allscore[n][13]).update({BranchGrade.total_score:str(float(total_score)),BranchGrade.sys_grade:kgrade[n],BranchGrade.grade:kgrade[n]})

            g.db_session.flush()
            #有调整等级则取调整之后的等级
            lscore = g.db_session.query(BranchGrade.adj_grade).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==allscore[n][13]).first()
            if not (lscore[0] is None):
                g.db_session.query(BranchGrade).filter(BranchGrade.org_no == org_no).update({BranchGrade.grade:lscore[1]})
        return "计算成功"

    def get_grade(self, **kwargs):
        score = kwargs.get('score')
        lens = kwargs.get('lens')
        grade = g.db_session.query(T_Para_Detail.detail_value).filter(T_Para_Detail.detail_key == 'branch_grade').order_by(T_Para_Detail.para_row_id).all()
        min_param = g.db_session.query(T_Para_Detail.detail_value).filter(T_Para_Detail.detail_key == 'min_branch_score').order_by(T_Para_Detail.para_row_id).all()
        max_param = g.db_session.query(T_Para_Detail.detail_value).filter(T_Para_Detail.detail_key == 'max_branch_score').order_by(T_Para_Detail.para_row_id).all()
        kgrade = []
        for n in range(0,int(lens)):
            if  float(score) >= float(min_param[0][0]) and float(score) < float(max_param[0][0]):
                mgrade = grade[0][0]
            for i in range(1,len(min_param)):
                if float(score) >= float(min_param[i][0]) and float(score) < float(max_param[i][0]):
                    mgrade = grade[i][0]
            kgrade.append(mgrade)
        return kgrade
    
    def add_grade(self, **kwargs):
        grade = g.db_session.query(BranchGrade.grade,BranchGrade.org_no,BranchGrade.kyear).filter(BranchGrade.kyear==last_year).order_by(BranchGrade.id).all()
        for i in range(0,len(grade)):
            date = grade[i][2] + '0101'
            org_no = grade[i][1]
            level = grade[i][0]
            result = ur.update_org_grade(org_no,level,True)
        return result

    def grade_param(self, **kwargs):
        real_data = kwargs.get('real_data')
        type_name = kwargs.get('type_name') 
        detail_key = kwargs.get('detail_key')   # 分值

        row_id = g.db_session.query(T_Para_Detail.para_row_id).\
                 join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
                 join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
                 filter(T_Para_Type.type_name == type_name).\
                 filter(T_Para_Detail.detail_value == real_data).first()
        row_id = row_id[0]
        score = g.db_session.query(T_Para_Detail.detail_value).\
                join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
                join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
                filter(T_Para_Type.type_name == type_name).\
                filter(T_Para_Detail.para_row_id == row_id).\
                filter(T_Para_Detail.detail_key == detail_key).first()
        if score:
            score = score[0]
        return score

    def get_weight(self, **kwargs):
        type_name = kwargs.get('type_name')
        header_key = kwargs.get('header_key')

        weight = g.db_session.query(T_Para_Detail.detail_value).\
                 join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
                 join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
                 filter(T_Para_Type.type_name == type_name).\
                 filter(T_Para_Header.header_key == header_key).\
                 order_by(T_Para_Detail.para_row_id).all()

        return weight

    def calculate_all_grade(self,*kwargs):
        #计算年度日均存款总量(亿元)
        org_etc_score=[]
        real_data = kwargs[0]
        temp=[]
        for i in range(0,len(real_data)):
            tup = ()
            dep = ur.dep_avg_all(real_data[i][2],str(real_data[i][1]),True)
            dep = str(round(dep/10000000000.00,2))
            tup = (dep,real_data[i][1],real_data[i][2])
            temp.append(tup)
        real_data=temp
        fscore = []
        min_header_key = ['min_ave_dbal_year']
        max_header_key = ['max_ave_dbal_year']
        para1 = {'type_name':'支行（部）业务经营管理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'等级值'}
        score = self.get_grade_param(**para1)
        para2 = {'type_name':'支行（部）业务经营管理等级指标权重参数','header_key':'branch_weight'}
        weight = self.get_weight(**para2)
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[0][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            org_no = real_data[n][1]
            org = g.db_session.query(BranchGrade.org_no).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).first()
            if org:
                g.db_session.query(BranchGrade).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).update({BranchGrade.ave_dbal_year_score:score[n][0],BranchGrade.ave_dbal_year_wscore:str(float(fscore[n])),BranchGrade.ave_dbal_year_weight:weight[0][0],BranchGrade.ave_dbal_year:real_data[n][0]})
               
        org_etc_score.append(fscore)

        #人均日均存款量(万元)
        temp=[]
        for i in range(0,len(real_data)):
            tup = ()
            dep = ur.dep_avg_all(real_data[i][2],str(real_data[i][1]),True)
            dep = (round(dep/1000000.00,2))
            pe_count = g.db_session.query(Hand_Maintain.org_count).filter(Hand_Maintain.syear==real_data[i][2],Hand_Maintain.org_code==real_data[i][1]).first()
            dep = str(round(dep/float(pe_count[0]) ,2))
            tup = (dep,real_data[i][1],real_data[i][2])
            temp.append(tup)
        real_data=temp
        fscore = []
        min_header_key = ['min_ave_dloan']
        max_header_key = ['max_ave_dloan']
        para1 = {'type_name':'支行（部）业务经营管理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'等级值'}
        score = self.get_grade_param(**para1)
        para2 = {'type_name':'支行（部）业务经营管理等级指标权重参数','header_key':'branch_weight'}
        weight = self.get_weight(**para2)
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[1][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            org_no = real_data[n][1]
            org = g.db_session.query(BranchGrade.org_no).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).first()
            if org:
                g.db_session.query(BranchGrade).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).update({BranchGrade.ave_dloan_score:score[n][0],BranchGrade.ave_dloan_wscore:str(float(fscore[n])),BranchGrade.ave_dloan_weight:weight[1][0],BranchGrade.ave_dloan:real_data[n][0]})
               
        org_etc_score.append(fscore)

        #日均贷款总量(亿元)
        temp=[]
        for i in range(0,len(real_data)):
            tup = ()
            dep = ur.loan_avg_all(real_data[i][2],str(real_data[i][1]),True)
            dep = (round(dep/10000000000.00,2))
            pe_count = g.db_session.query(Hand_Maintain.org_count).filter(Hand_Maintain.syear==real_data[i][2],Hand_Maintain.org_code==real_data[i][1]).first()
            dep = str(round(dep/float(pe_count[0]) ,2))
            tup = (dep,real_data[i][1],real_data[i][2])
            temp.append(tup)
        real_data=temp
        fscore = []
        min_header_key = ['min_ave_dloan_year']
        max_header_key = ['max_ave_dloan_year']
        para1 = {'type_name':'支行（部）业务经营管理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'等级值'}
        score = self.get_grade_param(**para1)
        para2 = {'type_name':'支行（部）业务经营管理等级指标权重参数','header_key':'branch_weight'}
        weight = self.get_weight(**para2)
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[2][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            org_no = real_data[n][1]
            org = g.db_session.query(BranchGrade.org_no).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).first()
            if org:
                g.db_session.query(BranchGrade).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).update({BranchGrade.ave_dloan_year_score:score[n][0],BranchGrade.ave_dloan_year_wscore:str(float(fscore[n])),BranchGrade.ave_dloan_year_weight:weight[2][0],BranchGrade.ave_dloan_year:real_data[n][0]})
               
        org_etc_score.append(fscore)

        #年度营业收入(万元)
        temp=[]
        for i in range(0,len(real_data)):
            tup = ()
            year_earn = g.db_session.query(Bank_ProfitEarning_Input.year_earning).filter(Bank_ProfitEarning_Input.syear==real_data[i][2],Bank_ProfitEarning_Input.org_code==real_data[i][1]).first()
            year_earn = str(round(float(year_earn[0]),2) )
            tup = (year_earn,real_data[i][1],real_data[i][2])
            temp.append(tup)
        real_data=temp
        fscore = []
        min_header_key = ['min_income_year']
        max_header_key = ['max_income_year']
        para1 = {'type_name':'支行（部）业务经营管理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'等级值'}
        score = self.get_grade_param(**para1)
        para2 = {'type_name':'支行（部）业务经营管理等级指标权重参数','header_key':'branch_weight'}
        weight = self.get_weight(**para2)
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[4][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            org_no = real_data[n][1]
            org = g.db_session.query(BranchGrade.org_no).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).first()
            if org:
                g.db_session.query(BranchGrade).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).update({BranchGrade.income_year_score:score[n][0],BranchGrade.income_year_wscore:str(float(fscore[n])),BranchGrade.income_year_weight:weight[4][0],BranchGrade.income_year:real_data[n][0]})
               
        org_etc_score.append(fscore)

        #国际结算量(万美元)
        temp=[]
        for i in range(0,len(real_data)):
            tup = ()
            earn = ur.international_num(real_data[i][2],str(real_data[i][1]),True)
            tup = (earn,real_data[i][1],real_data[i][2])
            temp.append(tup)
        real_data=temp
        fscore = []
        min_header_key = ['min_inter_set']
        max_header_key = ['max_inter_set']
        para1 = {'type_name':'支行（部）业务经营管理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'等级值'}
        score = self.get_grade_param(**para1)
        para2 = {'type_name':'支行（部）业务经营管理等级指标权重参数','header_key':'branch_weight'}
        weight = self.get_weight(**para2)
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[5][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            org_no = real_data[n][1]
            org = g.db_session.query(BranchGrade.org_no).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).first()
            if org:
                g.db_session.query(BranchGrade).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).update({BranchGrade.inter_set_score:score[n][0],BranchGrade.inter_set_wscore:str(float(fscore[n])),BranchGrade.inter_set_weight:weight[5][0],BranchGrade.inter_set:real_data[n][0]})
               
        org_etc_score.append(fscore)

        #电子银行开户数(户)
        temp=[]
        for i in range(0,len(real_data)):
            tup = ()
            earn = ur.ebank_num(real_data[i][2],str(real_data[i][1]),True)
            tup = (earn,real_data[i][1],real_data[i][2])
            temp.append(tup)
        real_data=temp
        fscore = []
        min_header_key = ['min_ebank_account_num']
        max_header_key = ['max_ebank_account_num']
        para1 = {'type_name':'支行（部）业务经营管理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'等级值'}
        score = self.get_grade_param(**para1)
        para2 = {'type_name':'支行（部）业务经营管理等级指标权重参数','header_key':'branch_weight'}
        weight = self.get_weight(**para2)
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[6][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            org_no = real_data[n][1]
            org = g.db_session.query(BranchGrade.org_no).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).first()
            if org:
                g.db_session.query(BranchGrade).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).update({BranchGrade.ebank_account_num_score:score[n][0],BranchGrade.ebank_account_num_wscore:str(float(fscore[n])),BranchGrade.ebank_account_num_weight:weight[6][0],BranchGrade.ebank_account_num:real_data[n][0]})
               
        org_etc_score.append(fscore)

        #贷记卡发卡量(户)
        temp=[]
        for i in range(0,len(real_data)):
            tup = ()
            num= ur.card_num(real_data[i][2],str(real_data[i][1]),True)
            tup = (num,real_data[i][1],real_data[i][2])
            temp.append(tup)
        real_data=temp
        fscore = []
        min_header_key = ['min_credit_card_num']
        max_header_key = ['max_credit_card_num']
        para1 = {'type_name':'支行（部）业务经营管理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'等级值'}
        score = self.get_grade_param(**para1)
        para2 = {'type_name':'支行（部）业务经营管理等级指标权重参数','header_key':'branch_weight'}
        weight = self.get_weight(**para2)
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[7][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            org_no = real_data[n][1]
            org = g.db_session.query(BranchGrade.org_no).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).first()
            if org:
                g.db_session.query(BranchGrade).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).update({BranchGrade.credit_card_num_score:score[n][0],BranchGrade.credit_card_num_wscore:str(float(fscore[n])),BranchGrade.credit_card_num_weight:weight[7][0],BranchGrade.credit_card_num:real_data[n][0]})
               
        org_etc_score.append(fscore)

        #贷款户数(户)
        temp=[]
        for i in range(0,len(real_data)):
            tup = ()
            num= ur.loan_num(real_data[i][2],str(real_data[i][1]),True)
            tup = (num,real_data[i][1],real_data[i][2])
            temp.append(tup)
        real_data=temp
        fscore = []
        min_header_key = ['min_loan_num']
        max_header_key = ['max_loan_num']
        para1 = {'type_name':'支行（部）业务经营管理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'等级值'}
        score = self.get_grade_param(**para1)
        para2 = {'type_name':'支行（部）业务经营管理等级指标权重参数','header_key':'branch_weight'}
        weight = self.get_weight(**para2)
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[8][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            org_no = real_data[n][1]
            org = g.db_session.query(BranchGrade.org_no).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).first()
            if org:
                g.db_session.query(BranchGrade).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).update({BranchGrade.loan_num_score:score[n][0],BranchGrade.loan_num_wscore:str(float(fscore[n])),BranchGrade.loan_num_weight:weight[8][0],BranchGrade.loan_num:real_data[n][0]})
               
        org_etc_score.append(fscore)

        #电子银行替代率
        temp=[]
        for i in range(0,len(real_data)):
            tup = ()
            num= str(ur.ebank_percent(real_data[i][2],str(real_data[i][1]),True))
            tup = (num,real_data[i][1],real_data[i][2])
            temp.append(tup)
        real_data=temp
        fscore = []
        min_header_key = ['min_ebank_sub_rate']
        max_header_key = ['max_ebank_sub_rate']
        para1 = {'type_name':'支行（部）业务经营管理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'等级值'}
        score = self.get_grade_param(**para1)
        para2 = {'type_name':'支行（部）业务经营管理等级指标权重参数','header_key':'branch_weight'}
        weight = self.get_weight(**para2)
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[9][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            org_no = real_data[n][1]
            org = g.db_session.query(BranchGrade.org_no).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).first()
            if org:
                g.db_session.query(BranchGrade).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).update({BranchGrade.ebank_sub_rate_score:score[n][0],BranchGrade.ebank_sub_rate_wscore:str(float(fscore[n])),BranchGrade.ebank_sub_rate_weight:weight[9][0],BranchGrade.ebank_sub_rate:real_data[n][0]})
               
        org_etc_score.append(fscore)

        #支行贷款户日均存贷挂钩率(%)
        temp=[]
        for i in range(0,len(real_data)):
            tup = ()
            num= str(ur.avg_dep_loan_percent(real_data[i][2],str(real_data[i][1]),True))
            tup = (num,real_data[i][1],real_data[i][2])
            temp.append(tup)
        real_data=temp
        fscore = []
        min_header_key = ['min_branch_ave_hook']
        max_header_key = ['max_branch_ave_hook']
        para1 = {'type_name':'支行（部）业务经营管理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'等级值'}
        score = self.get_grade_param(**para1)
        para2 = {'type_name':'支行（部）业务经营管理等级指标权重参数','header_key':'branch_weight'}
        weight = self.get_weight(**para2)
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[10][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            org_no = real_data[n][1]
            org = g.db_session.query(BranchGrade.org_no).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).first()
            if org:
                g.db_session.query(BranchGrade).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).update({BranchGrade.branch_ave_hook_score:score[n][0],BranchGrade.branch_ave_hook_wscore:str(float(fscore[n])),BranchGrade.branch_ave_hook_weight:weight[10][0],BranchGrade.branch_ave_hook:real_data[n][0]})
               
        org_etc_score.append(fscore)

        #四级不良贷款率(%)
        temp=[]
        for i in range(0,len(real_data)):
            tup = ()
            num= str(ur.bad_bal_percent(real_data[i][2],str(real_data[i][1]),True))
            tup = (num,real_data[i][1],real_data[i][2])
            temp.append(tup)
        real_data=temp
        fscore = []
        min_header_key = ['min_FOR_GRAD_BAD_rate']
        max_header_key = ['max_FOR_GRAD_BAD_rate']
        para1 = {'type_name':'支行（部）业务经营管理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'等级值'}
        score = self.get_grade_param(**para1)
        para2 = {'type_name':'支行（部）业务经营管理等级指标权重参数','header_key':'branch_weight'}
        weight = self.get_weight(**para2)
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[11][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            org_no = real_data[n][1]
            org = g.db_session.query(BranchGrade.org_no).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).first()
            if org:
                g.db_session.query(BranchGrade).filter(BranchGrade.org_no == org_no,BranchGrade.kyear==real_data[n][2]).update({BranchGrade.for_grad_bad_rate_score:score[n][0],BranchGrade.for_grad_bad_rate_wscore:str(float(fscore[n])),BranchGrade.for_grad_bad_rate_weight:weight[11][0],BranchGrade.for_grad_bad_rate:real_data[n][0]})
               
        org_etc_score.append(fscore)

        return org_etc_score
