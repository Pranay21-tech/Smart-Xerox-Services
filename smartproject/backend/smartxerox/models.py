from mongoengine import Document, StringField, EmailField, IntField, DateTimeField
from datetime import datetime
import uuid

class Customer(Document):
    firstname = StringField()
    lastname = StringField()
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    meta = {"collection": "customers"}


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
    created_at = DateTimeField(default=datetime.now)

    meta = {"collection": "orders"}

from django.db import models

class AdminSettings(models.Model):
    THEME_CHOICES = (
        ("light", "Light"),
        ("dark", "Dark"),
    )

    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default="light")

    max_upload_size = models.IntegerField(default=20)
    allowed_formats = models.JSONField(default=list)
    auto_delete_days = models.IntegerField(default=7)

    working_start_time = models.TimeField(default="09:00")
    working_end_time = models.TimeField(default="21:00")

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Admin Settings"
    
##printing Queue model for tracking print jobs and their statuses

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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="waiting")
    created_at = models.DateTimeField(auto_now_add=True)

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question