from django.urls import path
from customer.views import *


app_name = 'customer'
urlpatterns = [
    path('dang-nhap/', dang_nhap, name='dang_nhap'),
    path('dang-xuat/', dang_xuat, name='dang_xuat'),
    path('tai-khoan-cua-toi/', tai_khoan_cua_toi, name='tai_khoan_cua_toi'),
]
