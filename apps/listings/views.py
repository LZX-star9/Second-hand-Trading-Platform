from django.shortcuts import render, get_object_or_404

# Create your views here.
# apps/listings/views.py
from .models import Product  # 导入商品模型

def index(request):
    items = Product.objects.prefetch_related("images").all()  # 预加载图片，避免多次查询
    return render(request, "listings/index.html", {"items": items})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, "product_detail.html", {"product": product, "related_products": related_products})