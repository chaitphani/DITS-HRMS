from dashboard.models import StaffUser
from dashboard.decorator import is_authenticated


@is_authenticated
def get_members(request):

    try:
        members = StaffUser.objects.filter(active_status=True, is_employee=True, is_admin=False)
    except:
        members = ''
    return {'members':members}