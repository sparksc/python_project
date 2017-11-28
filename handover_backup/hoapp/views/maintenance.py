# -*- coding: utf-8 -*- 
from __future__ import unicode_literals 
from django.shortcuts import render 
# Create your views here. 
from django.shortcuts import render, render_to_response 
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.contrib.auth.decorators import login_required 
from django import forms 
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth.models import Group 
from hoapp.models import * 
from PIL import Image 
import uuid, os, time 
from django.db import transaction 
import traceback 
from django.db.models import Q 

@login_required
def show_teller(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        print staff_id
        try:
            inner_staff =  User.objects.get( id = staff_id )
            #branchs = Branch.objects.all()
            #bras = [[branch.id, branch.name] for branch in branchs]
            data  = {
                    'is_success' : True,
                    'serial' : inner_staff.username,
                    'name' : inner_staff.name,
                    'branch_id' : inner_staff.branch.id,
                    'branch_name' : inner_staff.branch.name,
                    #'branchs' : bras,  #返回所有的支行信息（id,name）
                    'tel': inner_staff.tel,
                    't_status' : inner_staff.status,
                    'remark' : inner_staff.remark
                    }
        except Exception,e:
            data = {
                    'is_success':True
                    }
            traceback.print_exc()

        return JsonResponse( data )

@login_required
def alterstaff(request):
    if request.method == 'POST':
        status = {'1':'在岗','2':'离岗'}
        form = request.POST
        staff_id = form.get('staff_id')
        teller_name = form.get('teller_name')
        tel = form.get('tel')
        tel_status = form.get('tel_status')
        remark = form.get( 'remark' )
        print form
        sid = transaction.savepoint()
        try:
            staff = User.objects.get( id = staff_id )
            staff.name = teller_name
            staff.tel = tel
            staff.tel_status = status[tel_status]
            staff.remark = remark
            staff.save()
            
            transaction.commit()
            data = {
                    'is_success' : True
                    }
        except Exception,e:
            data = {'is_success' : False }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        return JsonResponse( data )


        

@login_required
def rname_check(request):
    if request.method == 'GET':
        route_name = request.GET.get('route_name')
        data = { 
                'route_token' : RouteInfo.objects.filter( name = route_name ).exists()
                }
        return JsonResponse( data )


@login_required
def search_box(request):
    if request.method == 'GET':
        form = request.GET
        print form
        serial = form.get( 'serial' )
        branch = form.get( 'branch' )
        print type(serial),type(branch)
        if serial == "" and branch == "null":
            cashboxs = Cashbox.objects.filter(is_active='1').all()
        elif serial == "" and branch != "null":
            cashboxs = Cashbox.objects.filter( branch_id = branch ).filter(is_active='1').all() 
        elif serial != "" and branch =="null":
            cashboxs = Cashbox.objects.filter( serial = serial ).filter(is_active='1').all()
        else:
            cashboxs = Cashbox.objects.filter( serial = serial ).filter( branch_id = branch ).filter(is_active='1').all()
        branchs = Branch.objects.filter( is_active='1').all()
        return render_to_response('admin/cashbox/cashbox.html',{'branchs' : branchs,'cashboxs':cashboxs})







