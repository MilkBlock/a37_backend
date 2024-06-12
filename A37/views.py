from django.shortcuts import render
# from django.views.generic import DetailView,ListView
from django.http import JsonResponse
from django.http import HttpRequest
import  django.http as http
from django.db.models.query import QuerySet
import encodings
from .models import *
# from collections import namedtuple
from rest_framework.renderers import *
from rest_framework.viewsets import ModelViewSet
import A37.serializers as A37Serializers
from functools import wraps
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import  django.core.files.storage as storage
from rest_framework.views import APIView
import sys 
import os
from Site import settings
# from A37TextCNN import tc



refresh_flag = False 



def check_request(func):
    @wraps(func)
    def wrapper(request):
        print("request:")
        print("Parm",str(request.content_params))
        print("Type",str(request.content_type))
        if request.method=="POST":
            print("POST",request.POST)
        elif request.method=="GET":
            print("GET",request.GET)
        print("replied number:", request_num)
        print("IP",request.META["REMOTE_ADDR"])
        return func(request)
    return wrapper
def check_request_log(func):
    @wraps(func)
    def wrapper(request):
        print_log("request:")
        print_log("Parm"+str(request.content_params))
        print_log("Type"+str(request.content_type))
        if request.method=="POST":
            print_log("POST"+str(request.POST))
        elif request.method=="GET":
            print_log("GET"+str(request.GET))
        print_log("replied "+str( request_num))
        print_log("IP"+str(request.META["REMOTE_ADDR"]))
        return func(request)
    return wrapper


verifycode = -1
request_num = 0
current_phone = -1



def index_view(request):
    return render(request,"index.html")

# show all the records
@check_request_log
def auth_alipay(request):
    return render(request,"auth-alipay.html")


def decrease_time_by_8hour():
    import datetime as dt
    Ins_query = Ins.objects.all()
    Outs_query = Outs.objects.all()
    for record in Ins_query:
        record.btime = record.btime + dt.timedelta(hours=8)
        record.save()
    
def bulk_add(file_name,separator):
    with open(file_name) as f:
        lines = f.readlines()
        records=[]
        first_line = lines[0].strip()
        field_list = first_line.split(separator)
        for line in lines[1:]:
            if line =="\n":
                continue
            one_record_list = line.strip().split(separator)
            usr = Usr.objects.get(uid="780303f9-b0a1-4d7b-a7b4-d191daa85f47")
            print(list(zip(field_list,one_record_list)))
            one_reocrd_dict = Ins(**dict(zip(field_list,one_record_list)),usr=usr)
            records.append(one_reocrd_dict)
    Ins.objects.bulk_create(records)
    print(records)

def bulk_add_1(file_name,separator,encoding="utf-8"):
    with open(file_name,encoding=encoding) as f:
        lines = f.readlines()
        records=[]
        first_line = lines[0].strip()
        first_line = first_line.replace("\t","")
        field_list = first_line.split(separator)
        for line in lines[1:]:
            one_record_list = line.strip().split(separator)
            for index,v in enumerate(one_record_list):
                v = v.replace("\t"," ")
                v = v.replace("/","-")
                v = v.strip()
                one_record_list[index] = v
            usr = Usr.objects.get(uid="780303f9-b0a1-4d7b-a7b4-d191daa85f47")
            one_reocrd_dict = Outs(**dict(zip(field_list,one_record_list)),usr=usr)
            records.append(one_reocrd_dict)
    Outs.objects.bulk_create(records)
    print(records)


@check_request
def ins_query(request):
    from datetime import datetime 
    if request.method == 'POST':
        uid = request.POST.get('uid')
        start = request.POST.get('start')
        end = request.POST.get('end')

        if start == None:  # 没有 start 时间
            return JsonResponse({"error":"not specify start",})
        else : 
            if end == '' or end == None :  # 有start 无 end
                usr = Usr.objects.get(uid=uid)
                _q = Ins.objects.filter(usr=usr,btime__range=(datetime.strptime(start,r"%Y-%m-%d %H:%M:%S"),datetime.now()))
                print(len(_q))
                
                #_q.values_list()
                print(datetime.strptime(start,r"%Y-%m-%d %H:%M:%S"))
                if _q.exists():
                    print("_q exist")
                    data = A37Serializers.InsModelSerializer(_q,many=True).data
                    return JsonResponse({"data":data,"num":len(data)},safe=False)
                else :
                    print("_q don't exist")
                    return JsonResponse({"num":0},safe=False)
            
    return JsonResponse({"error":"You can't use GET to fetch",})

