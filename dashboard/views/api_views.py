from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from dashboard.models import *
from dashboard.serializers import *
from dashboard.views.dashboard_views import is_authenticated

# from django.core.mail import send_mail
from django.conf import settings
import re
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import datetime


class TaskView(APIView):

    serializer_class = TaskSerializer

    @method_decorator(is_authenticated)
    def post(self, request):
        logged_in_mem = StaffUser.objects.get(id=request.session.get('id'))
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if len(WorkSpace.objects.filter(status=True)) > 0:
                serialize = serializer.save()
                serialize.task_id = 'DIVT1-' + str(serialize.id)
                serialize.assigned_by = logged_in_mem
                serialize.save()
                if serializer.data['assigned_to'] != '' or serializer.data['assigned_to'] != None\
                        and serializer.data['priority'] != '' or serializer.data['priority'] != None:
                    staff_mem = StaffUser.objects.get(id=serializer.data['assigned_to'])
                    workspace_obj = WorkSpace.objects.get(id=serializer.data.get('workspace'))
                    task_new_obj = Task.objects.get(id=serializer.data.get('id'))
                    end_date = serializer.data.get('planned_end_date').split('T')[0]

                    from_mail = settings.EMAIL_HOST_USER
                    to_email = staff_mem.email
                    subject = 'A new task has been added for you..'

                    # body = "New task assigned :: details as below: \n\n"\
                    #         "Task: {} ".format(serializer.data['title'])+'\n'+\
                    #         "Description: {} ".format(serializer.data['description'])+'\n'+\
                    #         "Priority level: {} ".format(serializer.data['priority'])
                    # send_mail('A New Task has been added to your dashboard...',body,from_mail,[to_email],fail_silently=False,)

                    message = render_to_string('{0}/templates/mail_templates/task_assigned.html'.format(settings.BASE_DIR),{'name':staff_mem.name, 'workspace':workspace_obj.name, 'team':workspace_obj.team.name, 'task':task_new_obj.title, 'status':task_new_obj.get_task_status_display(), 'priority':task_new_obj.get_priority_display(), 'end_date':end_date, 'url':settings.BASE_DOMAIN + '/' + workspace_obj.slug + '/' + str(task_new_obj.id) + '/task'})
                    
                    msg = EmailMultiAlternatives(subject, message, from_mail, [to_email])

                    msg.attach_alternative(message, 'text/html')
                    msg.send(fail_silently=False)
                messages.success(request, 'Task add success...!')
                return redirect('/' + workspace_obj.slug) 
            else:
                messages.error(request, 'No workspace to assign task...!')
                return redirect('home')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkSpaceView(APIView):

    serializer_class = WorkSpaceSerializer

    @method_decorator(is_authenticated)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serialize = serializer.save()
            slug_name = serialize.name.lower()
            serialize.slug = re.sub("[$₹%\‘@’+;()/:&!?.'|*^–,`~#]", "", slug_name).replace(" ", "-")
            serialize.save()

            slug = serializer.data.get('slug')
            workspace_mem_list_email = []
            for mem in serializer.data.get('staff'):
                staff_mem = StaffUser.objects.get(id=mem)
                workspace_mem_list_email.append(staff_mem.email)

            from_mail = settings.EMAIL_HOST_USER
            subject = "You've been invited to the new Workspace..."
            message = render_to_string('{0}/templates/mail_templates/join_team_invitation.html'.format(settings.BASE_DIR),{'url':settings.BASE_DOMAIN + '/' + slug})
            msg = EmailMultiAlternatives(subject, message, from_mail, workspace_mem_list_email)
            msg.attach_alternative(message, 'text/html')
            msg.send(fail_silently=False)

            messages.success(request, 'Work space add success...')
            return redirect('home')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamView(APIView):

    serializer_class = TeamSerializer

    @method_decorator(is_authenticated)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serialize = serializer.save()
            slug_name = serialize.name.lower()
            serialize.slug = re.sub("[$₹%\‘@’+;()/:&!?.'|*^–,`~#]", "", slug_name).replace(" ", "-")
            serialize.save()

            messages.success(request, 'Team add success...')
            return redirect('home')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueView(APIView):

    serializer_class = IssueSerializer

    @method_decorator(is_authenticated)
    def post(self, request):
        logged_in = StaffUser.objects.get(id=request.session.get('id'))
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if len(WorkSpace.objects.filter(status=True)) > 0:
                serialize = serializer.save()
                serialize.issue_id = 'DIVI-1' + str(serialize.id)
                serialize.assigned_by = logged_in
                serialize.save()
                if serializer.data['assigned_to'] != '' or serializer.data['assigned_to'] != None\
                        and serializer.data['priority'] != '' or serializer.data['priority'] != None:
                    staff_mem = StaffUser.objects.get(id=serializer.data['assigned_to'])
                    workspace_obj = WorkSpace.objects.get(id=serializer.data.get('workspace'))
                    issue_new_obj = Issue.objects.get(id=serializer.data.get('id'))

                    end_date = serializer.data.get('planned_end_date').split('T')[0]

                    from_mail = settings.EMAIL_HOST_USER
                    to_email = staff_mem.email
                    subject = 'A new issue raised for you...'

                    # body = "New Issue raised for you :: details as below: \n\n"\
                    #         "Task: {} ".format(serializer.data['title'])+'\n'+\
                    #         "Description: {} ".format(serializer.data['description'])+'\n'+\
                    #         "Priority level: {} ".format(serializer.data['priority'])
                    # send_mail('A New issue has been added to your dashboard...',body,from_mail,[to_email], fail_silently=False,)       
                    
                    message = render_to_string('{0}/templates/mail_templates/issue_assigned.html'.format(settings.BASE_DIR),{'name':staff_mem.name, 'workspace':workspace_obj.name, 'team':workspace_obj.team.name, 'task':issue_new_obj.title, 'status':issue_new_obj.get_issue_status_display(), 'priority':issue_new_obj.get_priority_display(), 'end_date':end_date, 'url':settings.BASE_DOMAIN + '/' + workspace_obj.slug + '/' + str(issue_new_obj.id) + '/issue'})
                    msg = EmailMultiAlternatives(subject, message, from_mail, [to_email])

                    msg.attach_alternative(message, 'text/html')
                    msg.send(fail_silently=False)
                messages.success(request, 'Issue add success...')
                return redirect('/' + workspace_obj.slug)
            else:
                messages.error(request, 'No workspace to assign issue...!')
                return redirect('home')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskCommentView(APIView):

    def post(self, request, task_id):
        try:
            task_obj = Task.objects.get(id=task_id)
            user_obj = StaffUser.objects.get(id=request.session.get('id'))

            comment_obj = TaskComment.objects.create(user=user_obj, task=task_obj, comment=request.data.get('comment'), status=True)
            comment_obj.save()
            return redirect('/' + task_obj.workspace.slug + '/' + str(task_obj.id)+'/task')
        except Exception as e:
            # print('----error as e----', e)
            return Response({'error':'Task obj not found with the id..'}, status=status.HTTP_404_NOT_FOUND)


