from mongoengine import Document, StringField, EmailField

class Customer(Document):
    firstname = StringField()
    lastname = StringField()
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    meta = {"collection": "customers"}
