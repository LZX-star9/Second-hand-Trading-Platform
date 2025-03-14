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
from ..orders.models import Order
from ..users.models import Wishlist, Review

CATEGORY_CHOICES = [
    ('electronics', 'Electronics'),
    ('clothing', 'Clothing'),
    ('home', 'Home & Furniture'),
    ('books', 'Books'),
    ('vehicles', 'Vehicles'),
    ('others', 'Others'),
]
def index(request):
    category = request.GET.get('category', None)
    query = request.GET.get('q', None)
    sort_by = request.GET.get('sort', 'created_at')

    products = Product.objects.filter(is_sold=False)

    if category:
        products = products.filter(category=category)

    if query:
        products = products.filter(title__icontains=query)

    # 排序
    if sort_by in ['price', '-price', 'created_at', '-created_at', 'title', '-title']:
        products = products.order_by(sort_by)

    # 分页
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listings/index.html', {
        'items': page_obj,
        'CATEGORY_CHOICES': CATEGORY_CHOICES
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    seller = product.seller
    reviews = Review.objects.filter(seller=seller)
    return render(request, "product_detail.html", {"product": product, "related_products": related_products,"seller_reviews": reviews})


@login_required
def new_product(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        files = request.FILES.getlist("images")

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()

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
                remain = buyer.balance
                buyer.save()
                product.is_sold = True
                product.save()
                Wishlist.objects.filter(user=buyer,product=product).delete()
                Order.objects.create(buyer=buyer, product=product, total_price=product.price)

            return JsonResponse({
                "success": True,
                "redirect_url": reverse('listings:index'),
                "remain": remain
            })

        else:
            return JsonResponse({"success": False, "error": "Insufficient balance"})

    return JsonResponse({"error": "Invalid request"}, status=400)