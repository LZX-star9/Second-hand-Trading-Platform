# apps/listings/urls.py
from django.urls import path
from .views import index, product_detail, new_product
from . import views
app_name = 'listings'

urlpatterns = [
    path('', index, name='index'),  # 主页路由

    path('product_detail/<int:product_id>/',product_detail,name='product_detail'),

    path("new_product/", new_product, name="new_product"),
    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),
]
