from django.shortcuts import render, redirect
from django.contrib import messages

from dashboard.models import *
from dashboard.forms import *
from dashboard.serializers import *

from django.conf import settings

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail


def is_authenticated(f):
    def wrap(request, *args, **kwargs):
        # this check the session if userid key exist, if not it will redirect to login page
        try:
            user_obj = StaffUser.objects.get(id=request.session['id'])
        except:
            user_obj = False
        if 'id' in request.session.keys() and user_obj:
            return f(request, *args, **kwargs)

        request.session.clear()
        return redirect("login")
    wrap.__doc__ = f.__doc__
    # wrap.__name__ = f.__name__
    return wrap


@is_authenticated
def home(request):

    try:
        main_user_obj = ''
        staff_obj = ''
        workspace_obj = ''

        user_obj = StaffUser.objects.get(id=request.session.get('id'))
        employees = StaffUser.objects.filter(active_status=True, is_employee=True)

        if request.session.get('is_admin') == False:
            workspace = WorkSpace.objects.filter(status=True, staff=user_obj)
        else:
            workspace = WorkSpace.objects.filter(status=True)

        if request.method == 'POST':
            invite_email = request.POST.get('email')
            workspace_id = request.POST.get('workspace')
            workspace_obj = WorkSpace.objects.get(id=workspace_id)

            try:
                main_user_obj = User.objects.get(email=invite_email)
                staff_obj = StaffUser.objects.get(email=invite_email)
            except Exception as e:
                # print('----exception error in invite----', e)
                name = invite_email.split('@')[0]
                main_user_obj = User.objects.create_user(username=name, email=invite_email, password=str(name)+str(123))
                staff_obj = StaffUser.objects.create(name=name, email=invite_email, password=str(name)+str(123))

                from_mail = settings.EMAIL_HOST_USER
                to_email = main_user_obj.email
                body = "DITS staff acccount has been created: \n\n"\
                        "User Name : {} ".format(staff_obj.name)+'\n'+\
                        "Email: {} ".format(staff_obj.email)+'\n'+\
                        "Password: {} ".format(staff_obj.password)+'\n'+\
                        "link: {} ".format(settings.BASE_DOMAIN + '/login')

                send_mail(
                    'Welcome to DITS Task Management App',
                    body,
                    from_mail,
                    [to_email],
                    fail_silently=False,
                )

            workspace_obj.staff.add(staff_obj)

            from_mail = settings.EMAIL_HOST_USER
            subject = "You've been invited to the new Workspace..."
            message = render_to_string('{0}/templates/mail_templates/join_team_invitation.html'.format(settings.BASE_DIR),{'url':settings.BASE_DOMAIN + '/' + workspace_obj.slug})
            msg = EmailMultiAlternatives(subject, message, from_mail, [invite_email])
            msg.attach_alternative(message, 'text/html')
            msg.send(fail_silently=False)

        if request.GET.get('id'):
            if request.method == "GET" and request.is_ajax():
                task_obj = Task.objects.get(id=request.GET.get('id'))
                task_obj.priority = request.GET.get('priority')
                task_obj.save()
                messages.success(request, 'Task priority changed successfully...')

        elif request.GET.get('iss_id'):
            if request.method == 'GET' and request.is_ajax():
                issue_obj = Issue.objects.get(id=request.GET.get('iss_id'))
                issue_obj.priority = request.GET.get('issu_priority')
                issue_obj.save()
                messages.success(request, 'Issue prority changed successfully...')

    except Exception as e:
        # print('---exception as error------', e)
        user_obj = ''
        employees = ''
        workspace = ''
    return render(request,'dashboard/home.html', {
                        'obj': user_obj, 'employees':employees, 'workspace': workspace, 
                        'len_work':len(workspace),
    })


@is_authenticated
def workspace_edit(request, id):
    
    workspace_obj = WorkSpace.objects.get(id=id)
    if request.method == 'POST':
        form = WorkspaceUpdateForm(request.POST, instance=workspace_obj)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = WorkspaceUpdateForm(instance=workspace_obj)
    return render(request, 'dashboard/workspace_update.html', {'object':workspace_obj})
