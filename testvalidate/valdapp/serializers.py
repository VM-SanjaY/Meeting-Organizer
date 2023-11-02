from rest_framework import serializers
from .models import *



class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'title','discription','dateandtime']

class MeetingMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting_Members
        fields = ['id', 'user_id', 'meeting_id', 'meeting_status']
        depth = 1
        
        
class JoinedSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Meeting
        fields = ['id', 'title','discription']