from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Customer, Order



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

def admin_orders(request):
    return render(request, "admin_orders.html")

@csrf_exempt
def signup(request):

    if request.method == "POST":
        try:
            body = request.body.decode("utf-8").strip()
            if not body:
                return JsonResponse({"status": "invalid_json", "error": "Empty request body. Make sure you are submitting via JavaScript."})
            data = json.loads(body)
        except Exception as e:
            return JsonResponse({"status": "invalid_json", "error": str(e)})

        firstname = data.get("firstname", "").strip()
        lastname = data.get("lastname", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        if not firstname or not lastname or not email or not password:
            return JsonResponse({"status": "error", "message": "All fields are required."})

        if Customer.objects(email=email).first():
            return JsonResponse({"status": "exists", "message": "Email already exists."})

        user = Customer(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=make_password(password)
        )
        user.save()

        request.session["user_email"] = email
        return JsonResponse({"status": "success"})

    return render(request, "Form.html")


@csrf_exempt
def user_login(request):

    if request.method == "POST":
        try:
            body = request.body.decode("utf-8").strip()
            if not body:
                return JsonResponse({"status": "invalid_json", "error": "Empty request body. Make sure you are submitting via JavaScript."})
            data = json.loads(body)
        except Exception as e:
            return JsonResponse({"status": "invalid_json", "error": str(e)})

        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        if not email or not password:
            return JsonResponse({"status": "error", "message": "Email and password are required."})

        user = Customer.objects(email=email).first()
        if not user:
            return JsonResponse({"status": "error", "message": "Invalid email"})

        if check_password(password, user.password):
            request.session["user_email"] = email
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": "Wrong password"})

    return render(request, "index.html")


def main(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "main.html")


@csrf_exempt
def create_order(request):
    if "user_email" not in request.session:
        return JsonResponse({"status": "unauthenticated"}, status=401)

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST required"}, status=400)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception as e:
        return JsonResponse({"status": "invalid_json", "error": str(e)}, status=400)

    order = Order(
        user_email=request.session["user_email"],  # FIXED EMAIL
        doc_type=data.get("docType"),
        drive_link=data.get("driveLink"),
        print_type=data.get("printType"),
        orientation=data.get("orientation"),
        copies=int(data.get("copies", 0)),
        duplex_type=data.get("duplexType"),
        paper_size=data.get("paperSize"),
        college_doc=data.get("collegeDoc"),
        pages=int(data.get("pages", 0)),
        stationery_items=data.get("stationeryItems"),
    )

    order.save()

    return JsonResponse({"status": "success", "message": "Order placed successfully!"})


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_orders')

        return render(request, 'admin_login.html', {"error": "Invalid username or password"})

    return render(request, "admin_login.html")



@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, "admin_orders.html", {
        "orders": orders,
        "admin_name": request.user.username
    })

def update_order_status(request, order_id, new_status):
    order = Order.objects.filter(id=order_id).first()
    if not order:
        return JsonResponse({"success": False, "error": "Order not found"})

    order.status = new_status
    order.save()

    return JsonResponse({"success": True, "message": "Status updated"})




def logout_admin(request):
    logout(request)
    return redirect('admin_orders')
