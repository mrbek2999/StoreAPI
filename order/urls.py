from django.urls import path
from order import views
urlpatterns = (
    path('', views.index, name='index'),
    path('addtoshopcart/<int:id>', views.AddToShopCartView.as_view(), name='addtoshopcart'),
    path('deletefromcart/<int:id>', views.DeleteFromCartView.as_view(), name='deletefromcart'),
    path('orderproduct/', views.OrderProductView.as_view(), name='orderproduct'),
)
