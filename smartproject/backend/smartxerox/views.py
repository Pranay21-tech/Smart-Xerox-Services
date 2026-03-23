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
from urllib3 import request
from .models import FAQ, Payment
import json
import difflib
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation
from .models import UploadDocument
from .models import Customer, Order, AdminSettings, PrintOrder
from django.shortcuts import get_object_or_404, redirect



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

def form_page(request):
    return render(request, "form.html")

def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "our-services.html")

def contact(request):
    return render(request, "contact.html")

def privacy(request):
    return render(request, "privacy-policy.html")

def admin_settings_view(request):
    return render(request, "admin_settings.html")

# def printQueue_admin(request):
#     return render(request, "print_queue.html")  

def send_to_print_queue(request):
    return render(request, "send_to_print.html")

def Stationery(request):
    return render(request, "stationery.html")

def pdf_printing(request):
    return render(request, "pdf_printing.html")

def college_documents(request):
    return render(request, "college_documents.html")

def main(request):
    return render(request, "main.html")


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

        request.session["user_email"] = email

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "invalid"})

def logout_user(request):
    request.session.flush()
    return redirect("index")


def google_callback(request):
    email = request.GET.get("email")

    if not email:
        return redirect("index")

    # Clear only old session data if needed
    request.session.clear()

    # Save user email
    request.session["user_email"] = email

    return redirect("main")




def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")
        new_password = request.POST.get("password")

        user = Customer.objects(email=email).first()

        if not user:
            return render(request,"forgot_password.html",{"error":"Email not found"})

        user.password = make_password(new_password)
        user.save()

        return redirect("index")

    return render(request,"forgot_password.html")

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

        if user and user.is_staff:
            login(request, user)
            return redirect("admin_orders")

        return render(request, "admin_login.html", {"error": "Invalid credentials"})

    return render(request, "admin_login.html")


