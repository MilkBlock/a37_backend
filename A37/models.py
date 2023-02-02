# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ins(models.Model):
    uid = models.CharField(max_length=500)
    bname = models.CharField(max_length=500)
    ispic = models.IntegerField()
    bpic = models.CharField(max_length=1000, blank=True, null=True)
    bcategory = models.CharField(max_length=500)
    note = models.CharField(max_length=1000, blank=True, null=True)
    payment = models.CharField(max_length=500)
    amount = models.IntegerField()
    btime = models.DateTimeField()
    isreceipt = models.IntegerField()
    receipt = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ins'


class Outs(models.Model):
    uid = models.CharField(max_length=500)
    bname = models.CharField(max_length=500)
    ispic = models.IntegerField()
    bpic = models.CharField(max_length=1000, blank=True, null=True)
    isfinish = models.IntegerField()
    isremind = models.IntegerField()
    rtime = models.DateTimeField(blank=True, null=True)
    bcategory = models.CharField(max_length=500)
    note = models.CharField(max_length=1000, blank=True, null=True)
    payment = models.CharField(max_length=500)
    amount = models.IntegerField()
    btime = models.DateTimeField()
    isreceipt = models.IntegerField()
    receipt = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'outs'


class Usersinfo(models.Model):
    uid = models.CharField(primary_key=True, max_length=500)
    iswx = models.IntegerField()
    wxid = models.CharField(max_length=500, blank=True, null=True)
    iszfb = models.IntegerField()
    zfbid = models.CharField(max_length=500, blank=True, null=True)
    uname = models.CharField(max_length=500)
    uphone = models.CharField(max_length=30)
    ubirth = models.DateField()
    password = models.CharField(max_length=45)
    upic = models.CharField(max_length=1000)
    ucreate = models.DateField()

    class Meta:
        managed = False
        db_table = 'usersinfo'
""""
import datetime
Usersinfo.objects.create(uid="0",password="123456"
,iswx=True,wxid="xxxx",uname="李大壮",upic="not found",iszfb=False,uphone="18357193750",
ubirth=datetime.datetime(year=1990,month=3,day=27),ucreate=datetime.datetime(year=2023,month=2,day=3))
"""
