from django.urls import path

from apps.orders.views import order_list, order_detail, cancel_order, complete_order, submit_review

app_name = 'orders'

urlpatterns = [
    path("list/", order_list, name="order_list"),
    path("<int:order_id>/", order_detail, name="order_detail"),
    path("<int:order_id>/cancel/", cancel_order, name="cancel_order"),
    path("<int:order_id>/complete/", complete_order, name="complete_order"),
    path("<int:order_id>/submit_review/", submit_review, name="submit_review"),

]