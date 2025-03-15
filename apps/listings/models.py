from django.db import models



# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('home', 'Home & Furniture'),
        ('books', 'Books'),
        ('vehicles', 'Vehicles'),
        ('others', 'Others'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="products")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="others")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# product images
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")
