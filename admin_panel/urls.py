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
]
