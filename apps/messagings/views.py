from apps.listings.models import Product
from apps.users.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import Message
from django.contrib import messages

@login_required
def load_new_messages(request, seller_id, product_id=None):
    seller = get_object_or_404(User, pk=seller_id)
    product = None
    if product_id:
        product = get_object_or_404(Product, pk=product_id, seller=seller)

    last_msg_id = request.GET.get("last_id", None)

    chat_qs = Message.objects.filter(
        (Q(sender=request.user, receiver=seller) | Q(sender=seller, receiver=request.user))
    )
    if product:
        chat_qs = chat_qs.filter(product=product)

    if last_msg_id:
        chat_qs = chat_qs.filter(id__gt=last_msg_id)
    chat_qs = chat_qs.order_by("timestamp")

    # 返回 JSON
    data = []
    for msg in chat_qs:
        data.append({
            "id": msg.id,
            "sender_id": msg.sender.id,
            "sender_username": msg.sender.username,
            "content": msg.content,
            "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return JsonResponse({"chat_messages": data})

@login_required
def chat_with_seller(request, seller_id=None, product_id=None):
    current_user = request.user
    if seller_id == current_user.id:
        messages.error(request, "You cannot chat with yourself.")
        return redirect("listings:product_detail", product_id)
    messages_qs = Message.objects.filter(
        Q(sender=current_user) | Q(receiver=current_user)
    ).select_related("sender", "receiver", "product")
    conversation_set = {}
    for msg in messages_qs:
        if msg.sender == current_user:
            other = msg.receiver
        else:
            other = msg.sender

        key = (other.id, msg.product.id if msg.product else None)
        if key not in conversation_set:
            conversation_set[key] = {
                "other_user": other,
                "product": msg.product,
                "last_timestamp": msg.timestamp
            }
        else:
            if msg.timestamp > conversation_set[key]["last_timestamp"]:
                conversation_set[key]["last_timestamp"] = msg.timestamp

    conversation_list = sorted(
        conversation_set.values(),
        key=lambda x: x["last_timestamp"],
        reverse=True
    )

    chat_messages = []
    seller = None
    product = None
    if seller_id:
        seller = get_object_or_404(User, pk=seller_id)
        if product_id:
            product = get_object_or_404(Product, pk=product_id)
        chat_qs = Message.objects.filter(
            (Q(sender=current_user, receiver=seller) | Q(sender=seller, receiver=current_user))
        )
        if product:
            chat_qs = chat_qs.filter(product=product)
        chat_messages = chat_qs.order_by("timestamp")

        if request.method == "POST":
            content = request.POST.get("content", "").strip()
            if content:
                Message.objects.create(
                    sender=current_user,
                    receiver=seller,
                    product=product,
                    content=content
                )
            if product_id:
                return redirect("messagings:chat_with_seller_product", seller_id=seller_id, product_id=product_id)
            else:
                return redirect("messagings:chat_with_seller", seller_id=seller_id)

    return render(request, "chat.html", {
        "conversation_list": conversation_list,
        "seller": seller,
        "product": product,
        "chat_messages": chat_messages,
    })

@login_required
def chat(request):
    current_user = request.user
    messages_qs = Message.objects.filter(Q(sender=current_user) | Q(receiver=current_user))
    conversation_set = {}
    for msg in messages_qs.select_related('sender','receiver','product'):
        other_user = msg.receiver if msg.sender == current_user else msg.sender
        key = other_user.id
        if key not in conversation_set:
            conversation_set[key] = {
                "other_user": other_user,
                "last_timestamp": msg.timestamp
            }
        else:
            if msg.timestamp > conversation_set[key]["last_timestamp"]:
                conversation_set[key]["last_timestamp"] = msg.timestamp

    conversation_list = sorted(
        conversation_set.values(),
        key=lambda x: x["last_timestamp"],
        reverse=True
    )
    return render(request, "chat.html", {
        "conversation_list": conversation_list,
        "chat_messages": None,
    })


@login_required
def chat_detail(request, seller_id):
    current_user = request.user
    seller = get_object_or_404(User, pk=seller_id)
    messages_qs = Message.objects.filter(Q(sender=current_user) | Q(receiver=current_user))
    conversation_set = {}
    for msg in messages_qs.select_related('sender', 'receiver', 'product'):
        other_user = msg.receiver if msg.sender == current_user else msg.sender
        key = other_user.id
        if key not in conversation_set:
            conversation_set[key] = {
                "other_user": other_user,
                "last_timestamp": msg.timestamp
            }
        else:
            if msg.timestamp > conversation_set[key]["last_timestamp"]:
                conversation_set[key]["last_timestamp"] = msg.timestamp
    conversation_list = sorted(
        conversation_set.values(),
        key=lambda x: x["last_timestamp"],
        reverse=True
    )
    chat_messages = Message.objects.filter(
        (Q(sender=current_user, receiver=seller) | Q(sender=seller, receiver=current_user))
    ).order_by('timestamp')

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            Message.objects.create(
                sender=current_user,
                receiver=seller,
                content=content
            )
        return redirect("chat_detail", seller_id=seller_id)

    return render(request, "chat.html", {
        "conversation_list": conversation_list,
        "chat_messages": chat_messages,
        "seller": seller
    })
