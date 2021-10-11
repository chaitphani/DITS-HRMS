from django.db import models
from django.db.models.base import ModelStateFieldsCacheDescriptor
from django.contrib.auth.models import User

import re

priority_choices = (('High', 'High'),('Medium', 'Medium'),('Low', 'Low'), ('Critical', 'Critical'), )
task_status_choices = (('Not Started', 'Not Started'),('In Progress', 'In Progress'),('In Review', 'In Review'),('Completed', 'Completed'),('Blocked', 'Blocked'),)
issue_type = (('Bug','Bug'), ('Feature', 'Feature'), ('Improvement', 'Improvement'))


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
    priority = models.CharField(max_length=10, choices=priority_choices, default='Medium')
    task_status = models.CharField(max_length=15, choices=task_status_choices, default='In Progress')
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
    issue_type = models.CharField(max_length=20, choices=issue_type, default='Bug')
    priority = models.CharField(max_length=10, choices=priority_choices, default='Medium')
    issue_status = models.CharField(max_length=15, choices=task_status_choices, default='In Progress')
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


class IssueComment(models.Model):

    user = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True)
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}-{}'.format(self.user, self.issue)