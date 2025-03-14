from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect

from apps.listings.models import Product
from apps.orders.models import Order
from apps.users.models import Review


# Create your views here.
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Only buyer and seller and see the order
    if order.buyer != request.user and order.product.seller != request.user:
        return render(request, "forbidden.html", status=403)

    return render(request, "order_detail.html", {"order": order})


@login_required
def order_list(request):
    user_orders = Order.objects.filter(buyer=request.user).order_by("-order_date")
    # seller_orders = Order.objects.filter(product__seller=request.user)
    # user_orders = user_orders.union(seller_orders).distinct()

    return render(request, "order_list.html", {"orders": user_orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.buyer != request.user and order.product.seller != request.user:
        return render(request, "forbidden.html", status=403)

    show_review_popup = request.GET.get("review_popup", "0") == "1"

    return render(request, "order_detail.html", {
        "order": order,
        "show_review_popup": show_review_popup,
    })


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.buyer != request.user:
        messages.error(request, "Only buyer can cancel the order.")
        return redirect("orders:order_detail", order_id=order_id)

    if order.status == "completed":
        messages.warning(request, "Order is already completed, cannot cancel.")
    else:
        order.status = "canceled"
        order.save()
        # Mark the product as available
        product = get_object_or_404(Product, id=order.product.id)
        product.is_sold = False
        product.save()
        buyer = order.buyer
        buyer.balance += product.price
        buyer.save()
        messages.success(request, f"Order #{order.id} has been canceled.")

    return redirect("orders:order_detail", order_id=order_id)


@login_required
@transaction.atomic
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if (order.buyer != request.user and order.product.seller != request.user):
        messages.error(request, "You don't have permission to complete this order.")
        return redirect("orders:order_detail", order_id=order_id)

    if order.status == "canceled":
        messages.warning(request, "Order is canceled, cannot mark completed.")
    else:
        order.status = "completed"
        order.save()
        seller = order.product.seller
        seller.balance += order.total_price
        seller.save()
        messages.success(request, f"Order #{order.id} completed!")
        return redirect(f"/order/{order_id}/?review_popup=1")

    return redirect("orders:order_detail", order_id=order_id)

@login_required
def submit_review(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.buyer != request.user:
        messages.error(request, "You are not allowed to review this seller.")
        return redirect("orders:order_detail", order_id=order_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "")
        if rating:
            Review.objects.create(
                reviewer=request.user,
                seller=order.product.seller,
                rating=int(rating),
                comment=comment
            )
            messages.success(request, "Review submitted successfully!")
        else:
            messages.error(request, "Rating required.")

    return redirect("orders:order_detail", order_id=order_id)