# 测试中2023/3/9
@check_request
def outs_query(request):
    from datetime import datetime
    if request.method == 'POST':
        uid = request.POST.get('uid')
        start = request.POST.get('start')
        end = request.POST.get('end')

        if start == None:  # 没有 start 时间
            return JsonResponse({"error":"not specify start",})
        else : 
            if end == '' or end == None :  # 有start 无 end
                usr = Usr.objects.get(uid=uid)
                _q = Outs.objects.filter(usr=usr ,btime__range=(datetime.strptime(start,r"%Y-%m-%d %H:%M:%S"),datetime.now()))
                print(len(_q))
                
                #_q.values_list()
                data = A37Serializers.OutsModelSerializer(_q,many=True).data

                return JsonResponse({"data":data,"num":len(data)},safe=False)
            else :
                print("_q don't exist")
                return JsonResponse({"num":0},safe=False)
            
    return JsonResponse({"error":"You can't use GET to fetch",})
import asyncio
import time
import threading
# async def long_polling_check():
    
import os
# @check_request
def login(request):
    password = request.POST.get("password")
    uphone = request.POST.get("uphone")
    _q = Usr.objects.get(uphone = uphone)
    if _q:
        _q = A37Serializers.UsrModelSerializer(_q,context={"request":request})
        _dict = _q.data
        _dict["login"] = _dict.get("password")==password
        print("the result is :",_q.data)
        return JsonResponse(_dict)
    else:
        return JsonResponse({"login":"false"})

def check_and_create_own_relation(request:HttpRequest):
    room_num = request.POST.get("room_num")
    uphone = request.POST.get("uphone")
    _q = Usr.objects.get(uphone = uphone)
    if _q:
        Own.objects.create(room = Room.objects.get(room_num = room_num), usr = _q)
        return JsonResponse({"status":True,"prompt":"用户成功加入"})
    else:
        return JsonResponse({"status":False,"prompt":"用户不存在"})
    
def delete_relation(request:HttpRequest):
    room_num = request.POST.get("room_num")
    uphone = request.POST.get("uphone")
    _q = Usr.objects.get(uphone = uphone)
    if _q:
        Own.objects.create(room = Room.objects.get(room_num = room_num), usr = _q)
        return JsonResponse({"status":True,"prompt":"用户成功加入"})
    else:
        return JsonResponse({"status":False,"prompt":"用户不存在"})

# @check_request
def room_login(request):
    password = request.POST.get("password")
    room_num = request.POST.get("room_num")
    uid = request.POST.get("uid")
    _dict = dict()
    print(password,room_num,uid)
    # check if the OWN relation table confirm the user has the right to do this 
    _q:QuerySet = Own.objects.filter(room=room_num)
    _q = _q.filter(usr=uid)
    # _dict.update({"role":_q.first().comment})
    if not _q:
        return JsonResponse({"login":"false","reason":"no such own relation "})
    # then check the room's pwd 
    _q:QuerySet = Room.objects.filter(room_num=room_num)
    if _q:
        _q = A37Serializers.RoomModelSerializer(_q.first())
        print(_q)
        _dict.update(_q.data)
        _dict["info"] =A37Serializers.InfoModelSerializer(Info.objects.filter(room = room_num),many=True).data
        _dict["login"] = (_dict.get("pwd")==password)
        print("the result is :",_q.data)
        return JsonResponse(_dict)
    else:
        return JsonResponse({"login":"false"})
 


@check_request
def verification_code_GET(request):
    import datetime
    global request_num
    request_num += 1
    uphone = request.POST.get("uphone")
    global verifycode 
    verifycode = datetime.datetime.now().microsecond %9000 + 1000,
    json_data ={
        'code'  : verifycode,
        'uphone' : uphone ,
    }
    print(json_data)
    return JsonResponse(json_data)

from Site.settings import STATIC_ROOT
from pathlib import Path


