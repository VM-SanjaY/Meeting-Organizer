from django.urls import path
from . import views
from . import apiviews

urlpatterns = [
    path('loginpage/',views.loginpage,name="loginpage"),
    path('registerpage/',views.registerpage,name="registerpage"),
    path('logoutpage/',views.logoutpage,name="logoutpage"),
    path('',views.meetings,name="meetings"),
    path('add-meeting',views.addMeeting,name="addmeeting"),
    path('gettoken/',apiviews.get_your_token_here),
    path('api-meetings/',apiviews.requesttoJoin),
    path('api-meetings/<str:pk>/',apiviews.joinmeeting),
    path('meetingJoined/<str:pk>/',views.meetingJoined,name="joined")
]
