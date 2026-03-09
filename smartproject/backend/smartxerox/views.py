import email

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, FileResponse, Http404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
import json, uuid, base64, os, random
import razorpay
import urllib.parse
from django.http import JsonResponse
from .models import FAQ
import json
import difflib

from .models import Customer, Order, AdminSettings, PrintOrder


# ======================================
# Razorpay Client
# ======================================
razorpay_client = razorpay.Client(auth=(
    settings.RAZORPAY_KEY_ID,
    settings.RAZORPAY_KEY_SECRET
))


# ======================================
# Pages
# ======================================
def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "About.html")

def services(request):
    return render(request, "Our-services.html")

def contact(request):
    return render(request, "Contact.html")

def privacy(request):
    return render(request, "Privacy-policy.html")

def admin_settings_view(request):
    return render(request, "admin_settings.html")

def printQueue_admin(request):
    return render(request, "print_queue.html")

def send_to_print_queue(request):
    return render(request, "send_to_print.html")

def Stationery(request):
    return render(request, "Stationery.html")


# ======================================
# Signup
# ======================================
@csrf_exempt
def signup(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        if len(password) < 8:
            return JsonResponse({"status": "weak_password"})

        if Customer.objects(email=email).first():
            return JsonResponse({"status": "exists"})

        Customer.objects.create(
            firstname=request.POST.get("firstname"),
            lastname=request.POST.get("lastname"),
            email=email,
            password=make_password(password)
        )

        request.session.flush()
        request.session["user_email"] = email

        return redirect("main")

    return render(request, "Form.html")

def logout_user(request):
    request.session.flush()
    return redirect("index")


def google_callback(request):

    email = request.GET.get("email")

    if not email:
        return redirect("index")

    request.session.flush()
    request.session["user_email"] = email

    return redirect("main")

# ======================================
# Login
# ======================================
@csrf_exempt
def user_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Customer.objects(email=email).first()

        if not user:
            return redirect("index")

        if not check_password(password, user.password):
            return redirect("index")

        request.session.flush()
        request.session["user_email"] = email

        return redirect("main")

    return render(request, "index.html")

def logout_user(request):
    request.session.flush()
    return redirect("index")

# ======================================
# Main
# ======================================
def main(request):

    if "user_email" not in request.session:
        return redirect("index")

    return render(request,"main.html")


def admin_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_orders")

        return render(request, "admin_login.html", {
            "error": "Invalid credentials or not admin"
        })

    return render(request, "admin_login.html")


def logout_admin(request):
    logout(request)
    return redirect("admin_login")

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_staff)
def admin_orders(request):

    orders = Order.objects.order_by("-id")

    return render(request, "admin_orders.html", {
        "orders": orders
    })

def logout_admin(request):
    logout(request)
    return redirect("admin_login")

# ======================================
# CREATE ORDER
# ======================================
@csrf_exempt
def create_order(request):

    if "user_email" not in request.session:
        return JsonResponse({"status": "unauthenticated"}, status=401)

    data = json.loads(request.body.decode("utf-8"))

    pages = int(data.get("pages", 1))
    copies = int(data.get("copies", 1))
    print_type = data.get("printType")
    paper_size = data.get("paperSize")
    college_doc = data.get("collegeDoc")

    # Pricing Logic
    price_per_page = 2

    if print_type == "Colorprint":
        price_per_page = 5

    if paper_size in ["A3", "Letter", "Legal"]:
        price_per_page += 2

    if college_doc and college_doc != "none":
        price_per_page += 5
    total_price = pages * copies * price_per_page
    
    file_data = data.get("fileData")
    file_name = data.get("fileName") 
    file_path = None

    if file_data and ";base64," in file_data:
        
     header, encoded = file_data.split(";base64,")
    file_bytes = base64.b64decode(encoded)

    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    ext = file_name.split('.')[-1]
    safe_name = f"{uuid.uuid4().hex}.{ext}"

    file_path = os.path.join(upload_dir, safe_name)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # Save File
    file_path = None
    if data.get("fileData") and data.get("fileName"):

        header, encoded = data["fileData"].split(",", 1)
        file_bytes = base64.b64decode(encoded)

        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        safe_name = f"{uuid.uuid4().hex}_{data['fileName']}"
        file_path = os.path.join(upload_dir, safe_name)

        with open(file_path, "wb") as f:
            f.write(file_bytes)

    order = Order.objects.create(
        user_email=request.session["user_email"],
        file_path=file_path,
        print_type=print_type,
        pages=pages,
        copies=copies,
        total_price=total_price,
        pickup_code=str(random.randint(1000, 9999)),
        status="Pending"
    )

    return JsonResponse({
    "status": "success",
    "order_id": order.order_id,
    "amount": total_price * 100
})


