# -*- coding: utf-8 -*-
"""
    yinsho.api.img
    #####################

    yinsho  img  module

"""

from flask import Blueprint, request, json, abort, current_app, jsonify

from ..services import ImageService
from ..base import helpers
from . import route
import os, errno

igs = ImageService()
bp = Blueprint('img', __name__, url_prefix='/img')

def mkdir_p(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path, mode=0777)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def img_type(imgType):
    if imgType == 'octet-stream' :
        return "jpg"
    else:
        return imgType


@route(bp, '/', methods=['POST'])
def img_save():
    img_list = request.files.getlist('upload_file')
    application_id =  request.form.get('application_id')
    img_about = request.form.get('img_about')
    if application_id == None :
        return {'msg':'error'}
    return igs.save(application_id,img_about,img_list)

    '''
    file_dir = "".join(["../web/fabs/images/", str(application_id), '/'])
    for image in img_list:
        image_type =  image.content_type.split('/')[1]
        print image.filename
        fp = "".join([file_dir, image.filename, ".", img_type(image_type)])
        image.save(fp)
        igs.save(**{'filedir':fp,'name':image.filename,'application_id':application_id,'img_about':img_about})
    '''

@route(bp, '/<application_id>', methods=['GET'])
def img_query(application_id):
    return igs.img_query(application_id,request.args.get('about'))
    ##file_dir = "".join(["../web/fabs/views/image/", str(application_id), '/'])
    #if not os.path.exists(file_dir):
    #    return {'message':'没有该申请影像信息', 'filepath':''}

    #file_dict={}
    #files = os.listdir(file_dir)
    #for f in files:
    #    if(os.path.isfile(file_dir + '/' + f)):
    #        filename = f.split('.')[0]
    #        filetype = f.split('.')[1]
    #        file_dict[filename] = filetype
    #{'message':'查询成功', "filepath":"views/image/"+str(application_id), 'fileDict':file_dict}

@route(bp,'/img_print/',methods=['POST'])
def img_print():
    return igs.img_print(**request.json)


@route(bp,'/img_delete/',methods=['POST'])
def img_delete():
    return igs.img_delete(**request.json)
 
@route(bp,'/pdfile_upload/',methods=['POST'])
def pdfile_upload():
    flist = request.files
    kv={}
    #print flist
    pdflist = flist.getlist('pdfs')
    kv.update({'pdfs':pdflist})
    application_id = request.form.get('application_id')
    kv.update({'application_id':application_id})
    about = request.form.get('about')
    kv.update({'about':about})
    return igs.pdfile_upload(**kv)

@route(bp,'/pdfile_query/<application_id>',methods=['GET'])
def pdfile_query(application_id):
    return igs.pdfile_query(application_id,request.args.get('about'))
   
@route(bp,'/pdf_delete/',methods=['POST'])
def pdf_delete():
    return igs.pdf_delete(**request.json)

@route(bp,'/customer/upload/',methods=['POST'])
def cust_upload():
    files = request.files.getlist('file')
    party_id = request.form.get('party_id')
    about = request.form.get('about')
    return igs.cust_upload(party_id,about,files)

@route(bp,'/customer/<party_id>',methods=['GET'])
def cust_query(party_id):
    return igs.cust_query(party_id,request.args.get('about'))

@route(bp,'/bill/upload/',methods=['POST'])
def bill_upload():
    flist = request.files
    kv={}
    front = flist.get('front')
    if front:
        kv.update({'front':front})
    back = flist.get('back')
    if back :
        kv.update({'back':back})
    check =flist.get('check')
    if check:
        kv.update({'check':check})
    cert = flist.get('cert')
    if cert:
        kv.update({'cert':cert})
    bill_no = request.form.get('bill_no')
    kv.update({'bill_no':bill_no})
    return igs.bill_upload(**kv)

@route(bp,'/bill/query/<bill_no>',methods=['GET'])
def bill_query(bill_no):
    return igs.bill_query(bill_no)

@route(bp,'/bill/img_check/',methods=['POST'])
def bill_check():
    return igs.bill_check(**request.json)

@route(bp,'/discount_print/',methods=['POST'])
def discount_print():
    return igs.discount_print(**request.json)

@route(bp,'/billno_file/',methods=['POST'])
def billno_file():
    exc = request.files.get('billno_file')
    if exc == None:
        return []
    return igs.billno_file(exc)
