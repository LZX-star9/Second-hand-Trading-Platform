from django.urls import path

from apps.messagings.views import chat_with_seller, load_new_messages, chat, chat_detail

app_name = 'messagings'

urlpatterns = [
    path('chat/', chat, name='chat'),
    path("chat/<int:seller_id>/<int:product_id>/", chat_with_seller, name="chat_with_seller_product"),
    path('chat/<int:seller_id>/', chat_with_seller, name='chat_with_seller'),
    # 仅在做AJAX轮询时使用
    path('chat/<int:seller_id>/', chat_detail, name='chat_detail'),
    path("chat/new_messages/<int:seller_id>/", load_new_messages, name="load_new_messages"),
    path("chat/new_messages/<int:seller_id>/<int:product_id>/", load_new_messages, name="load_new_messages_product"),



]