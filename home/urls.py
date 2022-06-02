from django.urls import path
from home import views


urlpatterns = [
    path('', views.index,name='home'),
    path('faq/', views.FAQList.as_view(), name='faq'),
    path('searchs/', views.SearchList.as_view(), name='searchs'),
    path('categories', views.CategoriesList.as_view(), name='categories'),
    path('product-slider', views.ProductSlider.as_view(), name='product-slider'),
    path('product-latest', views.ProductLatest.as_view(), name='product-latest'),
    path('product-picked', views.ProductPicked.as_view(), name='product-picked'),
    path('shopcart-list', views.ShopCartList.as_view(), name='shopcart-list'),
    path('order-list', views.OrderList.as_view(), name='order-list'),
    path('category/<int:id>/<slug:slug>', views.CategoryProducts.as_view(), name='category_product'),
    path('product/<int:id>/<slug:slug>', views.ProductView.as_view(), name='product_detail'),
    path('contact/',views.contactus, name='contactus'), ###
    path('delete/<int:id>', views.delete, name='delete'), ###
]