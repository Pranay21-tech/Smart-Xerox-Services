from rest_framework import serializers
from .models import smartxerox

class smartserialiezer(serializers.Modelserialiezer):
    class Meta:
        model=smartxerox
        fields='_all_'