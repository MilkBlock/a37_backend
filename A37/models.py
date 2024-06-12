# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import uuid,datetime
class Usr(models.Model):
    uid = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,unique=True,verbose_name="UUID")
    iswx = models.BooleanField(default=False,blank=False,verbose_name="是否使用微信登陆")
    wxid = models.CharField(max_length=200, null=True,verbose_name="微信ID")
    iszfb = models.BooleanField(default=False,blank=False,verbose_name="是否使用支付宝登陆")
    zfbid = models.CharField(max_length=200, null=True)
    uname = models.CharField(max_length=200,default=uuid.uuid4)
    uphone = models.CharField(max_length=30, blank=False)
    ubirth = models.DateField(blank=False)
    password = models.CharField(max_length=45,blank=False)
    upic = models.CharField(max_length=500,default="static/a37/avatar_images/default.png",blank=True,null=True)
    ucreate = models.DateTimeField(default=datetime.datetime.now,editable=False)

class Ins(models.Model):
    usr = models.ForeignKey("Usr",on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True,verbose_name="自增id",editable=False,blank=True)
    bname = models.CharField(max_length=500,blank=False)
    ispic = models.BooleanField(default=False,blank=False)
    bpic = models.CharField(max_length=500, default=None,blank=True, null=True)
    bcategory = models.CharField(max_length=500)
    note = models.CharField(max_length=500, blank=True, null=True)
    payment = models.CharField(max_length=500)
    amount = models.FloatField(blank=False)
    btime = models.DateTimeField(blank=False,null=False)
    isreceipt = models.BooleanField(blank=True,default=False)
    receipt = models.CharField(max_length=300, blank=True, null=True,db_index=True)

class Outs(models.Model):
    usr = models.ForeignKey("Usr",on_delete=models.CASCADE,blank=False)
    id = models.AutoField(primary_key=True,verbose_name="自增id",editable=False,blank=True)
    bname = models.CharField(max_length=500,default="defaut-user-name",blank=True)
    ispic = models.BooleanField(default=False,blank=False)
    bpic = models.CharField(max_length=500, default=None,blank=True, null=True)
    isfinish = models.BooleanField(default=True,blank=False)
    isremind = models.BooleanField(default=False,blank=False)
    rtime = models.DateTimeField(blank=True, null=True)
    bcategory = models.CharField(max_length=500)
    note = models.CharField(max_length=500, blank=True, null=True)
    payment = models.CharField(max_length=500)
    amount = models.FloatField(blank=False)
    btime = models.DateTimeField()
    isreceipt = models.BooleanField(blank=False,default=False)
    receipt = models.CharField(max_length=500, blank=True, null=True)


class Room(models.Model):
    room_num =  models.IntegerField(primary_key=True)
    context =  models.CharField(max_length=500,blank=False)
    pwd = models.CharField(max_length = 500, blank=False,default="123456" )

class Info(models.Model):
    id = models.AutoField(primary_key=True)
    comment =  models.CharField(max_length=500)
    btime =  models.DateField(blank=False)
    amount = models.FloatField(blank=False)
    room = models.ForeignKey("Room",blank=False,on_delete=models.CASCADE)

class Own(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey("Room",blank=False,on_delete=models.CASCADE)
    usr = models.ForeignKey("Usr",on_delete=models.CASCADE)
    # role = models.CharField(max_length=500,blank=False)





