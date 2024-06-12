from rest_framework import routers
from A37 import views
from django.urls import path,include

import sys
print(sys.path)

router = routers.DefaultRouter()
router.register("usr",viewset=views.UsrModelViewSet)
router.register("ins",viewset=views.InsModelViewSet)
router.register("outs",viewset=views.OutsModelViewSet)
router.register("own",viewset=views.OwnModelViewSet)
router.register("info",viewset=views.InfoModelViewSet)
router.register("room",viewset=views.RoomModelViewSet)


urlpatterns = [
    # path("a37/usr/all",views.usr_view),
    # path("a37/outs/all",views.outs_view),
    # path("a37/consumption/query",views.consumption_query),
    # path("a37/avatar/upload",views.avatar_upload),
    # path("a37/avatar/get",views.avatar_get),
    path("index", views.index_view),
    path("login",views.login),
    path("verifycode",views.verification_code_GET),
    path("ins-query",views.ins_query),
    path("outs-query",views.outs_query),
    path("log",views.log),
    path("auth-alipay",views.auth_alipay),
    path("avatar-post",views.avatar_post),
    path("recog-post",views.recognize_img),
    path("outs-pic-post",views.outs_post),
    path("ins-pic-post",views.ins_post),
    path("chatgpt-ask",views.chatgpt_ask),
    path("room-login",views.room_login),
    path("check-create-own-relation",views.check_and_create_own_relation),
    path("number-extract",views.number_extract),
    # path("long_polling_update_info",views.long_polling_update_info),
] + router.urls