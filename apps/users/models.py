# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 账户余额

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="given_reviews",null=True)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="received_reviews",null=True)
    rating = models.IntegerField()  # 1-5星评分
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey('listings.Product', on_delete=models.CASCADE, related_name="wishlisted_by")
    added_at = models.DateTimeField(auto_now_add=True)