# ======================================
# Razorpay Order
# ======================================
@csrf_exempt
def create_razorpay_order(request):
    data = json.loads(request.body)
    amount = int(data.get("amount", 0))

    if amount <= 0:
        return JsonResponse({"status": "error"})

    razorpay_order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return JsonResponse({
        "status": "success",
        "order_id": razorpay_order["id"],
        "amount": amount
    })


# ======================================
# Payment Success
# ======================================
import urllib.parse
import random


def payment_success(request):
    order_id = request.GET.get("order_id")
    payment_id = request.GET.get("payment_id")
    
    

    if not order_id:
        return redirect("main")

    # Get order using custom order_id (ORD-XXXX)
    order = Order.objects(order_id=order_id).first()

    if not order:
        return redirect("main")

    # ✅ Update payment status
    order.payment_status = "Paid"

    # ✅ Generate pickup code ONLY if not already generated
    if not order.pickup_code:
        order.pickup_code = str(random.randint(1000, 9999))

    order.save()

    # ✅ Send Email
    try:
        send_mail(
            subject="Smart Xerox Services - Payment Successful",
            message=f"""
Smart Xerox Services

Payment Confirmed ✅

Order ID: {order.order_id}
Pickup Code: {order.pickup_code}

Please show this pickup code while collecting your documents.

Thank you for choosing Smart Xerox Services.
""",
            from_email=settings.EMAIL_HOST_USER,
            # recipient_list=["shekapurampranay@gmail.com"],
            recipient_list=[order.user_email],
            fail_silently=True,
        )
    except:
        pass  # Do not crash if email fail
    # ✅ Professional WhatsApp Message
    message = f"""
🖨️ SMART XEROX SERVICES
━━━━━━━━━━━━━━━
💳 PAYMENT CONFIRMED
━━━━━━━━━━━━━━━

🆔 Order ID : {order.order_id}
🔐 Pickup Code : {order.pickup_code}

⚠ Please keep this code safe.
Required during document collection.

Thank you for trusting Smart Xerox!
"""

    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/?text={encoded_message}"

    # ✅ Return Success Page
    return render(request, "payment_success.html", {
        "order_id": order.order_id,
        "payment_id": payment_id,
        "pickup_code": order.pickup_code,
        "whatsapp_url": whatsapp_url
    })

def payment_page(request):

    amount = request.GET.get("amount", "0")
    order_id = request.GET.get("order_id", "")

    return render(request, "payment_page.html", {
        "amount": amount,
        "order_id": order_id,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID
    })


