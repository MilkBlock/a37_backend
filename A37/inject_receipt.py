import requests
import json
import threading
import os
from A37.models import Outs
from A37.models import Usr

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def read_post_set(img_path):
    _app_id = '6b07d2d756f3be15198633de37dcc852'
    _secret_code = 'a38872198de6545a6464969c71ef1272'
    url = 'https://api.textin.com/robot/v1.0/api/receipt'
    if Outs.objects.filter(receipt = "static/a37/outs_images/"+os.path.basename(img_path)).exists():
        print("这个图片已经入库了already exist")
        return 
    head = {}
    try:
        image = get_file_content(img_path)
        head['x-ti-app-id'] = _app_id
        head['x-ti-secret-code'] = _secret_code
        result = requests.post(url, data=image, headers=head)
        set_record(result.json(),img_path)
    except Exception as e:
        print(img_path," 请求失败并抛出异常")
        print(str(e))

the_usr = Usr.objects.filter(uid = "a05086ff-df6b-4a0f-9ed5-a3de4064ec6b")[0]
def set_record(d,img_path):
    if(d["message"]!="success"):
        print("message :fail服务端无法识别")
        return
    d= d["result"]
    print("bname",_bname:= d["item_list"][3]["value"])
    print("bcategory",_bcategory:= "餐饮")
    print("note",_note:=d["item_list"][3]["value"])
    print("payment",_payment :="支付宝")
    print("amount",_amount := d["item_list"][0]["value"])
    print("btime",_btime :=d["item_list"][1]["value"])
    if len(_btime)==len("02-15 11:35"):
        _btime = "2022-"+_btime
    if len(_btime)==len(""):
        _btime = "2022-03-27 13:30"
    if _btime.strip().split(" ")!=2:
        _btime = "2022-03-27 13:30"
    if _btime.strip().split("-")!=3:
        _btime = "2022-03-27 13:30"
    print("isreceipt",_isreceipt :=True)
    Outs.objects.create(bname = _bname,
                        bcategory = _bcategory,
                        note = _note,
                        payment =_payment ,
                        amount = _amount,
                        btime=_btime,
                        isreceipt=_isreceipt,
                        usr = the_usr,
                        receipt = "static/a37/outs_images/"+os.path.basename(img_path))
    print(d)
if __name__ == "__main__":
    image_dir = "/home/ubuntu/Site/static/a37/outs_images"
    for ordinal, _dir in enumerate(os.listdir("/home/ubuntu/Site/static/a37/outs_images")[10:]):
        print("编号",ordinal)
        print(os.path.join(image_dir,_dir))
        read_post_set(img_path=os.path.join(image_dir,_dir))

