from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from dashboard.models import *
from dashboard.forms import *
from dashboard.decorator import is_authenticated


def login(request):

    login_obj = ''
    login_check = ''

    if request.method == 'POST':
        email_input = request.POST.get('email_temp')
        pwd = request.POST.get('pass_temp')

        try:
            try:
                login_obj = StaffUser.objects.get(name=email_input).email
            except:
                login_obj = StaffUser.objects.get(email=email_input)
        except:    
            pass

        if login_obj != '':
            try:
                try:
                    login_check = StaffUser.objects.get(name=email_input, password=pwd)
                except:
                    login_check = StaffUser.objects.get(email=email_input, password=pwd)

                if login_check:
                    request.session['id'] = login_check.id
                    request.session['user_name'] = login_check.name
                    messages.success(request, 'Login Success...!')
                    return redirect('home')
            except Exception as e:
                print('-exception as error in login---', e)
                messages.error(request, 'Invalid Password..!')
        else:
            messages.error(request, 'Please check email or user-name...!')
    team_list = Team.objects.filter(status=True)
    return render(request, 'dashboard/login.html', {'teams':team_list})


@is_authenticated
def logout(request):

    try:
        del request.session['id']
        del request.session['user_name']
        messages.success(request, 'Logout Success...!')
    except Exception as e:
        print('-exception error in logout---', e)
        pass

    return redirect('login')