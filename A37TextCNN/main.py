import json
import datetime
import jieba
import cn2an
import re
import os
from itertools import zip_longest
from torch.utils.data import Dataset,DataLoader
import torch
import torch.nn as nn
from BiLSTM_CRF_model import Mymodel

def get_pred(text):
    with open ("word_2_index.json","r",encoding="utf-8") as f:
        word_2_index = json.load(f)

    with open ("tag_2_index.json","r",encoding="utf-8") as f:
        tag_2_index = json.load(f)

    index_2_tag = [i for i in tag_2_index]

    corpus_num = 168
    embedding_num = 101
    hidden_num = 107
    class_num = 13
    bi = True

    model = Mymodel(corpus_num,embedding_num,hidden_num,class_num,bi)
    model.load_state_dict(torch.load("ner_model.pth"))
    model.eval()

    return(pred(text,model,word_2_index,index_2_tag))

def pred(text,model,word_2_index,index_2_tag):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    text_index = [[word_2_index.get(i,word_2_index["<UNK>"]) for i in text] + [word_2_index["<END>"]]]
    text_index = torch.tensor(text_index,dtype=torch.int64,device=device)
    pre = model.test(text_index,[len(text)+1])
    print(pre)
    pre = [index_2_tag[i] for i in pre]
    entities = extract_entities(pre,[i for i in text])

    print(entities)
    data = {}

    for entity in entities:
        entity_type = entity["entity_type"]
        entity_tokens = entity["tokens"]
        entity_text = "".join(entity_tokens)
        if entity_type == "TIME":
            entity_text = get_date(entity_text)
        if entity_type == "AMOUNT":
            entity_text = get_desofnum(entity_text)
        data[entity_type] = entity_text
    return data

def extract_entities(tags, tokens):
    entities = []
    current_entity = None

    for tag, token in zip(tags, tokens):
        if tag.startswith("B-"):
            if current_entity is not None:
                entities.append(current_entity)
            current_entity = {"entity_type": tag[2:], "tokens": [token]}
        elif tag.startswith("M-"):
            if current_entity is None:
                current_entity = {"entity_type": tag[2:], "tokens": [token]}
            else:
                current_entity["tokens"].append(token)
        elif tag.startswith("E-"):
            if current_entity is not None:
                current_entity["tokens"].append(token)
                entities.append(current_entity)
                current_entity = None
        elif tag == "O":
            if current_entity is not None:
                entities.append(current_entity)
                current_entity = None
        else:
            current_entity = None

    if current_entity is not None:
        entities.append(current_entity)

    return entities

