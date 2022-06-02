from rest_framework import serializers
from .models import FAQ
from product.models import Product, Category, Comment, Images
from order.models import ShopCart, Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('parent', 'title', 'description', 'image', 'status', 'slug')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'subject', 'comment', 'rate')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    image = ImageSerializer()
    class Meta:
        model = Product
        fields = ('title', 'category', 'description', 'image', 'price', 'amount', 'minamount', 'status', 'slug')


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ('ordernumber', 'question', 'answer', 'status')


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = ShopCart
        fields = ('product', 'quantity')
