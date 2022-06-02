from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from home import views
import creatoradmin

schema_view = get_schema_view(
    openapi.Info(
        title='Store API',
        default_version='v1',
        description='Redoc API Document',
        contact=openapi.Contact('Sayidiy Bekzodbek <info@bekzodbek.uz>'),
    ),
    public=True,
    permission_classes=(AllowAny,)
)

from order import views as OrderViews
from creatoradmin import views as CreatoradminViews
from creatoradmin import views as UserViews
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _



urlpatterns = [
    path('selectlanguage', views.selectlanguage, name='selectlanguage'),
    path('selectlanguagess',    CreatoradminViews.selectlanguagess, name='selectlanguagess'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='redoc-docs')
]


urlpatterns += i18n_patterns (

    path('admin/', admin.site.urls),
    path('api/', include('creatoradmin.urls')),
    path('', include('home.urls')),
    path('order/', include('order.urls')),
    path('shopcart/', OrderViews.ShopCartView.as_view(), name='shopcart'),
    path('user/', include('creatoradmin.urls')),
    path('login/', UserViews.LoginFormView.as_view(), name='login_form'),
    path('logout_form/', UserViews.logout_form, name='logout_form'),
    path('register/', UserViews.RegisterView.as_view(), name='register'),
    path('developer_home/', UserViews.DeveloperHomeView.as_view(), name='developer_home'),
    path('startapper_home/', UserViews.startapper_home, name='startapper_home'),
    path('product/', include('product.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('search_auto/', views.search_auto, name='search_auto'),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


