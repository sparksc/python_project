# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from views import user, gadmin,teller, maintenance
from django.views.generic.base import RedirectView

# 图标
favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
	url(r'^$', user.user_login, name='login'),
	url(r'^index/', user.index, name='index'),
	url(r'^login/', user.user_login, name='login'),
	url(r'^user_add/', user.user_add, name='user_add'),
	url(r'^logout/', user.user_logout, name='logout'),

	url(r'^admin/car_form_check/', gadmin.car_form_check, name='car_form_check'),
	url(r'^admin/car_save/', gadmin.car_save, name='car_save'),
	url(r'^admin/carmanage/', gadmin.carmanage, name='carmanage'),
	url(r'^admin/cardel/', gadmin.cardel, name='cardel'),
	url(r'^admin/staffmanage/', gadmin.staffmanage, name='staffmanage'),
	url(r'^admin/addteller/', gadmin.addteller, name='addteller'),
	url(r'^admin/delteller/', gadmin.del_teller, name='del_teller'),
	url(r'^admin/teller_form_check/', gadmin.teller_form_check, name='teller_form_check'),
	#personmanage
	url(r'^admin/personmanage/', gadmin.personmanage, name='personmanage'),
	#addambang
	url(r'^admin/addambang/', gadmin.addambang, name='addambang'),
	url(r'^admin/ambangdel/', gadmin.ambangdel, name='ambangdel'),
    url(r'^admin/showambang/', gadmin.show_ambang, name='show_ambang'),	
    url(r'^admin/alterambang/', gadmin.alter_ambang, name='alter_ambang'),

    #major
	url(r'^admin/addmajor/', gadmin.addmajor, name='addmajor'),
	url(r'^admin/delmajor/', gadmin.del_major, name='delmajor'),
    url(r'^admin/showmajor/', gadmin.show_major, name='show_major'),
    url(r'^admin/altermajor/', gadmin.alter_major, name='alter_major'),
    url(r'^admin/major_form_check/', gadmin.major_form_check, name='major_form_check'),
    
    #innserstaff
	url(r'^admin/get_branch_inter/', gadmin.get_branch_inter, name='get_branch_inter'),

	url(r'^admin/aplmanage/', gadmin.aplmanage, name='aplmanage'),
    #assist
	url(r'^admin/addassist/', gadmin.addassist, name='addassist'),
    url(r'^admin/delassist/', gadmin.del_assist, name='del_assist'),
    url(r'^admin/showassist/', gadmin.show_assist, name='show_assist'),
	url(r'^admin/alterassist/', gadmin.alter_assist, name='alter_assist'),
    url(r'^admin/assist_form_check/', gadmin.assist_form_check, name='assist_form_check'),

    #routemanage
	url(r'^admin/routemanager/', gadmin.route_manager, name='route_manager'),
	url(r'^admin/getbranch/', gadmin.get_branch, name='get_branch'),
	url(r'^admin/addroute/', gadmin.add_route, name='add_route'),
	url(r'^admin/delroute/', gadmin.del_route, name='del_route'),
	url(r'^admin/routeshow/', gadmin.route_show, name='route_show'),
	url(r'^admin/alterroute/', gadmin.alter_route, name='alter_route'),
	url(r'^admin/getroute/', gadmin.get_route, name='get_route'),
	url(r'^admin/apllist/', gadmin.apllist, name='apllist'),



    #aplist管理员审核钱箱配置路线
	url(r'^admin/aplmanage/', gadmin.apl_manage, name='apl_manage'),
	url(r'^admin/arrage_aplroute/', gadmin.arrage_aplroute, name='arrage_aplroute'),
	url(r'^admin/preview/', gadmin.preview, name='preview'),
    #测试使用
	url(r'^admin/delapl/', gadmin.del_apl, name='del_apl'),

    
    #cashbox
	url(r'^admin/cashboxmanage/', gadmin.cashbox_manage, name='cashbox_manage'),
	url(r'^admin/addcashbox_form/', gadmin.add_cashbox_form, name='add_cashbox_form'),
	url(r'^admin/addcashbox/', gadmin.add_cashbox, name='add_cashbox'),
	url(r'^admin/cashboxdel/', gadmin.cashbox_del, name='cashbox_del'),



    #柜员端路由
	url(r'^teller/aplboxmanage/', teller.aplbox_manage, name='aplbox_manage'),
	url(r'^teller/getcashbox/', teller.get_cashbox, name='get_cashbox'),
	url(r'^teller/aplbox/', teller.apl_box, name='apl_box'),
	url(r'^teller/recheck/', teller.recheck, name='recheck'),

    

    #维护页面
    #回显teller
	url(r'^maintenance/show_teller/', maintenance.show_teller, name='show_teller'),
    #修改teller
	url(r'^maintenance/alterstaff/', maintenance.alterstaff, name='alterstaff'),
    #验证路线名是否已存在
	url(r'^maintenance/rname_check/', maintenance.rname_check, name='rname_check'),
	url(r'^maintenance/searchbox/', maintenance.search_box, name='search_box'),



	url(r'^is_user_exist/', user.is_user_exist, name='is_user_exist'),

	url(r'^init/', user.init, name='init'),
    url(r'^favicon\.ico$', favicon_view),
]