class IssueCommentView(APIView):

    def post(self, request, issue_id):
        try:
            issue_obj = Issue.objects.get(id=issue_id)
            user_obj = StaffUser.objects.get(id=request.session.get('id'))
            
            comment_obj = IssueComment.objects.create(user=user_obj, issue=issue_obj, comment=request.data.get('comment'), status=True)
            comment_obj.save()
            return redirect('/' + issue_obj.workspace.slug + '/' + str(issue_obj.id) + '/issue')
        except Exception as e:
            return Response({'error':'Issue obj not found with the id..'}, status=status.HTTP_404_NOT_FOUND)


class AttendanceInView(APIView):

    serializer_class = AttendaceInSerializer

    def post(self, request):

        user_obj = StaffUser.objects.get(id=request.session.get('id'))
        Attendance.objects.create(staff_user=user_obj, in_time=request.data.get('in_time'), status=True)
        return redirect('/attendance/')


class AttendaceOutView(APIView):

    serializer_class = AttendaceOutSerializer

    def put(self, request):
        user_obj = StaffUser.objects.get(id=request.session.get('id'))
        today_date = datetime.date.today()

        attendace_obj = Attendance.objects.filter(staff_user=user_obj, in_time__day=today_date.day, in_time__month=today_date.month, in_time__year=today_date.year, status=True)

        if len(attendace_obj) > 0:
            # if request.data.get('out_time') == today_date:
            att_obj = attendace_obj.first()
            att_obj.out_time = request.data.get('out_time')
            att_obj.save()
            # else:
            #     messages.error(request, 'check-out date should match with the check-in date..')
        else:
            messages.error(request, "You haven't check-in to provide check-out..\nPlease contact manager..")

        return redirect('/attendance/')


