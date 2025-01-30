from django.db import models



# Create your models here.

#订单
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    buyer = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="orders")
    product = models.OneToOneField('listings.Product', on_delete=models.CASCADE, related_name="order")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} - {self.status}"
