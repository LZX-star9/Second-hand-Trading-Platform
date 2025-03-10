from django.urls import path

from apps.messagings.views import chat_with_seller

app_name = 'messagings'

urlpatterns = [

    path("chat/", chat_with_seller, name="chat_with_seller")

]