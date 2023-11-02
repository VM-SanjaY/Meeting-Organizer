from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework.response import Response
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from datetime import timedelta
from datetime import date
from django.utils import timezone
from django.db.models import Q


@api_view(['POST'])
@permission_classes([AllowAny])
def get_your_token_here(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username =="" or username == None:
        return Response({"status":True,"Message":"Please enter the Username"},status=400)
    elif username !="" or username is not None:
        isuserThere = User.objects.filter(username=username)
        if not isuserThere.exists():
            return Response({"status":True,"Message":"Username does not exist"},status=400)
    if password =="" or password == None:
        return Response({"status":True,"Message":"Please enter the password"},status=400)        
            
    user = authenticate(username=username,password=password)
    if user is not None:
        user = User.objects.get(username=username)                
        try:
            token = Token.objects.get(user_id=user.id)
            if token:
                tokencreated_time = token.created
                print(tokencreated_time)
                print(timezone.now(),"sdrdtdht")
                print(timezone.now()-tokencreated_time,"checking")
                compare = timezone.now()-tokencreated_time
                if compare > timedelta(hours = 1):
                    token.delete()
                    token = Token.objects.create(user_id=user.id)
        except Token.DoesNotExist:
            token = Token.objects.create(user_id=user.id)
            print(token.key)
    return Response({"status":True,"Token ":token.key},status=200)




@api_view(['GET'])
def requesttoJoin(request):
    print("sdrhydtj - ", request.user)
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = User.objects.get(id=user_id)
    if user.is_superuser == 1:
        meetings = Meeting.objects.all()
    else:
        try:
            memmeets = Meeting_Members.objects.filter(user_id=user.id)
            print("sdrhdrh - dxrjj", memmeets)
        except Meeting_Members.DoesNotExist:
            memmeets = []       
        meetings = []
        for memmeet in memmeets:
            meeting = Meeting.objects.filter(id=memmeet.meeting_id.id).first()
            if meeting:
                meetings.append(meeting)       
        print(meetings)
    serializer = MeetingSerializer(meetings,many=True)
    return Response({"status":True,"data":serializer.data},status=200)
    

@api_view(['GET'])
def joinmeeting(request, pk):
    try:
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        memmeets = Meeting_Members.objects.filter(user_id=user.id)
        meetings = []
        print("value of pk is", pk)
        for memmeet in memmeets:
            meeting = Meeting.objects.filter(id=memmeet.meeting_id.id).first()
            if meeting:
                meetings.append(meeting.id)
        print("all meeting list - ", type(meetings))
        idpk = int(pk)
        if idpk in meetings:
            print("yes, it is there")
            meetjoin = Meeting.objects.get(id=pk)
            print("drtjdtjf - ",meetjoin.dateandtime.date())
            meetingdate = meetjoin.dateandtime.date()
            today = date.today()
            if meetingdate == today:                
                memuser = Meeting_Members.objects.get(Q(user_id=user.id) & Q(meeting_id=pk))
                memuser.meeting_status = True
                memuser.save()
                serializer = JoinedSerializer(meetjoin, many=False)  # Use many=False for a single object
                return Response({"status": True, "data": serializer.data,"Info":"You have joined the meeting"}, status=200)
            else:
                return Response({"status": False, "data": "Please join at the given date"}, status=401)
        else:
            return Response({"status": False, "data": "Please mention the valid ID to join"}, status=401)
    except Token.DoesNotExist:
        return Response({"status": False, "data": "Invalid token"}, status=401)
    except User.DoesNotExist:
        return Response({"status": False, "data": "User does not exist"}, status=404)
    except Meeting.DoesNotExist:
        return Response({"status": False, "data": "Meeting does not exist"}, status=404)