class LeaveView(APIView):

    serializer_class = LeaveSerializer

    def post(self, request):
        user_obj = StaffUser.objects.get(id=request.session.get('id'))
        Leave.objects.create(user=user_obj, type=request.data.get('type'), from_date=request.data.get('from_date'), to_date=request.data.get('to_date'), descritpion=request.data.get('descritpion'), status=True, leave_status='Pending')

        messages.success(request, 'Leave applied success...')
        return redirect('/attendance/')


class HolidayView(APIView):

    serializers_class = HolidaysSerializer
    def post(self, request):
        Holidays.objects.create(name=request.data.get('name'), day=request.data.get('day'), month=request.data.get('month'), status=True, description=request.data.get('description'))

        messages.success(request, 'Holiday create success...')
        return redirect('/attendance/')
        

# class LoginView(APIView):

#     def post(self, request):

#         email_input = request.data.get('email_temp')
#         pwd = request.data.get('pass_temp')

#         try:
#             login_obj = StaffUser.objects.get(name=email_input).email
#         except:
#             login_obj = StaffUser.objects.get(email=email_input).email

#         if login_obj:
#             try:
#                 login_check = StaffUser.objects.get(email=login_obj, password=pwd)
#                 if login_check:
#                     request.session['id'] = login_check.id
#                     request.session['user_name'] = login_check.name
#                     messages.success(request, 'Login Success...!')
#                     return redirect('home')                    
#             except Exception as e:
#                 print('-exception as error in login---', e)
#                 messages.error(request, 'Invalid Password..!')
#         else:
#             messages.error(request, 'Please check email or user-name...!')
#         return Response({'msg':'error'}, status=status.HTTP_400_BAD_REQUEST)    



# class StaffView(APIView):

#     serializer_class = StaffUserSerializer

#     def post(self, request):

#         user = ''
#         try:
#             user = User.objects.create_user(username=request.data['name'], email=request.data['email'])
#         except Exception as e:
#             print('------error in exception---', e)
#             messages.error(request, 'Provided user already exists...')

#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serialize = serializer.save()
#             serialize.user_id = user
#             serialize.save()

#             from_mail = settings.EMAIL_HOST_USER
#             to_email = serializer.data['email']
#             body = "DITS staff acccount has been created: \n\n"\
#                     "User Name : {} ".format(serializer.data['name'])+'\n'+\
#                     "Email: {} ".format(serializer.data['email'])+'\n'+\
#                     "Password: {} ".format(serializer.data['password'])

#             send_mail(
#                 'Welcome to DITS Task Management App',
#                 body,
#                 from_mail,
#                 [to_email],
#                 fail_silently=False,
#             )

#             messages.success(request, 'Member ' + serializer.data['name'] + ' add success...!')
#             return redirect('login')
#         return Response({'msg':'error'}, status=status.HTTP_400_BAD_REQUEST)

