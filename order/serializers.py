from rest_framework import serializers
from product.models import Product, Category, Comment, Images
from order.models import ShopCart, Order
from creatoradmin.models import Customer
from home.serializers import ProductSerializer

class ShopCartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = ShopCart
        fields = "__all__"
