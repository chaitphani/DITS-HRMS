import datetime
from django.db import models
from django.db.models.base import Model, ModelStateFieldsCacheDescriptor
from django.contrib.auth.models import User

priority_choices = (('1', 'High'),('2', 'Medium'),('3', 'Low'), ('4', 'Critical'), )
task_status_choices = (('1', 'Not Started'),('2', 'In Progress'),('3', 'In Review'),('4', 'Completed'),('5', 'Blocked'),)
issue_type = (('1','Bug'), ('2', 'Feature'), ('3', 'Improvement'))


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
    leaves_provided = models.CharField(max_length=2, default='24')

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

    task_id = models.CharField(max_length=10, null=True, blank=True)
    title = models.CharField(max_length=120)
    assigned_to = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='task_assigned_to')
    priority = models.CharField(max_length=10, choices=priority_choices, default='2')
    task_status = models.CharField(max_length=15, choices=task_status_choices, default='2')
    description = models.TextField(null=True, blank=True)

    planned_start_date = models.DateTimeField(null=True, blank=True)
    planned_end_date = models.DateTimeField(null=True, blank=True)

    actual_start_date = models.DateTimeField(null=True, blank=True)
    actual_end_date = models.DateTimeField(null=True, blank=True)

    workspace = models.ForeignKey(WorkSpace, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_by = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='task_assigned_by')

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.title)


class Issue(models.Model):

    issue_id = models.CharField(max_length=10, null=True, blank=True)
    title = models.CharField(max_length=120)
    assigned_to = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='issue_assigned_to')
    issue_type = models.CharField(max_length=20, choices=issue_type, default='1')
    priority = models.CharField(max_length=10, choices=priority_choices, default='2')
    issue_status = models.CharField(max_length=15, choices=task_status_choices, default='2')
    description = models.TextField(null=True, blank=True)

    planned_start_date = models.DateTimeField(null=True, blank=True)
    planned_end_date = models.DateTimeField(null=True, blank=True)

    actual_start_date = models.DateTimeField(null=True, blank=True)
    actual_end_date = models.DateTimeField(null=True, blank=True)
    assigned_by = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='issue_assigned_by')

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


# attendance related models.
class Attendance(models.Model):

    # type_choices = (('from-office', 'from-office'), ('from-home', 'from-home'))
    # shift_type = (('general', 'general'), ('night', 'night'))

    staff_user = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True)
    # type = models.CharField(max_length=20, choices=type_choices, default='from-office')
    # shift = models.CharField(max_length=15, choices=shift_type, default='general')
    in_time = models.DateTimeField(null=True, blank=True)
    out_time = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.staff_user.name)

    class Meta: 
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance"


class Leave(models.Model):

    type_choices = (('sick', 'sick'), ('casual', 'casual') ,('other', 'other'), ('compensatory', 'compensatory'))
    status_choices = (('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'))

    user = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=12, choices=type_choices, default='casual')
    from_date = models.DateField()
    to_date = models.DateField()
    number_of_days = models.IntegerField()
    descritpion = models.TextField()
    leave_status = models.CharField(max_length=10, choices=status_choices, default='Pending')
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.user.name)


class Holidays(models.Model):
    
    name = models.CharField(max_length=120)
    day = models.CharField(max_length=2)
    month = models.CharField(max_length=5)
    status = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}'.format(self.name)

    class Meta: 
        verbose_name = "Holiday"
        verbose_name_plural = "Holidays"

class Notification(models.Model):

    staff_mem = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=120)
    content = models.CharField(max_length=550, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