AVATAR_PATH = str(STATIC_ROOT) + "/a37/avatar_images"
INS_PATH = str(STATIC_ROOT) + "/a37/ins_images"
RECOG_PATH = str(STATIC_ROOT) + "/a37/recog_images"
OUTS_PATH = str(STATIC_ROOT) + "/a37/outs_images"
LOG_PATH = str(STATIC_ROOT)+ "/log"
import encodings
def print_log(*args):
    with open(LOG_PATH,"a") as f:
        f.write("Time:"+str(datetime.datetime.now())+"\n")
        for arg in args:
            f.write(str(arg)+" ")
        f.write("\n")

# print = print_log
@check_request
def log(request:HttpRequest):
    # print_log("loggggggggggggggggggggggg")
    print("avatar_path:",AVATAR_PATH)
    print("log_path",LOG_PATH)
    with open(LOG_PATH,"a",encoding="utf-8") as f:
        f.write(request.POST.get("data"))
        f.write("\n")
        print(AVATAR_PATH)
        print("string data of the image:")
        print(request.POST.get("data"))
    return JsonResponse({"ok":True})
    
# 头像上传 api
@check_request_log
def avatar_post(request:HttpRequest):
    if request.method == "POST":
        _data_url = request.POST.get("data")
        uid  = request.POST.get("uid")
        if  _data_url == "":
            return JsonResponse({"status":"404","prompt":"not found data"})
        if  uid == "":
            return JsonResponse({"status":"404","prompt":"not found uid"})
        _q:QuerySet = Usr.objects.filter(uid = uid)
        print_log("   uid:"+str(uid))
        print_log("   data:"+str(_data_url))
        print_log("   _q:"+str(_q))
        if len(_q)==0:
            return JsonResponse({"status":"404","prompt":"not found user corresponding to uid"})
        _q:Usr = _q[0]  # get the first element in 
        _format  , _dataurl = _data_url.split(';base64,')
        _ , _extension = _format.split("/")
        _file_name = f"{uid}.{_extension}"
        _file_path = AVATAR_PATH  + "/" + _file_name
        image_io = io.BytesIO()
        image_io.write(base64.urlsafe_b64decode(_dataurl))
        image =  Image.open(image_io)
        image =image.resize((100,int(100 * image.height/image.width)),resample=Image.Resampling.BILINEAR)
        image.save(_file_path)

        print("save successfully")
        print("path:",_file_path)
        print("extension:",_extension)
        _q.upic = "static/a37/avatar_images/"+ _file_name
        _q.save()
        print_log(_file_path)
        return JsonResponse({"status":"200","upic":_q.upic})
    return HttpRequest("Use POST method to send it.")
def recognize_img(request:HttpRequest):
    if request.method == "POST":
        _data_url = request.POST.get("data")
        if  _data_url == "":
            return JsonResponse({"status":"404","prompt":"not found data"})
        _format  , _dataurl = _data_url.split(';base64,')
        _ , _extension = _format.split("/")
        _file_name = f"{uuid.uuid4()}.{_extension}"
        _file_path = RECOG_PATH  + "/" + _file_name
        image_io = io.BytesIO()
        image_io.write(base64.urlsafe_b64decode(_dataurl))
        image =  Image.open(image_io)
        image.save(_file_path)

        print("save successfully")
        print("path:",_file_path)
        print("extension:",_extension)
        print("import successfully")
        import subprocess
        out = None
        err = None
        command = "/home/ubuntu/anaconda3/bin/python /home/ubuntu/Site/A37TextCNN/tc.py %s"%_file_path
        # command = "python /home/ubuntu/python_repo/hello.py %s"%_file_path
        with subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) as p:
            err = p.stderr.read()
            out = p.stdout.read()
        # return JsonResponse({"out":out.decode(), "err":err.decode(),"command":command},safe=False)
        # print(j)
        out=eval(out)
        import re
        out["product_name"] = out["product_name"].replace('\n', '')
        # if out["product_name"] :
        #     out["product_name"]:str = out["product_name"].strip()
        #     out["product_name"] = out["product_name"].strip()
        #     out["商品"] = out["商品"].split("\n")
            # out["商品"]=re.split(out["商品"],"\n|，|,")
            # out["商品"] = str(out["商品"])
        out.update({"status":"200"})
        return JsonResponse(out,safe=False)
    return HttpRequest("Use POST method to send it.")
