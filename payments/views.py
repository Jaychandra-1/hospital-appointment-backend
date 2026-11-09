
import razorpay
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)


@api_view(["POST"])
def create_order(request):
    amount = request.data.get("amount")

    if not amount:
        return Response({"error": "Amount is required"}, status=400)

    try:
        amount_paise = int(amount) * 100

        if amount_paise <= 0:
            return Response({"error": "Invalid amount"}, status=400)

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
            {"error": "Unable to create payment order"},
            status=500
        )


@api_view(["POST"])
def verify_payment(request):
    razorpay_order_id = request.data.get("razorpay_order_id")
    razorpay_payment_id = request.data.get("razorpay_payment_id")
    razorpay_signature = request.data.get("razorpay_signature")

    if not all([
        razorpay_order_id,
        razorpay_payment_id,
        razorpay_signature
    ]):
        return Response(
            {"error": "Payment verification details are required"},
            status=400
        )

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })

        return Response({
            "success": True,
            "message": "Payment signature verified successfully"
        })

    except razorpay.errors.SignatureVerificationError:
        return Response({
            "success": False,
            "message": "Payment signature verification failed"
        }, status=400)

    except Exception as e:
        print("RAZORPAY VERIFICATION ERROR:", repr(e))
        return Response(
            {"error": "Payment verification could not be completed"},
            status=500
        )
