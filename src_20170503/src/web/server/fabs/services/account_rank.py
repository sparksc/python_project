#-*-coding:utf-8-*-
import datetime,xlrd
from flask import json, g, current_app
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all,aliased
from ..base import utils
from ..model import CustHook, Account_Rank, Branch,User,UserBranch,User,User_ExtraScore,T_Para_Detail,UserLevel,T_Para_Header,T_Para_Type,Group,UserGroup
import datetime

class Account_rankService():
    def add_save(self, **kwargs):
        try:
            syear = kwargs.get('syear')
            org_code = kwargs.get('org_code')
            user_code = kwargs.get('user_code')
            mis_rank = kwargs.get('mis_rank')
            basic_rank = kwargs.get('basic_rank')
            ryear = kwargs.get('ryear')
            score_rank = kwargs.get('score_rank')
            repleace_rank = kwargs.get('repleace_rank')
            skill = kwargs.get('skill')
            experience = kwargs.get('experience')
            remarks = kwargs.get('remarks')

            fx = g.db_session.query(User).join(UserGroup,UserGroup.user_id==User.role_id).join(Group,Group.id==UserGroup.group_id).filter(User.user_name==user_code).filter(Group.group_name=='助理会计').filter(Group.group_type_code=='1000').first()
            if not fx:
                return u'不存在该助理会计！'

            g.db_session.add(Account_Rank(syear=syear,org_code=org_code,user_code=user_code,mis_rank=mis_rank,basic_rank=basic_rank,ryear=ryear,score_rank=score_rank,repleace_rank=repleace_rank,skill=skill,experience=experience,remarks=remarks))
            return u'保存成功';
        except Exception, e:
            print type(e), Exception, '1111111111111111111111111111111111111111111111'
            return u'保存失败'

    def edit_save(self, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            syear = kwargs.get('syear')
            org_code = kwargs.get('org_code')
            user_code = kwargs.get('user_code')
            mis_rank = kwargs.get('mis_rank')
            basic_rank = kwargs.get('basic_rank')
            ryear = kwargs.get('ryear')
            score_rank = kwargs.get('score_rank')
            repleace_rank = kwargs.get('repleace_rank')
            skill = kwargs.get('skill')
            experience = kwargs.get('experience')
            remarks = kwargs.get('remarks')
            g.db_session.query(Account_Rank).filter(Account_Rank.id == item_id).update(
                {Account_Rank.syear:syear,Account_Rank.org_code:org_code,Account_Rank.user_code:user_code,Account_Rank.mis_rank:mis_rank,Account_Rank.basic_rank:basic_rank,Account_Rank.ryear:ryear,Account_Rank.score_rank:score_rank,Account_Rank.repleace_rank:repleace_rank,Account_Rank.skill:skill,Account_Rank.experience:experience,Account_Rank.remarks:remarks})
            return u'编辑成功'
        except Exception, e:
            print type(e),Exception,'1111111111111111111111111111111111111111111111111'
            return u'编辑失败'
    def delete(self, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            g.db_session.query(Account_Rank).filter(Account_Rank.id == item_id).delete()
            return u'删除成功'
        except Exception, e:
            print type(e), Exception, '11111111111111111111111111111111111111111111111'
            return u'删除失败'    

    def upload(self, filepath, filename):

        print u'正在导入'
        try:
            today = datetime.date.today()
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            
            nrows = sheet.nrows
            if nrows in [0, 2]:
                raise Exception(u"导入文件是空文件")
            bill_type_sign = ""
            list = []
        except Exception, e:
            return str(e)
        all_msg = []
        souser = []
        for r in range(2, nrows):
            try:
                syear = str(int(sheet.cell(r, 0).value))
                org_code =str(int(sheet.cell(r, 1).value))
                org_name = str(sheet.cell(r, 2).value)
                user_code =str(int(sheet.cell(r, 3).value))
                user_name = str(sheet.cell(r, 4).value)
                mis_rank = str(int(sheet.cell(r, 5).value))
                basic_rank = str(sheet.cell(r, 6).value)
                ryear = str(int(sheet.cell(r, 7).value))
                score_rank = str(int(sheet.cell(r, 8).value))
                repleace_rank = str(int(sheet.cell(r, 9).value))
                skill = str(sheet.cell(r, 10).value)
                experience = str(int(sheet.cell(r, 11).value))
                remarks = str(sheet.cell(r, 12).value)

                if len(syear) != 4:
                    e = u'年份长度有误'
                    raise Exception(e)
                if len(org_code) != 6 :
                    e = u'机构号长度有误'
                    raise Exception(e)
                if len(user_code) != 7:
                    e = u'员工号长度有误'
                    raise Exception(e)
                if org_name.strip() == '':
                    raise Exception(u'请填写机构名称')
                if user_name.strip() == '':
                    raise Exception(u'请填写员工名称')
                if mis_rank.strip() == '':
                    raise Exception(u'请填写业务差错率排名')
                if basic_rank.strip() == '':
                    raise Exception(u'请填写会计基础等级')
                if ryear.strip() == '':
                    raise Exception(u'请填写会计行龄')
                if score_rank.strip() == '':
                    raise Exception(u'请填写内勤人均违规积分分值排名')
                if repleace_rank.strip() == '':
                    raise Exception(u'请填写电子银行替代率完成率排名')
                if skill.strip() == '':
                    raise Exception(u'请填写助理会计市办业务知识技能达标（级）')
                if experience.strip() == '':
                    raise Exception(u'请填写助理会计工作经验（年）')

                if float(mis_rank) < 0:
                    e = u'业务差错率排名不能为负数'
                    raise Exception(e)
                if float(ryear) < 0:
                    e = u'委派会计主管行龄不能为负数'
                    raise Exception(e)
                if float(score_rank) < 0:
                    e = u'内勤人均违规积分分值排名不能为负数'
                    raise Exception(e)
                if float(repleace_rank) < 0:
                    e = u'电子银行替代率完成率排名不能为负数'
                    raise Exception(e)
                if float(experience) < 0:
                    e = u'委派会计主管工作经验不能为负数'
                    raise Exception(e)

                tbranch = g.db_session.query(UserBranch).join(User,User.role_id==UserBranch.user_id).join(Branch,Branch.role_id==UserBranch.branch_id).filter(Branch.branch_code == org_code).filter(User.user_name == user_code).first()
                if not tbranch:
                    raise Exception(u'该机构中没有该用户')

                fx = g.db_session.query(User).join(UserGroup,UserGroup.user_id==User.role_id).join(Group,Group.id==UserGroup.group_id).filter(User.user_name==user_code).filter(Group.group_name=='助理会计').filter(Group.group_type_code=='1000').first()
                if not fx:
                    return u'第'+str(r+1)+u'行不存在该助理会计！'
                
                temp = {'syear': syear,
                        'org_code': org_code,
                        'user_code': user_code,
                        'mis_rank':mis_rank,
                        'basic_rank':basic_rank,
                        'ryear':ryear,
                        'score_rank':score_rank,
                        'repleace_rank':repleace_rank,
                        'skill':skill,
                        'experience':experience,
                        'remarks':remarks
                        }
                fdata = g.db_session.query(Account_Rank).filter(Account_Rank.syear == syear).filter(Account_Rank.org_code == org_code).filter(Account_Rank.user_code==user_code).first()

                if fdata:
                    return u'第'+str(r+1)+u'行，'+syear+'年度,机构：'+org_code+',柜员:'+user_code+'数据已存在'

                all_msg.append(temp)
                key = str(syear) + str(org_code) + str(user_code)
                if key in souser:
                    return u'第'+str(r+1)+u'行，该年此员工已存在，请勿重复导入'
                else:
                    souser.append(key)

               # g.db_session.add(Account_Rank(**temp))
            except ValueError, e:
                g.db_session.rollback()
                return u'第'+str(r + 1) + u'行有错误,'+u"请检查该行是否有值为空或包含非法字符"
            except IndexError,e:
                g.db_session.rollback()
                return u'第'+str(r+1)+u'行有错误,请检查列数'
            except Exception, e:
                g.db_session.rollback()
                print Exception, ':', e
                return u'第' + str(r + 1) + u'行有错误,'+str(e)

        for i in range(0,len(all_msg)):
            g.db_session.add(Account_Rank(**all_msg[i]))

        return u'导入成功'

