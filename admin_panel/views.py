from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.users.models import User, Review, Wishlist
from django.contrib.auth.hashers import make_password
from django import forms

# 自定义用户表单
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'balance', 'is_staff', 'is_superuser']

@login_required
def dashboard(request):
    user_count = User.objects.count()
    review_count = Review.objects.count()
    wishlist_count = Wishlist.objects.count()
    return render(request, 'admin_panel/dashboard.html', {
        'user_count': user_count,
        'review_count': review_count,
        'wishlist_count': wishlist_count,
    })

# 用户管理
@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin_panel/user_list.html', {'users': users})

@login_required
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

@login_required
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

@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('admin_panel:user_list')

# 评价管理
@login_required
def review_list(request):
    reviews = Review.objects.select_related('reviewer', 'seller')
    return render(request, 'admin_panel/review_list.html', {'reviews': reviews})

@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    messages.success(request, "Review deleted successfully!")
    return redirect('admin_panel:review_list')

# 心愿单管理
@login_required
def wishlist_list(request):
    wishlists = Wishlist.objects.select_related('user', 'product')
    return render(request, 'admin_panel/wishlist_list.html', {'wishlists': wishlists})

@login_required
def wishlist_delete(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id)
    wishlist.delete()
    messages.success(request, "Wishlist deleted successfully!")
    return redirect('admin_panel:wishlist_list')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'balance', 'is_staff', 'is_superuser']