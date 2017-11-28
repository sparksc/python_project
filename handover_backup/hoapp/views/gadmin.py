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
class CarForm(forms.Form):
    serial = forms.CharField(label='车辆序号')
    number_plate = forms.CharField(label='车牌号')

class UserForm(forms.Form):
    teller_name = forms.CharField()
    teller_pwd = forms.CharField()
    teller_serial = forms.CharField()
    teller_branch = forms.CharField()
    teller_tel = forms.CharField()
    teller_status = forms.CharField()
    teller_remark = forms.CharField(required=False)

class AmbangForm(forms.Form):
    name = forms.CharField()

class MajorForm(forms.Form):
    name = forms.CharField()
    serial = forms.CharField()

class AssistForm(forms.Form):
    name = forms.CharField()
    serial = forms.CharField()


def get_branchs(is_obj=False):
    
    branchs_object = Branch.objects.filter( is_active='1' ).all()
    if is_obj:
        return branchs_object
    branchs = [branch.name for branch in branchs_object]
    if branchs is None:
        branchs = ['测试城北银行', '测试城西银行', '测试城南银行', '测试城东银行']
    return branchs


@login_required
def car_form_check(request):
    if request.method == 'POST':
        form = request.POST
        number_plate = form.get('number_plate')
        data = {
            'is_number_plate_taken': CarInfo.objects.filter(number_plate=number_plate).exists()
        }

    return JsonResponse(data)


@login_required
def car_save(request):
    """
    if not 'fimg' in request.FILES or not 'bimg' in request.FILES:
        pass
    """
    if request.method == 'POST':
        form = request.POST
        number_plate = form.get('number_plate')
        number_plate = number_plate.upper()
        path = os.path.dirname(__file__)

        if form.get('method'):
            car = CarInfo.objects.get(id=carid)
        else:
            car = CarInfo.objects.create( number_plate=number_plate, img_serial='0', is_active='1')
        car.save()
        car_id = car.id
        print car_id
        img_serial = '%s' % uuid.uuid5(uuid.NAMESPACE_DNS, str(car.id))
        fimg = Image.open(request.FILES['fimg'])
        fimg.save(os.path.join(path, '../static/images/car/fimg_%s.png' % img_serial), 'PNG', quality=80)
        bimg = Image.open(request.FILES['bimg'])
        bimg.save(os.path.join(path, '../static/images/car/bimg_%s.png' % img_serial), 'PNG', quality=80)
        car.img_serial = img_serial
        car.save()

    data = {'123': 123}
    return JsonResponse(data)


@csrf_exempt
@login_required
def carmanage(request):
    if request.method == 'POST':
        form = request.POST
        carid = form.get('carid')
        try:
            car = CarInfo.objects.get(id=carid)
            if car:
                data = {
                    'is_success': True,
                    'serial': car.serial,
                    'number_plate': car.number_plate
                }
            else:
                data = {
                    'is_success': False,
                    'rtn': '车辆信息错误！'
                }
        except Exception, e:
            data = {
                'is_success': False
            }
        return JsonResponse(data)
    all_car = CarInfo.objects.all()
    return render_to_response('admin/car/carmanage.html', {'all_car':all_car})
    # return HttpResponseRedirect('/admin/carmanage/')







@login_required
def cardel(request):
    if request.method == 'POST':
        form = request.POST
        carid = form.get('id')
        try:
            car = CarInfo.objects.get(id=carid)
            if car:
                car.is_active = '0'
                car.save()
            data = {
                'is_success': True
            }
        except Exception, e:
            data = {
                'is_success': False
            }
    return JsonResponse(data)


@login_required
def staffmanage(request):
    group = Group.objects.get(name='teller')
    users = group.user_set.filter(is_active='1').all()
    return render_to_response('admin/internalStaff/staffmanage.html', {'users': users})


@login_required
def addteller(request):
    status = {'1': '在岗', '2':'离岗'}
    if request.method == 'POST':
        form = request.POST 
        teller_serial = form.get('teller_serial')
        teller_pwd = form.get('teller_pwd')
        teller_name = form.get('teller_name')
        teller_branch = form.get('teller_branch')
        teller_tel = form.get('teller_tel')
        teller_status = status[form.get('teller_status')]
        teller_remark = form.get('teller_remark')
        sid = transaction.savepoint()
        print teller_branch
        try:
            branch = Branch.objects.get( id=teller_branch )
            print branch.name
            user = User.objects.create_user(username=teller_serial, password=teller_pwd,
                    name=teller_name, branch=branch, tel=teller_tel,
                    status=teller_status, remark=teller_remark)
            g = Group.objects.get(name='teller')
            user.groups.add(g)
            user.save()
            transaction.commit()
            data = {
                    'is_success' : True
                    }
        except Exception, e:
            data = {
                    'is_success' : False
                    }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        return JsonResponse(data)

