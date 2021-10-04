from dashboard.models import *
from django.contrib import messages
from django.http.response import HttpResponse


def tasK_status_change(request):

    if request.method == "GET" and request.is_ajax():
        task_obj = Task.objects.get(id=request.GET.get('id'),)
        task_obj.task_status = request.GET.get('task_status',)
        task_obj.save()
        messages.success(request, task_obj.title + ' task-status change success...')
    return HttpResponse('success')


def issue_status_change(request):

    if request.method == "GET" and request.is_ajax():
        task_obj = Task.objects.get(id=request.GET.get('id'),)
        task_obj.task_status = request.GET.get('issue_status',)
        task_obj.save()
        messages.success(request, task_obj.title + ' issue-status change success...')
    return HttpResponse('success')