def get_date(des):
    current_date = str(datetime.datetime.now())
    year = current_date[:4]
    month = current_date[5:7]
    day = current_date[8:10]
    hour =current_date[11:13]
    minute = current_date[14:16]
    second = current_date[17:19]
    out = jieba.lcut(des)
    now_num = datetime.date(int(year),int(month),int(day)).weekday()+1
    print
    if str(out[0]).find("今")!=-1:
        if str(out[0]).find("上午")!=-1 or str(out[0]).find("早")!=-1:
            hour = get_num(out[1][:-1])
            minute = "00"
            second = "00"
            return str(year) + "-" + str(month) + "-" + str(day) +" "+ str(hour)+":"+str(minute)+":"+str(second)
        elif str(out[0]).find("下午")!=-1 or str(out[0]).find("晚")!=-1:
            hour = str(12+int(get_num(out[1][:-1])))
            minute = "00"
            second = "00"
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + minute + ":" + second
        else:
            hour = 12
            minute = "00"
            second = "00"
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + minute + ":" + second
    elif str(out[0]).find("昨")!=-1:
        if str(out[0]).find("上午")!=-1 or str(out[0]).find("早")!=-1:
            hour = get_num(out[1][:-1])
            minute = "00"
            second = "00"
            if int(day)-1 <=  0:
                month = month-1
                day = is_last(month)
            else:
                day = int(day)-1
            return str(year) + "-" + str(month) + "-" + str(day) +" "+ str(hour)+":"+str(minute)+":"+str(second)
        elif str(out[0]).find("下午")!=-1 or str(out[0]).find("晚")!=-1:
            hour = str(12+int(get_num(out[1][:-1])))
            minute = "00"
            second = "00"
            if int(day)-1 <= 0:
                month = month-1
                day = is_last(month)
            else:
                day = int(day)-1
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + minute + ":" + second
        else:
            hour = 12
            minute = "00"
            second = "00"
            if int(day)-1 <= 0:
                month = month-1
                day = is_last(month)
            else:
                day = int(day) - 1
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + minute + ":" + second
    elif str(out[0]).find("前")!=-1:
        if str(out[1]).find("上午")!=-1 or str(out[1]).find("早")!=-1:
            hour = get_num(out[2][:-1])
            minute = "00"
            second = "00"
            if int(day)-1 < 0:
                month = month-1
                day = is_last(month)
            else:
                day = int(day)-1
            if int(day) - 1 < 0:
                month = int(month)-1
                day = is_last(month)
            else:
                day = int(day) - 1
            return str(year) + "-" + str(month) + "-" + str(day) +" "+ str(hour)+":"+str(minute)+":"+str(second)
        elif str(out[1]).find("下午")!=-1 or str(out[1]).find("晚")!=-1:
            hour = str(12+int(get_num(out[2][:-1])))
            minute = "00"
            second = "00"
            if int(day) - 1 < 0:
                month = int(month)-1
                day = is_last(month)
            else:
                day = int(day) - 1
            if int(day) - 1 < 0:
                month = int(month)-1
                day = is_last(month)
            else:
                day = int(day) - 1
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + minute + ":" + second
        else:
            hour = 12
            minute = "00"
            second = "00"
            if int(day) - 1 < 0:
                month = int(month)-1
                day = is_last(month)
            else:
                day = int(day) - 1
            if int(day) - 1 < 0:
                month = int(month)-1
                day = is_last(month)
            else:
                day = int(day) - 1
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + minute + ":" + second
    elif str(out[0]).find("上周")!=-1:
        total = now_num + (7 - get_num(out[0][-1]))
        print(now_num)
        print(7 - get_num(out[0][-1]))
        print(total)
        # total = now_num+get_num(out[0][-1])+1
        for i in range(total):
            if int(day) - 1 < 0:
                month = int(month) - 1
                day = is_last(month)
            else:
                day = int(day) - 1
        if str(out[1]).find("上午")!=-1 or str(out[1]).find("早")!=-1:
            hour = get_num(out[2][:-1])
            minute = "00"
            second = "00"
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(
                second)
        elif str(out[1]).find("下午")!=-1 or str(out[1]).find("晚")!=-1:
            hour = str(12 + int(get_num(out[2][:-1])))
            minute = "00"
            second = "00"
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + minute + ":" + second
        else:
            hour = 12
            minute = "00"
            second = "00"
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + minute + ":" + second
    elif str(out[0]).find("上个月")!=-1:
        month = int(month)-1
        day = get_num(out[1][:-1])
        if str(out[2]).find("上午")!=-1 or str(out[2]).find("早")!=-1:
            hour = get_num(out[3][:-1])
            minute = "00"
            second = "00"
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(
                second)
        elif str(out[2]).find("下午")!=-1 or str(out[2]).find("晚")!=-1:
            hour = str(12 + int(get_num(out[3][:-1])))
            minute = "00"
            second = "00"
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + minute + ":" + second
        else:
            hour = 12
            minute = "00"
            second = "00"
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + minute + ":" + second
    elif str(out[0]).find("上") != -1 and (str(out[1]).find("星期") !=-1 or str(out[1]).find("周") !=-1):
        total = now_num + (7-get_num(out[1][-1]))
        print(now_num)
        print(total)
        for i in range(total):
            if int(day) - 1 < 0:
                month = int(month) - 1
                day = is_last(month)
            else:
                day = int(day) - 1
        if str(out[2]).find("上午") != -1 or str(out[2]).find("早") != -1:
            hour = get_num(out[3][:-1])
            minute = "00"
            second = "00"
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(
                second)
        elif str(out[2]).find("下午") != -1 or str(out[2]).find("晚") != -1:
            hour = str(12 + int(get_num(out[3][:-1])))
            minute = "00"
            second = "00"
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + minute + ":" + second
        else:
            hour = 12
            minute = "00"
            second = "00"
            return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + minute + ":" + second


def get_num(des):
    chinese_number_map = {
        "零": 0,
        "一": 1,
        "二": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
        "十": 10,
        "十一":11,
        "十二":12,
        "十三":13,
        "十四": 14,
        "十五": 15,
        "十六": 16,
        "十七": 17,
        "十八": 18,
        "十九": 19,
        "二十": 20,
        "二十一": 21,
        "二十二": 22,
        "二十三": 23,
        "二十四": 24,
        "二十五": 25,
        "二十六": 26,
        "二十七": 27,
        "二十八": 28,
        "二十九": 29,
        "三十":30,
        "三十一":31
    }
    return chinese_number_map[des]

def is_last(month):
    chinese_number_map = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }
    return chinese_number_map[month]

def get_desofnum(text):
    num = ""
    for item in text:
        if item.find("块") !=-1 or item.find("元")!=-1:
            break
        else: num+=item
    number = cn2an.cn2an(num,"smart")
    return number

def turnnumbertochinese(text):
    def replace_with_chinese(match):
        arabic_number = int(match.group())
        print("the number to substitute",arabic_number)
        chinese_number = cn2an.an2cn(arabic_number)
        return chinese_number

    import re
    # 使用正则表达式将句子中的中文数字提取出来
    pattern = r'\d+'
    result = re.sub(pattern, replace_with_chinese, text)

    return result

if __name__ == '__main__':
    # text = "今天上午10点我去菜市场买了10块钱的菜"
    import sys
    text = sys.argv[1]
    # print("is equal",text == text_d)
    # text = "我去菜市场用10块"
    # print(turnnumbertochinese(text))
    t = turnnumbertochinese(text)
    print(get_pred(t))