def admin_orders(request):

    if not request.session.get("admin_logged"):
        return redirect("admin_login")

    orders = Order.objects.all()
    return render(request, "admin_orders.html", {"orders": orders})


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

    manual_pages = int(data.get("pages", 0))
    copies = int(data.get("copies", 1))
    print_type = data.get("printType")
    paper_size = data.get("paperSize")
    college_doc = data.get("collegeDoc")

    file_data = data.get("fileData")
    file_name = data.get("fileName")
    file_path = None

    pdf_pages = 1   # ✅ default safe value

    # =========================
    # SAVE FILE
    # =========================
    if file_data and file_name:
        try:
            header, encoded = file_data.split(",", 1)
            file_bytes = base64.b64decode(encoded)

            upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
            os.makedirs(upload_dir, exist_ok=True)

            safe_name = f"{uuid.uuid4().hex}_{file_name}"
            file_path = os.path.join(upload_dir, safe_name)

            with open(file_path, "wb") as f:
                f.write(file_bytes)

            # =========================
            # DOCUMENT PAGE DETECTION
            # =========================
            ext = file_name.split(".")[-1].lower()

            if ext == "pdf":
                reader = PdfReader(file_path)
                pdf_pages = len(reader.pages)

            elif ext in ["doc", "docx"]:
                doc = Document(file_path)
                pdf_pages = max(len(doc.paragraphs) // 40, 1)

            elif ext in ["ppt", "pptx"]:
                prs = Presentation(file_path)
                pdf_pages = len(prs.slides)

            elif ext in ["jpg", "jpeg", "png"]:
                pdf_pages = 1

        except Exception as e:
            print("Document page detection error:", e)
            pdf_pages = 1   # ✅ fallback safe value

    # =========================
    # TOTAL PAGE CALCULATION
    # =========================
    pdf_pages = max(pdf_pages, 1)
    manual_pages = max(manual_pages, 0)
    total_pages = pdf_pages + manual_pages

    # =========================
    # PRICING LOGIC
    # =========================
    price_per_page = 5

    if print_type == "Colorprint":
        price_per_page = 5

    paper_extra = 0
    if paper_size in ["A3", "Letter", "Legal"]:
        paper_extra = 2

    college_fee = 0
    if college_doc and college_doc != "none":
        college_fee = 5

    printing_cost = total_pages * copies * (price_per_page + paper_extra)
    total_price = printing_cost + college_fee

    # =========================
    # CREATE ORDER
    # =========================
    order = Order.objects.create(
        user_email=request.session["user_email"],
        file_path=file_path,
        print_type=print_type,
        pages=pdf_pages,
        copies=copies,
        total_price=total_price,
        pickup_code=str(random.randint(1000, 9999)),
        status="Pending"
    )

    return JsonResponse({
        "status": "success",
        "order_id": order.order_id,
        "amount": total_price,
        "pages": pdf_pages
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
from django.utils import timezone

@login_required
def payment_success(request):

    if "user_email" not in request.session:
        return redirect("index")

    order_id = request.GET.get("order_id")
    payment_id = request.GET.get("payment_id")

    if not order_id:
        return redirect("main")

    order = Order.objects(order_id=order_id).first()

    if not order:
        return redirect("main")

    # Update payment
    order.payment_status = "Paid"

    if not order.pickup_code:
        order.pickup_code = str(random.randint(1000, 9999))

    order.save()

    # File name
    file_name = os.path.basename(order.file_path) if order.file_path else "No File"

    relative_file = None
    if order.file_path:
        relative_file = "uploads/" + file_name

    # -----------------------------
    # SAVE ORDER HISTORY
    # -----------------------------
    UploadDocument.objects.create(
        user=request.user,
        file=relative_file,
        file_name=file_name,
        pages=order.pages,
        copies=order.copies,
        print_type=order.print_type,
        status="pending",
        payment_status="paid",
        created_at=timezone.now()
    )

    # -----------------------------
    # ✅ SAVE PAYMENT HISTORY (FIX)
    # -----------------------------
    Payment.objects.create(
        user=request.user,
        order_id=order.order_id,
        file_name=file_name,
        pages=order.pages,
        amount=order.total_price,
        status="Paid"
    )

    # Email
    try:
        send_mail(
            subject="Smart Xerox Services - Payment Successful",
            message=f"""
Smart Xerox Services

Payment Confirmed ✅

Order ID: {order.order_id}
Pickup Code: {order.pickup_code}
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[order.user_email],
            fail_silently=False,
        )
    except Exception as e:
        print("Email error:", e)

    # WhatsApp
    message = f"""
🖨️ SMART XEROX SERVICES
━━━━━━━━━━━━━━━
💳 PAYMENT CONFIRMED
━━━━━━━━━━━━━━━

🆔 Order ID : {order.order_id}
🔐 Pickup Code : {order.pickup_code}
"""

    whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(message)}"

    return render(request, "payment_success.html", {
        "order_id": order.order_id,
        "payment_id": payment_id,
        "pickup_code": order.pickup_code,
        "whatsapp_url": whatsapp_url
    })

def payment_page(request):

    amount = request.GET.get("amount", "0")
    order_id = request.GET.get("order_id", "")

    pdf_pages = int(request.GET.get("pdf_pages", 1))
    if pdf_pages < 1:
        pdf_pages = 1

    return render(request, "payment_page.html", {
        "amount": amount,
        "pdf_pages": pdf_pages,
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

    return render(request, "print_queue.html", {
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

import mimetypes

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_staff)
def open_print_file(request, order_id):

    order = Order.objects(order_id=order_id).first()

    if not order:
        raise Http404("Order not found")

    if not order.file_path:
        raise Http404("File not uploaded")

    file_path = order.file_path

    # ✅ Fix path
    if not os.path.isabs(file_path):
        file_path = os.path.join(settings.MEDIA_ROOT, file_path)

    if not os.path.exists(file_path):
        raise Http404(f"File not found: {file_path}")

    # ✅ Detect file type automatically
    content_type, _ = mimetypes.guess_type(file_path)

    if not content_type:
        content_type = 'application/octet-stream'

    filename = os.path.basename(file_path)

    return FileResponse(
        open(file_path, "rb"),
        content_type=content_type,
        headers={
            "Content-Disposition": f'inline; filename="{filename}"'
        }
    )


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

@login_required
def profile(request):

    # SAVE NEW ORDER FIRST
    if request.method == "POST":

        uploaded_file = request.FILES.get("file")
        pages = request.POST.get("pages")
        copies = request.POST.get("copies")
        print_type = request.POST.get("print_type")

        if uploaded_file:

            UploadDocument.objects.create(
                user=request.user,
                file=uploaded_file,
                file_name=uploaded_file.name,
                pages=int(pages),
                copies=int(copies),
                print_type=print_type,
                status="pending",
                payment_status="paid"
            )

        return redirect("profile")   # reload page after saving


    # FETCH DATA AFTER SAVING
    uploads = UploadDocument.objects.filter(user=request.user).order_by("-created_at")

    total_docs = uploads.count()
    total_pages = sum(doc.pages * doc.copies for doc in uploads)
    total_orders = uploads.count()

    notifications = []

    for doc in uploads:

        if doc.payment_status.lower() == "paid":
            notifications.append(f"Payment successful for {os.path.basename(doc.file_name)}")

        if doc.status.lower() == "printing":
            notifications.append(f"{doc.file_name} is currently printing")

        if doc.status.lower() == "completed":
            notifications.append(f"{doc.file_name} is ready for pickup")


    context = {
        "uploads": uploads,
        "total_docs": total_docs,
        "total_pages": total_pages,
        "total_orders": total_orders,
        "notifications": notifications
    }

    return render(request, "profile.html", context)

@login_required
def delete_order(request, id):

    order = get_object_or_404(UploadDocument, id=id, user=request.user)

    if request.method == "POST":
        order.delete()

    return redirect("profile")

def save_payment(request):

    if request.method == "POST":

        file_name = request.POST.get("file")
        pages = request.POST.get("pages")
        amount = request.POST.get("amount")

        order_id = "ORD" + str(uuid.uuid4().hex[:6])

        Payment.objects.create(
            user=request.user,
            order_id=order_id,
            file_name=file_name,
            pages=pages,
            amount=amount,
            status="Paid"
        )

        return redirect("/payment-history")

@login_required
def payment_history(request):

    # ✅ Admin can see all
    if request.user.is_staff:
        payments = Payment.objects.all().order_by("-date")

    else:
        # ✅ Session-based user fix
        user_email = request.session.get("user_email")

        payments = Payment.objects.filter(
            user__email=user_email
        ).order_by("-date")

    return render(request, "payment_history.html", {
        "payments": payments
    })

@login_required
def update_order_status(request, id):

    order = get_object_or_404(UploadDocument, id=id, user=request.user)

    if request.method == "POST":

        new_status = request.POST.get("status")

        if new_status:
            order.status = new_status
            order.save()

    return redirect("profile")

from django.http import HttpResponse
from reportlab.pdfgen import canvas 
from io import BytesIO

@login_required
def download_receipt(request, order_id):

    payment = Payment.objects.filter(order_id=order_id).first()

    if not payment:
        return HttpResponse("Receipt not found")

    buffer = BytesIO()

    p = canvas.Canvas(buffer)

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Payment Receipt")

    # Content
    p.setFont("Helvetica", 12)
    p.drawString(50, 750, f"Order ID: {payment.order_id}")
    p.drawString(50, 720, f"File Name: {payment.file_name}")
    p.drawString(50, 690, f"Pages: {payment.pages}")
    p.drawString(50, 660, f"Amount: ₹{payment.amount}")
    p.drawString(50, 630, f"Status: {payment.status}")
    p.drawString(50, 600, f"Date: {payment.date}")

    p.drawString(50, 550, "Thank you for using Smart Xerox Services!")

    p.showPage()
    p.save()

    buffer.seek(0)

    return HttpResponse(buffer, content_type='application/pdf', headers={
        'Content-Disposition': f'attachment; filename=receipt_{order_id}.pdf'
    })

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_staff)
def start_print(request, id):
    order = get_object_or_404(PrintOrder, id=id)
    order.status = "printing"
    order.save()
    return redirect("printQueue_admin")


@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_staff)
def pause_print(request, id):
    order = get_object_or_404(PrintOrder, id=id)
    order.status = "paused"
    order.save()
    return redirect("printQueue_admin")


@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_staff)
def delete_print(request, id):
    order = get_object_or_404(PrintOrder, id=id)
    order.delete()
    return redirect("printQueue_admin")


@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_staff)
def college_documents(request):

    if "user_email" not in request.session:
        return redirect("index")

    return render(request, "college_documents.html")