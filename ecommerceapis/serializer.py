from e_commerce.models import *
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # same as model Product class
        fields = "__all__"