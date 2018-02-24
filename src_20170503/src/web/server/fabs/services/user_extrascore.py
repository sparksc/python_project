#-*-coding:utf-8-*-
import datetime,xlrd
from flask import json, g,current_app
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all,aliased
from ..base import utils
from ..model import CustHook, User_ExtraScore, Branch,User,UserBranch,T_Para_Detail,UserLevel,T_Para_Header,T_Para_Type
from man_gradejdg import Man_gradejdgService
import datetime

msg = Man_gradejdgService()
class User_extrascoreService():
    def add_save(self, **kwargs):
        try:
            syear = kwargs.get('syear')
            org_code = kwargs.get('org_code')
            user_code = kwargs.get('user_code')
            credential_code = kwargs.get('credential_code')
            #is_gleader = kwargs.get('is_gleader')
            remarks = kwargs.get('remarks')

            g.db_session.add(User_ExtraScore(syear=syear,
                              org_code=org_code,user_code=user_code,
                              credential_code=credential_code,remarks=remarks))
            return u'保存成功';
        except Exception, e:
            return u'保存失败'

    def edit_save(self, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            syear = kwargs.get('syear')
            org_code = kwargs.get('org_code')
            user_code = kwargs.get('user_code')
            credential_code = kwargs.get('credential_code')
            #is_gleader = kwargs.get('is_gleader')
            remarks = kwargs.get('remarks')
            #判断该员工的证书录入是否重复
            fdata = g.db_session.query(User_ExtraScore).filter(User_ExtraScore.credential_code==credential_code).filter(User_ExtraScore.org_code == org_code).filter(User_ExtraScore.user_code==user_code).first()
            if fdata:
                return u'该员工的此证书已录入，请勿重复录入'
            g.db_session.query(User_ExtraScore).filter(User_ExtraScore.id == item_id).update(
                {User_ExtraScore.syear:syear,User_ExtraScore.org_code:org_code,User_ExtraScore.user_code:user_code,User_ExtraScore.credential_code:credential_code,User_ExtraScore.remarks:remarks})
            return u'编辑成功'
        except Exception, e:
            return u'编辑失败'
    def delete(self, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            g.db_session.query(User_ExtraScore).filter(User_ExtraScore.id == item_id).delete()
            return u'删除成功'
        except Exception, e:
            return u'删除失败'    

    def upload(self, filepath, filename):

        print u'正在导入'
        try:
            today = datetime.date.today()
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            
            nrows = sheet.nrows
            if nrows in [0, 1]:
                raise Exception(u"导入文件是空文件")
            bill_type_sign = ""
            list = []
        except Exception, e:
            return str(e)
        #取员工附加分项参数,得证书编号
        detail_value = g.db_session.query(T_Para_Detail.detail_value).join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).filter(T_Para_Type.type_name == '员工附加分项参数').filter(T_Para_Detail.detail_key == 'credential_code').all()
        code_list = []
        for i in range(0,len(detail_value)):
            code_list.append(detail_value[i][0]) 
        all_msg = []
        souser = []
        for r in range(1, nrows):
            try:
                syear = str(int(sheet.cell(r, 0).value))
                org_code =str((sheet.cell(r, 1).value)).replace('.0','')
                org_name = str(sheet.cell(r, 2).value)
                user_code =str(int(sheet.cell(r, 3).value))
                user_name = str(sheet.cell(r, 4).value)
                credential_code = str(int(sheet.cell(r, 5).value))
                credential_name = str(sheet.cell(r, 6).value)
                remarks = str(sheet.cell(r, 7).value)

                syear = syear[0:4]  #+'/'+kyear[4:6] 
                if len(syear) < 4:
                    e = u'第'+str(r+1)+u'行请填写正确所属年份'
                    raise Exception(e)
                if len(org_code) < 6 or len(org_code) > 7:
                    e = u'第'+str(r+1)+u'行请填写正确的机构号'
                    raise Exception(e)
                if len(user_code) < 7 or len(user_code) > 8:
                    e = u'第'+str(r+1)+u'行请填写正确的员工号'
                    raise Exception(e)
                if str(credential_code) not in code_list:
                    e = u'第'+str(r+1)+u'行请填写证书编号'
                    raise Exception(e)

                #判断员工与机构是否关联
                tbranch = g.db_session.query(UserBranch).join(User,User.role_id==UserBranch.user_id).join(Branch,Branch.role_id==UserBranch.branch_id).filter(Branch.branch_code == org_code).filter(User.user_name == user_code).first()
                if not tbranch:
                    e = u'第'+str(r+1)+u'行该机构中没有该用户'
                    raise Exception(e)
                
                syear = syear[0:4]                
                temp = {'syear': syear,
                        'org_code': org_code,
                        'user_code': user_code,
                        'credential_code':credential_code,
                        'remarks':remarks
                        }
                #判断该员工的证书录入是否重复
                fdata = g.db_session.query(User_ExtraScore).filter(User_ExtraScore.credential_code==credential_code).filter(User_ExtraScore.org_code == org_code).filter(User_ExtraScore.user_code==user_code).first()
                if fdata:
                    return u'第'+str(r+1)+u'行，该员工的此证书已录入，请勿重复录入'

                all_msg.append(temp)
                key = str(credential_code)+str(user_code)
                if key in souser:
                    return u'第'+str(r+1)+u'行'+str(user_code)+u'该证书已存在请勿重复导入'
                else:
                    souser.append(key)
            except ValueError, e:
                g.db_session.rollback()
                return u'第'+str(r + 1) + u'行有错误'+str(e)+u"请检查年份和机构号是否正确,证书编号是否包含非法字符"
            except IndexError,e:
                g.db_session.rollback()
                return u'第'+str(r+1)+u'行有错误,请检查列数'
            except Exception, e:
                g.db_session.rollback()
                return u'第' + str(r + 1) + u'行有错误'+str(e)

        for i in range(0,len(all_msg)):
            g.db_session.add(User_ExtraScore(**all_msg[i]))
        return u'导入成功'

    def credentials(self,**kwargs):
        d1 = aliased(T_Para_Detail, name='d1')
        d2 = aliased(T_Para_Detail, name='d2')

        credentials = g.db_session.query(d1.detail_value,d2.detail_value).filter(d1.para_row_id==d2.para_row_id).filter(d1.detail_key=='credential_code').filter(d2.detail_key=='credential_name').order_by(d1.detail_value).all()
                
        return [{"credential_code":n[0],"credential_name":n[1]} for n in credentials]
        
    def calculate(self,**kwargs):
        #附加分
        row1 = g.db_session.query(User.user_name,User.name,User.is_headman,User_ExtraScore.credential_code).outerjoin(User_ExtraScore, User_ExtraScore.user_code == User.user_name).order_by(User.user_name).all()
        #文化水平，市办知识技能，文明服务，出错率，满意度，工龄，柜龄，扣分
        row2 = g.db_session.query(User.user_name,User.name,UserLevel.task_level,UserLevel.civilized_service,UserLevel.task_errorrate,UserLevel.cust_satisfaction,UserLevel.work_year,User.edu,UserLevel.bankterm_year,UserLevel.violation_score).outerjoin(UserLevel, UserLevel.user_code == User.user_name).order_by(User.user_name).all()
        #扣分平均值
        lens = len(row2)
        total = 0
        rs = g.db_session.query(UserLevel.violation_score).outerjoin(User,User.user_name == UserLevel.user_code).order_by(User.user_name).all()       
        for i in range(0,len(rs)):
            total += float(rs[i][0])
        avgs = round(total/lens,2)
        alllist = []#存放各个员工的最终得分
        param1 = {'type_name':'员工附加分项参数','real_data':'','detail_key':'extra_code'}
        param2 = {'type_name':'柜员附加分最高值参数','detail_key':'Max_ExtraScore'}
        maxscore = self.getMaxScore(**param2)
        for item in row1:
            #用户附加分
            if not item[3]:
                cscore = 0
            else:
                param1['real_data'] = item[3]
                cscore = msg.grade_param(**param1)            
            #用户是否是柜组长
            is_gleader = item[2]
            if is_gleader == '是':
               fscore = float(cscore) + 1

            if fscore > float(maxscore):
                fscore = float(maxscore)       
           
            perlist = []
            perlist.append(fscore)
            alllist.append(perlist)
            break

        weights = msg.get_weight(**{'type_name':'柜员等级指标权重参数','header_key':'GY_Weight'})
        print u'权重:',weights
        i = 0
        for item in row2:
            #市办业务知识技能达标
            kw = {'real_data':item[2],'type_name':u'柜员等级指标标准值和等级值参数','detail_key':'DJScore','detail_value':u'市办业务知识技能达标','weight':weights[1][0]}
            self.get_fscores(alllist[i],**kw)
            #文明服务
            kw = {'real_data':item[3],'type_name':u'柜员等级指标标准值和等级值参数','min_header_key':'Min_FWScore','max_header_key':'Max_FWScore','header_name':'分值(分)','weight':weights[2][0]}
            self.get_fscores(alllist[i],**kw)
            #出错率
            kw = {'real_data':item[4],'type_name':u'柜员等级指标标准值和等级值参数','min_header_key':'Min_CCScore','max_header_key':'Max_CCScore','header_name':'分值(分)','weight':weights[3][0]}
            self.get_fscores(alllist[i],**kw)
            #满意度
            kw = {'real_data':item[5],'type_name':u'柜员等级指标标准值和等级值参数','min_header_key':'Min_MYScore','max_header_key':'Max_MYScore','header_name':'分值(分)','weight':weights[4][0]}
            self.get_fscores(alllist[i],**kw)
            #行龄
            kw = {'real_data':item[6],'type_name':u'柜员等级指标标准值和等级值参数','min_header_key':'Min_HL','max_header_key':'Max_HL','header_name':'分值(分)','weight':weights[5][0]}
            self.get_fscores(alllist[i],**kw)
            #文化程度
            kw = {'real_data':item[7],'type_name':u'柜员等级指标标准值和等级值参数','detail_key':'DJScore','detail_value':u'文化程度','weight':weights[6][0]}
            self.get_fscores(alllist[i],**kw)
            #临柜
            kw = {'real_data':item[8],'type_name':u'柜员等级指标标准值和等级值参数','min_header_key':'Min_LG','max_header_key':'Max_LG','header_name':'分值(分)','weight':weights[7][0]}
            self.get_fscores(alllist[i],**kw)
            #扣分
            #real_data = (float(item[9])/avgs -1)*100            
            kw = {'real_data':item[9],'type_name':u'员工违规积分附加分项参数','min_header_key':'Min_WScore','max_header_key':'Max_WScore','header_name':'扣分(分)'}
            self.get_fscores(alllist[i],**kw)
            #总分
            total = self.get_totalscore(alllist[i])
            alllist[i].append(total)            
            #等级
            kw = {'real_data':alllist[i][9],'type_name':u'柜员等级划分参数','min_header_key':'Min_JScore','max_header_key':'Max_JScore','header_name':'等级'}
            self.get_fscores(alllist[i],**kw)
            print u'最后得分',alllist             
            i += 1
            break

    def get_fscores(self,arr,**kwargs):
        real_data = kwargs.get('real_data')
        detail_value = kwargs.get('detail_value')
        weight = kwargs.get('weight')
        header_name = kwargs.get('header_name')
        if real_data:
            if not detail_value:
                cscore = self.get_grade_param(**kwargs)
            else:
                cscore = msg.grade_param(**kwargs)
            if cscore == None:
                cscore = 0

            if header_name != '等级':
                cscore = float(cscore)
                if weight == None:
                    weight = 100
                weight = float(weight)
                fscore = cscore*weight/100
            else:
                fscore = cscore
        else:
            fscore = 0
        arr.append(fscore)

    def getMaxScore(self,**kwargs):
        detail_key = kwargs.get("detail_key")
        score = g.db_session.query(T_Para_Detail.detail_value).filter(T_Para_Detail.detail_key ==detail_key).first()
        score = score[0]
        return score
    
    def get_grade_param(self, **kwargs):
        type_name = kwargs.get('type_name')
        min_header_key = kwargs.get('min_header_key')
        max_header_key = kwargs.get('max_header_key')
        real_data = kwargs.get('real_data')              # 实绩
        header_name = kwargs.get('header_name')          # 分值
        print min_header_key,max_header_key,real_data
        fscore = 0
                
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

        if min_header_key in ['Min_FWScore','Min_CCScore','Min_LG','Min_HL','Min_MYScore','Min_YWScore','Min_WScore','Min_JScore']:
            for i in range(0,len(min_param)):
                if float(real_data) >= float(min_param[i][0]) and float(real_data) < float(max_param[i][0]):
                    fscore = score[i][0]
        return fscore
    def get_totalscore(self,arr):
        total = 0
        for i in arr:
            i = float(i)
            total += i
        return round(total,2)
