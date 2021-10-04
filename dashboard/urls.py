from django.urls import path
from dashboard.views.dashboard_views import *
from dashboard.views.api_views import *
from dashboard.helpers import *
from dashboard.views.auth_views import *


urlpatterns = (

    path('', home, name='home'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),

    path('task-status', tasK_status_change, name='task-status'),
    path('issue-status', issue_status_change, name='issue-status'),

    path('task/<int:id>/edit', task_detail_update_view, name='task-edit'),
    path('issue/<int:id>/edit', issue_detail_update_view, name='issue-edit'),

    path('staff', StaffView.as_view(), name='signup'),
    path('api/team', TeamView.as_view(), name='team-add'),
    path('api/task', TaskView.as_view(), name='task-add'),
    path('api/issue', IssueView.as_view(), name='issue-add'),
    path('api/work-space', WorkSpaceView.as_view(), name='work-space-add'),

)