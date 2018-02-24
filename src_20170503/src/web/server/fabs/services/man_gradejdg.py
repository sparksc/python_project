# -*- coding: utf-8 -*-

import datetime,xlrd
from flask import json, g, current_app
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all

from .service import BaseService
from ..base import utils
from ..model import ManGrade,Branch,UserBranch,User,UserGroup,T_Para_Detail,T_Para_Type,T_Para_Header,Group,ManScore,User_ExtraScore
import datetime
from userreport import UserReport


ur = UserReport()
local_year,last_year,local_satrday,last_endday = ur.get_year_day()
class Man_gradejdgService():
    """ Target Service  """

    def add_save(self, **kwargs):
        try:
            kyear = kwargs.get('kyear')
            org_no = kwargs.get('org_no')
            org_name = kwargs.get('org_name')
            user_name = kwargs.get('user_name')
            name = kwargs.get('name')
            loan_exp = kwargs.get('loan_exp')
            illegal_score = kwargs.get('illegal_score')
            remarks = kwargs.get('remarks')
            
            if float(illegal_score) < 0:
                return u'违规积分不能为负'
 
            fx = g.db_session.query(User).join(UserGroup,UserGroup.user_id==User.role_id).join(Group,Group.id==UserGroup.group_id).filter(User.user_name==user_name).filter(Group.group_name=='客户经理').filter(Group.group_type_code=='2000').first()
            fy = g.db_session.query(ManGrade).filter(ManGrade.user_name==user_name,ManGrade.kyear==kyear).first()
            if not fx:
                return u'不存在该客户经理！'
            if fy:
                return u'该客户经理已存在！'

            g.db_session.add(ManGrade(kyear=kyear, org_no=org_no, org_name=org_name, user_name=user_name, name=name, loan_exp=loan_exp, illegal_score=illegal_score, remarks=remarks))
            return u'添加成功！'
        except Exception,e:
            return str(e)
 

    def edit_save(self, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            kyear = kwargs.get('kyear')
            org_no = kwargs.get('org_no')
            org_name = kwargs.get('org_name')
            user_name = kwargs.get('user_name')
            name = kwargs.get('name')
            loan_exp = kwargs.get('loan_exp')
            illegal_score = kwargs.get('illegal_score')
            remarks = kwargs.get('remarks')

            if float(illegal_score) < 0:
                return u'违规积分不能为负'

            g.db_session.query(ManGrade).filter(ManGrade.id == item_id).update({ManGrade.kyear:kyear, ManGrade.org_no:org_no, ManGrade.org_name:org_name, ManGrade.user_name:user_name, ManGrade.name:name, ManGrade.loan_exp:loan_exp, ManGrade.illegal_score:illegal_score, ManGrade.remarks:remarks})
            return u'修改成功！'
        except Exception, e:
            return str(e)

    def update(self, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            adj_grade = kwargs.get('adj_grade')

            g.db_session.query(ManScore).filter(ManScore.id == item_id).update({ManScore.adj_grade:adj_grade,ManScore.grade:adj_grade})
            return u'修改成功！'
        except Exception,e:
            return u'修改失败！'

    def delete(sel, **kwargs):
        try:
            row_id = kwargs.get('row_id')

            g.db_session.query(ManGrade).filter(ManGrade.id == row_id).delete()

            return u'删除成功！'
        except Exception, e:
            return u'删除失败！'

    def delete_man(self, **kwargs):
        try:
            row_id = kwargs.get('row_id')

            g.db_session.query(ManScore).filter(ManScore.id == row_id).delete()

            return u'删除成功！'
        except Exception, e:
            return u'删除失败！'
            
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

                if min_header_key in ['min_ave_dbal','min_ave_dloan','min_loan_num','min_loan_exp','Min_YWScore','Min_MYScore','Min_HL','Min_LG','net_lownum','lowyear','low_experience']:
                    if float(real_data) >= float(min_param[0][0]):
                        fscore.append(score[0][0])
                    temp=0
                    for i in range(1,len(min_param)):
                        if float(real_data) >= float(min_param[i][0]) and float(real_data) < float(max_param[i][0]):
                            fscore.append(score[i][0])
                        temp=i
                    if float(real_data)<float(min_param[temp][0]):
                        fscore.append('0')
                elif min_header_key == 'MIN_DAILY_AVE_LOAN':
                    if float(real_data) > float(min_param[0][0]):
                        fscore.append(score[0][0])
                    temp=0
                    for i in range(1,len(min_param)):
                        if float(real_data) > float(min_param[i][0]) and float(real_data) <= float(max_param[i][0]):
                            fscore.append(score[i][0])
                        temp=i
                    if float(real_data)<float(min_param[temp][0]):
                        fscore.append('0')
                elif min_header_key in ['MIN_FOR_GRAD_BAD','Min_FWScore','mis_lowrank','all_lowrank','integration_lowrank','etc_lowrank']:
                    if float(real_data[0]) <= float(min_param[0][0]):
                        fscore.append(score[0][0])
                    for i in range(0,len(min_param)):
                        if float(real_data[0]) >= float(min_param[i][0]) and float(real_data[0]) < float(max_param[i][0]):
                            fscore.append(score[i][0])
                    if float(real_data[0]) > float(min_param[len(min_param)-1][0]):
                        #fscore.append(score[len(min_param)-1][0])
                        fscore.append('0')
                elif min_header_key in ['MIN_FOR_GRAD_BADNUM']:
                    for i in range(1,len(min_param)):
                        if float(real_data[1]) >= float(min_param[i][0]) and float(real_data[1]) < float(max_param[i][0]):
                            fscore.append(score[i][0])
                    if float(real_data[1]) > float(min_param[len(min_param)-1][0]):
                        #fscore.append(score[len(min_param)-1][0])
                        fscore.append('0')
                elif min_header_key == 'Min_CCScore':
                    for i in range(0,len(min_param)-1):
                        if float(real_data) >= float(min_param[i][0]) and float(real_data) < float(max_param[i][0]):
                            fscore.append(score[i][0])
                    if float(real_data) >= float(min_param[len(min_param)][0]):
                        fscore.append(score[len(min_param)][0])
                elif min_header_key in ['min_abv_ave','Min_WScore']:
                    if float(real_data) < float(max_param[0][0]):
                        fscore.append(score[0][0])
                    if float(real_data) >= float(min_param[len(max_param)-1][0]):
                        fscore.append(score[len(min_param)-1][0])
                    for i in range(1,len(min_param)-1):
                        if float(real_data) >= float(min_param[i][0]) and float(real_data) < float(max_param[i][0]):
                            fscore.append(score[i][0])
            kscore.append(fscore)
        return kscore
            
    def get_score(self, **kwargs):
        #从客户经理等级手工维护中获取客户经理信息
        real_data = g.db_session.query(ManGrade.loan_exp,ManGrade.user_name,ManGrade.kyear).filter(ManGrade.kyear == last_year).order_by(ManGrade.id).all()
        #current_app.logger.debug(real_data)
        fscore = []
        min_header_key = ['min_loan_exp']
        max_header_key = ['max_loan_exp']
        para1 = {'type_name':'客户经理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'分值'}
        score = self.get_grade_param(**para1)
        para2 = {'type_name':'客户经理等级指标权重参数','header_key':'man_weight'}
        weight = self.get_weight(**para2)
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[6][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            user_name = real_data[n][1]
            user = g.db_session.query(ManScore.user_name).filter(ManScore.user_name == user_name,ManScore.kyear == real_data[n][2]).first()
            if user:
                #更新信贷工作经验（年）分值,信贷工作经验（年）得分,信贷工作经验（年）权重
                g.db_session.query(ManScore).filter(ManScore.user_name == user_name,ManScore.kyear==real_data[n][2]).update({ManScore.loan_exp_score:score[n][0],ManScore.loan_exp_wscore:str(float(fscore[n])),ManScore.loan_exp_weight:weight[6][0],ManScore.loan_exp:real_data[n][0]})
            elif not user:
                g.db_session.add(ManScore(user_name=real_data[n][1], loan_exp_score=score[n][0], loan_exp_wscore=str(float(fscore[n])), loan_exp_weight=weight[6][0],loan_exp=real_data[n][0], kyear=real_data[n][2]))
            g.db_session.flush()
            #信贷工作经验为0时,直接变成助理客户经理
            if float(real_data[n][0]) == 0:
                para0 = {'score':score[n][0],'ave_dbal':0,'lens':1}
                kgrade = self.get_grade(**para0)
                g.db_session.query(ManScore).filter(ManScore.user_name == user_name,ManScore.kyear==real_data[n][2]).update({ManScore.adj_grade:kgrade[0]})

        #计算存贷款等得分
        dep_etc_score=self.calculate_dep_etc(real_data)
        #违规积分附扣分
        illegals = g.db_session.query(ManGrade.illegal_score,ManGrade.user_name,ManGrade.kyear).filter(ManGrade.kyear == last_year).order_by(ManGrade.user_name).all()
        s = 0
        for illegal in illegals:
            s += float(illegal[0])
        ave = s/len(illegals)
        ave1 = []
        for illegal in illegals:
            a1 = []
            if float(ave) >0:
                a = (float(illegal[0])-ave)/ave*100
            else:
                a = 0
            a1.append(a)
            a1.append(illegal[1])
            ave1.append(a1) 
        min_header_key = ['min_abv_ave']
        max_header_key = ['max_abv_ave']
        para5 = {'type_name':'客户经理违规积分附扣分项参数','real_data':ave1,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'扣分（分）'}
        bscore = self.get_grade_param(**para5)
        for n in range(0,len(illegals)):
            user_name = illegals[n][1]
            user = g.db_session.query(ManScore.user_name).filter(ManScore.user_name == user_name,ManScore.kyear==illegals[n][2]).first()
            if user:
                g.db_session.query(ManScore).filter(ManScore.user_name == user_name,ManScore.kyear == illegals[n][2]).update({ManScore.illegal_score:bscore[n][0]})
        
        #证书附加分
        zlscore = []
        para3 = {'type_name':'员工附加分项参数','real_data':'','detail_key':'extra_code'}
        para4 = {'type_name':'客户经理附加分最高值参数','detail_key':'man_score'}
        #for real_data in card:
        for n in range(0,len(real_data)):
            #获取用户的证书附加分
            card = g.db_session.query(User_ExtraScore.credential_code,User_ExtraScore.user_code,User_ExtraScore.syear).filter(User_ExtraScore.user_code==real_data[n][1]).all()
            user_code= real_data[n][1]
            cscore=0.0
            for i in range(0,len(card)):
                para3['real_data'] = card[i][0] 
                cscore_tmp = self.grade_param(**para3)
                if not cscore_tmp is None:
                    cscore=cscore+float(cscore_tmp)
      
            #获取用户的最大附加分
            mscore = self.getMaxScore(**para4)
            if float(cscore) > float(mscore):
                cscore = float(mscore)
            zlscore.append(str(cscore))
            user_name = real_data[n][1]
            user = g.db_session.query(ManScore.user_name).filter(ManScore.user_name == user_name,ManScore.kyear==real_data[n][2]).first()
            if user:
                g.db_session.query(ManScore).filter(ManScore.user_name == user_name,ManScore.kyear == real_data[n][2]).update({ManScore.extra_score:str(cscore)})
        
        #文化程度得分情况
        edu = g.db_session.query(User.edu,User.user_name).join(ManGrade,ManGrade.user_name == User.user_name).order_by(User.role_id).all()
        dscore = []
        para6 = {'type_name':'客户经理等级指标标准值和等级值参数','real_data':'','detail_key':'Score'}
        for i in edu:
            para6['real_data'] = i[0]
            kscore = self.grade_param(**para6)
            mscore = float(kscore)*float(weight[5][0])/100
            user_name = i[1]
            dscore.append(mscore)
            user = g.db_session.query(ManScore.user_name).filter(ManScore.user_name == user_name).first()
            if user:
                #g.db_session.query(ManScore).filter(ManScore.user_name == user_name,ManScore.kyear==real_data[n][2]).update({ManScore.edu_score:kscore,ManScore.edu_wscore:str(float(mscore)),ManScore.edu_weight:weight[5][0]})
                g.db_session.query(ManScore).filter(ManScore.user_name == user_name).update({ManScore.edu_score:kscore,ManScore.edu_wscore:str(float(mscore)),ManScore.edu_weight:weight[5][0]})

        #计算综合分
        allscore=g.db_session.query(ManScore.ave_dbal_wscore,ManScore.ave_dloan_wscore,ManScore.loan_num_wscore,ManScore.dave_loan_wscore,ManScore.fgrad_bad_wscore,ManScore.edu_wscore,ManScore.loan_exp_wscore,ManScore.extra_score,ManScore.illegal_score,ManScore.user_name,ManScore.kyear).filter(ManScore.kyear == last_year).all() 
        for n in range(0,len(allscore)):
            user_name =allscore[n][9]
            #取存款余额
            ave_dbal = g.db_session.query(ManScore.ave_dbal).filter(ManScore.user_name==user_name,ManScore.kyear==allscore[n][10]).first()
            ave_dbal=ave_dbal[0]
            total_score=0
            lens=len(allscore)
            for i in range(0,8):
                if not allscore[n][i] is None :
                    total_score=total_score + float(allscore[n][i])
            total_score = total_score - float(allscore[n][8]) #减去违规扣分
            para0 = {'score':total_score,'ave_dbal':ave_dbal,'lens':lens}
            kgrade = self.get_grade(**para0)
            g.db_session.query(ManScore).filter(ManScore.user_name == user_name,ManScore.kyear==allscore[n][10]).update({ManScore.total_score:str(float(total_score)),ManScore.sys_grade:kgrade[n]})
            g.db_session.flush()

            g.db_session.query(ManScore).filter(ManScore.user_name == user_name,ManScore.kyear==allscore[n][10]).update({ManScore.grade:kgrade[n]})
            g.db_session.flush()
            lscore = g.db_session.query(ManScore.adj_grade).filter(ManScore.user_name == user_name,ManScore.kyear==allscore[n][10]).first()
            if not (lscore[0] is None):
                g.db_session.query(ManScore).filter(ManScore.user_name == user_name,ManScore.kyear==allscore[n][10]).update({ManScore.grade:lscore[0]})
        return "计算成功"

    def get_grade(self, **kwargs):
        score = kwargs.get('score')
        ave_dbal = kwargs.get('ave_dbal')
        lens = kwargs.get('lens')
        type_name = '客户经理等级划分参数'
        grade = g.db_session.query(T_Para_Detail.detail_value).\
                join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
                join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
                filter(T_Para_Type.type_name == type_name).\
                filter(T_Para_Detail.detail_key == 'Grade').\
                order_by(T_Para_Detail.para_row_id).all()
        min_param = g.db_session.query(T_Para_Detail.detail_value).\
                join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
                join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
                filter(T_Para_Type.type_name == type_name).\
                filter(T_Para_Detail.detail_key == 'min_score').\
                order_by(T_Para_Detail.para_row_id).all()
        max_param = g.db_session.query(T_Para_Detail.detail_value).\
                join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
                join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
                filter(T_Para_Type.type_name == type_name).\
                filter(T_Para_Detail.detail_key == 'max_score').\
                order_by(T_Para_Detail.para_row_id).all()
        min_cun = g.db_session.query(T_Para_Detail.detail_value).\
                join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
                join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
                filter(T_Para_Type.type_name == type_name).\
                filter(T_Para_Detail.detail_key == 'min_ave_dbal').\
                order_by(T_Para_Detail.para_row_id).first()
        kgrade = []
        mgrade=''
        for n in range(0,int(lens)):
            if float(ave_dbal) > float(min_cun[0]) and float(score) >= float(min_param[0][0]) and float(score) < float(max_param[0][0]):
                mgrade = grade[0][0]
            for i in range(1,len(min_param)):
                if float(score) >= float(min_param[i][0]) and float(score) < float(max_param[i][0]):
                    mgrade = grade[i][0]
            if float(score) < float(max_param[len(max_param)-1][0]):
                mgrade = grade[len(max_param)-1][0]
            kgrade.append(mgrade)
        return kgrade
    
    def add_grade(self, **kwargs):
        grade = g.db_session.query(ManScore.grade,ManScore.user_name,ManScore.kyear).filter(ManScore.kyear == last_year).order_by(ManScore.id).all()
        for i in range(0,len(grade)):
            date = local_satrday
            user_name = grade[i][1]
            result = ur.check_update_his(last_endday,local_satrday,user_name,grade[i][0])
        return result

    def getMaxScore(self,**kwargs):
        detail_key = kwargs.get('detail_key')
        type_name = kwargs.get('type_name')
        score = g.db_session.query(T_Para_Detail.detail_value).\
                join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
                join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
                filter(T_Para_Type.type_name == type_name).\
                filter(T_Para_Detail.detail_key == detail_key).\
                order_by(T_Para_Detail.para_row_id).first()
        if score:
            score = score[0]
        return score
    
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

    def calculate_dep_etc(self,*kwargs):
        #计算日均存款余额(亿元)
        real_data=ur.dep_balance(kwargs)
        dep_etc_score=[]
        min_header_key=['min_ave_dbal']
        max_header_key=['max_ave_dbal']
        deppara={'type_name':'客户经理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'分值'}
        score = self.get_grade_param(**deppara)
        para2 = {'type_name':'客户经理等级指标权重参数','header_key':'man_weight'}
        weight = self.get_weight(**para2)
        fscore=[]
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[0][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            user_name = real_data[n][1]
            user = g.db_session.query(ManScore.user_name).filter(ManScore.user_name == user_name,ManScore.kyear==real_data[n][2]).first()
            if user:
                #更新日均存款余额(亿元)
                g.db_session.query(ManScore).filter(ManScore.user_name == user_name,ManScore.kyear==real_data[n][2]).update({ManScore.kyear:real_data[n][2],ManScore.ave_dbal_score:score[n][0],ManScore.ave_dbal_wscore:str(float(fscore[n])),ManScore.ave_dbal_weight:weight[0][0],ManScore.ave_dbal:str(round(float(real_data[n][0]),4))})
        dep_etc_score.append(fscore)

        #计算日均贷款余额（亿元）
        real_data=ur.manage_loan_avg_bal(kwargs)
        min_header_key=['min_ave_dloan']
        max_header_key=['max_ave_dloan']
        deppara={'type_name':'客户经理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'分值'}
        score = self.get_grade_param(**deppara)
        fscore=[]
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[1][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            user_name = real_data[n][1]
            user = g.db_session.query(ManScore.user_name).filter(ManScore.user_name == user_name,ManScore.kyear==real_data[n][2]).first()
            if user:
                g.db_session.query(ManScore).filter(ManScore.user_name == user_name,ManScore.kyear==real_data[n][2]).update({ManScore.kyear:real_data[n][2],ManScore.ave_dloan_score:score[n][0],ManScore.ave_dloan_wscore:str(float(fscore[n])),ManScore.ave_dloan_weight:weight[1][0],ManScore.ave_dloan:str(round(float(real_data[n][0]),4))})
        dep_etc_score.append(fscore)

        #计算管贷户数（户）
        real_data=ur.manage_loan_num(kwargs)
        min_header_key=['min_loan_num']
        max_header_key=['max_loan_num']
        deppara={'type_name':'客户经理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'分值'}
        score = self.get_grade_param(**deppara)
        fscore=[]
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[2][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            user_name = real_data[n][1]
            user = g.db_session.query(ManScore.user_name).filter(ManScore.user_name == user_name,ManScore.kyear==real_data[n][2]).first()
            if user:
                #更新ManScore
                g.db_session.query(ManScore).filter(ManScore.user_name == user_name,ManScore.kyear==real_data[n][2]).update({ManScore.kyear:real_data[n][2],ManScore.loan_num_score:score[n][0],ManScore.loan_num_wscore:str(float(fscore[n])),ManScore.loan_num_weight:weight[2][0],ManScore.loan_num:real_data[n][0]})
        dep_etc_score.append(fscore)

        #计算贷款户日均存贷挂钩率（%）
        real_data=ur.manage_avg_dep_loan_percent(kwargs)
        min_header_key=['MIN_DAILY_AVE_LOAN']
        max_header_key=['MAX_DAILY_AVE_LOAN']
        deppara={'type_name':'客户经理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'分值'}
        score = self.get_grade_param(**deppara)
        fscore=[]
        for i in range(0,len(score)):
            rscore = float(score[i][0])*float(weight[3][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            user_name = real_data[n][1]
            user = g.db_session.query(ManScore.user_name).filter(ManScore.user_name == user_name,ManScore.kyear==real_data[n][2]).first()
            if user:
                #更新ManScore
                g.db_session.query(ManScore).filter(ManScore.user_name == user_name,ManScore.kyear==real_data[n][2]).update({ManScore.kyear:real_data[n][2],ManScore.dave_loan_score:score[n][0],ManScore.dave_loan_wscore:str(float(fscore[n])),ManScore.dave_loan_weight:weight[3][0],ManScore.dave_loan:real_data[n][0]})
        dep_etc_score.append(fscore)

        #计算四级不良贷款控制（%）
        real_data=ur.manage_bad_bal_percent(kwargs)
        min_header_key=['MIN_FOR_GRAD_BAD']
        max_header_key=['MAX_FOR_GRAD_BAD']
        deppara={'type_name':'客户经理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'分值'}
        score1 = self.get_grade_param(**deppara)
        min_header_key=['MIN_FOR_GRAD_BADNUM']
        max_header_key=['MAX_FOR_GRAD_BADNUM']
        deppara={'type_name':'客户经理等级指标标准值和等级值参数','real_data':real_data,'min_header_key':min_header_key,'max_header_key':max_header_key,'header_name':'分值'}
        score2 = self.get_grade_param(**deppara)
        fscore=[]
        score_list=[]
        for i in range(0,len(score)):
            score = max(float(score1[i][0]),float(score2[i][0])) 
            score_list.append(score)
            rscore = float(score)*float(weight[4][0])/100
            fscore.append(rscore)
        for n in range(0,len(real_data)):
            user_name = real_data[n][1]
            user = g.db_session.query(ManScore.user_name).filter(ManScore.user_name == user_name,ManScore.kyear==real_data[n][2]).first()
            if user:
                #更新ManScore
                g.db_session.query(ManScore).filter(ManScore.user_name == user_name,ManScore.kyear==real_data[n][2]).update({ManScore.kyear:real_data[n][2],ManScore.fgrad_bad_score:str(score_list[n]),ManScore.fgrad_bad_wscore:str(float(fscore[n])),ManScore.fgrad_bad_weight:weight[4][0],ManScore.fgrad_bad:str(str(real_data[n][0][0])+'('+str(real_data[n][0][1])+')')})
        dep_etc_score.append(fscore)
        return dep_etc_score

    def upload(self, filepath, filename):
        """
            批量录入
        """
        print '正在导入'
        try:
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)

            nrows = sheet.nrows
            if nrows in [0, 1]:
                raise Exception(u"警告:文件为空")
            bill_type_sign = ""
            list = []
        except Exception, e:
            return str(e)
        all_msg = []
        souser = []
        for r in range(1, nrows):
            try:
                kyear = str(int(sheet.cell(r, 0).value))
                org_no = str((sheet.cell(r, 1).value))
                org_name = str(sheet.cell(r,2).value)
                user_name = str(int(sheet.cell(r, 3).value))
                name = str(sheet.cell(r, 4).value)
                loan_exp = str(int(sheet.cell(r, 5).value))
                illegal_score = str(float(sheet.cell(r,6).value))
                remarks = sheet.cell(r, 7).value
                kyear = kyear[0:4]  #+'/'+kyear[4:6] 
                if len(kyear) < 4:
                    e = u'第'+str(r+1)+u'行请填写正确所属年份'
                    raise Exception(e)
                if org_no.strip() == '' or len(org_no) < 6 or len(org_no) > 7:
                    e = u'第'+str(r+1)+u'行请填写正确的机构号'
                    raise Exception(e)
                if user_name.strip() == '':
                    raise Exception(u'请填写客户经理编号')
                if int(loan_exp) < 0:
                    e = u'第'+str(r+1)+u'行信贷工作经验不能为负数' 
                    raise Exception(e)
                if float(illegal_score) < 0:
                    e = u'第'+str(r+1)+u'行违规积分不能为负数' 
                    raise Exception(e)
                
                temp = {'kyear': kyear[0:4],
                        'org_no': org_no,
                        'org_name': '',
                        'user_name': user_name,
                        'name': '',
                        'loan_exp': loan_exp,
                        'illegal_score': illegal_score,
                        'remarks': remarks,
                }
                #tbranch = g.db_session.query(UserBranch).join(User,User.role_id==UserBranch.user_id).join(UserGroup,UserGroup.user_id==User.role_id).join(Branch,Branch.role_id==UserBranch.branch_id).filter(Branch.branch_code == org_no).filter(User.user_name == user_name).first()
                #if not tbranch:
                #    raise Exception(u'该机构中没有该客户经理')
                fx = g.db_session.query(User).join(UserGroup,UserGroup.user_id==User.role_id).join(Group,Group.id==UserGroup.group_id).filter(User.user_name==user_name).filter(Group.group_name=='客户经理').filter(Group.group_type_code=='2000').first()
                fy = g.db_session.query(ManGrade).filter(ManGrade.user_name==user_name,ManGrade.kyear==kyear).first()
                if not fx:
                    return u'第'+str(r+1)+u'行'+str(user_name)+u'没有此客户经理'
                if fy:
                    return u'第'+str(r+1)+u'行'+str(user_name)+u'该年已存在请勿重复导入'


                all_msg.append(temp)
                key = str(kyear)+str(org_no)+str(user_name)
                if key in souser:
                    return u'第'+str(r+1)+u'行'+str(user_name)+u'该年已存在请勿重复导入'
                else:
                    souser.append(key)
            except ValueError, e:
                g.db_session.rollback()
                return u'第'+str(r + 1) + u'行有错误'+str(e)+u"请检查年份和机构号是否正确,信贷工作经验违和规积分是否包含非法字符"
            except IndexError,e:
                g.db_session.rollback()
                return u'第'+str(r+1)+u'行有错误,请检查列数'
            except Exception, e:
                g.db_session.rollback()
                print Exception, ':', e
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        for i in range(0,len(all_msg)):
            g.db_session.add(ManGrade(**all_msg[i]))
        return u'导入成功'