# @check_request
def number_extract(request:HttpRequest):
    if request.method == "POST":
        data = request.POST.get("data")
        import subprocess
        # coding_set = sys.getdefaultencoding()
        args = ['/home/ubuntu/anaconda3/bin/python','main.py',data]
        # args = ['ls']
        result:subprocess.CompletedProcess= subprocess.run(args,shell=False,cwd="/home/ubuntu/Site/A37TextCNN/",text=True,capture_output=True)
        # out = subprocess.check_output(args,cwd='/home/ubuntu/Site/A37TextCNN/',text=True,encoding='utf-8')
        # out = subprocess.check_output(['ls'],cwd='/home/ubuntu/Site/A37TextCNN/',text=True,shell=True)
        # command = '/home/ubuntu/anaconda3/bin/python main.py \"%s\"'% data
        # command = "python /home/ubuntu/python_repo/hello.py %s"%_file_path
        # with subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) as p:
        #     err = p.stderr.read()
        #     out = p.stdout.read()
        # return JsonResponse({"out":out.decode(), "err":err.decode(),"command":command},safe=False)
        # print(j)
        # out = out.decode()


        out = result.stdout
        out = out.strip()
        out = eval(out.split("\n")[-1])
        out = {'out':out}
        out.update({"status":200})
        # return JsonResponse({'stdout':result.stdout,'stderr':result.stderr,'all':str(result)},safe=False)
        return JsonResponse(out,safe=False)
    return HttpRequest("Use POST method to send it.")
def ins_post(request:HttpRequest):
    if request.method == "POST":
        _data_url = request.POST.get("data")
        _id  = request.POST.get("id")
        if  _data_url == "":
            return JsonResponse({"status":"404","prompt":"dataurl shouldn't be null"})
        if  _id == "":
            return JsonResponse({"status":"404","prompt":"id shouldn't be null"})
        _q:QuerySet = Ins.objects.filter(id = _id)
        if not _q.exists():
            return JsonResponse({"status":"404","prompt":"not found consumption corresponding to id"})
        _q:Ins = _q[0]  # get the first element in 
        _format  , _dataurl = _data_url.split(';base64,')
        _ , _extension = _format.split("/")
        _file_name = f"{_id}.{_extension}"
        _file_path = INS_PATH + "/" + _file_name
        image_io = io.BytesIO()
        image_io.write(base64.urlsafe_b64decode(_dataurl))
        image =  Image.open(image_io)
        image.save(_file_path)

        print("save successfully")
        print("path:",_file_path)
        print("extension:",_extension)

        _q.receipt = "static/a37/ins_images/"+ _file_name
        _q.isreceipt = True
        _q.save()
        print_log(_file_path)
        return JsonResponse({"status":"200","receipt":_q.receipt})
    return HttpRequest("Use POST method to send it.")
def outs_post(request:HttpRequest):
    if request.method == "POST":
        _data_url = request.POST.get("data")
        _id  = request.POST.get("id")
        if  _data_url == "" or _data_url ==None:
            return JsonResponse({"status":"404","prompt":"dataurl shoudn't be null"})
        if  _id == "" or _id == None:
            return JsonResponse({"status":"404","prompt":"id shoudn't be null"})
        _q:QuerySet = Outs.objects.filter(id = _id)
        if not _q.exists():
            return JsonResponse({"status":"404","prompt":"not found consumption corresponding to id"})
        _q:Outs = _q[0]  # get the first element in 
        _format  , _dataurl = _data_url.split(';base64,')
        _ , _extension = _format.split("/")
        _file_name = f"{_id}.{_extension}"
        _file_path = OUTS_PATH + "/" + _file_name
        image_io = io.BytesIO()
        image_io.write(base64.urlsafe_b64decode(_dataurl))
        image =  Image.open(image_io)
        image.save(_file_path)

        print("save successfully")
        print("path:",_file_path)
        print("extension:",_extension)

        _q.receipt = "static/a37/outs_images/"+ _file_name
        _q.isreceipt = True
        _q.save()
        print_log(_file_path)
        return JsonResponse({"status":"200","receipt":_q.receipt})
    return HttpRequest("Use POST method to send it.")

# export https_proxy=http://127.0.0.1:33210 http_proxy=http://127.0.0.1:33210 all_proxy=socks5://127.0.0.1:33211


