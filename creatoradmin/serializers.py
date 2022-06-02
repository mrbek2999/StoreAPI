from rest_framework import serializers
from .models import Customer, Creator
from home.models import FAQ
from product.models import Product, Category, Images, Comment
from order.models import OrderProduct, Order


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = "__all__"


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'image', 'price', 'amount', 'minamount', 'status')



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'address', 'phone', 'city', 'country')


class OrderProductSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    class Meta:
        model = OrderProduct
        fields = ('order', 'user', 'product', 'quantity', 'price', 'amount', 'status')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('product', 'user', 'subject', 'comment', 'rate', 'status', 'create_at')





