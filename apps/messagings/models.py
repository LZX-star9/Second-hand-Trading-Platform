from django.db import models



# Create your models here.
#交易私信
class Message(models.Model):
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="received_messages")
    product = models.ForeignKey('listings.Product', on_delete=models.CASCADE, related_name="messages", null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

