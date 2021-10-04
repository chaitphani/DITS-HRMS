from django.shortcuts import render, redirect
from django.contrib import messages

from datetime import datetime

from dashboard.models import *
from dashboard.forms import *
from dashboard.serializers import *
from django.db.models import Sum, Count


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
    wrap.__name__ = f.__name__
    return wrap


@is_authenticated
def home(request):
    
    try:
        user_obj = StaffUser.objects.get(id=request.session.get('id'))
        employees = StaffUser.objects.filter(active_status=True, is_employee=True)
        tasks = Task.objects.filter(status=True).order_by('-id')
        workspace = WorkSpace.objects.filter(status=True)
        issues = Issue.objects.filter(status=True).order_by('-id')
    
        tasks_in_workspace = Task.objects.filter(status=True)
        # .annotate(number_of_answers=Count('workspace'))

        if request.GET.get('id'):
            if request.method == "GET" and request.is_ajax():
                task_obj = Task.objects.get(id=request.GET.get('id'))
                task_obj.priority = request.GET.get('priority')
                task_obj.save()
                messages.success(request, task_obj.title + ' priority change success...')
                
        elif request.GET.get('iss_id'):
            if request.method == 'GET' and request.is_ajax():
                issue_obj = Issue.objects.get(id=request.GET.get('iss_id'))
                issue_obj.priority = request.GET.get('issu_priority')
                issue_obj.save()
                messages.success(request, issue_obj.title + ' prority change success...')

    except Exception as e:
        # print('---exception as error------', e)
        user_obj = ''
        employees = ''
        tasks = ''
        workspace = ''
        issues = ''
    return render(request,'dashboard/home.html', {
                        'obj': user_obj, 'employees':employees, 'tasks':tasks, 'workspace': workspace, 
                        'len_work':len(workspace), 'issues':issues
    })


@is_authenticated
def task_detail_update_view(request, id):

    task_obj = Task.objects.get(status=True, id=id)

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
        messages.success(request, task_obj.title + ' update success...')
        return redirect('/task/'+task_obj.id+'/edit')
        
    employees = StaffUser.objects.filter(active_status=True, is_employee=True)
    return render(request, 'dashboard/task_detail_update.html', {'obj':task_obj, 'employees':employees})


@is_authenticated
def issue_detail_update_view(request, id):

    issue_obj = Issue.objects.get(status=True, id=id)

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
        messages.success(request, issue_obj.title + ' update success...')
        return redirect('/issue/'+str(issue_obj.id)+'/edit')

    employees = StaffUser.objects.filter(active_status=True, is_employee=True)
    return render(request, 'dashboard/issue_detail_update.html', {'obj':issue_obj, 'employees':employees})



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
