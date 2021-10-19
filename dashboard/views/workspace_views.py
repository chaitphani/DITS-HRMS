from django.shortcuts import render, redirect
from django.contrib import messages

from datetime import datetime

from dashboard.models import *
from dashboard.forms import *
from dashboard.serializers import *
from django.db.models import Sum, Count, F

from django.conf import settings

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def is_authenticated(f):
    def wrap(request, *args, **kwargs):
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


def is_staff_at_work(f):
    def wrap(request, *args, **kwargs):
        staff_in_work = []
        list_staff_ = WorkSpace.objects.filter(status=True).values('staff__name')

        for staff in list_staff_:
            staff_in_work.append(staff['staff__name'])

        if request.session['user_name'] in staff_in_work or request.session['is_admin'] == True:
            return f(request, *args, **kwargs)

        messages.info(request, 'You have no workspace yet..!')
        return redirect("home")
    wrap.__doc__ = f.__doc__
    # wrap.__name__ = f.__name__
    return wrap


@is_authenticated
@is_staff_at_work
def workspace_view(request, name):

    workspace_obj = WorkSpace.objects.filter(slug=name)
    tasks = Task.objects.filter(status=True, workspace__slug=name).order_by('-id')
    issues = Issue.objects.filter(status=True, workspace__slug=name).order_by('-id')

    employees = StaffUser.objects.filter(active_status=True, is_employee=True)
    return render(request, 'dashboard/workspace.html', {'tasks':tasks, 'issues':issues, 'employees':employees, 'workspace':workspace_obj,
    })


@is_authenticated
@is_staff_at_work
def task_detail_update_view(request, id, workspace_slug):
    
    task_obj = Task.objects.get(status=True, id=id, workspace__slug=workspace_slug)
    prev_assigned_user = task_obj.assigned_to.name

    if request.method == 'POST':
        planned_start_date = request.POST.get('planned_start_date')
        actual_start_date = request.POST.get('actual_start_date')
        planned_end_date = request.POST.get('planned_end_date')
        actual_end_date = request.POST.get('actual_end_date')
        description = request.POST.get('description')
        assigned_to = request.POST.get('assigned_to')
        priority = request.POST.get('priority')

        staff_mem = StaffUser.objects.get(id=assigned_to)
        if planned_start_date != '':
            task_obj.planned_start_date = datetime.strptime(planned_start_date, "%Y-%m-%dT%H:%M")
        if planned_end_date != '':
            task_obj.planned_end_date = datetime.strptime(planned_end_date, "%Y-%m-%dT%H:%M")
        if actual_start_date != '':
            task_obj.actual_start_date = datetime.strptime(actual_start_date, "%Y-%m-%dT%H:%M")
        if actual_end_date != '':
            task_obj.actual_end_date = datetime.strptime(actual_end_date, "%Y-%m-%dT%H:%M")

        task_obj.priority = priority
        task_obj.description = description
        task_obj.assigned_to = staff_mem
        task_obj.save()
        
        if prev_assigned_user != staff_mem.name:
            from_mail = settings.EMAIL_HOST_USER
            to_mail = staff_mem.email
            subject = 'A new task has been added for you..'

            message = render_to_string('{0}/templates/mail_templates/task_assigned.html'.format(settings.BASE_DIR),{'name':staff_mem.name, 'workspace':task_obj.workspace.name, 'team':task_obj.workspace.team.name, 'task':task_obj.title, 'status':task_obj.get_task_status_display(), 'priority':task_obj.get_priority_display(), 'end_date':task_obj.planned_end_date})
            
            msg = EmailMultiAlternatives(subject, message, from_mail, [to_mail])
            msg.attach_alternative(message, 'text/html')
            msg.send(fail_silently=False)

        messages.success(request, 'Task update success...')
        return redirect('/' + task_obj.workspace.slug + '/' + str(task_obj.id)+'/task')
        
    employees = StaffUser.objects.filter(active_status=True, is_employee=True)
    task_comments = TaskComment.objects.filter(status=True, task=task_obj).order_by('-id')
    return render(request, 'dashboard/task_detail_update.html', {'object':task_obj, 'employees':employees, 'comments':task_comments, 'id':id})


@is_authenticated
@is_staff_at_work
def issue_detail_update_view(request, id, workspace_slug):

    issue_obj = Issue.objects.get(status=True, id=id, workspace__slug=workspace_slug)
    prev_assigned_user = issue_obj.assigned_to.name

    if request.method == 'POST':
        priority = request.POST.get('priority')
        assigned_to = request.POST.get('assigned_to')
        description = request.POST.get('description')
        actual_end_date = request.POST.get('actual_end_date')
        planned_end_date = request.POST.get('planned_end_date')
        actual_start_date = request.POST.get('actual_start_date')
        planned_start_date = request.POST.get('planned_start_date')
        staff_mem = StaffUser.objects.get(id=assigned_to)
        
        if planned_start_date != '':
            issue_obj.planned_start_date = datetime.strptime(planned_start_date, "%Y-%m-%dT%H:%M")
        if planned_end_date != '':
            issue_obj.planned_end_date = datetime.strptime(planned_end_date, "%Y-%m-%dT%H:%M")
        if actual_start_date != '':
            issue_obj.actual_start_date = datetime.strptime(actual_start_date, "%Y-%m-%dT%H:%M")
        if actual_end_date != '':
            issue_obj.actual_end_date = datetime.strptime(actual_end_date, "%Y-%m-%dT%H:%M")

        issue_obj.priority = priority
        issue_obj.description = description
        issue_obj.assigned_to = staff_mem
        issue_obj.save()

        if prev_assigned_user != staff_mem.name:
            from_mail = settings.EMAIL_HOST_USER
            to_mail = staff_mem.email
            subject = 'A new task has been added for you..'
            message = render_to_string('{0}/templates/mail_templates/issue_assigned.html'.format(settings.BASE_DIR),{'name':staff_mem.name, 'workspace':issue_obj.workspace.name, 'team':issue_obj.workspace.team.name, 'task':issue_obj.title, 'status':issue_obj.get_issue_status_display(), 'priority':issue_obj.get_priority_display(), 'end_date':issue_obj.planned_end_date})
            
            msg = EmailMultiAlternatives(subject, message, from_mail, [to_mail])
            msg.attach_alternative(message, 'text/html')
            msg.send(fail_silently=False)

        messages.success(request, 'Issue update success...')
        return redirect('/' + issue_obj.workspace.slug + '/' + str(issue_obj.id) + '/issue')

    employees = StaffUser.objects.filter(active_status=True, is_employee=True)
    issue_comments = IssueComment.objects.filter(status=True, issue=issue_obj).order_by('-id')
    return render(request, 'dashboard/issue_detail_update.html', {'object':issue_obj, 'employees':employees, 'comments':issue_comments, 'id':id})


@is_authenticated
def task_delete(request, id):

    task_obj = Task.objects.get(status=True, id=id)
    task_obj.status=False
    task_obj.save()
    return redirect('/')


@is_authenticated
def issue_delete(request, id):

    issue_obj = Issue.objects.get(id=id, status=True)
    issue_obj.status=False
    issue_obj.save()
    return redirect('/')