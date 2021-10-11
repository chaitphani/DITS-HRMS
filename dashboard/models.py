from django.db import models
from django.db.models.base import ModelStateFieldsCacheDescriptor
from django.contrib.auth.models import User

import re

priority_choices = (('1', 'High'),('2', 'Medium'),('3', 'Low'), ('4', 'Critical'), )
task_status_choices = (('1', 'Not Started'),('2', 'In Progress'),('3', 'In Review'),('4', 'Completed'),('5', 'Cancelled'),)
issue_type = (('1','Bug'), ('2', 'Feature'), ('3', 'Improvement'))


class Team(models.Model):

    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    
    description = models.CharField(max_length=50, null=True,blank=True)

    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.name)


class StaffUser(models.Model):

    user_id = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    active_status = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.name)


class WorkSpace(models.Model):

    name = models.CharField(max_length=120)
    slug = models.CharField(max_length=120)

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    staff = models.ManyToManyField(StaffUser)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.name)

    # def save(self, *args, **kwargs):
    #     self.slug = self.name.lower()
    #     self.slug = re.sub("[$₹%\‘@’+;()/:&!?.'|*^–,`~#]", "", self.slug).replace(" ", "-")
    #     super(WorkSpace, self).save(*args, *kwargs)


class Task(models.Model):

    title = models.CharField(max_length=120)
    assigned_to = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=1, choices=priority_choices, default='2')
    task_status = models.CharField(max_length=1, choices=task_status_choices, default='2')
    description = models.TextField(null=True, blank=True)

    planned_start_date = models.DateTimeField(null=True, blank=True)
    planned_end_date = models.DateTimeField(null=True, blank=True)

    actual_start_date = models.DateTimeField(null=True, blank=True)
    actual_end_date = models.DateTimeField(null=True, blank=True)

    workspace = models.ForeignKey(WorkSpace, on_delete=models.SET_NULL, null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.title)


class Issue(models.Model):

    title = models.CharField(max_length=120)
    assigned_to = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True)
    issue_type = models.CharField(max_length=1, choices=issue_type, default='1')
    priority = models.CharField(max_length=1, choices=priority_choices, default='2')
    issue_status = models.CharField(max_length=1, choices=task_status_choices, default='2')
    description = models.TextField(null=True, blank=True)

    planned_start_date = models.DateTimeField(null=True, blank=True)
    planned_end_date = models.DateTimeField(null=True, blank=True)

    actual_start_date = models.DateTimeField(null=True, blank=True)
    actual_end_date = models.DateTimeField(null=True, blank=True)

    workspace = models.ForeignKey(WorkSpace, on_delete=models.SET_NULL, null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.title)


class TaskComment(models.Model):

    user = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}-{}'.format(self.user, self.task)