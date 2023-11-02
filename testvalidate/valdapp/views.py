from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import re
# Create your views here.


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('meetings')
    else:
        login_errors={}
        old_data = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username =="":
                login_errors['username'] = 'Please Enter Username or Email'
            if password =="":
                login_errors['password'] = 'Please Enter Password'
            old_data={'username':username}
            if username !='' and '@' in username:
                usermodal = User.objects.filter(email=username)
                print("usermodal is = ",usermodal[0])
                username = usermodal[0]          
            if login_errors =={}:
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request,user)
                    messages.info(request,'Logged in Succesfully')
                    return redirect('meetings')
                else:
                    messages.warning(request,'Invalid Credentials')
                
        context={'login_errors':login_errors,'old_data':old_data}
        return render(request,'reg&log/login.html',context)


def registerpage(request):
    if request.user.is_authenticated:
        return redirect('loginpage')
    else:
        registor_errors = {}
        old_data = {}
        if request.method == 'POST':
            global usernameofuser
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirmpassword = request.POST.get('confirmpassword')
                           
            if username =="":
                registor_errors['username'] = 'Please enter a username.'
                
            elif username != "":
                username_valid = User.objects.filter(username=username)
                if username_valid:
                    registor_errors['username'] = 'This Username is already taken'
                      
            if email =="":
                registor_errors['email'] = 'Please Enter the Email'
            elif email!="":
                regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                if(re.fullmatch(regex, email)):
                    email_valid = User.objects.filter(email=email)
                    if email_valid:
                        registor_errors['email'] = 'This Email is already taken'
                else:
                    registor_errors['email'] = 'Please enter a valid Email adddress!'
                        
            if password =="":
                registor_errors['password'] = 'Please enter your password!'
            if confirmpassword =="":
                registor_errors['confirmpassword'] = 'Please enter your confirm password!'
            if password !='' and confirmpassword !='':
                if password != confirmpassword:
                    registor_errors['password'] = 'Password miss match'

            old_data = {'username':username,'email':email}
            if registor_errors == {}:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                messages.info(request,'User Created Successfully')
                return redirect('loginpage')
            
        context = {'registor_errors':registor_errors,'old_data':old_data}
        return render(request,'reg&log/register.html',context)

def logoutpage(request):
    logout(request)
    messages.info(request,'User Logged Out Successfully')
    return redirect('loginpage')




def meetings(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            meetings = Meeting.objects.all()
        else:
            try:
                memmeets = Meeting_Members.objects.filter(user_id=request.user.id)
                print("sdrhdrh - dxrjj", memmeets)
            except Meeting_Members.DoesNotExist:
                memmeets = []       
            meetings = []
            for memmeet in memmeets:
                meeting = Meeting.objects.filter(id=memmeet.meeting_id.id).first()
                if meeting:
                    meetings.append(meeting)       
        print(meetings,"ESRHSERHERTHRHYH")
        context = {"meetings": meetings}
        return render(request, 'pages/meeting.html', context)
    else:
        return redirect('loginpage')
    
    
def addMeeting(request):
    if request.user.is_authenticated:
        userdetail = User.objects.all()
        meeting_errors={}
        if request.method =="POST":
            title = request.POST.get('title')
            description = request.POST.get('description')
            dateandtime = request.POST.get('date')
            members = request.POST.getlist('members[]')
            datehere = dateandtime[0:10]
            timehere = dateandtime[-5:]+":00"
            valofdattime = datehere+" "+timehere            
            if title == "" or title == None:
                meeting_errors['title'] = 'Please enter the title'
                print(meeting_errors)            
            if description == "" or description == None:
                meeting_errors['description'] = 'Please enter something in the description'
            
            if dateandtime == "" or dateandtime == None:
                meeting_errors['dateandtime'] = 'Please enter the date and time'
            
            if members == [] or members == None:
                meeting_errors['members'] = 'Please atleast choose one member'  
            
            if title:
                meeting = Meeting(
                    title = title,
                    discription = description,
                    dateandtime = valofdattime
                )
                meeting.save()
                memdata = Meeting.objects.filter().last()
                for mem in members:
                    dataofuser = User.objects.get(username=mem)
                    member = Meeting_Members(
                        user_id = dataofuser,
                        meeting_id = memdata                          
                    )
                    member.save()
                dataofuser = User.objects.get(username=request.user.username)    
                usermember = Meeting_Members(
                    user_id = dataofuser,
                    meeting_id = memdata                          
                )
                usermember.save()
                messages.info(request,'New Metting Added Successfully')
                return redirect('meetings')
        context={"userdetail":userdetail,"meeting_errors":meeting_errors}
        return render(request,'pages/addmeeting.html',context)
    else:
        return redirect('loginpage')
    


def meetingJoined(request,pk):
    meeting = Meeting.objects.get(pk=pk)
    members = Meeting_Members.objects.filter(meeting_id=pk)
    context ={"meeting":meeting,"members":members}
    messages.info(request,str(request.user) +' - Welcome to the meeting')
    return render(request,'pages/attendmeeting.html',context)   
   


     
    


