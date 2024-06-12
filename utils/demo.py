from A37.views import bulk_add_1
bulk_add_1("数据ins_bulk.txt",",")






# from collections import namedtuple
# from django.core
# Student  = namedtuple("Student",["grade","age"])
# students = [
#     Student(grade = 31, age=23),
#     Student(grade = 41, age=19),
#     Student(grade = 21, age=22),
#     Student(grade = 1, age=24),
# ]

# def cmp(x:Student,y:Student):
#     if x.age < y.age:
#         return 1
#     else:
#         return -1

# print(sorted(students,key=lambda student:student.age))

# import os
# os.
# import sys
# sys.stdout = 



# class a:
#     pass

# demo = a()
# demo.__dict__["this"] = "True"
# print(demo.this)
# from functools import wraps
# def check(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         print("hello world")
#         return func(*args, **kwargs)
#     return wrapper

# @check
# def add(x,y):
#     return x,y

# print(add(3,4))
# print(add.__name__)


# # from A37.models import *
# # a = Ins.objects.all()
# # print(a[0].usr)



# # from collections import namedtuple

# if(1):
#     print('''hello 
#                 this ''')



# class Point:
#     # 类 = 模版 
#     x,y=0,0
#     def __init__(self,_x,_y) -> None:
#         self.x = _x
#         self.y = _y
#     def __iadd__(self, another_point):
#         self.x += another_point.x
#         self.y += another_point.y
#         print("调用了iadd method")
#         return self
#     def __isub__(self, another_point):
#         self.x -= another_point.x
#         self.y -= another_point.y
#         print("调用了isub method")
#         return self
    
#     def print_itself(self):
#         print(self.x,self.y)

# a = Point(3,4)
# b = Point(2,4)
# a-=b

# a.print_itself()

# my_tuple = (1,2,[3,4]) 
# print(id(my_tuple[2]))
# my_tuple[2] +=[5,6]
# print(id(my_tuple[2]))
# print(my_tuple)

# s= 'sthis'
# s.partition



# from A37.views import G*
# bulk_add("数据outs.txt",",")


# import base64
# a= b'this is not true'
# print(type(a))
# c = []
# # print(b:=str(base64.standard_b64encode(a),'utf-8'))
# # print(str(base64.standard_b64decode(b),"utf-8"))

# print(base64.b64encode("thi".encode()))
# print(base64.b64encode("thisis".encode()))
# print("    ".encode().hex())
# print(base64.a85encode("    ".encode()))
# print(base64.b85encode("    ".encode()))
# print("0123456789ABCDEFGHIJVKLMNOPQRSTUVWXYZ".encode().hex())
# print("abcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~".encode().hex())

# from A37.serializers import UsrModelSerializer
# UsrModelSerializer()

# from rest_framework.views import APIView
# from rest_framework.status import x
# from django.views import View

# def check_para(func):
#     def inner(*args,**kwargs):
#         print("the paras are:",*args,**kwargs)
#         return func(*args,**kwargs)
#     return inner

# from math import sqrt

# @check_para
# def get_distance(x,y):
#     return sqrt(x**2 + y**2)

# from functools import wraps
# print(get_distance(3,4))
# class Point():
#     @classmethod
#     def get_class_name(cls):
#         return cls.__name__

#     def __init__(self,x,y) -> None:
#         self.x,self.y = x,y
    

#     def __call__(self) :
#         print("Point x:%d,y:%d "%(self.x,self.y))

# Point.get_class_name()


# class demo:
#     def __init__(self,*args, **kwargs) -> None:
#         # self.func,self.duration = func,duration
#         print("init args",args)
#         print("init kwargs",kwargs)

#     def __call__(self,*args,**kwargs) :
#         print("called args",args)
#         print("called kwargs",kwargs)
#         return self.func(*args, **kwargs)

# @demo #(duration = 3 )
# def add(x,y):
#     return x+y

# #print(type(add))
# add(3,4)

# '''
# 学习中遇到问题没人解答？小编创建了一个Python学习交流QQ群：857662006
# 寻找有志同道合的小伙伴，互帮互助,群里还有不错的视频学习教程和PDF电子书！
# '''
# import time
# import functools

# class DelayFunc:
#     def __init__(self,  duration, func):
#         self.duration = duration
#         self.func = func

#     def __call__(self, *args, **kwargs):
#         print(f'Wait for {self.duration} seconds...')
#         time.sleep(self.duration)
#         return self.func(*args, **kwargs)

#     def eager_call(self, *args, **kwargs):
#         print('Call without delay')
#         return self.func(*args, **kwargs)

# def delay(duration):
#     """
#     装饰器：推迟某个函数的执行。
#     同时提供 .eager_call 方法立即执行
#     """
#     # 此处为了避免定义额外函数，
#     # 直接使用 functools.partial 帮助构造 DelayFunc 实例
#     return functools.partial(DelayFunc, duration)
# @delay(duration=2)
# def add(a, b):
#     return a+b

# add(3,5)


# import time
# import functools

# class demo:
#     def __init__(self,duration) -> None:
#         self.duration = duration
#     def __call__(self,func):
#         def wrapper(*args, **kwargs):
#             print("print args&kwargs*",args, **kwargs)
#             time.sleep(self.duration)
#             return func(*args, **kwargs)
#         return wrapper

# # 一般而言 如果不是 类修饰器 我们需要的只不过是一个 返回函数的函数，因此我们也必须要把函数的参数传进去
# # 但如果你使用的是类修饰器，首先会根据你传进类构造方法的参数生成一个 对象，这个对象应当是一个 返回函数的函数 能
# @demo(duration=2)
# def add(x,y):
#     return x+y

# print(add(3,4))

# class demo:
#     x=3
#     y=4
#     def __get__(self,func,name=None):
#         print("fucked")

# from  functools import partial
# object

# class father:
#     @demo
#     def a(self):
#         return 3
    
# j = father()
# print(j)
# non_data_descriptor.py

# class NonDataDescriptor(object):
#     """ descriptor example """
#     def __init__(self):
#         self.value = 0

#     def __get__(self, instance, cls):
#         print("non-data descriptor __get__")
#         return self.value + 10
    
#     def __set__(self,instance,value):
#         print("set",value)

# class A(object):
#     attr =  NonDataDescriptor()

# a = A()
# print(a.attr)
# # non-data descriptor __get__
# # 10

# a.attr = 3
# a.attr = 3
# print(a.__dict__) # {'attr': 4} 

