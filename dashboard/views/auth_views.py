from django.contrib import messages
from django.core import exceptions
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from dashboard.models import *
from dashboard.forms import *
from dashboard.views.dashboard_views import is_authenticated

from django.core.mail import send_mail
from django.conf import settings


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
                    messages.success(request, 'Login Successfully...!')
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
        messages.success(request, 'Logout Successfully...!')
    except Exception as e:
        print('-exception error in logout---', e)
        pass

    return redirect('login')


def signup(request):

    if request.method == 'POST':
        try:
            if len(User.objects.filter(username=request.POST['name'])) > 0:
                messages.error(request, 'provided user name already taken..')
            elif len(User.objects.filter(email=request.POST['email'])) > 0:
                messages.error(request, 'Provided Email already taken..')
            else:
                form = StaffUserForm(request.POST)
                if form.is_valid():
                    form_save = form.save(commit = False)
                    user = User.objects.create_user(username=request.POST['name'], email=request.POST['email'], password=request.POST['password'])
                    form_save.user_id = user
                    form_save.save()

                    from_mail = settings.EMAIL_HOST_USER
                    to_email = form_save.email
                    body = "DITS staff acccount has been created: \n\n"\
                            "User Name : {} ".format(form_save.name)+'\n'+\
                            "Email: {} ".format(form_save.email)+'\n'+\
                            "Password: {} ".format(form_save.password)

                    send_mail(
                        'Welcome to DITS Task Management App',
                        body,
                        from_mail,
                        [to_email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Member ' + form_save.name + ' added successfully...!')
                    return redirect('login')
        except Exception as e:
            print('----error as e----', e)
            messages.error(request, 'Provided user already exists..')
    else:
        form = StaffUserForm()
    return render(request, 'dashboard/login.html')
    