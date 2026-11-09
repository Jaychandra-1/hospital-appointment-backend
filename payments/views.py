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
    try:
        amount = request.data.get("amount")

        if not amount:
            return Response(
                {"error": "Amount is required"},
                status=400
            )

        amount_paise = int(amount) * 100

        order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1
        })

        return Response({
            "key": settings.RAZORPAY_KEY_ID,
            "amount": order["amount"],
            "order_id": order["id"]
        })

    except Exception as e:
        print("RAZORPAY ORDER ERROR:", repr(e))
        return Response(
            {"error": str(e)},
            status=500
        )