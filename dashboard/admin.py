from django.contrib import admin
from .models import *

admin.site.register(StaffUser)
admin.site.register(Team)
admin.site.register(WorkSpace)
admin.site.register(Task)
admin.site.register(Issue)
admin.site.register(TaskComment)

admin.site.register(Attendance)
admin.site.register(Leave)
