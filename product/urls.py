from django.urls import path
from product import views
urlpatterns = [

    path('', views.index,name='index'),
    path('addcomment/<int:id>', views.AddCommentView.as_view(), name='addcomment'),
]