from django.http import *

def serve_avatar_images(request,filename):
    return JsonResponse({"filename":filename})