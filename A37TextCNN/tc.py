import json
import torch
import requests
import threading
import queue
import jionlp as jio
import time
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from TextCNN import TextCNNModel

result_queue = queue.Queue()
judge_result_queue = queue.Queue()
max_len = 50

LOG_PATH = "/home/ubuntu/Site/static/log"
def print_log(*args):
    import datetime
    with open(LOG_PATH,"a") as f:
        f.write("Time:"+str(datetime.datetime.now())+"\n")
        for arg in args:
            f.write(str(arg)+" ")
        f.write("\n")

# print = print_log    你也许会用到这个

def init_model():
    # print("init model start")
    with open('/home/ubuntu/Site/static/A37TextCNN/word_2_index_2.json', 'r', encoding='utf-8') as f:
        word_2_index = json.load(f)

    embedding_dim = 200
    vocab_size = len(word_2_index)
    class_num = 2
    hidden_num = 20
    embedding = nn.Embedding(vocab_size, embedding_dim)
    model = TextCNNModel(embedding,max_len,class_num,hidden_num)
    model.load_state_dict(torch.load('/home/ubuntu/Site/static/A37TextCNN/text_cnn_model_2.pth'))
    model.eval()  # 设置模型为评估模式
    # print("init completed ")
    return model,word_2_index

model,word_2_index = init_model()

def changetoneed(text,word_2_index,max_len):
    tokens = [x for x in text]
    # print(tokens)
    indexed_tokens = [word_2_index.get(token, word_2_index['<UNK>']) for token in tokens]
    # print(indexed_tokens)
    padded_tokens = indexed_tokens[:max_len] + [word_2_index['<PAD>']] * (max_len - len(indexed_tokens))
    # print(padded_tokens)
    input_tensor = torch.tensor(padded_tokens).unsqueeze(0)
    return input_tensor

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

class CommonOcr(object):
    def __init__(self, img_path):
        # 请登录后前往 “工作台-账号设置-开发者信息” 查看 x-ti-app-id
        # 示例代码中 x-ti-app-id 非真实数据
        self._app_id = '6b07d2d756f3be15198633de37dcc852'
        # 请登录后前往 “工作台-账号设置-开发者信息” 查看 x-ti-secret-code
        # 示例代码中 x-ti-secret-code 非真实数据
        self._secret_code = 'a38872198de6545a6464969c71ef1272'
        self._img_path = img_path

    def receipt_recognize(self):
        # 商铺小票识别
        url = 'https://api.textin.com/robot/v1.0/api/receipt'
        head = {}
        try:
            image = get_file_content(self._img_path)
            head['x-ti-app-id'] = self._app_id
            head['x-ti-secret-code'] = self._secret_code
            result = requests.post(url, data=image, headers=head)
            return result.text
        except Exception as e:
            return e

    def universal_recognize(self):
        # 通用文字识别
        url = 'https://api.textin.com/ai/service/v2/recognize'
        head = {}
        try:
            image = get_file_content(self._img_path)
            head['x-ti-app-id'] = self._app_id
            head['x-ti-secret-code'] = self._secret_code
            result = requests.post(url, data=image, headers=head)
            return result.text
        except Exception as e:
            return e

def get_receipt_part(img_path):
    data = json.loads(CommonOcr(img_path).receipt_recognize())
    # print("receipt recog completed")
    item_list = data['result']['item_list']
    output_list = {}
    for item in item_list:
        # print(item)
        if item['description'] == '商户编号' or item['description'] == '单号':
            continue
        elif item['description'] == '商户':
            name = result_queue.get()
            output_list.update({item['description']: name})
        else:
            output_list.update({item['description']: item['value']})
    judge_result_queue.put(output_list)

def get_universal_part_then_torch(model,img_path):
    data_all = json.loads(CommonOcr(img_path).universal_recognize())
    # print("universal recog completed")
    item_list_name = data_all['result']['lines']
    find_name = []
    name =None
    for item in item_list_name:
        find_name.append(item['text'])

    for item in find_name:
        if torch.argmax(model(changetoneed(item, word_2_index, max_len)), dim=1) == 1:
            name = item
            break
    result_queue.put(name)

def judge(img_path):
    # print("size of judge_result_queue is",judge_result_queue.qsize())
    thread1 = threading.Thread(target=get_universal_part_then_torch(model,img_path))
    thread2 = threading.Thread(target=get_receipt_part(img_path))
    thread1.start()
    thread2.start()
    return judge_result_queue.get()
    
import sys
if __name__ == '__main__':
    # print("hello")
    # print(sys.argv)
    d1 = dict(judge(sys.argv[1]))
    d2 = dict()
    d2["product_name"]= d1["商品"]
    d2["shop_name"] = d1["商户"]
    d2["time"] = d1["时间"]
    d2["amount"] = d1["金额"]
    t = jio.parse_time(d2["time"], time_base=time.time())["time"]
    if type(t) == list:
        d2["time"] = t[0]
    elif type(t) == str:
        d2["time"] = t
    print(d2)  

