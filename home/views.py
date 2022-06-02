import json

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.core.paginator import (Paginator, PageNotAnInteger, EmptyPage)
# Create your views here.
from django.utils import translation
from home.models import Setting, ContactForm, ContactMessage, FAQ
from home.forms import SearchForm
from order.models import ShopCart, Order
from product.models import Category, Product, Images,  Comment
from home.serializers import ProductSerializer, CategorySerializer, OrderSerializer, \
    CommentSerializer, CartSerializer, ImageSerializer, FAQSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class CategoriesList(APIView):
    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)


class ProductSlider(APIView):
    def get(self, request):
        product_slider = Product.objects.all().order_by('id')[:5]
        serializer = ProductSerializer(product_slider, many=True)
        return Response(serializer.data)


class ProductLatest(APIView):
    def get(self, request):
        product_latest = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(product_latest, many=True)
        return Response(serializer.data)


class ProductPicked(APIView):
    def get(self, request):
        product_picked = Product.objects.all().order_by('?')[:8]
        serializer = ProductSerializer(product_picked, many=True)
        return Response(serializer.data)


class ShopCartList(APIView):
    def get(self, request):
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        serializer = CartSerializer(shopcart, many=True)
        return Response(serializer.data)


class OrderList(APIView):
    def get(self, request):
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)


class CategoryProducts(APIView):
    def get(self, request, slug, id):
        products = Product.objects.filter(category__slug=slug)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductView(APIView):
    def get(self, request, slug, id):
        product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class SearchList(APIView):
    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)


class FAQList(APIView):
    def get(self, request):
        faq = FAQ.objects.filter(status='True').order_by('ordernumber')
        serializer = FAQSerializer(faq, many=True)
        return Response(serializer.data)






################################################################
def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for rs in products:
            products_json = {}
            products_json = rs.title
            results.append(products_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def selectlanguage(request):
    if request.method == 'POST':  # check post
        cur_language = translation.get_language()
        lasturl= request.META.get('HTTP_REFERER')
        lang = request.POST['language']
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY]=lang
        #return HttpResponse(lang)
        return HttpResponseRedirect("/"+lang)



def delete(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted from Shop Cart!")
    return HttpResponseRedirect("/")



def contactus(request):
    if request.method =='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.phone = form.cleaned_data['phone']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Sizning xabaringiz yuborildi! Rahmat")
            return HttpResponseRedirect('/contact')
    setting = Setting.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    order = Order.objects.all()
    total = 0
    total_qty = 0
    for rs in shopcart:
        total_qty += rs.quantity
        total += rs.product.price * rs.quantity
    form = ContactForm
    context = {'setting': setting,
               'form': form,
               'shopcart': shopcart,
               'order': order,
               'total': total,
               'total_qty': total_qty,
               }
    return render(request,'contact.html', context)



def index(request):
    setting = Setting.objects.all()
    category = Category.objects.all()
    product_slider = Product.objects.all().order_by('id')[:5]
    product_latest = Product.objects.all().order_by('-id')
    product_picked = Product.objects.all().order_by('?')[:8]
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    order = Order.objects.all()
    total = 0
    total_qty = 0
    # for rs in shopcart:
    #     total_qty += rs.quantity
    #     total += rs.product.price * rs.quantity
    page = "home"
    context = {

        'setting': setting,
        'category': category,
        'product_slider': product_slider,
        'product_latest':product_latest,
        'product_picked': product_picked,
        'page': page,
        'shopcart':shopcart,
        'order':order,
        'total': total,
        'total_qty': total_qty,

    }
    return render(request,'index.html', context)