@login_required
def del_teller(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        sid = transaction.savepoint()
        try:
            user = User.objects.get( id = user_id )
            user.delete()
            transaction.commit()
            data = {
                    'is_success' : True
                    }

        except Exception, e:
            data = {
                    'is_success' : False
                    }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        return JsonResponse(data)
        
@login_required
def teller_form_check(request):
    if request.method == 'POST':
        form = request.POST
        teller_serial = form.get('teller_serial')
        try:
            user = User.objects.filter( username = teller_serial ).first()
            if user:
                 data = { 'user_token' : True }
            else:  
                 data = { 'user_token' : False }
        except Exception,e:
            data = { 'user_token' : False }
            traceback.print_exc()
        return JsonResponse(data)






@login_required
def personmanage(request):
    ambangs = AmbangInfo.objects.all()
    majors = MajorInfo.objects.all()
    assists = AssistInfo.objects.all()
    return render_to_response('admin/personmanage/personmanage.html',
            {'ambangs': ambangs, 'majors': majors, 'assists': assists})


@login_required
def addambang(request):
    if not 'fimg' in request.FILES or not 'bimg' in request.FILES:
        pass
    if request.method == 'POST':
        form = request.POST
        name = form.get('amp_name')
        path = os.path.dirname(__file__)
        img_serial = '%s' % uuid.uuid5(uuid.NAMESPACE_DNS, str(time.time()))
        sid = transaction.savepoint()
        try:
            fimg = Image.open(request.FILES['fimg'])
            fimg.save(os.path.join(path, '../static/images/person/ambang/fimg_%s.png' % img_serial), 'PNG', quality=80)

            bimg = Image.open(request.FILES['bimg'])
            bimg.save(os.path.join(path, '../static/images/person/ambang/bimg_%s.png' % img_serial), 'PNG', quality=80)
            ambang = AmbangInfo.objects.create(name=name, img_serial=img_serial, is_active='1')
            ambang.save()
            transaction.commit()
            data = { 'is_success' : True }
        except Exception, e:
            data = { 'is_success' : False }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        return JsonResponse(data)


@login_required
def show_ambang(request):
    if request.method == 'POST':
        form = request.POST
        ambang_id = form.get("ampang_id")
        try:
            ambang=AmbangInfo.objects.get(id=ambang_id)
            if ambang:
                data = {
                        'is_success' : True,
                        'ambang_id'  : ambang.id,
                        'ambang_name': ambang.name
                        }
        except:
            data = {
                    'is_success':False
                    }
        return JsonResponse(data)
    ambangs = AmbangInfo.objects.all()
    return render_to_response('admin/personmanage/ampanginfo.html', {'ambangs': ambangs})


@login_required
def alter_ambang(request):
    if not 'fimg' in request.FILES or not 'bimg' in request.FILES:
        pass
    if request.method == 'POST':
        form = request.POST
        path = os.path.dirname(__file__)
        img_serial = '%s'%uuid.uuid5(uuid.NAMESPACE_DNS, str(time.time()))
        fimg = Image.open(request.FILES['fimg'])
        fimg.save(os.path.join(path, '../static/images/person/ambang/fimg_%s.png'%img_serial), 'PNG', quality=80)

        bimg = Image.open(request.FILES['bimg'])
        bimg.save(os.path.join(path, '../static/images/person/ambang/bimg_%s.png' % img_serial), 'PNG',quality = 80)
        ambang_id = form.get('ambang_id')
        name = form.get('name')
        sid = transaction.savepoint() 
        try:
            ambang = AmbangInfo.objects.get( id=ambang_id ) 
            os.remove(os.path.join(path, '../static/images/person/ambang/fimg_%s.png'%ambang.img_serial)) 
            os.remove(os.path.join(path, '../static/images/person/ambang/bimg_%s.png'%ambang.img_serial)) 

            if ambang:
                ambang.img_serial = img_serial
                ambang.save()
            transaction.commit()
            data = {
                    'is_success' : True
                    }
        except Exception, e:
            data = {
                    'is_success' : False
                    }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        return JsonResponse(data)


@login_required
def ambangdel(request):
    if request.method == 'GET':
        ambang_id = request.GET.get('ambang_id')
        ambang = AmbangInfo.objects.get( id=ambang_id )
        if ambang:
            ambang.is_active = '0'
            ambang.save()
            data = { 'is_success' : True }
        else:
            data = { 'is_success' : False }
        return JsonResponse(data) 

@login_required
def addmajor(request):
    if request.method == 'POST':
        form = request.POST
        name = form.get('major_name')
        serial = form.get('major_serial')
        path = os.path.dirname(__file__)
        img_serial = '%s'%uuid.uuid5(uuid.NAMESPACE_DNS, str(serial))
        sid = transaction.savepoint()
        try:
            img = Image.open(request.FILES['himg'])
            img.save(os.path.join(path, '../static/images/person/major/img_%s.png'% img_serial), 'PNG', quality=80)
            major = MajorInfo.objects.create(name=name, serial=serial,img_serial=img_serial,is_active='1')
            major.save()
            transaction.commit()
            data = { 'is_success' : True 
                    }
        except Exception,e:
            data = { 'is_success' : False }
            traceback.print_exc()
            assisttransaction.savepoint_rollback(sid)
        return JsonResponse(data)

@login_required
def del_major(request):
    if request.method == 'POST':
        form = request.POST
        major_id = form.get('major_id')
        sid = transaction.savepoint()
        try:
            major = MajorInfo.objects.get( id=major_id )
            if major:
                major.is_active = '0'
                major.save()
                data = {
                        'is_success' : True
                        }
        except Exception, e:
            data = {
                    'is_success' : False 
                    }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        else:
            transaction.commit()
    else:
        data = {
            'is_success' : False
                }
    return JsonResponse(data)

@login_required
def show_major(request):
    if request.method == 'POST':
        form = request.POST
        major_id = form.get('major_id')
        try:
            major = MajorInfo.objects.get( id=major_id )
            if major:
                data = {
                        'is_success' : True,
                        'major_id' : major.id,
                        'major_name' : major.name,
                        'major_serial' : major.serial
                        
                        }
                return JsonResponse(data)
        except Exception, e:
            traceback.print_exc()
            data = {
                    'is_success' : False
                    }
    else:
        data = {
                'is_success': False
                }
    return JsonResponse(data)

@login_required
def alter_major(request):
    if request.method == 'POST':
        form = request.POST
        path = os.path.dirname(__file__)
        img_serial = '%s'%uuid.uuid5(uuid.NAMESPACE_DNS,str(time.time()))
        fimg = Image.open(request.FILES['himg'])
        fimg.save( os.path.join( path, '../static/images/person/major/img_%s.png'%img_serial), 'PNG', quality = 80 )
        major_id = form.get('major_id')
        major_name = form.get('major_name')
        major_serial = form.get('major_serial')
        sid = transaction.savepoint()
        try:
            major = MajorInfo.objects.get( id=major_id )
            os.remove(os.path.join(path, '../static/images/person/major/img_%s.png'%major.img_serial))
            if major:
                major.name = major_name
                major.serial = major_serial
                major.img_serial = img_serial
                major.save()
                data = {
                        'is_success' : True
                        }
        except Exception, e:
            data = {
                    'is_success' : False
                    }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        else:
            transaction.commit()
        return JsonResponse(data)
@login_required
def major_form_check(request):
    if request.method == 'GET':
        major_serial = request.GET.get('major_serial')
        major = MajorInfo.objects.filter(serial=major_serial).first()
        if major is not None:
            if major.is_active == '1':
                data = {
                        'is_major_serial_exist' : True
                        }
            else:
                data = {
                        'is_major_serial_exist' : False
                        }
        else:
            data = {
                    'is_major_serial_exist' : False
                    
                    }
            #print data['is_major_serial_exist']
    return JsonResponse(data)















@login_required
def del_assist(request):
    if request.method == 'GET':
        assist_id = request.GET.get('assist_id')
        sid = transaction.savepoint()
        try:
            assist = AssistInfo.objects.get( id=assist_id )
            if assist:
                assist.is_active = '0'
                assist.save()
                data = {
                        'is_success' : True
                        }
        except Exception, e:
            data = {
                    'is_success' : False
                    }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        else:
            transaction.commit()
    else:
        data = {
                'is_success' : True
                }
    return JsonResponse(data)




@login_required
def addassist(request):
    if not 'himg' in request.FILES:
        pass
    if request.method == 'POST':
        form = request.POST
        name = form.get('assist_name')
        serial = form.get('assist_serial')
        path = os.path.dirname(__file__)
        img_serial = '%s' % uuid.uuid5(uuid.NAMESPACE_DNS, str(serial))
        sid = transaction.savepoint()
        try:
            img = Image.open(request.FILES['himg'])
            img.save(os.path.join(path, '../static/images/person/assist/img_%s.png' % img_serial), 'PNG', quality=80)

            assist = AssistInfo.objects.create(name=name, serial=serial, img_serial=img_serial, is_active='1')
            assist.save()
            data = {
                    'is_success' : True
                    }
        except Exception,e:
            data = {
                    'is_success' : False
                    
                    }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        else:
            transaction.commit()
        return JsonResponse(data) 

@login_required
def show_assist(request):
    if request.method == 'POST':
        form = request.POST
        assist_id = form.get('assist_id')
        try:
            assist = AssistInfo.objects.get( id=assist_id )
            if assist:
                data = {
                        'is_success' : True,
                        'assist_id' : assist.id,
                        'assist_name' : assist.name,
                        'assist_serial' : assist.serial
                        }
            else:
                data = {
                        'is_success' : False
                        }
        except Exception, e:
            traceback.print_exc()
            data = {
                    'is_success' : False
                    }
    else:
        data = {
                'is_success' : False
                }                
    return JsonResponse(data)



@login_required
def alter_assist(request):
    if not 'himg' in request.FILES:
        pass
    if request.method == 'POST':
        form = request.POST
        path = os.path.dirname(__file__)
        img_serial = '%s'%uuid.uuid5(uuid.NAMESPACE_DNS, str(time.time()));
        himg = Image.open(request.FILES['himg'])
        himg.save( os.path.join(path,'../static/images/person/assist/img_%s.png'%img_serial), 'PNG', quality=80 )
        assist_id = form.get('assist_id')
        #assist_name = form.get('assist_name')
        sid = transaction.savepoint()
        try:
            assist = AssistInfo.objects.get( id=assist_id )
            os.remove(os.path.join(path, '../static/images/person/assist/img_%s.png'%assist.img_serial)) 
            if assist:
                assist.img_serial = img_serial
                #assist.name = assist_name
                assist.save()
                data = {
                        'is_success' : True
                        }
            else:
                pass
        except Exception, e:
            data = {
                    'is_success': False
                    }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        else:
            transaction.commit()
        return JsonResponse(data)

@login_required
def assist_form_check(request):
    if request.method == 'GET':
        assist_serial = request.GET.get('assist_serial')
        assist = AssistInfo.objects.filter( serial=assist_serial ).first()
        if assist is not None:
            if assist.is_active == '1':
                data = {
                        'assist_serial_token' : True
                        }
            else:
                data = {
                        'assist_serial_token' : False
                        }
        else:
            data = {
                    'assist_serial_token' : False
                    }
    return JsonResponse(data)
    

@csrf_exempt
@login_required
def route_manager(request):
    branchs = Branch.objects.filter( is_active = '1' ).all()
    cars = CarInfo.objects.filter( is_active = '1' ).all()
    routes = RouteInfo.objects.filter( is_active='1' ).all()
    majors = MajorInfo.objects.filter( is_active ='1').all()
    assists = AssistInfo.objects.filter( is_active='1' ).all()
    ambs = AmbangInfo.objects.filter( is_active='1' ).all()
    return render_to_response('admin/routemanage/routemanage.html', {'cars': cars, 'routes' : routes, 'majors':majors, 'assists':assists,'ambs':ambs,'branchs' : branchs})

@login_required
def get_branch(request):
    if request.method == 'GET':
        branchs = get_branchs() 
        data = {
                'is_success' : True,
                'branch' : branchs
                }
        print data
        return JsonResponse(data)

#内部人员管理获取银行信息
@login_required
def get_branch_inter(request):
    if request.method == 'GET':
        branchs = get_branchs(True)
        bras = [[branch.id, branch.name] for branch in branchs]
        data = {
                'is_success' : True,
                'branchs' : bras
                }
        return JsonResponse(data)


@login_required
def add_route(request):
    if request.method == 'POST':
        form = request.POST
        route_name = form.get('route_name')
        route_ids = form.get('route')
        sid = transaction.savepoint()
        try:
            route = RouteInfo( name=route_name,is_active='1' )
            route.save()

            rids = route_ids.split('-')
            for i in rids:
                branch = Branch.objects.get( id = i )
                route.routes.add(branch)
            print route.routes.all()
            route.save()
            data = {
                    'is_success' : True
                    
                    }
        except Exception, e:
            data = {
                    'is_success' : False 
                    }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        else:
            transaction.commit()
        return JsonResponse(data)


@login_required
def del_route(request):
    if request.method == 'GET':
        route_id = request.GET.get('route_id')
        sid = transaction.savepoint()
        try:
            route = RouteInfo.objects.get( id = route_id )
            route.is_active = '0'
            route.save()
            data = {
                    'is_success' : False
                    }
        except Exception, e:
            data = {
                    'is_success' : True
                    }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        else:
            transaction.commit()
        return JsonResponse(data)

#回显数据
@login_required
def route_show(request):
    if request.method == 'POST':
        form = request.POST
        route_id = form.get('route_id')
        try:
            route = RouteInfo.objects.get( id = route_id )
            if route:
                branchs = route.routes.all()
                branch_routes = [[b.id,b.name] for b in branchs]
                    
                print branch_routes
                data = {
                        'is_success' : True,
                        'name' : route.name,
                        'branch_routes' : branch_routes,
                        'modify_date' : route.modify_date
                        }
            else:
                data = {
                        'is_success' : False
                        }
        except Exception, e:
            data = {
                    'is_success': False
                    }
    else:
        data = {
                'is_success' : False
                }
    return JsonResponse(data)
            

@login_required
def alter_route(request):
    if request.method =='POST':
        form = request.POST
        route_name = form.get('route_name')
        route = form.get('route')#branch的id集合
        route_id = form.get('route_id')
        sid = transaction.savepoint()
        route_ids = route.split('--')
        try:
            routeins = RouteInfo.objects.get( id = route_id )
            if routeins:
                routeins.name = route_name
                routeins.routes.clear()
                routeins.save()
                for i in route_ids:
                    print i,"======"
                    br = Branch.objects.get( id = i )
                    routeins.routes.add(br)
                routeins.save()
                for b in routeins.routes.all():
                    print b.name
                data = {
                        'is_success' : True
                        }
                transaction.commit()
            else:
                data = {
                        'is_success' : False
                        }
        except Exception,e:
            data = {
                    'is_success' : False
                    }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        return JsonResponse( data )

#网点申请情况界面
@login_required
def apl_manage(request):
    pass



@login_required
def get_route(request):
    if request.method == 'GET':
        route_id = request.GET.get('route_id')
        try:
            routes = RouteInfo.objects.get( id=route_id )
            rs = ""
            for branch in routes.routes.all():
                if rs == "":
                    rs = branch.name
                else:
                    rs = rs + '-'+branch.name
                
            data = {
                    'is_success' : True,
                    'routes' : rs 
                    }
            
        except Exception,e:
            traceback.print_exc()
            data = {
                    'is_success' : False
                    }
        return JsonResponse( data )





#钱箱管理index
@login_required
def cashbox_manage(request):
    branchs = get_branchs(True)
    cashboxs = Cashbox.objects.filter(is_active='1').all()
    
    return render_to_response('admin/cashbox/cashbox.html',{'branchs' : branchs,'cashboxs':cashboxs})


#添加钱箱form
@login_required
def add_cashbox_form(request):
    if request.method == 'GET':
        try:
            branchs_obj = get_branchs(True)
            branchs = [(branch.id, branch.name) for branch in branchs_obj]
            data = {
                    'is_success' : True,
                    'branchs' : branchs
                    } 
        except Exception, e:
            traceback.print_exc()
            data = {
                    'is_success' : False
                    }
        return JsonResponse( data )

#添加cashbox
@login_required
def add_cashbox(request):
    if request.method == 'POST':
        form = request.POST
        serial = form.get('serial')
        kind = form.get('kind')
        branch_id = form.get('branch_id')
        print branch_id
        remark = form.get('remark')
        sid = transaction.savepoint()
        try:
            branch = Branch.objects.get( id=branch_id ) 
            print branch.name,branch.id,branch.serial
            cashbox = Cashbox.objects.create( serial=serial, status=Cashbox.ATSTOCK,kind=kind ,branch=branch, remark=remark, is_active='1')
            cashbox.save()
            data = {
                    'is_success': True
                    }
        except Exception, e:
            data = {
                    'is_success' : False
                    }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        else:
            transaction.commit()
        return JsonResponse(data)



#删除cashbox
@login_required
def cashbox_del(request):
    if request.method == 'GET':
        cashbox_id = request.GET.get('cashbox_id')
        sid = transaction.savepoint()
        try:
            cashbox = Cashbox.objects.get( id=cashbox_id )
            cashbox.is_active='0'
            cashbox.save()
            data = {
                    'is_success' : True
                    }
        except Exception, e:
            data = {
                    'is_success' : False
                    }
            traceback.print_exc()
            transaction.savepoint_rollback(sid)
        else:
            transaction.commit()
        return JsonResponse(data)



#网点申请列表
@login_required
def apllist(request):
    aplboxs_obj = CashboxaplInfo.objects.filter( is_active = '1' ).filter( ~Q(apl_status='0') ).all()
    return render_to_response('admin/arrangeroute/arrangemanage.html', {'aplboxs': aplboxs_obj})

@login_required
def del_apl(request):
    if request.method == 'GET':
        apl_id = request.GET.get('apl_id')
        apl = CashboxaplInfo.objects.get( id = apl_id )
        apl.is_active = '0'
        apl.save()
        data = {
                'is_success' : True
                }
        return JsonResponse( data)

@login_required
def preview(request):
    pass
    '''
    if request.method == 'POST':
        form = request.POST
        route_ids = form.get('route_id')
        car_ids = form.get('car_id')
        site_ids = form.get('site_ids')
        major_ids = form.get('major_ids')
        assist_ids = form.get('assist_ids')
        amb_ids = form.get('amb_ids')
        sites = site_ids.split('-') #网点id集合
        majors = major_ids.split('-') #主办人员id集合
        assists = assist_ids.split('-') #网点协办人员id集合
        ambs = amb_ids.split('-') #押运人员id集合
        try:
            cnci = CboxconfirmInfo.objects.create()
            for i in site_dis:
                branch = Branch.objects.get( id = i )
                cbi = CashboxaplInfo.objects.filter( branch=branch ).all()
                for c in cbi:
                    cnci.
                
    '''


def routeutl(ids):
    #1获取路线id
    rb_id = []
    r_id = [] #路径id
    routes_obj = RouteInfo.objects.filter(is_active = '1').all()
    for r_obj in routes_obj:
        r =  r_obj.route.split('-')
        r_int = map( eval, r )
        rb_id.append( r_int )
        r_id.append(r_obj.id)
    #2获取申请银行id
    apl_branch = [] #申请银行id
    ids_list = ids.split('-')
    for i in ids_list:
        apl_obj = CashboxaplInfo.objects.get( id=i )
        apl_branch.append( apl_obj.branch.id )
    maxRo = -1#路线重合最大值
    for idx,ri in enumerate(rb_id):
        max_route = [i for i in ri if i in apl_branch]#求交集
        if len( max_route ) > maxRo:
            maxRo = len(max_route)
            best_route_id = r_id[idx] #最佳路线id
    print best_route_id,"========="
    return best_route_id,max_route


#安排线路
@login_required
def arrage_aplroute(request):
    if request.method == 'GET':
        #ids = request.GET.get('ids')
        branchs = Branch.objects.filter( is_active = '1' ).all()
        cars = CarInfo.objects.filter( is_active = '1' ).all()
        routes = RouteInfo.objects.filter( is_active='1' ).all()
        majors = MajorInfo.objects.filter( is_active ='1').all()
        assists = AssistInfo.objects.filter( is_active='1' ).all()
        ambs = AmbangInfo.objects.filter( is_active='1' ).all()
        return render_to_response('admin/arrangeroute/aplmanage.html',{'branchs': branchs,'cars':cars, 'routes':routes, 'majors': majors,'assists':assists, 'ambs':ambs}) 

@login_required
def aplmanage(request):
    branchs = Branch.objects.filter( is_active = '1' ).all()
    cars = CarInfo.objects.filter( is_active = '1' ).all()
    routes = RouteInfo.objects.filter( is_active='1' ).all()
    majors = MajorInfo.objects.filter( is_active ='1').all()
    assists = AssistInfo.objects.filter( is_active='1' ).all()
    ambs = AmbangInfo.objects.filter( is_active='1' ).all()
    return render_to_response('admin/arrangeroute/aplmanage.html',{'branchs': branchs,'cars':cars, 'routes':routes, 'majors': majors,'assists':assists, 'ambs':ambs}) 
