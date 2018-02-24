#!/usr/bin/python
#-*- coding:utf-8 -*-
import socket
import urllib2
import urllib
import datetime
import time
import os
import sys

from reportlab.lib.pagesizes import A4,letter, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Image
from PIL import Image


from  decimal import Decimal as Dcm
#ls=[{'in':,'len':10},]
convertLs={
            'compliance_rate':'1000',
            'amount':'100',
            'product_rate':'1000',
            'product_rate_float':'1000',
            'execute_rate':'1000',
            'overdue_rate_more':'1000',
            'overdue_rate':'1000',
            'shift_fine_rate':'1000',
            'shift_rate':'1000',
            'debt_interest':'1000',
            'debt_interest_and':'1000',
            'gty_percent':'1000',
            'gty_amount':'1000',
            'discount_rate':'1000',
            'discount_interest':'1000',
            'bill_rate_sum':'1000',
            'reg_amount':'10000',
            'paid_amount':'10000',
            'asset_amount':'10000',
            'liability_amount':'10000',
            'bill_amount':'100',
}

def float_to_int(data):
    for item in data.keys():
        up = convertLs.get(item)
        value = data.get(item)
        if up and value:
            result = Dcm(value)*Dcm(up)
            data.update({item:str(result.to_integral_value())})

def int_to_float(data):
    for item in data.keys():
        down = convertLs.get(item)
        value = data.get(item)
        if down and value:
            result = Dcm(value)/Dcm(down)
            data.update({item:str(result)})

DPI = 72
def img_cut(img):
    global DPI
    cutList=[]
    w = img.size[0]
    h = img.size[1]
    tmpfile = time.time()
    tmpfile = str(tmpfile).replace('.','')
    l = 0;
    while l < h:
        region = (l,w,400,500)
        l = l + 400;


def jpg_convert(fileList):
    global DPI
    maxw,maxh = A4
    newList = []
    for i in fileList:
        im = Image.open(i)
        w = im.size[0]
        h = im.size[1]
        dpi = im.info.get('dpi')

        if dpi:
            w = (w*1.0)/dpi[0]*DPI
            h = (h*1.0)/dpi[1]*DPI
            if h > maxh:
                newList.extend(img_cut(im))
            else:
                if w > maxw:
                    w = maxw
                newList.append({'w':w,'h':h,'path':i})
        else:
            if w > maxw:
                w = maxw
            if h > maxh:
                h = maxh
            newList.append({'w':w,'h':h,'path':i})


def jpg2pdf(fileList=[],fit=True):
    u"""  jpg 转 pdf  """
    maxw = 0
    maxh = 0
    tmpfile = time.time()
    tmpfile = str(tmpfile).replace('.','')
    for i in fileList:
        im = Image.open(i)
        print im.size,im.info
        dpi = im.info.get('dpi')
        print dpi
        if maxw < im.size[0]:
            maxw = im.size[0]
        if maxh < im.size[1]:
            maxh = im.size[1]
    filename_pdf = '../web/fabs/images/tmp/'+tmpfile+'.pdf'
    print filename_pdf
    maxsize = (maxw,maxh)
    #maxsize
    #fit=False
    #maxw,maxh = A4
    c = canvas.Canvas(filename_pdf, pagesize=maxsize )
    for fl in fileList:
        (w, h) =maxsize
        #width, height = A4
        #print width,height
        # fit = True 画图片原始大小 否则 图片填充pdf
        if fit == True:
            c.drawImage(fl,0,0)
        else:
            c.drawImage(fl,0,0,maxw,maxh)
        c.showPage()
    c.save()
    return filename_pdf

def tree_dump(model):
    """ Model find children merge to dict """
    if model.children:
        children = [tree_dump(m) for m in  model.children]
        new_model = row_dict(model)
        new_model['children'] = children
        return new_model
    else:
        return row_dict(model)

""" Model to dict """
row_dict =lambda r: {c.name: unicode(getattr(r, c.name)) for c in r.__table__.columns}

def to_md5(pwd):
    import hashlib
    encryption = hashlib.md5()
    if pwd:
        encryption.update(pwd)
        return encryption.hexdigest()
    return False
