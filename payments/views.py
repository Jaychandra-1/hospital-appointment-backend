import razorpay
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from notifications.models import Notification

client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)

@api_view(["POST"])
def create_order(request):
    amount = request.data.get("amount")

    order = client.order.create({
        "amount": int(amount) * 100,
        "currency": "INR",
        "payment_capture": 1
    })

    return Response({
        "key": settings.RAZORPAY_KEY_ID,
        "amount": order["amount"],
        "order_id": order["id"]
    })
