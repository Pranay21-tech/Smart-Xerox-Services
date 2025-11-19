from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Customer


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

@csrf_exempt
def signup(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except:
            return JsonResponse({"status": "invalid_json"})

        firstname = data.get("firstname")
        lastname = data.get("lastname")
        email = data.get("email")
        password = data.get("password")

        if Customer.objects(email=email).first():
            return JsonResponse({"status": "exists"})

        user = Customer(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=make_password(password)
        )
        user.save()

        request.session["user_email"] = email
        return JsonResponse({"status": "success"})

    return render(request, "form.html")


@csrf_exempt
def login(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except:
            return JsonResponse({"status": "invalid_json"})

        email = data.get("email")
        password = data.get("password")

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
    if "user_email" not in request.session:
        return redirect("login")

    return render(request, "main.html")
