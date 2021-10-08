from dashboard.models import StaffUser, Team


def get_members(request):

    try:
        members = StaffUser.objects.filter(active_status=True, is_employee=True, is_admin=False)
        teams = Team.objects.filter(status=True)
    except:
        members = ''
        teams = ''
    return {'members':members, 'teams':teams}