def chatgpt_ask(request : HttpRequest):
    prompt = request.GET.get("prompt")
    print(prompt)
    response = openai.ChatCompletion.create(
		  model="gpt-3.5-turbo",
		  messages=[
		        {"role": "user", "content": prompt}
		    ]
		)
    print("end fetching")
    return response['choices'][0]['message']['content']

# python standard lib

# django and pillow lib

from PIL import Image
import io
import base64


class UsrModelViewSet(ModelViewSet):
    queryset = Usr.objects.all()
    serializer_class = A37Serializers.UsrModelSerializer

class InsModelViewSet(ModelViewSet):
    queryset = Ins.objects.all()
    serializer_class = A37Serializers.InsModelSerializer

class OutsModelViewSet(ModelViewSet):
    queryset = Outs.objects.all()
    serializer_class = A37Serializers.OutsModelSerializer

class RoomModelViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = A37Serializers.RoomModelSerializer

class OwnModelViewSet(ModelViewSet):
    queryset = Own.objects.all()
    serializer_class = A37Serializers.OwnModelSerializer

class InfoModelViewSet(ModelViewSet):
    queryset = Info.objects.all()
    # def create(self, request, *args, **kwargs):
    #     refresh_flag =True
    #     return super(InfoModelViewSet,self).create(self,request,*args,**kwargs)
    serializer_class = A37Serializers.InfoModelSerializer


# 为特定uid的用户指定头像   
# @check_request
# class avatar(APIView):
#     def get(request):
#         pass
#     def post(request:HttpRequest):

#     def post(request):
#         if request.method == 'POST':
#             image = request.FILES["image"]
#             uid = request.POST["uid"]

#             # print(request.body)
#             # print("THE DATA TYPE is ",type(image))
#             # print(muld.keys.__str__)
#             # print(request.FILES)
#             # print(request.GET)
#             print(request.content_params)
#             print(request.content_type)
#             # muld.keys.__str__

            
#             if image and uid != None:
#                 print("image received")
#                 now = datetime.now()
#                 file_name = str(uid) + "_%d"*6%(now.year,now.month,now.day,now.hour,now.minute,now.second)
#                 print("uid是",uid)
#                 _t = Usr.objects.get(uid=uid)
#                 _t.upic = file_name
#                 _t.save()

#                 path = "./static/avatar_images/"+  file_name
#                 print(path)
#                 default_storage.save(path, ContentFile(image.read()))
#                 print("the filename is",file_name)
#                 return render(request, 'success.html', {'filename': file_name})
#             else:
#                 return JsonResponse({ "error" : "要发送的文件不存在 或 没有指定 uid "})
#         return render(request, 'upload.html')

# @check_request
# def avatar_GET(request):
#     uid = -1
#     pic_name =""
#     _t =None
#     if request.method == "GET": 
#         uid = request.GET.get("uid")
#         print(request.GET.get("uid"))
#         _t = Usr.objects.get(uid = uid )
#         print(request.POST.get("uid"))
#         _t = Usr.objects.get(uid = uid )
#     # combine the url 
#     url  = "https://mineralsteins:8080/static/A37/avatar_images/"+ _t.upic 
#     if request.method == "POST":
#         json_data = { "url" : url}
#         return JsonResponse(json_data)
#     else: 
#         return render(request,"show_image.html",{"path" : url})

            # else :  # start end 都有
            #     _q = Outs.objects.filter(uid=uid,btime__range=(datetime.strptime(start,"%Y-%m-%d %H:%M:%S"),datetime.strptime(end,"%Y-%m-%d %H:%M:%S")))
            #     #_q.values_list()
            #     if _q.exists():
            #         data = A37Serializers.InsSerializer(_q,many=True).data
            #         json_data = {key:data[key] for key in fields}
            #         return JsonResponse(json_data)
            #     else :
            #         return JsonResponse({"error":"start + end but no answer"})
            # else :  # start end 都有
            #     _q = Outs.objects.filter(uid=uid,btime__range=(datetime.strptime(start,"%Y-%m-%d %H:%M:%S"),datetime.strptime(end,"%Y-%m-%d %H:%M:%S")))
            #     #_q.values_list()
            #     if _q.exists():
            #         data = A37Serializers.InsSerializer(_q,many=True).data
            #         json_data = {key:data[key] for key in fields}
            #         return JsonResponse(json_data)
            #     else :
            #         return JsonResponse({"error":"start + end but no answer"})
