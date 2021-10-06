from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from dashboard.models import *
from dashboard.serializers import *
from dashboard.views.dashboard_views import is_authenticated

from django.core.mail import send_mail
from django.conf import settings


class TaskView(APIView):

    serializer_class = TaskSerializer

    @method_decorator(is_authenticated)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if len(WorkSpace.objects.filter(status=True)) > 0:
                serializer.save()
                if serializer.data['assigned_to'] != '' or serializer.data['assigned_to'] != None\
                        and serializer.data['priority'] != '' or serializer.data['priority'] != None:
                    staff_mem = StaffUser.objects.get(id=serializer.data['assigned_to'])

                    from_mail = settings.EMAIL_HOST_USER
                    to_email = staff_mem.email
                    body = "New task assigned :: details as below: \n\n"\
                            "Task: {} ".format(serializer.data['title'])+'\n'+\
                            "Description: {} ".format(serializer.data['description'])+'\n'+\
                            "Priority level: {} ".format(serializer.data['priority'])

                    send_mail(
                        'A New Task has been added to your dashboard...',
                        body,
                        from_mail,
                        [to_email],
                        fail_silently=False,
                    )
                messages.success(request, 'Task add success...!')
                return redirect('home') 
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
            messages.success(request, 'Work space add success...')
            return redirect('home')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamView(APIView):

    serializer_class = TeamSerializer

    @method_decorator(is_authenticated)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Team add success...')
            return redirect('home')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueView(APIView):

    serializer_class = IssueSerializer

    @method_decorator(is_authenticated)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if len(WorkSpace.objects.filter(status=True)) > 0:
                serializer.save()
                if serializer.data['assigned_to'] != '' or serializer.data['assigned_to'] != None\
                        and serializer.data['priority'] != '' or serializer.data['priority'] != None:
                    staff_mem = StaffUser.objects.get(id=serializer.data['assigned_to'])
                    from_mail = settings.EMAIL_HOST_USER
                    to_email = staff_mem.email
                    body = "New task assigned :: details as below: \n\n"\
                            "Task: {} ".format(serializer.data['title'])+'\n'+\
                            "Description: {} ".format(serializer.data['description'])+'\n'+\
                            "Priority level: {} ".format(serializer.data['priority'])

                    send_mail(
                        'A New Task has been added to your dashboard...',
                        body,
                        from_mail,
                        [to_email],
                        fail_silently=False,
                    )                
                messages.success(request, 'Issue add success...')
                return redirect('home')
            else:
                messages.error(request, 'No workspace to assign task...!')
                return redirect('home')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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