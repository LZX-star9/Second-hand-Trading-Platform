import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout

from apps.listings.models import Product
from apps.users.forms import  UserProfileUpdateForm
from apps.users.models import User, Wishlist
from decimal import Decimal

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("listings:index")  # 登录成功跳转首页
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone = request.POST["phone"]
        email = request.POST.get("email", "")
        address = request.POST.get("address", "")
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # 确保两次密码一致
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, "register.html")

        # 检查用户名或手机号是否已存在
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "register.html")

        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered!")
            return render(request, "register.html")

        # 创建新用户
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            address=address,
            password=password1,
        )

        login(request, user)  # 自动登录
        return redirect("listings:index")  # 注册成功后跳转首页

    return render(request, "register.html")



def user_logout(request):
    logout(request)  # 退出用户
    return redirect("listings:index")


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def update_profile(request):
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("users:profile")
    else:
        form = UserProfileUpdateForm(instance=request.user)

    return render(request, "profile.html", {"form": form})


@login_required
def add_to_wishlist(request, product_id):
    """ 添加商品到收藏夹 """
    product = get_object_or_404(Product, id=product_id)

    if Wishlist.objects.filter(user=request.user, product=product).exists():
        messages.warning(request, "This product is already in your wishlist.")
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, "Added to your wishlist!")

    return redirect("listings:product_detail", product_id=product_id)

@login_required
def remove_from_wishlist(request, product_id):
    """ 从收藏夹移除商品 """
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product)

    if wishlist_item.exists():
        wishlist_item.delete()
        messages.success(request, "Removed from your wishlist.")
    else:
        messages.warning(request, "This product is not in your wishlist.")

    return redirect("users:my_wishlist")

@login_required
def my_wishlist(request):
    """ 显示用户的收藏夹 """
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related("product")
    return render(request, "my_wishlist.html", {"wishlist_items": wishlist_items})


@login_required
def add_to_favorite(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

        if not created:
            wishlist_item.delete()
            return JsonResponse({"status": "removed"})

        return JsonResponse({"status": "added"})

    return JsonResponse({"error": "Invalid request"}, status=400)

def recharge_view(request):
    if request.method == "POST":
        amount = request.POST.get("amount")

        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError("Invalid amount")
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid amount.")
            return redirect("users:recharge")


        request.user.balance += amount
        request.user.save()

        messages.success(request, f"Successfully added £{amount} to your balance!")
        return redirect("users:profile")  # 充值成功后跳转到 profile 页面

    return render(request, "recharge.html")