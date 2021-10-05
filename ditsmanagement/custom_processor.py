from dashboard.models import StaffUser


def get_members(request):

    try:
        members = StaffUser.objects.filter(active_status=True, is_employee=True, is_admin=False)
    except:
        members = ''
    return {'members':members}