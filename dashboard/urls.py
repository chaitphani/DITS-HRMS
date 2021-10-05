from django.urls import path
from dashboard.views import dashboard_views as dash_views
from dashboard.views import api_views
from dashboard import helpers as helper_views
from dashboard.views import auth_views


urlpatterns = (

    path('', dash_views.home, name='home'),

    path('login', auth_views.login, name='login'),
    path('signup', auth_views.signup, name='signup'),
    path('logout', auth_views.logout, name='logout'),

    path('task-status', helper_views.tasK_status_change, name='task-status'),
    path('issue-status', helper_views.issue_status_change, name='issue-status'),

    path('task/<int:id>/edit', dash_views.task_detail_update_view, name='task-edit'),
    path('issue/<int:id>/edit', dash_views.issue_detail_update_view, name='issue-edit'),

    path('api/team', api_views.TeamView.as_view(), name='team-add'),
    path('api/task', api_views.TaskView.as_view(), name='task-add'),
    path('api/issue', api_views.IssueView.as_view(), name='issue-add'),
    path('api/work-space', api_views.WorkSpaceView.as_view(), name='work-space-add'),

    # path('staff', StaffView.as_view(), name='signup'),
)