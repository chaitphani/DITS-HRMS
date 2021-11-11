from django.shortcuts import render
from dashboard.models import *
import datetime


def home(request):

    today = datetime.datetime.now()
    user_obj = StaffUser.objects.get(id=request.session.get('id'))
    att_obj = Attendance.objects.filter(staff_user=user_obj, status=True)

    today_in_obj = att_obj.filter(in_time__day=today.day, in_time__month=today.month, in_time__year=today.year)

    if len(today_in_obj)>0:
        in_current_day = today_in_obj.first()
    else:
        in_current_day = 'none'

    today_out_obj = att_obj.filter(out_time__day=today.day, out_time__month=today.month, out_time__year=today.year)

    if len(today_out_obj)>0:
        out_current_day = today_out_obj.first()
    else:
        out_current_day = 'none'
        
    if not user_obj.is_admin == True:
        leaves = Leave.objects.filter(user=user_obj, status=True)
    else:
        leaves = Leave.objects.filter(status=True)

    return render(request,'attendance/home.html', {'obj':att_obj, 'in_current_day':in_current_day, 'out_current_day':out_current_day, 'leaves':leaves})
