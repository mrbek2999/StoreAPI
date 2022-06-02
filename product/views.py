from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse

# Create your views here.
from product.models import CommentForm, Comment
from rest_framework.views import APIView
from rest_framework.response import Response


def index(request):
    return HttpResponse('Product Page')


class AddCommentView(APIView):
    def post(self, request, id):
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()
            return Response(data={"message": "Sizning kommentariyangiz qabul qilindi!"})
        return Response(data={"message": "Xatolik!!!"})
