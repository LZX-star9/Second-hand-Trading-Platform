from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import NewListingForm
# Create your views here.
# apps/listings/views.py
from .models import Product, ProductImage  # 导入商品模型

CATEGORY_CHOICES = [
    ('electronics', 'Electronics'),
    ('clothing', 'Clothing'),
    ('home', 'Home & Furniture'),
    ('books', 'Books'),
    ('vehicles', 'Vehicles'),
    ('others', 'Others'),
]
def index(request):
    """ 商品列表视图，支持分类筛选、搜索、排序和分页 """
    category = request.GET.get('category', None)
    query = request.GET.get('q', None)
    sort_by = request.GET.get('sort', 'created_at')  # 默认按创建时间排序

    products = Product.objects.filter(is_sold=False)  # 只显示未售出的商品

    if category:
        products = products.filter(category=category)

    if query:
        products = products.filter(title__icontains=query)

    # 排序
    if sort_by in ['price', '-price', 'created_at', '-created_at', 'title', '-title']:
        products = products.order_by(sort_by)

    # 分页
    paginator = Paginator(products, 4)  # 每页4个商品
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listings/index.html', {
        'items': page_obj,
        'CATEGORY_CHOICES': CATEGORY_CHOICES
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, "product_detail.html", {"product": product, "related_products": related_products})


@login_required
def new_product(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)  # 这里不要传 `request.FILES`
        files = request.FILES.getlist("images")  # 获取所有上传的图片

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # 赋值当前用户
            product.save()  # 先保存 Product

            # 遍历所有上传的图片并保存
            for file in files:
                ProductImage.objects.create(product=product, image=file)

            return redirect("listings:product_detail", product_id=product.id)

    else:
        form = NewListingForm()
    return render(request, "new_product.html", {"form": form})

@login_required
def buy_now(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        buyer = request.user
        seller = product.seller

        if buyer == seller:
            return JsonResponse({"success": False, "error": "You cannot buy your own product."})

        if buyer.balance >= product.price:
            with transaction.atomic():
                buyer.balance -= product.price
                buyer.save()

                seller.balance += product.price
                seller.save()

                product.is_sold = True
                product.save()

            return JsonResponse({
                "success": True,
                "redirect_url": reverse('listings:index')
            })

        else:
            return JsonResponse({"success": False, "error": "Insufficient balance"})

    return JsonResponse({"error": "Invalid request"}, status=400)