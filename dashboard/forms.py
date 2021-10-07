from django import forms
from .models import *


class StaffUserForm(forms.ModelForm):
    class Meta:
        model = StaffUser
        fields = ['name', 'email', 'password']


class TaskUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = ['planned_start_date', 'planned_end_date', 'actual_start_date', 'actual_end_date', 'priority']