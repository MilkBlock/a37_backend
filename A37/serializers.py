from A37.models import *
from rest_framework import serializers
#serializers.HyperlinkedModelSerializer
class OutsModelSerializer(serializers.ModelSerializer):
    btime = serializers.DateTimeField(format=r"%Y-%m-%d %H:%M:%S")
    rtime = serializers.DateTimeField(format=r"%Y-%m-%d %H:%M:%S",required=False)
    class Meta:
        model = Outs
        fields="__all__"

class InsModelSerializer(serializers.ModelSerializer):
    btime = serializers.DateTimeField(format=r"%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Ins
        fields="__all__"

class UsrModelSerializer(serializers.ModelSerializer):
    ucreate = serializers.DateTimeField(format=r"%Y-%m-%d %H:%M:%S",required=False)  
    # ucreate = str(serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S"))+"bbac"   
    # ModelSerializer里面没有资格直接对数据进行处理，只能进行一般性配置

    class Meta:
        model = Usr
        fields = "__all__"
        read_only_fields=["password"]
        # read_only_field=["uid"]
    
class OwnModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Own
        fields = "__all__"
        # read_only_field=["uid"]
    
class InfoModelSerializer(serializers.ModelSerializer):
    btime = serializers.DateField(format=r"%Y-%m-%d",required=False)  

    class Meta:
        model = Info
        fields = "__all__"
        # read_only_field=["uid"]
    
class RoomModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = "__all__"
        # read_only_field=["uid"]