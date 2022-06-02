import profile

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from home.models import Setting
from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from product.models import Category, Product, Images, Comment
from creatoradmin.models import Customer

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ShopCartSerializer


def index(request):
    return HttpResponse('Order Page')


class ShopCartView(APIView):
    def get(self, request):
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        serializer = ShopCartSerializer(shopcart, many=True)
        return Response(serializer.data)


class AddToShopCartView(APIView):
    def get(self, request, id):
        url = request.META.get('HTTP_REFERER')  # get last url
        checkproduct = ShopCart.objects.filter(product_id=id)  # Check product in shopcart
        if checkproduct:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart
        if control == 1:  # Update shopcart
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()  #
        else:  # Insert to shopcart
            data = ShopCart()  # model
            data.user_id = request.user.id
            data.product_id = id
            data.quantity = 1
            data.save()  #
        return Response(data={"message": "Product added to ShopCart"})

    def post(self, request, id):
        url = request.META.get('HTTP_REFERER')  # get last url
        checkproduct = ShopCart.objects.filter(product_id=id)  # Check product in shopcart
        if checkproduct:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update shopcart
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:  # Insert to Shopcart
                data = ShopCart()
                data.user_id = request.user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        return Response(data={"message": "Product added to ShopCart"})


class DeleteFromCartView(APIView):
    def get(self, request, id):
        ShopCart.objects.filter(pk=id).delete()
        return Response(data={"message": "Your item deleted from Shop Cart!"})


###################################################################################################################
###################################################################################################################
###################################################################################################################


class OrderProductView(APIView):
    def get(self, request):
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        serializer = ShopCartSerializer(shopcart, many=True)
        return Response(serializer.data)

    def post(self, request):
        current_user = request.user
        total_quantity = 0
        total = 0
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        for rs in shopcart:
            total += rs.product.price * rs.quantity
            total_quantity += rs.quantity
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']  # get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.phone = form.cleaned_data['phone']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.user_id = current_user.id
            data.total = total
            data.total_quantity = total_quantity
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(12).upper()  # random code
            data.code = ordercode
            data.save()

            # Move Shopcart items to Order Product items
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()
                # Reduce quantity of sold product from Amount of Product
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            return Response(data={"message": "Your Order Has Been Completed! Thank you!"})

        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")
