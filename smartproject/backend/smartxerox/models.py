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
    order_id = StringField(unique=True, default=lambda: f"🆔-ORD-{uuid.uuid4().hex[:6].upper()}")

    # Email of user placing order
    user_email = EmailField(required=True)

    # MAIN FIELDS (matching your script.js + HTML)
    doc_type = StringField()
    drive_link = StringField()
    print_type = StringField()
    orientation = StringField()
    copies = IntField(default=1)
    duplex_type = StringField()
    paper_size = StringField()
    college_doc = StringField()
    pages = IntField(default=0)
    stationery_items = StringField()

    # Order status
    status = StringField(
        default="Pending",
        choices=["Pending", "Approved", "Rejected", "Printed"]
    )

    created_at = DateTimeField(default=datetime.now)

    meta = {"collection": "orders"}

