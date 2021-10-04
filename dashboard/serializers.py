from rest_framework import serializers
from .models import *


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['title', 'workspace', 'assigned_to', 'priority', 'task_status', 'description', 'planned_start_date', 'planned_end_date']


class WorkSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpace
        fields = ['name']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'description']


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUser
        fields = ['user_id', 'name', 'email', 'password', 'team']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['title', 'workspace', 'assigned_to', 'priority', 'issue_status', 'description', 'planned_start_date', 'planned_end_date']