# -*- coding: utf-8 -*-
"""
    yinsho.services.ImageServic
    #####################

    yinsho ImageServic module
"""
import hashlib, copy
from flask import json, g
from ..model.img import *
from ..model.credit import Bill_message
from .service import BaseService
from datetime import datetime
from ..base import utils
import os
import uuid
import xlrd

class ImageService(BaseService):
    __model__ = Image

    def mkdir_p(self,path):
        try:
            if not os.path.exists(path):
                os.makedirs(path, mode=0777)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def save(self,application_id,img_about,img_list):
        u'''  保存图片信息  '''
        file_dir = "".join(["../web/fabs/images/", str(application_id), '/'])
        print application_id,'save',img_about
        self.mkdir_p(file_dir)
        for image in img_list:
            unique_name = str(uuid.uuid1())+'.jpg'
            save_path = "".join([file_dir,unique_name])
            image.save(save_path)
            img = Image(application_id = application_id,name=image.filename,url='.'+save_path[11:],img_about=img_about)
            g.db_session.add(img)
        return {'msg':'success'}
    
    def img_query(self,application_id,about):
        u'''  查询图片   '''
        print application_id,'query',about
        q = g.db_session.query(Image).filter(Image.application_id == application_id)
        if about in ['','null','undefined',None]:
            about = None
            return {'research':q.filter(Image.img_about=='research').all(),
                   }
        else:
            about = about.strip()
            q = q.filter(Image.img_about == about)
        return q.all()

    def img_print(self,**kwargs):
        u'''  图片打印  '''
        img_list = kwargs.get('img_list')
        new_list = []
        for img in img_list:
            new_list.append('../web/fabs/'+img[1:])
        return utils.jpg2pdf(new_list);

    def img_delete(self,**kwargs):
        u'''  图片删除  '''
        url_list = kwargs.get('url_list')
        for url in url_list:
            img = g.db_session.query(Image).filter(url == url).first()
            g.db_session.delete(img)
        return {'msg':'success'}

    def pdfile_upload(self,**kwargs):
        u'''  pdf文件上传  '''
        application_id = kwargs.get('application_id')
        about = kwargs.get('about')
        print application_id,'pdf_upload',about
        file_dir = "".join(["../web/fabs/images/pdfs/",str(application_id),'/'])
        self.mkdir_p(file_dir)
        count = 0
        pdflist = kwargs.get('pdfs')
        for pdf in pdflist:
            unique_name = str(uuid.uuid1())+'.pdf'
            count = count + 1
            fpath = "".join([file_dir,unique_name]) 
            pdf.save(fpath)
            pdfile = PDFile(application_id = application_id,url='.'+fpath[11:],name=pdf.filename,about=about)
            g.db_session.add(pdfile)

        return {"msg":u"成功上传文件%d个"%(count,)} 

    def pdfile_query(self,application_id,about):
        u'''  pdf文件查询  '''
        return g.db_session.query(PDFile).filter(PDFile.application_id == application_id).filter(PDFile.about == about).all()

    def pdf_delete(self,**kwargs):
        u'''  pdf文件删除  '''
        url_list = kwargs.get('url_list')
        for url in url_list:
            pdf = g.db_session.query(PDFile).filter(url == url).first()
            g.db_session.delete(pdf)
        return {'msg':'success'}

    def cust_upload(self,party_id,about,files):
        file_dir = "".join(["../web/fabs/images/customer/",str(party_id),'/'])
        self.mkdir_p(file_dir)
        for f in files:
            fsave = "".join([file_dir,f.filename])
            f.save(fsave)
            cust_img = CustImage(party_id=party_id,about=about,url=fsave,name=f.filename)
            g.db_session.add(cust_img)
        return {'msg':u'成功保存文件%d个'%(len(files),)}

    def cust_query(self,party_id,about):
        print party_id,'cust_save',about
        return g.db_session.query(CustImage).filter(CustImage.party_id == party_id).filter(CustImage.about == about.strip()).all()

        
    def bill_upload(self,**kwargs):
        u'''    票据上传   '''
        bill_no = kwargs.get('bill_no')
        kwargs.pop('bill_no')
        file_dir = "".join(["../web/fabs/images/bill/",str(bill_no),'/'])
        self.mkdir_p(file_dir)
        #---  默认 jpg
        count = 0
        for k in kwargs.keys():
            v = kwargs.get(k)
            count = count + 1
            #'图片类型' 扩展后缀名
            ext = u'.'+v.filename.split('.')[-1:][0]
            fpath = "".join([file_dir,k+ext]) 
            v.save(fpath)
            have = g.db_session.query(BillImage).filter(BillImage.bill_no == bill_no).filter(BillImage.name == k).first()
            if have == None:
                bill_image = BillImage(bill_no = bill_no,url=fpath,name=k)
                g.db_session.add(bill_image)

        return {"msg":u"成功上传文件%d个"%(count,)} 
    def bill_query(self,bill_no):
        u'''    票据查询   '''
        arg = g.db_session.query(Bill_message.img_check,Bill_message.img_remark).filter(Bill_message.bill_no == bill_no).first()
        
        print arg
        return {'img_check':arg[0],'img_remark':arg[1],'bill_img':g.db_session.query(BillImage).filter(BillImage.bill_no == bill_no).all()}

    def bill_check(self,**kwargs):
        u'''  票据图片检验  '''
        bill_no = kwargs.get('bill_no')
        img_check = kwargs.get('img_check')
        img_remark = kwargs.get('img_remark')
        g.db_session.query(Bill_message).filter(Bill_message.bill_no == bill_no).update({'img_check':img_check,'img_remark':img_remark})
        return {'msg':u"提交成功"}


    def discount_print(self,**kwargs):
        u''' 贴现打印   '''
        disList = kwargs.get('disList')
        
        jpgList = []
        for one in disList:
            if one.get('front_url'):
                jpgList.append('../web/fabs/'+one.get('front_url')[1:])
            if one.get('back_url'):
                jpgList.append('../web/fabs/'+one.get('back_url')[1:])
            if one.get('check_url'):
                jpgList.append('../web/fabs/'+one.get('check_url')[1:])
            if one.get('cert_url'):
                jpgList.append('../web/fabs/'+one.get('cert_url')[1:])

        return utils.jpg2pdf(jpgList)

    def billno_file(self,exc):
        u''' 批量票号查询   '''
        fpath = "".join(['./fabs/static/',exc.filename])       
        exc.save(fpath)
        data = xlrd.open_workbook(fpath)
        sheet = data.sheet_by_index(0)
        nrows = sheet.nrows
        msg = ""
        count_no = ":"
        billList=[]
        for r in range(nrows):
            bill_no = sheet.cell(r,0).value
            print bill_no
            one = self.bill_query(bill_no)
            if len(one.get('bill_img')) == 0:
                count_no = count_no + bill_no + ','
            else:
                billList.append(one)
         
        if len(count_no) >1:
            count_no = count_no + u'没有图片'
            return {'msg':count_no,'billList':billList}
        else:
            return {'msg':'0','billList':billList}



