from django.urls import path

from apps.users.views import user_login, register, user_logout, profile_view, update_profile, add_to_wishlist, \
    remove_from_wishlist, my_wishlist

app_name = 'users'

urlpatterns = [
    path("login/", user_login, name="login"),

    path("register/", register, name="register"),

    path("logout/", user_logout, name="logout"),

    path('profile/', profile_view, name='profile'),

    # path('profile/update/', update_profile, name='update_profile'),

    path("update/", update_profile, name="update_profile"),

    path("add/<int:product_id>/", add_to_wishlist, name="add_to_wishlist"),
    path("remove/<int:product_id>/", remove_from_wishlist, name="remove_from_wishlist"),
    path("my/", my_wishlist, name="my_wishlist"),
]