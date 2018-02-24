# -*- coding: utf-8 -*-
"""
    yinsho.services.TParaService
    #####################

    yinsho TParaService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func,text
from sqlalchemy.orm import joinedload_all,joinedload

from ..base import utils
from ..model import T_Para_Type,T_Para_Header,T_Para_Row,T_Para_Detail
  

class TParaService():
    """ TParaService """
    "参数类型的保存，所有项都是必填，插入前检查key是否已存在"
    def type_save(self,**kwargs):
        self.save_list = ['type_status','type_name','type_key','type_detail','type_module']
        newdata =  kwargs.get('newdata')
        data ={}
        for field in self.save_list:
            value = newdata.get(field)
            if value:
                data[field] = value
            else:
                return u"%s 需要填写" % field
        type_key = newdata.get('type_key')
        if g.db_session.query(T_Para_Type).filter(T_Para_Type.type_key==type_key).all():
            return u"key已存在，请修改"
        g.db_session.add(T_Para_Type(**data))
        return u"添加成功"    

    "参数类型的更新，只允许更新少量信息"
    def type_update(self, **kwargs):
        self.save_list = ['type_status','type_name','type_detail','type_module']
        newdata =  kwargs.get('updata')
        data ={}
        tid = newdata.get('id')
        if not tid:return u"无更新主键"
        for k,v in newdata.items():
            if k in self.save_list : data[k] = v
        g.db_session.query(T_Para_Type).filter(T_Para_Type.id==tid).update(data)
        return u"修改成功"

    "参数头的保存，全部必填,只有备注选填，检查外键，检查key"
    def header_save(self,**kwargs):
        self.save_list = ['para_type_id','header_name','header_key','header_detail','header_type','header_status','header_order']
        newdata =  kwargs.get('newdata')
        data ={}
        for field in self.save_list:
            value = newdata.get(field)
            if value:
                data[field] = value
            elif field !='header_detail':
                return u"%s 需要填写" % field
        header_key = newdata.get('header_key')
        para_type_id = newdata.get('para_type_id')
        #print para_type_id
        if not g.db_session.query(T_Para_Type).filter(T_Para_Type.id==para_type_id).all():
            return u'参数类型不存在,无法添加'
        if g.db_session.query(T_Para_Header).filter(and_(T_Para_Header.header_key==header_key,T_Para_Header.para_type_id == para_type_id)).all():
            return u"key已存在，请修改"
        g.db_session.add(T_Para_Header(**data))
        return u"添加成功"    

    "参数头的更新，只允许更新少量信息"
    def header_update(self, **kwargs):
        self.save_list = ['header_status','header_name','header_detail','header_order','header_type']
        newdata =  kwargs.get('updata')
        data ={}
        tid = newdata.get('id')
        if not tid:return u"无更新主键"
        for k,v in newdata.items():
            if k in self.save_list : data[k] = v
        g.db_session.query(T_Para_Header).filter(T_Para_Header.id==tid).update(data)
        return u"修改成功"
     
    "参数的保存，全部需要填写，检查外键，检查key"
    def para_save(self,**kwargs):
        flag,msg = self.row_save(kwargs)
        if not flag:
            return msg
        return self.detail_save(kwargs,msg)

    "参数行状态的更新，只允许更新少量信息"
    def row_update(self, **kwargs):
        self.save_list = ['row_status','row_start_date','row_end_date']
        newdata =  kwargs.get('updata')
        data ={}
        tid = newdata.get('id')
        if not tid:return u"无更新主键"
        for k,v in newdata.items():
            if k in self.save_list : data[k] = v
        g.db_session.query(T_Para_Row).filter(T_Para_Row.id==tid).update(data)
        return u"修改成功"

    "参数值的更新，只允许更新值"
    def detail_update(self, **kwargs):
        newdata =  kwargs.get('updata')
        rid = kwargs.get('rid')
        for k,v in newdata.items():
            data ={}
            hid = k
            if not rid or not hid:return u"无更新主键"
            data['detail_value']=v
            isexit = g.db_session.query(T_Para_Detail).filter(and_(T_Para_Detail.para_header_id==hid,T_Para_Detail.para_row_id==rid)).all()
            if len(isexit)>0:
                g.db_session.query(T_Para_Detail).filter(and_(T_Para_Detail.para_header_id==hid,T_Para_Detail.para_row_id==rid)).update(data)
            else:
                t_para_header  = g.db_session.query(T_Para_Header).filter(T_Para_Header.id==hid).all()
                if t_para_header:
                    data['detail_key'] = t_para_header[0].header_key   
                    data['para_header_id'] = hid   
                    data['para_row_id'] = rid
                    g.db_session.add(T_Para_Detail(**data))
                else:
                    return u"新属性保存出错"
        return u"修改成功"
        
    def detail_save(self,kwargs,msg):
        self.detail_list = ['para_header_id','detail_value']
        detaillist =  kwargs.get('detaildata')
        detaildata={}
        for k,v in detaillist.items():
            detaildata['para_header_id'] = k
            detaildata['detail_value'] = v
            para_header_id = detaildata.get('para_header_id')
            t_para_header  = g.db_session.query(T_Para_Header).filter(and_(T_Para_Header.id==para_header_id,T_Para_Header.header_status == u'启用')).all() 
            if not para_header_id or not t_para_header:
                return u"没有参数头，参数头未启用"
            detaildata['detail_key'] = t_para_header[0].header_key   
            data = {}
            for field in self.detail_list:
                value = detaildata.get(field)
                if value:
                    data[field] = value
                else:
                    return u"%s 需要填写" % field
            data['detail_key'] = detaildata['detail_key']
            data['para_row_id'] = msg 
            g.db_session.add(T_Para_Detail(**data))
        return u"添加成功"    

    def row_save(self,kwargs):
        self.row_list = ['para_type_id','row_status','row_start_date','row_end_date']
        rowdata =  kwargs.get('rowdata')
        data ={}
        for field in self.row_list:
            value = rowdata.get(field)
            if value:
                data[field] = value
            else:
                return False,u"%s 需要填写" % field
        para_type_id = rowdata.get('para_type_id')
        if not g.db_session.query(T_Para_Type).filter(T_Para_Type.id==para_type_id).all():
            return False,u'参数类型不存在,无法添加'
        max_row_num = g.db_session.query(func.max(T_Para_Row.row_num)).first()
        if max_row_num[0]:
            max_row_num = max_row_num[0]+1
        else:
            max_row_num = 1
        data['row_num'] = max_row_num
        t_row = T_Para_Row(**data)
        g.db_session.add(t_row)
        g.db_session.flush()
        return True,t_row.id

