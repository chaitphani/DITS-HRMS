from django.shortcuts import render

from attendance.models import Holiday
from .models import *
# Create your views here.
def home(request):
    holiday = Holiday.objects.all()
    return render(request,'attendance/home.html',{'holiday':holiday})
