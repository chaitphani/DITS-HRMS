from dashboard.models import StaffUser, Team, WorkSpace


def get_members(request):

    try:
        members = StaffUser.objects.filter(active_status=True, is_employee=True, is_admin=False)
        all_staff = StaffUser.objects.filter(active_status=True, is_employee=True)
        teams = Team.objects.filter(status=True)
        user_obj = StaffUser.objects.get(id=request.session.get('id'))
        workspaces = WorkSpace.objects.filter(status=True)
        # member_in_workspace = WorkSpace.objects.filter(status=True, )
    except:
        members = ''
        teams = ''
        user_obj= ''
        workspaces = ''
        all_staff = ''
    return {'obj': user_obj, 'members':members, 'teams':teams, 'all_staff':all_staff, 'workspaces':workspaces}