from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from admin_panel.forms import UserForm, ProductForm
from apps.users.models import User, Review, Wishlist
from django.contrib.auth.hashers import make_password
from django import forms
from apps.listings.models import Product

def dashboard(request):
    user_count = User.objects.count()
    review_count = Review.objects.count()
    wishlist_count = Wishlist.objects.count()
    product_count = Product.objects.count()
    return render(request, 'admin_panel/dashboard.html', {
        'user_count': user_count,
        'review_count': review_count,
        'wishlist_count': wishlist_count,
        'product_count': product_count,
    })


def user_list(request):
    users = User.objects.all()
    return render(request, 'admin_panel/user_list.html', {'users': users})


def user_add(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password('defaultpassword')  # 默认密码
            user.save()
            messages.success(request, "User added successfully!")
            return redirect('admin_panel:user_list')
    else:
        form = UserForm()
    return render(request, 'admin_panel/user_form.html', {'form': form})


def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully!")
            return redirect('admin_panel:user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'admin_panel/user_form.html', {'form': form})


def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('admin_panel:user_list')


def review_list(request):
    reviews = Review.objects.select_related('reviewer', 'seller')
    return render(request, 'admin_panel/review_list.html', {'reviews': reviews})


def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    messages.success(request, "Review deleted successfully!")
    return redirect('admin_panel:review_list')


def wishlist_list(request):
    wishlists = Wishlist.objects.select_related('user', 'product')
    return render(request, 'admin_panel/wishlist_list.html', {'wishlists': wishlists})


def wishlist_delete(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id)
    wishlist.delete()
    messages.success(request, "Wishlist deleted successfully!")
    return redirect('admin_panel:wishlist_list')





def product_list(request):
    products = Product.objects.all()
    return render(request, 'admin_panel/product_list.html', {'products': products})


def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('admin_panel:product_list')
    else:
        form = ProductForm()
    return render(request, 'admin_panel/product_form.html', {'form': form})

def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('admin_panel:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_panel/product_form.html', {'form': form})

def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('admin_panel:product_list')