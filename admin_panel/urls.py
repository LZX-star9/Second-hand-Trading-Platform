from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/edit/<int:user_id>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),

    path('reviews/', views.review_list, name='review_list'),
    path('reviews/delete/<int:review_id>/', views.review_delete, name='review_delete'),

    path('wishlists/', views.wishlist_list, name='wishlist_list'),
    path('wishlists/delete/<int:wishlist_id>/', views.wishlist_delete, name='wishlist_delete'),

    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/edit/<int:product_id>/', views.product_edit, name='product_edit'),
    path('products/delete/<int:product_id>/', views.product_delete, name='product_delete'),
]