@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_staff)
def admin_settings_view(request):

    settings_obj = AdminSettings.objects.first()

    if not settings_obj:
        settings_obj = AdminSettings.objects.create()

    if request.method == "POST":
        settings_obj.theme = "dark" if request.POST.get("theme") == "on" else "light"
        settings_obj.max_upload_size = request.POST.get("maxUploadSize")
        settings_obj.auto_delete_days = request.POST.get("autoDeleteDays")
        settings_obj.allowed_formats = request.POST.getlist("formats")
        settings_obj.working_start_time = request.POST.get("startTime")
        settings_obj.working_end_time = request.POST.get("endTime")

        settings_obj.save()
        return redirect("admin_settings")

    return render(request, "admin_settings.html", {"settings": settings_obj})

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_staff)
def printQueue_admin(request):

    orders = Order.objects.filter(status="Approved").order_by("-id")

    return render(request, "printQueue_admin.html", {
        "orders": orders
    })

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_staff)
def send_to_print_queue(request):

    if request.method == "POST":
        order_id = request.POST.get("order_id")

        order = Order.objects.get(id=order_id)

        # Update order status
        order.status = "Printed"
        order.save()

        # Create entry in PrintOrder collection
        PrintOrder.objects.create(
            order_id=str(order.id),
            customer_name=order.user_email,
            file_name=os.path.basename(order.file_path) if order.file_path else "No File",
            pages=order.pages,
            copies=order.copies,
            print_type=order.print_type,
            status="waiting"
        )

    return redirect("printQueue_admin")

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_staff)
def printQueue_admin(request):

    orders = PrintOrder.objects.order_by("-id")

    return render(request, "printQueue_admin.html", {
        "orders": orders
    })



from django.http import FileResponse, Http404
import os

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_staff)
def open_print_file(request, order_id):

    order = Order.objects(order_id=order_id).first()

    if not order:
        raise Http404("Order not found")

    if not order.file_path:
        raise Http404("File not uploaded")

    if not os.path.exists(order.file_path):
        raise Http404("File not found")

    # ✅ Custom filename for printing
    filename = f"Order_{order.order_id}_{order.user_email}.pdf"

    response = FileResponse(
        open(order.file_path, "rb"),
        content_type="application/pdf"
    )

    response["Content-Disposition"] = f'inline; filename="{filename}"'

    return response





from django.core.mail import send_mail
from django.conf import settings
import json
import razorpay


@csrf_exempt
def verify_payment(request):
    if request.method == "POST":

        data = json.loads(request.body)

        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_signature = data.get("razorpay_signature")
        email = data.get("email")   # 👈 coming from frontend

        client = razorpay.Client(auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        ))

        params_dict = {
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_order_id": razorpay_order_id,
            "razorpay_signature": razorpay_signature
        }

        try:
            # ✅ Verify signature
            client.utility.verify_payment_signature(params_dict)

            # ✅ Get order from DB
            order = Order.objects.get(order_id=razorpay_order_id)

            # ✅ Update order
            order.payment_status = "Paid"
            order.customer_email = email
            order.save()

            # ✅ SEND EMAIL HERE
            send_mail(
                subject="Smart Xerox - Payment Successful",
                message=f"""
Hi,

Your payment was successful!

Order ID: {order.order_id}
Payment ID: {razorpay_payment_id}

Thank you for using Smart Xerox Services.
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            return JsonResponse({"status": "success"})

        except Exception as e:
            print("Verification Error:", e)
            return JsonResponse({"status": "failed"})

        
def admin_orders(request):
    orders = Order.objects.filter(payment_status="Paid").order_by("-created_at")
    return render(request, "admin_order.html", {"orders": orders})



# FAQ PAGE VIEW
def faq_page(request):
    return render(request, "Faq.html")


# CHATBOT INTELLIGENT RESPONSE
def chatbot_response(request):

    if request.method == "POST":

        data = json.loads(request.body)
        user_message = data.get("message", "").lower()

        faqs = FAQ.objects.all()

        best_match = None
        highest_score = 0

        for faq in faqs:
            score = difflib.SequenceMatcher(
                None,
                user_message,
                faq.question.lower()
            ).ratio()

            if score > highest_score:
                highest_score = score
                best_match = faq

        # If match found
        if best_match and highest_score > 0.4:
            return JsonResponse({
                "reply": best_match.answer
            })

        # If no good match
        return JsonResponse({
            "reply": "Sorry, I couldn’t find a related answer. Please contact support."
        })

    # If not POST request
    return JsonResponse({
        "reply": "Invalid request method."
    })