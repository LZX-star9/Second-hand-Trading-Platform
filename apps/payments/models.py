from django.db import models



# Create your models here.
#记录用户支付、充值、提现等操作
class Transaction(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw')])
    created_at = models.DateTimeField(auto_now_add=True)