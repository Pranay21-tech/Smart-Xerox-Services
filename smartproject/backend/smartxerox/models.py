import uuid
from datetime import datetime
from django.utils import timezone
from django.db import models
from mongoengine import Document, StringField, EmailField, IntField, DateTimeField
from django.contrib.auth.models import User


# -----------------------------
# MongoDB Customer Model
# -----------------------------
class Customer(Document):

    firstname = StringField()
    lastname = StringField()

    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    meta = {"collection": "customers"}


# -----------------------------
# MongoDB Order Model
# -----------------------------
class Order(Document):

    order_id = StringField(
        unique=True,
        default=lambda: f"ORD-{uuid.uuid4().hex[:6].upper()}"
    )

    user_email = EmailField(required=True)

    file_path = StringField()

    print_type = StringField()

    pages = IntField(default=0)

    copies = IntField(default=1)

    total_price = IntField(default=0)

    pickup_code = StringField()

    status = StringField(
        choices=["Pending", "Printed", "Completed", "Paid"],
        default="Pending"
    )

    payment_status = StringField(
        choices=["Pending", "Paid", "Failed"],
        default="Pending"
    )

    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "orders"}


# -----------------------------
# Django Admin Settings
# -----------------------------
class AdminSettings(models.Model):

    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
    ]

    theme = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default="light"
    )

    max_upload_size = models.IntegerField(default=20)

    allowed_formats = models.JSONField(default=list)

    auto_delete_days = models.IntegerField(default=7)

    working_start_time = models.TimeField(default="09:00")

    working_end_time = models.TimeField(default="21:00")

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Admin Settings"


# -----------------------------
# Printing Queue Model
# -----------------------------
class PrintOrder(models.Model):

    STATUS_CHOICES = [
        ("waiting", "Waiting"),
        ("printing", "Printing"),
        ("paused", "Paused"),
        ("done", "Done"),
        ("failed", "Failed"),
    ]

    order_id = models.CharField(max_length=50, unique=True)

    customer_name = models.CharField(max_length=100)

    file_name = models.CharField(max_length=200)

    pages = models.IntegerField()

    copies = models.IntegerField(default=1)

    print_type = models.CharField(max_length=10)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="waiting"
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.order_id


# -----------------------------
# FAQ Model
# -----------------------------
class FAQ(models.Model):

    question = models.CharField(max_length=255)

    answer = models.TextField()

    def __str__(self):
        return self.question


# -----------------------------
# Upload Document Model
# -----------------------------
class UploadDocument(models.Model):

    PRINT_TYPE_CHOICES = [
        ("bw", "Black & White"),
        ("color", "Color"),
    ]

    PAPER_SIZE_CHOICES = [
        ("A4", "A4"),
        ("A3", "A3"),
        ("Letter", "Letter"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("printing", "Printing"),
        ("completed", "Completed"),
    ]

    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    file = models.FileField(
        upload_to="documents/",
        null=True,
        blank=True
    )

    file_name = models.CharField(max_length=255)

    pages = models.IntegerField(default=1)

    copies = models.IntegerField(default=1)

    print_type = models.CharField(
        max_length=10,
        choices=PRINT_TYPE_CHOICES,
        default="bw"
    )

    paper_size = models.CharField(
        max_length=10,
        choices=PAPER_SIZE_CHOICES,
        default="A4"
    )

    total_price = models.FloatField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="pending"
    )

    created_at = models.DateTimeField(default=timezone.now)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.file_name} - {self.user.username}"


# -----------------------------
# Payment Model
# -----------------------------
class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    file_name = models.CharField(max_length=255)
    pages = models.IntegerField()
    amount = models.FloatField()
    status = models.CharField(max_length=50)
    payment_id = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_id} - {self.status}"