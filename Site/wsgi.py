"""
WSGI config for Site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Site.settings")

# application = get_wsgi_application()

# 上面是不知道哪里提供的


import os
from os.path import join,dirname,abspath
 
PROJECT_DIR = dirname(dirname(abspath(__file__)))#3
import sys # 4
sys.path.insert(0,PROJECT_DIR) # 5
 
#上面这个一定要把blog改成你自己的网站名
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Site.settings")
 
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
