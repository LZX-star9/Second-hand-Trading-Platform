from django.shortcuts import render

# Create your views here.
# apps/listings/views.py
from .models import Product  # 导入商品模型

def index(request):
    items = Product.objects.prefetch_related("images").all()  # 预加载图片，避免多次查询
    return render(request, "listings/index.html", {"items": items})
