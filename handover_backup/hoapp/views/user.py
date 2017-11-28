# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group

from hoapp.models import User

class UserForm(forms.Form):
    username = forms.CharField(label='用户名', error_messages={'required':'用户名不能为空'})
    password = forms.CharField(label='密码', error_messages={'required':'密码不能为空'})

def is_user_exist(request):
    if request.method == 'POST':
        form = request.POST
        username = form.get('username')
        password = form.get('password')
        flag = False
        if password:
            data = {'method': 'login'}
            user = authenticate(username=username, password=password)
            if user:
                data['is_right'] = True
                login(request, user)
        else:
            data = {
                'is_taken': User.objects.filter(username=username).exists()
            }
    return JsonResponse(data)

@csrf_exempt
def user_login(request):
    logout(request)

    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    print 'login success'
                    login(request, user)
                    response = HttpResponseRedirect('/index/')
                    return response
            else:
                print 'login failed'
                return HttpResponseRedirect('/login/')
        else:
            return get_login(request, errors=form.errors)
    else:
        return render_to_response('login.html')
    """
    return render_to_response('login.html')


def user_logout(request):
    logout(request)
    response = HttpResponseRedirect('/login/')
    return response


def init(request):
    username = '12'
    password = '12'
    user = User.objects.create_user(username=username, password=password)
    group1 = Group(name="teller")
    group1.save()
    group2 = Group(name="admin")
    group2.save()
    user.groups.add(group2)        # user is now in the "Editor" group
    user.save()
    return HttpResponseRedirect('/login/')


@login_required
@csrf_exempt
def user_add(request):
    if request.method == 'POST':
        inf = UserForm(request.POST)
        if inf.is_valid():
            username = inf.cleaned_data['username']
            password = inf.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            g = Group.objects.get(name='teller')
            g.user_set.add(user)
            user.save()
    return render_to_response('login.html')


@login_required
def index(request):
    user = request.user
    flag = user.groups.filter(name='teller').exists()
    if flag:
        return render_to_response('teller/tnavindex.html', {'user': user, 'flag': flag})
    else:
        return render_to_response('admin/navindex.html', {'user': user, 'flag': flag})
