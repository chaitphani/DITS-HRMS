from django.db.models.query import InstanceCheckMeta
from django.shortcuts import render, redirect
from django.contrib import messages

from datetime import datetime

from rest_framework import RemovedInDRF313Warning

from dashboard.models import *
from dashboard.forms import *
from dashboard.serializers import *
from django.db.models import Sum, Count, F

from django.core.mail import send_mail
from django.conf import settings

from dashboard.views.workspace_views import workspace_view


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
        user_obj = StaffUser.objects.get(id=request.session.get('id'))
        employees = StaffUser.objects.filter(active_status=True, is_employee=True)
        if request.session.get('is_admin') == False:
            workspace = WorkSpace.objects.filter(status=True, staff=user_obj)
        else:
            workspace = WorkSpace.objects.filter(status=True)

        # tasks = Task.objects.filter(status=True).order_by('-id')
        # issues = Issue.objects.filter(status=True).order_by('-id')
        # tasks_in_workspace = workspace.prefetch_related('task_set', 'issue_set').filter(status=True).annotate(task_count=Count('task__id'), task_assignees=F('task__assigned_to__name'), issue_count=Count('issue__id')).values()
        # tasks_in_workspace = WorkSpace.objects.prefetch_related('issue_set').filter(status=True).annotate(task_count=Count('issue__id'))
        # .annotate(number_of_answers=Count('workspace'))

        if request.GET.get('id'):
            if request.method == "GET" and request.is_ajax():
                task_obj = Task.objects.get(id=request.GET.get('id'))
                task_obj.priority = request.GET.get('priority')
                task_obj.save()
                messages.success(request, task_obj.title + ' Priority changed successfully...')

        elif request.GET.get('iss_id'):
            if request.method == 'GET' and request.is_ajax():
                issue_obj = Issue.objects.get(id=request.GET.get('iss_id'))
                issue_obj.priority = request.GET.get('issu_priority')
                issue_obj.save()
                messages.success(request, issue_obj.title + ' Prority changed successfully...')

    except Exception as e:
        print('---exception as error------', e)
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



# @is_authenticated
# def invite_member(request):

#     if request.method == "POST":
#         mem_email = request.POST.get('email')
        # try:
        #     staff_check = StaffUser.objects.get(email = mem_email)
        #     try:
        #         team_obj = Team.objects.get(slug=request.GET.get('team'))
        #         staff_check.team = team_obj
        #         staff_check.save()
        #         messages.success(request, 'Member invite success...!') 
        #         return redirect('/')
        #     except Exception as err:
        #         print('----error in team check of invite----', err)
        #         messages.error(request, 'No team found with the name...')
        #         return redirect('team')
        # except Exception as e:
        #     print('---error in invite member----', e)
        #     messages.error(request, 'No user found with the email...')
        #     return redirect('team')
        # re


# @is_authenticated
# def task_detail_update_view(request, id):

#     task_obj = Task.objects.get(status=True, id=id)

#     if request.method == 'POST':
#         planned_start_date = request.POST.get('planned_start_date')
#         actual_start_date = request.POST.get('actual_start_date')
#         planned_end_date = request.POST.get('planned_end_date')
#         actual_end_date = request.POST.get('actual_end_date')
#         description = request.POST.get('description')
#         assigned_to = request.POST.get('assigned_to')
#         priority = request.POST.get('priority')
#         staff_mem = StaffUser.objects.get(id=assigned_to)

#         if planned_start_date != '':
#             task_obj.planned_start_date = datetime.strptime(planned_start_date, "%Y-%m-%dT%H:%M")
#         if planned_end_date != '':
#             task_obj.planned_end_date = datetime.strptime(planned_end_date, "%Y-%m-%dT%H:%M")
#         if actual_start_date != '':
#             task_obj.actual_start_date = datetime.strptime(actual_start_date, "%Y-%m-%dT%H:%M")
#         if actual_end_date != '':
#             task_obj.actual_end_date = datetime.strptime(actual_end_date, "%Y-%m-%dT%H:%M")

#         task_obj.priority = priority
#         task_obj.description = description
#         task_obj.assigned_to = staff_mem
#         task_obj.save()
#         messages.success(request, task_obj.title + ' update success...')
#         return redirect('/task/'+task_obj.id+'/edit')
        
#     employees = StaffUser.objects.filter(active_status=True, is_employee=True)
#     return render(request, 'dashboard/task_detail_update.html', {'obj':task_obj, 'employees':employees})


# @is_authenticated
# def issue_detail_update_view(request, id):

#     issue_obj = Issue.objects.get(status=True, id=id)

#     if request.method == 'POST':
#         priority = request.POST.get('priority')
#         assigned_to = request.POST.get('assigned_to')
#         description = request.POST.get('description')
#         actual_end_date = request.POST.get('actual_end_date')
#         planned_end_date = request.POST.get('planned_end_date')
#         actual_start_date = request.POST.get('actual_start_date')
#         planned_start_date = request.POST.get('planned_start_date')
#         staff_mem = StaffUser.objects.get(id=assigned_to)
        
#         if planned_start_date != '':
#             issue_obj.planned_start_date = datetime.strptime(planned_start_date, "%Y-%m-%dT%H:%M")
#         if planned_end_date != '':
#             issue_obj.planned_end_date = datetime.strptime(planned_end_date, "%Y-%m-%dT%H:%M")
#         if actual_start_date != '':
#             issue_obj.actual_start_date = datetime.strptime(actual_start_date, "%Y-%m-%dT%H:%M")
#         if actual_end_date != '':
#             issue_obj.actual_end_date = datetime.strptime(actual_end_date, "%Y-%m-%dT%H:%M")

#         issue_obj.priority = priority
#         issue_obj.description = description
#         issue_obj.assigned_to = staff_mem
#         issue_obj.save()
#         messages.success(request, issue_obj.title + ' update success...')
#         return redirect('/issue/'+str(issue_obj.id)+'/edit')

#     employees = StaffUser.objects.filter(active_status=True, is_employee=True)
#     return render(request, 'dashboard/issue_detail_update.html', {'obj':issue_obj, 'employees':employees})



# def task_view(request, id):

#     task_obj =  Task.objects.get(id=id)
#     task_info = {}
#     try:
#         task_info['id'] = task_obj.id
#         task_info["title"] = task_obj.title
#         task_info["planned_start_date"] = task_obj.planned_start_date
#         task_info["planned_end_date"] = task_obj.planned_end_date
#         task_info["actual_start_date"] = task_obj.actual_start_date
#         task_info["actual_end_date"] = task_obj.actual_end_date
#         task_info["priority"] = task_obj.priority
#         task_info["description"] = task_obj.description
#         task_info["task_status"] = task_obj.task_status
#         task_info["created_on"] = task_obj.created_on
#     except Exception as e:
#         print('---exception error in product info api---', e)
#         messages.error(request, 'data is missing for the product..')
#     return JsonResponse({'task_info': task_info})

