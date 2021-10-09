from dashboard.models import StaffUser, Team


def get_members(request):

    try:
        members = StaffUser.objects.filter(active_status=True, is_employee=True, is_admin=False)
        teams = Team.objects.filter(status=True)
        user_obj = StaffUser.objects.get(id=request.session.get('id'))
    except:
        members = ''
        teams = ''
        user_obj= ''
    return {'obj': user_obj, 'members':members, 'teams':teams}