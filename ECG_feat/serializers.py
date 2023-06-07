from rest_framework import serializers
from .models import ECG_models

class Temp_serializer(serializers.ModelSerializer):# POST

    class Meta:
        model = ECG_models
        fields =["amp"]

class Temp_serializer2(serializers.ModelSerializer):# GET

    class Meta:
        model = ECG_models
        fields =["amp", "data"]