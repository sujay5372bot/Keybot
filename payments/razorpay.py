#jddj
import razorpay
from config import RAZORPAY_KEY, RAZORPAY_SECRET

client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))

def create_link(uid):
    return client.payment_link.create({
        "amount": 9900,
        "currency": "INR",
        "notes": {"user": uid}
    })["short_url"]
