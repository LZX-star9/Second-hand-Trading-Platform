from django.shortcuts import render

# Create your views here.

@login_required
def chat_with_seller(request, product_id):
    # Implement chat functionality here
    return render(request, 'chat_with_seller.html')