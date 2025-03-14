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
    """
    用于前端轮询：返回新消息 JSON 列表
    (可选：如果不做轮询，可以不写这个视图)
    """
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

    # 转成列表排序：按最新一条消息时间逆序
    conversation_list = sorted(
        conversation_set.values(),
        key=lambda x: x["last_timestamp"],
        reverse=True
    )

    # 2) 右侧聊天对象
    # 如果没给 seller_id，右侧可以留空
    chat_messages = []
    seller = None
    product = None
    if seller_id:
        seller = get_object_or_404(User, pk=seller_id)
        # 校验 product
        if product_id:
            product = get_object_or_404(Product, pk=product_id)
        # 查询双方的消息
        chat_qs = Message.objects.filter(
            (Q(sender=current_user, receiver=seller) | Q(sender=seller, receiver=current_user))
        )
        if product:
            chat_qs = chat_qs.filter(product=product)
        chat_messages = chat_qs.order_by("timestamp")

        if request.method == "POST":
            content = request.POST.get("content", "").strip()
            if content:
                # 创建消息
                Message.objects.create(
                    sender=current_user,
                    receiver=seller,
                    product=product,
                    content=content
                )
            # 重定向避免表单重复提交
            if product_id:
                return redirect("messagings:chat_with_seller_product", seller_id=seller_id, product_id=product_id)
            else:
                return redirect("messagings:chat_with_seller", seller_id=seller_id)

    return render(request, "chat.html", {
        "conversation_list": conversation_list,  # 左侧对话列表
        "seller": seller,                        # 右侧聊天对象
        "product": product,
        "chat_messages": chat_messages,
    })

@login_required
def chat(request):
    """
    显示当前用户所有对话列表(左侧)，右侧可为空(或默认显示最近一个对话)。
    """
    current_user = request.user

    # 1) 构造对话列表
    # 先查询用户相关的所有消息
    messages_qs = Message.objects.filter(Q(sender=current_user) | Q(receiver=current_user))

    # 用 (对方user, product) 做分组，或只用对方user
    # 这里先演示只基于对方user分组
    conversation_set = {}
    for msg in messages_qs.select_related('sender','receiver','product'):
        other_user = msg.receiver if msg.sender == current_user else msg.sender
        key = other_user.id
        # 如果需要区分product则 key = (other_user.id, msg.product.id if msg.product else None)
        if key not in conversation_set:
            conversation_set[key] = {
                "other_user": other_user,
                "last_timestamp": msg.timestamp
            }
        else:
            # 更新为最新时间
            if msg.timestamp > conversation_set[key]["last_timestamp"]:
                conversation_set[key]["last_timestamp"] = msg.timestamp

    # 转化成列表并按时间倒序
    conversation_list = sorted(
        conversation_set.values(),
        key=lambda x: x["last_timestamp"],
        reverse=True
    )

    # 2) 右侧可以空白，也可以默认显示第一项
    # 这里示例：就留空
    return render(request, "chat.html", {
        "conversation_list": conversation_list,
        "chat_messages": None,  # 不展示具体对话
    })


@login_required
def chat_detail(request, seller_id):
    """
    左侧列表 & 右侧和 seller_id 的聊天明细
    """
    current_user = request.user
    seller = get_object_or_404(User, pk=seller_id)

    # 1) 左侧对话列表（同上）
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

    # 2) 右侧和 seller 的消息列表
    chat_messages = Message.objects.filter(
        (Q(sender=current_user, receiver=seller) | Q(sender=seller, receiver=current_user))
    ).order_by('timestamp')

    # 如果用户提交了新消息
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
        "conversation_list": conversation_list,  # 左侧
        "chat_messages": chat_messages,  # 右侧
        "seller": seller
    })
