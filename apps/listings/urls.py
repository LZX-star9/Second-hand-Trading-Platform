# apps/listings/urls.py
from django.urls import path
from .views import index, product_detail

app_name = 'listings'

urlpatterns = [
    path('', index, name='index'),  # 主页路由

    path('product_detail/<int:product_id>/',product_detail,name='product_detail'),
]
