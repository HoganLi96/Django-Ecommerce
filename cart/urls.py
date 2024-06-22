from django.urls import path
from cart.views import *


app_name = 'cart'
urlpatterns = [
    path('gio-hang/', gio_hang, name='gio_hang'),
    path('thanh-toan/', thanh_toan, name='thanh_toan'),
    path('mua-ngay/<int:product_id>/', mua_ngay, name='mua_ngay'),
    path('xoa-san-pham/<int:product_id>/', xoa_san_pham, name='xoa_san_pham'),
]
