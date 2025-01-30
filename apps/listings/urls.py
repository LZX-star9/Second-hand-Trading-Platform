# apps/listings/urls.py
from django.urls import path
from .views import index

app_name = 'listings'

urlpatterns = [
    path('', index, name='index'),  # 主页路由
]
